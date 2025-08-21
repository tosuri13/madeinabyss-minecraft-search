import os
from pathlib import Path

import boto3
import faiss
import numpy as np
from langchain_aws import BedrockEmbeddings
from langchain_text_splitters import MarkdownTextSplitter
from mcpi import block as Block
from mcpi.minecraft import Minecraft
from tqdm import tqdm

from mappings import BLOCK_MAPPING, REVERSE_BLOCK_MAPPING

DEFAULT_ORIGIN_X = 0
DEFAULT_ORIGIN_Y = 50
DEFAULT_ORIGIN_Z = 0


class MinecraftVectorStore:
    def __init__(
        self,
        host: str,
        port: int = 4711,
        ox: int = DEFAULT_ORIGIN_X,
        oy: int = DEFAULT_ORIGIN_Y,
        oz: int = DEFAULT_ORIGIN_Z,
    ):
        self.mc = Minecraft.create(host, port)
        self.ox = ox
        self.oy = oy
        self.oz = oz
        self.index = None

    def build(self, chunks: list[str]):
        client = boto3.client("bedrock-runtime", "us-east-1")
        embedding_model = BedrockEmbeddings(
            client=client,
            model_id="amazon.titan-embed-text-v2:0",
            model_kwargs={
                "dimensions": 256,
                "embeddingTypes": ["float"],
            },
        )

        print("● Creating vectors...")

        vectors = [embedding_model.embed_query(chunk) for chunk in tqdm(chunks)]
        vectors = np.array(vectors, dtype=np.float32)

        self.index = faiss.IndexFlatL2(256)
        self.index.add(vectors)  # type: ignore

        print("● Build index in your Minecreft World...")

        for i, chunk in tqdm(enumerate(chunks)):
            gap = 2

            # NOTE: y軸8個 → x軸8個 → z軸8個の順番でチャンクを配置する
            y_grid = (i % 8) * 4
            x_grid = ((i // 8) % 8) * (32 + gap)
            z_grid = (i // 64) * (32 + gap)

            # NOTE: 宙に浮けないブロックを支えるための土台(ガラス)を設置
            for x in range(32):
                for z in range(32):
                    self.mc.setBlock(
                        self.ox + x_grid + x,
                        self.oy + y_grid,
                        self.oz + z_grid + z,
                        Block.GLASS,
                    )

            # NOTE: ベクトルを構成するバイト列ごとに対応するブロックを配置する
            comps = vectors[i].tobytes()
            for j, comp in enumerate(comps):
                id, data = BLOCK_MAPPING[comp]
                self.mc.setBlock(
                    self.ox + x_grid + j % 32,
                    self.oy + y_grid + 1,
                    self.oz + z_grid + j // 32,
                    id,
                    data,
                )

        print("● Success to create index.")

    def load(self):
        print("● Loading index from your Minecraft World...")

        i = 0
        vectors = []

        while True:
            gap = 2

            # NOTE: y軸8個 → x軸8個 → z軸8個の順番でチャンクが配置されていると仮定する
            y_grid = (i % 8) * 4
            x_grid = ((i // 8) % 8) * (32 + gap)
            z_grid = (i // 64) * (32 + gap)

            # NOTE: ガラスブロックの有無でチャンクが存在するかどうか判定する
            id = self.mc.getBlock(
                self.ox + x_grid,
                self.oy + y_grid,
                self.oz + z_grid,
            )
            if id != Block.GLASS.id:
                break

            # NOTE: ブロックの集合から元のベクトルを復元する
            comps = []
            for j in range(256 * 4):
                x = j % 32
                z = j // 32

                block = self.mc.getBlockWithData(
                    self.ox + x_grid + x,
                    self.oy + y_grid + 1,
                    self.oz + z_grid + z,
                )
                comp = REVERSE_BLOCK_MAPPING[(block.id, block.data)]
                comps.append(comp)

            comps = np.array(comps, dtype=np.uint8)
            comps = np.frombuffer(comps.tobytes(), dtype=np.float32)

            vectors.append(comps)
            i += 1

        if not vectors:
            print("🚨 No valid vectors found in the world.")
            print("\t└─ Please run the build method first to create the index.")
            return

        self.index = faiss.IndexFlatL2(256)
        self.index.add(np.array(vectors, dtype=np.float32))  # type: ignore

        print("● Success to load index.")

    def get_vector(self, i: int):
        vectors = self.index.reconstruct(i)  # type: ignore
        return np.array(vectors, dtype=np.float32)


if __name__ == "__main__":
    source = Path("assets/source.txt").read_text()

    splitter = MarkdownTextSplitter(
        chunk_size=1024,
        chunk_overlap=256,
    )
    chunks = splitter.split_text(source)[:10]

    mvc = MinecraftVectorStore(os.environ["MINECRAFT_HOST"])
    mvc.build(chunks)

    # mvc.load()
    # vector = mvc.get_vector(0)
    # print(vector)
