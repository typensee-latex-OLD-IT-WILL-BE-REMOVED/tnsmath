#! /usr/bin/env python3

from mistool.os_use import PPath
from mistool.string_use import between, joinand
from orpyste.data import ReadBlock

THIS_DIR = PPath( __file__ ).parent

DECO = " "*4


with open(
    file     = THIS_DIR / "config" / "header.tex",
    encoding = "utf-8"
) as headerfile:
    _, HEADER, _ = between(
        text = headerfile.read(),
        seps = [
            r"\documentclass[12pt,a4paper]{article}",
            r"\begin{document}"
        ]
    )

    HEADER = f"\n{HEADER.rstrip()}\n\n"


for subdir in THIS_DIR.walk("dir::"):
    subdir_name = str(subdir.name)

    if subdir_name in [
        "config",
    ] or subdir_name[:2] == "x-":
        continue

    for latexfile in subdir.walk("file::**.tex"):
        print("   * Updating << {0} >>".format(latexfile - THIS_DIR))

        with open(
            file     = latexfile,
            encoding = "utf-8"
        ) as filetoupdate:
            start, _, end = between(
                text = filetoupdate.read(),
                seps = [
                    "% == FOR DOC AND TESTS - START == %",
                    "% == FOR DOC AND TESTS - END == %"
                ],
                keepseps = True
            )

        with open(
            file     = latexfile,
            mode     = "w",
            encoding = "utf-8"
        ) as filetoupdate:
            filetoupdate.write(start + HEADER + end)
