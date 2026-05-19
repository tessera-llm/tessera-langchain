"""
anthropic-langchain.py — ChatAnthropic through the Tessera proxy.

Usage:

    pip install tessera-langchain langchain-anthropic
    export ANTHROPIC_API_KEY=sk-ant-...
    export TESSERA_API_KEY=tsr_...
    python anthropic-langchain.py
"""

from __future__ import annotations

import os

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

from tessera_langchain import tessera_anthropic_config


def main() -> None:
    anthropic_key = os.environ["ANTHROPIC_API_KEY"]
    tessera_key = os.environ["TESSERA_API_KEY"]

    llm = ChatAnthropic(
        model="claude-sonnet-4-5-20250929",
        anthropic_api_key=anthropic_key,
        **tessera_anthropic_config(api_key=tessera_key),
    )

    response = llm.invoke(
        [
            HumanMessage(
                content=(
                    "Explain the difference between a database commit lock and "
                    "an advisory lock in PostgreSQL. 4 sentences."
                )
            )
        ]
    )

    print(response.content)


if __name__ == "__main__":
    main()
