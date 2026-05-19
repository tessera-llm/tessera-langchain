"""
cohere-langchain.py — ChatCohere through the Tessera proxy.

Usage:

    pip install tessera-langchain langchain-cohere
    export COHERE_API_KEY=...
    export TESSERA_API_KEY=tk_...
    python cohere-langchain.py
"""

from __future__ import annotations

import os

from langchain_cohere import ChatCohere
from langchain_core.messages import HumanMessage

from tessera_langchain import tessera_cohere_config


def main() -> None:
    cohere_key = os.environ["COHERE_API_KEY"]
    tessera_key = os.environ["TESSERA_API_KEY"]

    llm = ChatCohere(
        model="command-r-plus-08-2024",
        cohere_api_key=cohere_key,
        **tessera_cohere_config(api_key=tessera_key),
    )

    response = llm.invoke(
        [
            HumanMessage(
                content=(
                    "Explain how Cohere's Rerank model differs from a dense "
                    "vector retriever. 4 sentences."
                )
            )
        ]
    )

    print(response.content)


if __name__ == "__main__":
    main()
