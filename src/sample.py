import os
from pathlib import Path

import boto3
import questionary
from chonkie import TokenChunker
from strands import Agent, tool
from strands.models import BedrockModel

from mvs import MinecraftVectorStore

if __name__ == "__main__":
    host = os.environ["MINECRAFT_HOST"]
    password = os.environ["MCRCON_PASSWORD"]

    mvc = MinecraftVectorStore(host, password)

    if mvc.exists():
        mvc.load()
    else:
        source = Path("assets/source.txt").read_text()
        chunker = TokenChunker(
            tokenizer="character",
            chunk_size=256,
            chunk_overlap=0,
        )
        chunks = [chunk.text for chunk in chunker.chunk(source)]
        mvc.build(chunks)

    @tool
    def semantic_search(query: str):
        """自然言語で入力されたクエリを利用して、メイドインアビスに関するドキュメントをセマンティックに検索します"""
        return mvc.retrieve(query, k=3)

    agent = Agent(
        model=BedrockModel(
            boto_session=boto3.Session(region_name="us-east-1"),
            model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
        ),
        system_prompt=(
            "あなたはメイドインアビスと呼ばれる作品に関する質問に回答するチャットボットです。\n"
            "検索ツールを利用して正しい情報を引用しつつ、ユーザのリクエストに対する回答を生成してください。"
        ),
        tools=[semantic_search],
    )

    while True:
        agent(questionary.text("質問:").ask())
        print()
