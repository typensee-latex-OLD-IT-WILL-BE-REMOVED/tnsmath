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
        nbparam, latex = v.split(";")

        functions['parameter'][k] = {
            'nbparam': nbparam.strip(),
            'latex'  : latex.strip()
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

text_start += "\n"

text_auto = "\n\\foreach \k in {{{0}}}{{\IDconstant{{\k}}}}".format(
    ", ".join(functions['no-parameter'])
)

text_table = []

tablewidth = 3

for i in range(0, len(functions['no-parameter']), tablewidth):
    sublist = functions['no-parameter'][i:i + tablewidth]
    sublist += ['']*(tablewidth - len(sublist))

    text_table.append(
        " & ".join(
            r"\verb+\{0}+".format(name)
            if name else ""
            for name in sublist
        ) + r"\\"
    )

text_table = DECO + ("\n" + DECO).join(text_table)

text_auto += r"""

\begin{{tabular*}}{{\textwidth}}{{@{{\extracolsep{{\fill}}}}*{{4}}{{l}}}}
{0}
\end{{tabular*}}

""".format(text_table)

template_tex = text_start + text_auto + text_end


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

text_table = []

paramfuncs = []

for name, infos in functions['parameter'].items():
    nbparam = int(infos['nbparam'])

    if nbparam != 1:
        plurial = "s"

    else:
        plurial = ""

    paramfuncs.append(
        r"\verb+\{0}+ \, ({1} paramètre{2})".format(
            name,
            nbparam,
            plurial
        )
    )

for i in range(0, len(paramfuncs), 4):
    sublist = paramfuncs[i:i+4]
    sublist += ['']*(4 - len(sublist))

    text_table.append(
        " & ".join(sublist) + r"\\"
    )

text_table = DECO + ("\n" + DECO).join(text_table)

text_auto = r"""
\begin{{tabular*}}{{\textwidth}}{{@{{\extracolsep{{\fill}}}}*{{4}}{{l}}}}
{0}
\end{{tabular*}}

""".format(text_table)

template_tex = text_start + text_auto + text_end
# text_auto = "\n\\foreach \k in {{{0}}}{{\IDmacro{{\k}}}}".format(
#     ", ".join(functions['parameter'])




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
