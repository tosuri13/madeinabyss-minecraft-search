import os
import pickle
from pathlib import Path

import boto3
import faiss
import mcpi.block as Block
import numpy as np
from langchain_aws import BedrockEmbeddings
from langchain_text_splitters import MarkdownTextSplitter
from mcpi.minecraft import Minecraft
from scipy import stats
from tqdm import tqdm

DEFAULT_MVC_DIR = ".mvc"
MINECRAFT_HOST = os.environ["MINECRAFT_HOST"]


class MinecraftVectorStore:
    def __init__(self):
        self.mc = Minecraft.create(MINECRAFT_HOST)
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

        print("● Creating embeddings...")

        embeddings = [embedding_model.embed_query(chunk) for chunk in tqdm(chunks)]
        embeddings = np.array(embeddings, dtype=np.float32)
        embeddings = ((embeddings + 1) * 127.5).astype(np.uint8)

        # NOTE: 量子化されたベクトルからFAISSのインデックスを構築する
        self.index = faiss.IndexFlatL2(256)
        self.index.add(embeddings.astype(np.float32))  # type: ignore

        print("● Build index in your Minecreft World...")

        for i, chunk in enumerate(chunks):
            # print(chunk)
            for j, comp in enumerate(embeddings[i]):
                self.mc.setBlock(0, 51, j, comp)

        print("● Success to create index.")


if __name__ == "__main__":
    source = Path("assets/source.txt").read_text()

    splitter = MarkdownTextSplitter(
        chunk_size=1024,
        chunk_overlap=256,
    )
    chunks = splitter.split_text(source)[:1]

    mvc = MinecraftVectorStore()
    mvc.build(chunks)

    # mc = Minecraft.create(MINECRAFT_HOST)

    # block_id = mc.getBlock(0, 0, 0)
    # print(f"ブロックID: {block_id}")
