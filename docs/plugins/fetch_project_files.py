from __future__ import annotations

import logging
import textwrap
from pathlib import Path

from mkdocs.config import Config

logger = logging.getLogger("mkdocs.plugin")

ROOT = Path(__file__).parents[2]
DOCS = ROOT / "docs"


def on_pre_build(config: Config):
    """Before build starts."""
    _add_tracked_file(
        ROOT / "CHANGES.md",
        DOCS / "changes.md",
        prepend=(
            """
            ---
            toc_depth: 2
            ---
            """
        ),
    )
    _add_tracked_file(
        ROOT / "CONTRIBUTING.md",
        DOCS / "contributing.md",
    )
    _add_tracked_file(
        ROOT / "LICENSE.md",
        DOCS / "license.md",
    )


def _add_tracked_file(
    file: Path,
    new_file: Path,
    prepend: str = "",
    append: str = "",
):
    prepend = prepend.lstrip("\n") + "\n" if prepend else ""
    append = append.lstrip("\n") + "\n" if append else ""

    text = file.read_text(encoding="utf-8")
    text = "".join(
        (
            textwrap.dedent(prepend),
            text,
            textwrap.dedent(append),
        )
    )

    # avoid writing file unless the content has changed to avoid infinite build loop
    if not new_file.is_file() or new_file.read_text(encoding="utf-8") != text:
        new_file.write_text(text, encoding="utf-8")
