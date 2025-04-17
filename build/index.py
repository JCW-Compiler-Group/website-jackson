import argparse
import glob
import os
from build.rendering import read_frontmatter


def build_index(base_dir: str):
    # remove leading slash
    base_dir = base_dir.lstrip("/")

    for file in glob.glob("*.md", root_dir=os.path.join("content", base_dir)):
        # ignore index.md
        if file == "index.md":
            continue

        # build full path to file
        full_path = os.path.join("content", base_dir, file)

        # read frontmatter
        with open(full_path, "r") as f:
            meta = read_frontmatter(f)

        # print link
        print(f'- [{meta.get("title", file)}]({file[:-3]}.html)')


if __name__ == "__main__":
    parser = argparse.ArgumentParser("build.index", "Builds an index of a folder")
    parser.add_argument(
        "directory",
        help="The base directory (relative from /content) for which to generate the index for",
    )

    args = parser.parse_args()
    build_index(args.directory)
