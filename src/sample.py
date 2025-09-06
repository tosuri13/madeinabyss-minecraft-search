import os
from pathlib import Path

from langchain_text_splitters import MarkdownTextSplitter

from mvs import MinecraftVectorStore

if __name__ == "__main__":
    host = os.environ["MINECRAFT_HOST"]
    password = os.environ["MCRCON_PASSWORD"]

    mvc = MinecraftVectorStore(host, password)

    if mvc.exists():
        mvc.load()
    else:
        source = Path("assets/source.txt").read_text()
        splitter = MarkdownTextSplitter(
            chunk_size=256,
            chunk_overlap=0,
        )
        chunks = splitter.split_text(source)[:3]
        mvc.build(chunks)

    print(mvc.chunks)
