#!/usr/bin/env python
import os
import sys

from pathlib import Path

import yaml


def mac_outfile(out, syn):
    import plistlib
    with open(out, "wb") as fp:
        plistlib.dump(syn, fp)


def main():
    current_dir = Path(os.path.abspath(os.path.dirname(__file__)))
    in_path = current_dir.joinpath("restructuredtext.tmLanguage.yaml")
    out_path = current_dir.joinpath("restructuredtext.tmLanguage")
    with open(in_path, "rt") as fp:
        syntax = yaml.safe_load(fp)

    if sys.platform.startswith('osx'):  # is this right?
        mac_outfile(out_path, syntax)
    import pdb; pdb.set_trace()


if __name__ == "__main__":
    main()
