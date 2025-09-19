import json
import re
from pathlib import Path
from string import Template

import boto3
import faiss
import nbtlib
import numpy as np
from mcrcon import MCRcon
from tqdm import tqdm

from .mappings import MVS_BLOCK_MAP, MVS_BLOCK_RMAP

DEFAULT_ORIGIN_X = 0
DEFAULT_ORIGIN_Y = 0
DEFAULT_ORIGIN_Z = 0


class MinecraftVectorStore:
    def __init__(
        self,
        host: str,
        password: str,
        port: int = 25575,
        ox: int = DEFAULT_ORIGIN_X,
        oy: int = DEFAULT_ORIGIN_Y,
        oz: int = DEFAULT_ORIGIN_Z,
    ):
        self.mcrcon = MCRcon(host, password, port)
        self.mcrcon.connect()

        self.bedrock_client = boto3.client("bedrock-runtime", "us-east-1")

        self.ox = ox
        self.oy = oy
        self.oz = oz

        self.chunks = []
        self.index = None

        def read_template(funcname: str):
            mcfunctions_path = Path(__file__).parent / "mcfunctions"
            with open(mcfunctions_path / f"{funcname}.mcfunction") as f:
                return Template(f.read())

        self.get_block_template = read_template("getBlock")
        self.set_block_template = read_template("setBlock")
        self.set_dropper_template = read_template("setDropper")

    def _embed(self, query: str):
        response = self.bedrock_client.invoke_model(
            modelId="amazon.titan-embed-text-v2:0",
            body=json.dumps(
                {
                    "inputText": query,
                    "dimensions": 256,
                }
            ),
        )
        response = json.loads(response["body"].read())

        return response["embedding"]

    def _get_block(self, x, y, z):
        command = self.get_block_template.substitute(x=x, y=y, z=z)
        return self.mcrcon.command(command)

    def _set_block(self, x, y, z, block):
        command = self.set_block_template.substitute(x=x, y=y, z=z, block=block)
        return self.mcrcon.command(command)

    def build(self, chunks: list[str]):
        self.chunks = chunks

        print("● Creating vectors...")

        # vectors = [self._embed(chunk) for chunk in tqdm(chunks)]
        # vectors = np.array(vectors, dtype=np.float32)

        # self.index = faiss.IndexFlatL2(256)
        # self.index.add(vectors)  # type: ignore

        print("● Build index in your Minecreft World...")

        for i, chunk in tqdm(enumerate(chunks)):
            gap = 2

            # NOTE: y軸8個 → x軸8個 → z軸8個の順番でチャンクを配置する
            y_grid = (i % 8) * 4
            x_grid = ((i // 8) % 8) * (32 + gap)
            z_grid = (i // 64) * (32 + gap)

            # NOTE: ガラスの土台の角にチャンクを格納するドロッパーを配置する
            # FIXME: ここだけ_set_block使ってないのが気になる
            command = self.set_dropper_template.substitute(
                x=self.ox + x_grid,
                y=self.oy + y_grid,
                z=self.oz + z_grid,
                tag=json.dumps(
                    {"pages": [re.sub(r"\s+", "", chunk)]},
                    ensure_ascii=False,
                ),
            )
            self.mcrcon.command(command)

            # NOTE: 宙に浮けないブロックを支えるための土台(ガラス)を設置
            for x in range(32):
                for z in range(32):
                    if x == 0 and z == 0:
                        continue

                    self._set_block(
                        x=self.ox + x_grid + x,
                        y=self.oy + y_grid,
                        z=self.oz + z_grid + z,
                        block="minecraft:glass",
                    )

            # # NOTE: ベクトルを構成するバイト列ごとに対応するブロックを配置する
            # comps = vectors[i].tobytes()
            # for j, comp in enumerate(comps):
            #     id, data = MVS_BLOCK_MAP[comp]
            #     self.mcpi.setBlock(
            #         self.ox + x_grid + j % 32,
            #         self.oy + y_grid + 1,
            #         self.oz + z_grid + j // 32,
            #         id,
            #         data,
            #     )

        print("● Success to create index.")

    def load(self):
        print("● Loading index from your Minecraft World...")

        i = 0
        chunks = []
        vectors = []

        while True:
            gap = 2

            # NOTE: y軸8個 → x軸8個 → z軸8個の順番でチャンクが配置されていると仮定する
            y_grid = (i % 8) * 4
            x_grid = ((i // 8) % 8) * (32 + gap)
            z_grid = (i // 64) * (32 + gap)

            # NOTE: ドロッパーの有無でチャンクが存在するかどうかを判定する
            id = self.mcpi.getBlock(
                self.ox + x_grid,
                self.oy + y_grid,
                self.oz + z_grid,
            )
            if id != DROPPER.id:
                break

            # NOTE: チャンクが格納されているドロッパーの情報を読み取る
            command = self.get_block_template.substitute(
                x=self.ox + x_grid,
                y=self.oy + y_grid,
                z=self.oz + z_grid,
            )
            response = self.mcrcon.command(command)

            prefix = "The data tag did not change: "
            nbt = nbtlib.parse_nbt(response.replace(prefix, ""))

            pages = nbt["Items"][0]["tag"]["pages"]
            chunk = "".join([str(page) for page in pages])
            chunks.append(chunk)

            # NOTE: ブロックの集合から元のベクトルを復元する
            comps = []
            for j in range(256 * 4):
                x = j % 32
                z = j // 32

                block = self.mcpi.getBlockWithData(
                    self.ox + x_grid + x,
                    self.oy + y_grid + 1,
                    self.oz + z_grid + z,
                )
                comp = MVS_BLOCK_RMAP[(block.id, block.data)]
                comps.append(comp)

            comps = np.array(comps, dtype=np.uint8)
            comps = np.frombuffer(comps.tobytes(), dtype=np.float32)
            vectors.append(comps)

            i += 1

        if not chunks or not vectors or len(vectors) != len(chunks):
            print("🚨 No valid index found in the world.")
            print("\t└─ Please run the build method first to create the index.")
            return

        self.chunks = chunks
        self.index = faiss.IndexFlatL2(256)
        self.index.add(np.array(vectors, dtype=np.float32))  # type: ignore

        print("● Success to load index.")

    def test(self, chunk: str):
        command = self.set_dropper_template.substitute(
            x=0,
            y=0,
            z=0,
            tag=json.dumps(
                {"pages": [re.sub(r"\s+", "", chunk)]},
                ensure_ascii=False,
            ),
        )
        print(command)
        res = self.mcrcon.command(command)
        print(res)

    def exists(self) -> bool:
        # NOTE: オリジンとして指定された座標にドロッパーがあるかどうかを確認する
        id = self.mcpi.getBlock(
            self.ox,
            self.oy,
            self.oz,
        )
        return id == DROPPER.id

    def retrieve(self, query: str, k: int, show_overworld: bool = False) -> list[str]:
        embedding = np.array([self._embed(query)], dtype="float32")
        _, indices = self.index.search(embedding, k=k)  # type: ignore

        if show_overworld:
            self._highlight_chunks(indices[0])
            input("Press Enter to turn off the glow...")
            self._restore_chunks(indices[0])

        return [self.chunks[i] for i in indices[0]]

    def _highlight_chunks(self, chunk_indices: list[int]):
        for chunk_idx in chunk_indices:
            gap = 2
            y_grid = (chunk_idx % 8) * 4
            x_grid = ((chunk_idx // 8) % 8) * (32 + gap)
            z_grid = (chunk_idx // 64) * (32 + gap)

            # ガラス土台をシーランタンに置き換え（角のドロッパーは除外）
            for x in range(32):
                for z in range(32):
                    if x == 0 and z == 0:
                        continue
                    self.mcpi.setBlock(
                        self.ox + x_grid + x,
                        self.oy + y_grid,
                        self.oz + z_grid + z,
                        SEA_LANTERN,
                    )

    def _restore_chunks(self, chunk_indices: list[int]):
        for chunk_idx in chunk_indices:
            gap = 2
            y_grid = (chunk_idx % 8) * 4
            x_grid = ((chunk_idx // 8) % 8) * (32 + gap)
            z_grid = (chunk_idx // 64) * (32 + gap)

            # シーランタンをガラスに戻す（角のドロッパーは除外）
            for x in range(32):
                for z in range(32):
                    if x == 0 and z == 0:
                        continue
                    self.mcpi.setBlock(
                        self.ox + x_grid + x,
                        self.oy + y_grid,
                        self.oz + z_grid + z,
                        Block.GLASS,
                    )
