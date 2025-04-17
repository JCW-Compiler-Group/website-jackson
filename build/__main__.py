import os
import glob
import argparse
import pathlib

import shutil
import sys


from build.rendering import render_markdown_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="build", usage="Builds Jackson Woodruffs Website"
    )
    parser.add_argument("-o", "--output", default="out/", help="Output directory")
    parser.add_argument(
        "-d", "--base-dir", default="./", help="The base directory of the blog"
    )
    parser.add_argument(
        "-l", "--live", action="store_true", help="Run a live demo of the website"
    )
    parser.add_argument(
        "--pure",
        action="store_true",
        help="Delete output directory if present before building",
    )
    parser.add_argument(
        "--sub-dir",
        default="",
        help="Sub-directory from which the website is served (e.g. if the website is deployed to https://mydomain.com/wiki/, this value should be set to `/wiki`)",
    )
    parser.add_argument("--host", default="localhost", help="Host to serve on")
    parser.add_argument("--port", default=8080, type=int, help="Port to serve on")

    args = parser.parse_args()

    # chdir to base_dir
    os.chdir(args.base_dir)

    # allow live serving
    if args.live:
        import build.live

        build.live.serve_live(args.host, args.port)
        sys.exit(0)

    # empty previous output
    if args.pure:
        shutil.rmtree(args.output, ignore_errors=True)

    # create out dir
    pathlib.Path(args.output).mkdir(parents=True, exist_ok=True)

    # find all markdown files
    for file in glob.glob("**/*.md", root_dir="content", recursive=True):
        # render them out
        dest_file = f"{file[:-3]}.html"

        dest_path = os.path.join(args.output, dest_file)

        # make sure folder exists
        pathlib.Path(os.path.dirname(dest_path)).mkdir(parents=True, exist_ok=True)

        # convert and write to file:
        with open(dest_path, "w") as f:
            f.write(render_markdown_file(os.path.join("content", file), args.sub_dir))

    # copy over static content
    shutil.copytree("static", args.output + "/static", dirs_exist_ok=True)

    # make sure favicon.ico is copied to base dir (if it exists)
    if os.path.exists("static/favicon.ico"):
        shutil.copy2("static/favicon.ico", os.path.join(args.output, "favicon.ico"))
