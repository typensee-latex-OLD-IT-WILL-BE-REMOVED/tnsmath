#! /usr/bin/env python3

from mistool.os_use import PPath
from mistool.string_use import between, joinand
from orpyste.data import ReadBlock

THIS_DIR = PPath( __file__ ).parent
TEX_FILE = THIS_DIR / '01-constants.tex'

DECO = " "*4


# -------------------------- #
# -- THE CONSTANTS TO ADD -- #
# -------------------------- #

with ReadBlock(
    content = THIS_DIR / "constants.peuf",
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
    file     = TEX_FILE,
    mode     = 'r',
    encoding = 'utf-8'
) as docfile:
    template = docfile.read()


# --------------------- #
# -- UPDATING MACROS -- #
# --------------------- #

text_start, _, text_end = between(
    text = template,
    seps = [
        "% User's constants",
        r"\begin{document}"
    ]
)

text_start += "% User's constants\n"
text_end    = r"\begin{document}" + text_end

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

text_auto.append("\n"*3)

text_auto = "\n".join(text_auto)

template = text_start + text_auto + text_end


# ------------------------------- #
# -- UPDATING LIST FOR THE DOC -- #
# ------------------------------- #

text_start, _, text_end = between(
    text = template,
    seps = [
        "% List of classical constants",
        r"\end{tcblisting}"
    ]
)

text_start += "% List of classical constants\n"

text_auto = "\n\\foreach \k in {{{0}}}{{\IDconstant{{\k}}}}".format(
    ", ".join(
        "{0[0]}{0}".format(x) for x in allconstants
    )
)

text_auto += r"""

\begin{{tcblisting}}{{}}
List of all classical constants where $\ttau = 2 \ppi$ is the youngest one:
{0}.
\end{{tcblisting}}""".format(
    joinand([
        "$\{0[0]}{0}$".format(c) for c in allconstants
    ])
)

text = text_start + text_auto + text_end


with open(
    file     = TEX_FILE,
    mode     = 'w',
    encoding = 'utf-8'
) as docfile:
    docfile.write(text)
