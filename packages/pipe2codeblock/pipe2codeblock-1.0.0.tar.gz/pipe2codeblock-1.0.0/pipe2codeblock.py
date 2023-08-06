#!/usr/bin/env python
import re
import sys
from argparse import ArgumentParser
from contextlib import contextmanager
from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE, SIG_DFL)


@contextmanager
def file_or_stdin(fpath=None):
    if fpath:
        with open(fpath) as f:
            yield f
    elif not sys.stdin.isatty():
        yield sys.stdin
    else:
        yield None


class MarkdownBlocker:
    prefix_pattern = r"^(`{3,}|~{3,})"
    suffix_pattern = r"\s*\n"

    def __init__(self, outer_stream, info_str):
        self.outer_stream = outer_stream

        self.initiator_re = re.compile(
            f"{self.prefix_pattern}{info_str}{self.suffix_pattern}", flags=re.MULTILINE
        )

        self.terminator_re = None

        self.inside_block = False
        self.after_block = False

        self.lines = []

    def make_terminator_re(self, c, n):
        return re.compile(
            "^" + c + "{3," + str(n) + "}" + self.suffix_pattern, flags=re.MULTILINE
        )

    def is_initiator(self, line):
        if self.inside_block or self.after_block:
            return None
        ret = self.initiator_re.search(line)
        if ret:
            grp = ret.groups()[0]
            return grp[0], len(grp)
        else:
            return None

    def is_terminator(self, line):
        return self.inside_block and self.terminator_re.match(line)

    def parse(self, inner_stream):
        for line in self.outer_stream:
            if self.inside_block:
                if not self.is_terminator(line):
                    continue
                self.inside_block = False
                self.after_block = True
            elif not self.after_block:
                init = self.is_initiator(line)
                if init:
                    self.lines.append(line)
                    self.terminator_re = self.make_terminator_re(*init)
                    self.inside_block = True
                    self.lines.extend(inner_stream)
                    continue

            self.lines.append(line)

        if self.inside_block:
            raise ValueError("Unterminated code block")
        return self

    def write(self):
        self.outer_stream.seek(0)
        for line in self.lines:
            self.outer_stream.write(line)


def run(outfile, tgt_str="help", infile=None):
    with open(outfile, "r+") as tgt_file, file_or_stdin(infile) as src_file:
        MarkdownBlocker(tgt_file, tgt_str).parse(src_file).write()


def main():
    parser = ArgumentParser(
        prog="p2c", description="Pipe text into a code block in a markdown file."
    )
    parser.add_argument("outfile")
    parser.add_argument(
        "--tgt",
        default="help",
        help="Target a code block with a different info string (default 'help')",
    )
    parser.add_argument("infile", nargs="?")

    parsed = parser.parse_args()

    run(parsed.outfile, parsed.tgt, parsed.infile)


if __name__ == "__main__":
    main()
