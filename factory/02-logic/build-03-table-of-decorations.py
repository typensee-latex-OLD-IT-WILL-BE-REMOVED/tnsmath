#! /usr/bin/env python3

from collections import defaultdict
import re

from mistool.os_use import PPath
from mistool.string_use import between, joinand
from orpyste.data import ReadBlock

BASENAME = PPath(__file__).stem.replace("build-", "")

THIS_DIR = PPath(__file__).parent
TEX_FILE = THIS_DIR / f"{BASENAME}[fr].tex"

DECO = " "*4


# -------------------------- #
# -- THE OPERATORS TO ADD -- #
# -------------------------- #

opedecos = defaultdict(list)

for peufname in [
    "equal-signs-n-co",
    "operators",
]:
    with ReadBlock(
        content = THIS_DIR / f"{peufname}.peuf",
        mode    = {
            'verbatim'  : "decorations",
            'keyval:: =': ":default:"
        }
    ) as data:
        infos    = data.mydict("std mini")
        alldecos = infos["decorations"]

        opedecos[":alldecos:"] += alldecos

        for openames, decos in infos["todecorate"].items():
            openames = [
                n.strip()
                for n in openames.split(",")
            ]

            if decos == ":all:":
                decos = list(alldecos)

            else:
                decos = [
                    d.strip()
                    for d in decos.split(",")
                ]

            for onename in openames:
                opedecos[onename] = decos

        if "stars" in infos:
            for starversion in infos["stars"]:
                namedeco = starversion
                stars    = ""

                while(namedeco[-1] == "*"):
                    namedeco  = namedeco[:-1]
                    stars    += "*"

                suffix = ""

                for deco in alldecos:
                    if len(deco) > len(suffix) \
                    and namedeco.endswith(deco):
                        suffix = deco

                namealone = namedeco[:-len(suffix)]

                stardeco = suffix + stars

                opedecos[namealone].append(stardeco)
                opedecos[":alldecos:"].append(stardeco)


alldecos = list(set(opedecos[":alldecos:"]))
alldecos.sort()

del opedecos[":alldecos:"]

# ------------------------- #
# -- TEMPLATES TO UPDATE -- #
# ------------------------- #

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
    text = template_tex,
    seps = [
        "% == Table - START == %\n",
        "% == Table - END == %"
    ],
    keepseps = True
)

table_header = DECO*3 + "  & {0} \\\\".format(
    " & ".join(
        f"\\verb+{d}+" for d in alldecos
    )
)

table_lines = []

for oneopedeco, itsdecos in opedecos.items():
    cells = [f"\\verb+\\{oneopedeco}+"]

    for d in alldecos:
        hasdeco = True

        if d not in itsdecos:
            hasdeco = False

        if hasdeco:
            cells.append(r'$\times$')

        else:
            cells.append('        ')

    table_lines.append(" & ".join(cells) + r' \\')

table_lines = f'{DECO*3}\\hline ' \
            + f'\n{DECO*3}\\hline '.join(table_lines)

latextable = f"""
\\begin{{table}}[h]
    \\caption{{Décorations}}
    \\begin{{center}}
        \\begin{{tabular}}{{{'c|'*(len( alldecos))}c}}
{table_header}
{table_lines}
        \\end{{tabular}}
    \\end{{center}}
    \\label{{table:decorations-operators}}
\\end{{table}}

"""

template_tex = text_start + latextable + text_end


# -------------------------- #
# -- UPDATES OF THE FILES -- #
# -------------------------- #

with open(
    file     = TEX_FILE,
    mode     = 'w',
    encoding = 'utf-8'
) as docfile:
    docfile.write(template_tex)
