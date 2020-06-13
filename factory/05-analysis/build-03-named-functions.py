#! /usr/bin/env python3

import re

from collections import defaultdict
from itertools import product

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
# -- THE CONSTANTS TO ADD -- #
# -------------------------- #

with ReadBlock(
    content = PEUF_FILE,
    mode    = "keyval:: ="
) as data:
    functions = data.mydict("std mini")

    for k, v in functions['no-parameter'].items():
        if not v:
            functions['no-parameter'][k] = k

    for k, v in functions['parameter'].items():
        nbparam, latex, *desc = v.split(";")

        functions['parameter'][k] = {
            'nbparam': nbparam.strip(),
            'latex'  : latex.strip(),
            'desc'   : [d.strip() for d in desc],
        }


# ------------------------------ #
# -- LATEX TEMPLATE TO UPDATE -- #
# ------------------------------ #

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
        "% Classical functions - START",
        "% Classical functions - END"
    ],
    keepseps = True
)

text_auto = [
    "\n",
    "\n".join(
        r"\DeclareMathOperator{{\{0}}}{{\operatorname{{{1}}}}}".format(
            latexname,
            humanname
        )
        for latexname, humanname in functions['no-parameter'].items()
    ),
    "",
    "\n".join(
        r"\newcommand\{0}[{1[nbparam]}]{{{1[latex]}}}".format(
            name,
            infos
        )
        for name, infos in functions['parameter'].items()
    )
]

text_auto.append("\n")

text_auto = "\n".join(text_auto)

template_sty = text_start + text_auto + text_end


# ------------------------------ #
# -- UPDATING SUMMARING TABLE -- #
# ------------------------------ #

text_start, _, text_end = between(
    text = template_tex,
    seps = [
        "% Table of all - START",
        "% Table of all - END"
    ],
    keepseps = True
)

tabletex = [
    f"\\verb+{name}+ : $\\{name}\dots$"
    for name in list(functions['no-parameter'])
] + [
    f"\\verb+{name}{{p}}+ : $\\{name}{{p}}\dots$"
    for name in list(functions['parameter'])
]

tabletex = '\n\n'.join(tabletex)

template_tex = text_start + f"\n{tabletex}\n" + text_end


# ----------------------------------------------- #
# -- UPDATING LISTS FOR THE DOC - NO PARAMETER -- #
# ----------------------------------------------- #

text_start, _, text_end = between(
    text = template_tex,
    seps = [
        "% List of functions without parameter - START",
        "% List of functions without parameter - END"
    ],
    keepseps = True
)


template_tex = []
lastmacros   = []
lastfirst    = ""
lastlenght   = -1

for onemacro in list(functions['no-parameter'].keys()) + ["ZZZZ-unsed-ZZZZ"]:
    if lastfirst:
        if lastfirst != onemacro[0] \
        or lastlenght != len(onemacro):
            lastmacros = ", ".join(lastmacros)

            if lastfirst == "f":
                extra ="  où \\quad \\mwhyprefix{{f}}{{rench}}"

            else:
                extra = ""

            template_tex += [
                f"""
\\foreach \\k in {{{lastmacros}}}{{

    \\IDmacro*{{\k}}{{0}}{extra}
}}
                """,
                "\\separation"
                ""
            ]

            lastfirst  = onemacro[0]
            lastlenght = len(onemacro)
            lastmacros = []

    else:
        lastfirst  = onemacro[0]
        lastlenght = len(onemacro)

    lastmacros.append(onemacro)


template_tex = "\n".join(template_tex[:-3])
template_tex = f"{text_start}{template_tex}{text_end}"



# --------------------------------------------- #
# -- UPDATING LISTS FOR THE DOC - PARAMETERS -- #
# --------------------------------------------- #

text_start, _, text_end = between(
    text = template_tex,
    seps = [
        "% List of functions with parameters - START",
        "% List of functions with parameters - END"
    ],
    keepseps = True
)

text_start += "\n"

docinfos = []

for name, infos in functions['parameter'].items():
    nbparam = int(infos['nbparam'])

    docinfos += [
        "\\separation",
        f"\\IDmacro*{{{name}}}{{{nbparam}}}"
    ]

    desc = infos["desc"]

    if len(desc) == 1:
        docinfos.append(f"\\IDarg{{}} {desc[0]}")

    else:
        for i, d in enumerate(desc, 1):
            docinfos.append(f"\\IDarg{{{i}}} {d}")

docinfos.append("")
docinfos = [""] + docinfos[1:]

template_tex = text_start + "\n\n".join(docinfos) + text_end


# -------------------------- #
# -- UPDATES OF THE FILES -- #
# -------------------------- #

with open(
    file     = TEX_FILE,
    mode     = 'w',
    encoding = 'utf-8'
) as docfile:
    docfile.write(template_tex)

with open(
    file     = STY_FILE,
    mode     = 'w',
    encoding = 'utf-8'
) as docfile:
    docfile.write(template_sty)
