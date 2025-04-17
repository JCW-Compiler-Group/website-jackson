from functools import cache
import os
import markdown
import yaml
from typing import TextIO
from build.md_extension import PyIncludes
from datetime import date, datetime


def headers(sub_dir: str) -> list[str]:
    return [
        f'<link rel="stylesheet" href="static/style.css">',
        f'<script src="static/main.js"></script>',
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        '<link href="https://fonts.googleapis.com/css2?family=Raleway:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">',
    ]


def convert_markdown_with_frontmatter(text: TextIO) -> tuple[dict, str]:
    """
    Takes a file and reads both the frontmatter and the markdown.

    The markdown is converted to HTML.
    """
    return (
        read_frontmatter(text),
        markdown.markdown(
            text.read(),
            extensions=[
                PyIncludes(),
                "footnotes",
                "md_in_html",
                "sane_lists",
                "fenced_code",
            ],
        ),
    )


def render_markdown_file(md_path: str, sub_dir: str = "") -> str:
    """
    Takes a markdown file path as input, converts it to markdown and puts it
    inside the requested template.
    """
    with open(md_path, "r") as f:
        meta, html = convert_markdown_with_frontmatter(f)
    template = meta.get("template", "base.html")

    if "title" not in meta:
        meta["title"] = "title"

    # put stuff into the template
    return load_template(template).format(
        content=html,
        misc={
            "now": datetime.now(),
        },
        meta=meta,
        headers="\n".join(headers(sub_dir)),
    )


def write_markdown(path: str, html: str, meta: str):
    pass


def read_frontmatter(text: TextIO) -> dict:
    pos = text.tell()
    line = text.readline()
    if line.strip() != "---":
        text.seek(pos)
        return dict()

    data = []
    while not (line := text.readline()).startswith("---"):
        data.append(line)

    res = yaml.safe_load("".join(data))
    if not isinstance(res, dict):
        print(f"invalid frontmatter type: {res}")
    return res


def load_template(name: str) -> str:
    if not os.path.exists(os.path.join("templates", name)):
        return f"<b>Template <code>{name}</code> not found!</b>\n" + "{content}"

    with open(os.path.join("templates", name), "r") as f:
        return f.read()
