"""
groq-langchain.py — ChatGroq through the Tessera proxy.

Usage:

    pip install tessera-langchain langchain-groq
    export GROQ_API_KEY=gsk_...
    export TESSERA_API_KEY=tk_...
    python groq-langchain.py
"""

from __future__ import annotations

import os

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from tessera_langchain import tessera_groq_config


def main() -> None:
    groq_key = os.environ["GROQ_API_KEY"]
    tessera_key = os.environ["TESSERA_API_KEY"]

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=groq_key,
        **tessera_groq_config(api_key=tessera_key),
    )

    response = llm.invoke(
        [
            HumanMessage(
                content=(
                    "Explain how Llama 3 differs from Llama 2 architecturally. "
                    "4 sentences."
                )
            )
        ]
    )

    print(response.content)


if __name__ == "__main__":
    main()
