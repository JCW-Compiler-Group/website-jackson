# Jackson Woodruffs Website

## Build Process:

Every file in `/content` will be converted to an output file in `/out`.

Markdown files will be parsed and converted to HTML according to their meta information (frontmatter).

Markdown files can call out to arbitrary python methods for dynamically generated content
(such as bibliography, team member profiles, etc.)

Building is done simply by running `poetry install && poetry run python -m build`.

There's a yaml file with a bunch of information such as team members, published papers, etc. called `meta.yml`. A bunch of build steps read from that file to e.g. create the publications list.

### Build Includes

The current build process makes use of the following generators:

- `build.members list` to build the list of team members from the data in `meta.yml`
- `build.publications` to build the publications of the front page, also from `meta.yml`
- `build.index`, generic thingy to build an index for a given folder. Just prints a markdown list of links.

## Running Locally:

Make sure you install dependencies with poetry beforehand (`poetry install`), you can then enter a shell with the venv active using `poetry shell`. In there you can run `python -m build -l`, which will serve the website locally, enabling you to change the markdown and reload instantly without building.

## Python Script Includes

During parsing, `![[<source> <arguments?>]]` blocks will result in a call to `<source>`, possibly with `arguments` as args. Source might be either a module `my_module.submodule`, a Python file `coolstuff.py`, or a module + a method name `my_module:some_function`. The arguments (of present) are passed onto the function, module or file.

## How This Website Builder Works:

This website is a tiny shim on top of `markdown`. Basically, the markdown is parsed, and then script includes are executed. This allows one to execute python to generate parts of files: `![[build.members list]]` will run `python -m build.members list` and paste the output into the resultant file. This process is meant to simplify managing member lists in multiple places, as well as including publications, etc.

The markdown file is then converted to HTML, and pasted into a HTML shell (called template) through simple python format strings.

The generated files are dumped into `/out`, the `static` folder is copied over, and that's it. No more magic.

##Deploy Instructions
copy /out to /docs.
