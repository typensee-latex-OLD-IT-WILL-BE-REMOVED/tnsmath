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
    mode    = "verbatim"
) as data:
    constants = {
        k: " ".join(v).split()
        for k, v in data.mydict("std mini").items()
    }

allconstants = constants["greek"] + constants["roman"]


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
        "% Constants - START",
        "% Constants - END"
    ],
    keepseps = True
)

text_start += "\n\n% User's constants\n"
text_end = text_end.lstrip()

text_auto = [
    r"""
\newcommand\ct[1]{{%
    \IfStrEqCase{{#1}}{{%
        {0}
    }}[\text{{\textbf{{#1}}}}]
}}

% Classical constants
    """.format(
        ("\n" + DECO*2).join(
            r"{{{0}}}{{\up{0}}}%".format(gletter)
            for gletter in constants["greek"]
        )
    )
]

for ct in constants["greek"] + constants["roman"]:
    text_auto.append(
        "\\newcommand\{0[0]}{0}{{\ct{{{0}}}}}".format(ct)
    )

text_auto.append("\n")

text_auto = "\n".join(text_auto)

template_sty = text_start + text_auto + text_end


# ------------------------------- #
# -- UPDATING LIST FOR THE DOC -- #
# ------------------------------- #

text_start, _, text_end = between(
    text = template_tex,
    seps = [
        "% List of classical constants - START",
        "% List of classical constants - END",
    ],
    keepseps = True
)

text_auto = "\n\n\\foreach \k in {{{0}}}{{\IDconstant{{\k}}}}".format(
    ", ".join(
        "{0[0]}{0}".format(x) for x in allconstants
    )
)

text_auto += r"""

\begin{{tcblisting}}{{}}
Voici la liste des constantes classiques où $\ttau = 2 \ppi$ est la benjamine :
{0}.
\end{{tcblisting}}

""".format(
    joinand([
        "$\{0[0]}{0}$".format(c) for c in allconstants
    ])
)

template_tex = text_start + text_auto + text_end


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
