#! /usr/bin/env python3

import re

from mistool.os_use import PPath
from mistool.string_use import between, joinand
from orpyste.data import ReadBlock

BASENAME = PPath(__file__).stem.replace("build-", "")

THIS_DIR = PPath(__file__).parent
STY_FILE = THIS_DIR / f'{BASENAME}.sty'
TEX_FILE = STY_FILE.parent / (STY_FILE.stem + "[fr].tex")

PATTERN_FOR_PEUF = re.compile("\d+-(.*)")
match            = re.search(PATTERN_FOR_PEUF, STY_FILE.stem)
PEUF_FILE        = STY_FILE.parent / (match.group(1).strip() + ".peuf")

DECO = " "*4


# -------------------------- #
# -- THE OPERATORS TO ADD -- #
# -------------------------- #

with ReadBlock(
    content = PEUF_FILE,
    mode    = {
        'verbatim'  : "decorations",
        'keyval:: =': ["latex", "todecorate"]
    }
) as data:
    infos = data.mydict("std mini")

    infos["decorations"] = [
        d.strip()
        for d in infos["decorations"]
        if d.strip()
    ]


# ------------------------- #
# -- TEMPLATES TO UPDATE -- #
# ------------------------- #

with open(
    file     = STY_FILE,
    mode     = 'r',
    encoding = 'utf-8'
) as styfile:
    template_sty = styfile.read()


with open(
    file     = TEX_FILE,
    mode     = 'r',
    encoding = 'utf-8'
) as docfile:
    template_tex = docfile.read()


# --------------------- #
# -- UPDATING MACROS -- #
# --------------------- #

text_start, _, text_end = between(
    text = template_sty,
    seps = [
        "% == Decorated versions - START == %\n",
        "\n% == Decorated versions - END == %"
    ],
    keepseps = True
)

newmacros   = []
latexmacros = []

for symb, assocdecos in infos["todecorate"].items():
    if symb in infos["latex"]:
        latexmacros.append(
            f"\\newcommand\\{symb}{{{infos['latex'][symb]}}}"
        )

    newmacros.append("")

    if assocdecos == ":all:":
        for onedeco in infos["decorations"]:
            newmacros.append(
f"\\newcommand\\{symb}{onedeco}{{\\@over@math@symbol{{\\textop{onedeco}}}{{\\{symb}}}}}"
            )


newmacros   = '\n'.join(newmacros[1:])
latexmacros = '\n'.join(latexmacros)

template_sty = text_start + f"""
{latexmacros}

{newmacros}
""" + text_end


# ---------------------- #
# -- UPDATING THE DOC -- #
# ---------------------- #

text_start, _, text_end = between(
    text = template_tex,
    seps = [
        "% == Example of decorated versions - START == %\n",
        "\n% == Example of decorated versions - END == %"
    ],
    keepseps = True
)

fullnames = {
    'iff'    : "Équivalences",
    'implies': "Implications directes",
    'liesimp': "Implications indirectes",
}

latexample = []

for symb, assocdecos in infos["todecorate"].items():
    latexample += ["", f"{fullnames[symb]} :"]

    examples = [f"{chr(65)}"]

    for i, onedeco in enumerate(infos["decorations"], start = 1):
        examples.append(f"\\{symb}{onedeco} {chr(65 + i)}")

    if symb == "iff":
        fullexample = " ".join(examples)

    else:
        fullexample = examples[0] + " "

        for i in range(1, len(examples), 3):
            if i != 1:
                fullexample += "\n   "

            fullexample += " ".join(examples[i: i+3])

    latexample.append(f"${fullexample}$")

latexample = "\n".join(latexample[1:])

template_tex = text_start + f"""
\\begin{{tcblisting}}{{}}
{latexample}
\\end{{tcblisting}}
""" + text_end


text_start, _, text_end = between(
    text = template_tex,
    seps = [
        "% == Decorated versions - START == %\n",
        "\n% == Decorated versions - END == %"
    ],
    keepseps = True
)

allmacros = []

for symb, assocdecos in infos["todecorate"].items():
    allmacros += [symb]

    if assocdecos == ":all:":
        for onedeco in infos["decorations"]:
            allmacros.append(f"{symb}{onedeco}")

allmacros = ", ".join(allmacros)

template_tex = text_start + f"""
\\foreach \\k in {{{allmacros}}}{{

	\\IDmacro*{{\k}}{{0}}

}}
""" + text_end


text_start, _, text_end = between(
    text = template_tex,
    seps = [
        "% == Vertical versions - START == %\n",
        "\n% == Vertical versions - END == %"
    ],
    keepseps = True
)

allmacros = [
    "v" + m
    for m in infos["todecorate"]
]

allmacros = ", ".join(allmacros)

template_tex = text_start + f"""
\\foreach \\k in {{{allmacros}}}{{

	\\IDmacro*{{\k}}{{0}}

}}
""" + text_end

# -------------------------- #
# -- UPDATES OF THE FILES -- #
# -------------------------- #

with open(
    file     = STY_FILE,
    mode     = 'w',
    encoding = 'utf-8'
) as docfile:
    docfile.write(template_sty)

with open(
    file     = TEX_FILE,
    mode     = 'w',
    encoding = 'utf-8'
) as docfile:
    docfile.write(template_tex)
