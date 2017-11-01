#! /usr/bin/env python3

from mistool.os_use import PPath
from mistool.string_use import between, joinand
from orpyste.data import ReadBlock

THIS_DIR = PPath( __file__ ).parent
TEX_FILE = THIS_DIR / '03-named-functions.tex'

DECO = " "*4


# -------------------------- #
# -- THE CONSTANTS TO ADD -- #
# -------------------------- #

with ReadBlock(
    content = THIS_DIR / "functions.peuf",
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
        "% Classical functions",
        r"\begin{document}"
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

text_auto.append("\n"*3)

text_auto = "\n".join(text_auto)

template = text_start + text_auto + text_end


# ----------------------------------------------- #
# -- UPDATING LISTS FOR THE DOC - NO PARAMETER -- #
# ----------------------------------------------- #

text_start, _, text_end = between(
    text = template,
    seps = [
        "% List of functions without parameter",
        r"\end{tabular*}"
    ]
)

text_start += "% List of functions without parameter\n"

text_auto = "\n\\foreach \k in {{{0}}}{{\IDconstant{{\k}}}}".format(
    ", ".join(functions['no-parameter'])
)

text_table = []

for i in range(0, len(functions['no-parameter']), 4):
    sublist = functions['no-parameter'][i:i+4]
    sublist += ['']*(4 - len(sublist))

    text_table.append(
        " & ".join(
            r"\verb+\{0}+".format(name)
            if name else ""
            for name in sublist
        ) + r"\\"
    )

text_table = DECO + ("\n" + DECO).join(text_table)

text_auto += r"""

\medskip

\begin{{tabular*}}{{\textwidth}}%
                {{@{{\extracolsep{{\fill}}}}*{{4}}{{l}}}}
{0}
\end{{tabular*}}
""".format(text_table)

text_auto = text_auto.rstrip()

template = text_start + text_auto + text_end


# --------------------------------------------- #
# -- UPDATING LISTS FOR THE DOC - PARAMETERS -- #
# --------------------------------------------- #

text_start, _, text_end = between(
    text = template,
    seps = [
        "% List of functions with parameters",
        r"\end{tabular*}"
    ]
)

text_start += "% List of functions with parameters\n"

text_table = []

paramfuncs = []

for name, infos in functions['parameter'].items():
    nbparam = int(infos['nbparam'])

    if nbparam != 1:
        plurial = "s"

    else:
        plurial = ""

    paramfuncs.append(
        r"\verb+\{0}+ \, ({1} parameter{2})".format(
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
\medskip

\begin{{tabular*}}{{\textwidth}}%
                {{@{{\extracolsep{{\fill}}}}*{{4}}{{l}}}}
{0}
\end{{tabular*}}""".format(text_table)

text = text_start + text_auto + text_end
# text_auto = "\n\\foreach \k in {{{0}}}{{\IDmacro{{\k}}}}".format(
#     ", ".join(functions['parameter'])
# )


with open(
    file     = TEX_FILE,
    mode     = 'w',
    encoding = 'utf-8'
) as docfile:
    docfile.write(text)
