"""
openai-langchain.py — ChatOpenAI through the Tessera proxy.

Usage:

    pip install tessera-langchain langchain-openai
    export OPENAI_API_KEY=sk-...
    export TESSERA_API_KEY=tsr_...
    python openai-langchain.py
"""

from __future__ import annotations

import os

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from tessera_langchain import tessera_openai_config


def main() -> None:
    openai_key = os.environ["OPENAI_API_KEY"]
    tessera_key = os.environ["TESSERA_API_KEY"]

    llm = ChatOpenAI(
        model="gpt-4o",
        openai_api_key=openai_key,
        **tessera_openai_config(api_key=tessera_key),
    )

    response = llm.invoke(
        [
            SystemMessage(
                content=(
                    "You are a senior platform engineer reviewing infrastructure "
                    "decisions. Answer in 3 concise bullets."
                )
            ),
            HumanMessage(
                content=(
                    "Compare a service mesh sidecar approach vs an eBPF-based "
                    "approach for east-west traffic policy enforcement."
                )
            ),
        ]
    )

    print(response.content)


if __name__ == "__main__":
    main()
