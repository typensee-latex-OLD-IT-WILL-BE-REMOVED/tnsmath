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
    mode    = {
        "verbatim"  : 'no-parameter',
        "keyval:: =": 'parameter'
    }
) as data:
    functions = data.mydict("std mini")

    functions['no-parameter'] = " ".join(
        functions['no-parameter']
    ).split()

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
        r"\DeclareMathMacro{{\{0}}}{{\operatorname{{{0}}}}}".format(name)
        for name in functions['no-parameter']
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

template_tex = text_start + f"""

\\foreach \\k in {{{", ".join(functions['no-parameter'])}}}{{

	\\IDmacro*{{\k}}{{0}}

}}
""" + "\n" + text_end


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
        "\\bigskip",
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
