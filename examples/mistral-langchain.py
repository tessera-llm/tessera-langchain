"""
mistral-langchain.py — ChatMistralAI through the Tessera proxy.

Usage:

    pip install tessera-langchain langchain-mistralai
    export MISTRAL_API_KEY=...
    export TESSERA_API_KEY=tk_...
    python mistral-langchain.py
"""

from __future__ import annotations

import os

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage

from tessera_langchain import tessera_mistral_config


def main() -> None:
    mistral_key = os.environ["MISTRAL_API_KEY"]
    tessera_key = os.environ["TESSERA_API_KEY"]

    llm = ChatMistralAI(
        model="mistral-large-latest",
        mistral_api_key=mistral_key,
        **tessera_mistral_config(api_key=tessera_key),
    )

    response = llm.invoke(
        [
            HumanMessage(
                content=(
                    "Explain the difference between async-await and a thread "
                    "pool in Python. 4 sentences."
                )
            )
        ]
    )

    print(response.content)


if __name__ == "__main__":
    main()
