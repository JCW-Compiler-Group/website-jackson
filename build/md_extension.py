import markdown
import markdown.blockprocessors
import re
import xml.etree.ElementTree as etree
import logging
import subprocess

logger = logging.getLogger(__name__)


class IncludeSyntaxProcessor(markdown.blockprocessors.BlockProcessor):
    RE = re.compile(r"(?:^|\n)!\[\[(\S+(:\S+)?)( (.*))?\]\]\s*$")

    def test(self, parent: etree.Element, block: str) -> bool:
        return bool(self.RE.search(block))

    def run(self, parent: etree.Element, blocks: list[str]) -> None:
        block = blocks.pop(0)
        m = self.RE.search(block)
        if m:
            before = block[: m.start()]  # All lines before include
            after = block[m.end() :]  # All lines after include
            if before:
                # As the include was not the first line of the block and the
                # lines before the include must be parsed first,
                # recursively parse this lines as a block.
                self.parser.parseBlocks(parent, [before])
            # Create header using named groups from RE
            content = run_included_file(m.group(1), m.group(4))
            blocks.insert(0, content)
            if after:
                # Insert remaining lines as first block for future parsing.
                blocks.insert(1, after)
        else:  # pragma: no cover
            # This should never happen, but just in case...
            logger.warning("We've got a problem include: %r" % block)


def run_included_file(name: str, args: str | None):
    if ":" in name:
        module, fn = name.split(":", 1)
    else:
        module, fn = name, None
    args = [] if args is None else split_arguments(args)

    if module.endswith(".py"):
        if ":" in name:
            logger.error("Can't run method from file, use module syntax instead!")
            return "Error - see log!"

        return run_file(module, args)
    else:
        return run_module(module, fn, args)


def split_arguments(args: str) -> list[str]:
    """
    Split whitespace separated arguments into a list of arguments.

    Respects quoted strings
    """
    out_args = []
    # temporary list to buffer enclosed strings
    tmp: list[str] | None = None
    for part in args.split(" "):
        if tmp is not None:
            tmp.append(part)
            if part.endswith('"') and not part.endswith('\\"'):
                out_args.append(" ".join(tmp))
            tmp = None
        if part.startswith('"'):
            if part.endswith('"') and not part.endswith('\\"'):
                out_args.append(part)
            else:
                tmp = [part]
        else:
            out_args.append(part)
    if tmp is not None:
        raise ValueError("Malformed argument string")
    return out_args


def run_module(module: str, fn: str | None, args: list) -> str:
    if fn is None:
        # just run the module's main:
        return subprocess.check_output(["python", "-m", module, *args], text=True)

    # build an invocatin that imports the module and runs the file:
    return subprocess.check_output(
        ["python", "-c", f"import {module}; print({module}.{fn}({','.join(args)}))"],
        text=True,
    )


def run_file(path: str, args: list) -> str:
    return subprocess.check_output(["python", path, *args], text=True)


class PyIncludes(markdown.Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(
            IncludeSyntaxProcessor(md.parser), "include", 90
        )
