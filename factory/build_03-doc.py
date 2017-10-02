#! /usr/bin/env python3

from collections import defaultdict

from mistool.latex_use import Build
from mistool.os_use import cd, PPath, runthis
from mistool.string_use import between, case, joinand, MultiReplace
from mistool.term_use import ALL_FRAMES, withframe
from orpyste.data import ReadBlock

THIS_DIR = PPath( __file__ ).parent

TEMPLATE_PATH = THIS_DIR / "config" / "doc.tex"
DOC_PATH      = THIS_DIR.parent / "lymath" / "lymath-doc.tex"

DOUBLE_BRACES = MultiReplace({
    '{': '{{',
    '}': '}}'
})

PYFORMAT = MultiReplace({
    '%((': '{',
    '))%': '}'
})


# ----------------------- #
# -- TOOLS & CONSTANTS -- #
# ----------------------- #

DECO = " "*4
RULE = "-"*30

MYFRAME = lambda x: withframe(
    text  = x,
    frame = ALL_FRAMES['latex_pretty']
)

SECTIONS = """
section
subsection
subsubsection
paragraph
""".strip()

SECTIONS = [
    f"\\{seccmd}" for seccmd in SECTIONS.split("\n")[::-1]
]

def uplevelsections(source):
    global SECTIONS

    for i, seccmd in enumerate(SECTIONS[1:]):
         source = source.replace(seccmd, SECTIONS[i])

    return source


# ------------ #
# -- HEADER -- #
# ------------ #

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

    HEADER = HEADER.strip()


# ---------------------- #
# -- LOOKING FOR DOCS -- #
# ---------------------- #

CONTENTS = []

for subdir in THIS_DIR.walk("dir::"):
    subdir_name = str(subdir.name)

    if subdir_name in [
        "config",
    ] or subdir_name[:2] == "x-":
        continue

    sectionname = subdir_name.split("-", 1)[1]
    sectionname = sectionname.replace("-", " ")
    sectionname = case(sectionname, "sentence")

    CONTENTS.append(f"\\section{{{sectionname}}}\n")

    for latexfile in subdir.walk("file::**.tex"):
        with latexfile.open(
            mode     = "r",
            encoding = "utf-8"
        ) as texfile:
            _, content, _ = between(
                text = texfile.read(),
                seps = [
                    r"\begin{document}",
                    r"\end{document}"
                ]
            )

            content = uplevelsections(content)

            CONTENTS.append(content)


# ------------------------- #
# -- UPDATE THE DOC FILE -- #
# ------------------------- #

print(f"{DECO}* Update of << {DOC_PATH.name} >> done.")

with TEMPLATE_PATH.open(
    mode     = "r",
    encoding = "utf-8"
) as docfile:
    content = DOUBLE_BRACES(docfile.read())
    content = PYFORMAT(content)
    content = content.format(
        HEADER,
        "\n".join(CONTENTS)
    )


with DOC_PATH.open(
    mode     = "w",
    encoding = "utf-8"
) as docfile:
    docfile.write(content)


# -------------------------- #
# -- COMPILE THE DOC FILE -- #
# -------------------------- #

print(
    f"{DECO}* Compilation of << {DOC_PATH.name} >> started.",
    RULE,
    sep = "\n"
)

builder = Build(DOC_PATH, 3)
builder.pdf()

print(
    RULE,
    f"{DECO}* Compilation of << {DOC_PATH.name} >> finished.",
    sep = "\n"
)
