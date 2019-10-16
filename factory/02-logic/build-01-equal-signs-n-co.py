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
        'keyval:: =': ":default:"
    }
) as data:
    INFOS = data.mydict("std mini")

    INFOS["decorations"] = [
        d.strip()
        for d in INFOS["decorations"]
        if d.strip()
    ]


STAR_VERSIONS = {
    "*" : {},
    "**": {},
}

stardeco = ["**", "*"]
macromet = []

for macro, latexdef in INFOS["stars"].items():
    for onedeco in stardeco:
        if macro in macromet:
            continue

        nbstars = len(onedeco)

        if macro.endswith(onedeco):
            STAR_VERSIONS[onedeco][macro[:-nbstars]] = latexdef

            macromet.append(macro)

del INFOS["stars"]

ALL_DECOS = [
    d
    for d in INFOS["decorations"]
]

easydecos = {}

for symbnames, decos in INFOS["todecorate"].items():
    if decos == ":all:":
        decos = ALL_DECOS

    else:
        decos = [
            d.strip()
            for d in decos.split(',')
        ]

    for onesymbname in symbnames.split(","):
        onesymbname = onesymbname.strip()

        easydecos[onesymbname] = decos

INFOS["todecorate"] = easydecos

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

ALL_OPES_DECO = []

newmacros = []

for symbname, decos in INFOS["todecorate"].items():
    symb = INFOS["latex"][symbname]
    newmacros.append('')

    for onedeco in decos:
        macroname   = symbname + onedeco
        textversion = f"\\@over@math@symbol{{\\textop{onedeco}}}{{{symb}}}"

        ALL_OPES_DECO.append(macroname)

# Double star version
        if macroname in STAR_VERSIONS["**"]:
            onestarver  = STAR_VERSIONS["*"][macroname]
            twostarsver = STAR_VERSIONS["**"][macroname]

            ALL_OPES_DECO += [ALL_OPES_DECO[-1] + "*"]
            ALL_OPES_DECO += [ALL_OPES_DECO[-1] + "*"]

            newmacros += [
f"\\newcommand\\{macroname}{{\@ifstar{{\@{macroname}@pre@star}}{{\@{macroname}@no@star}}}}",
f"\\newcommand\\@{macroname}@pre@star{{\@ifstar{{\@{macroname}@star@star}}{{\@{macroname}@star}}}}",
f"\\newcommand\\@{macroname}@no@star{{{textversion}}}",
f"\\newcommand\\@{macroname}@star{{{onestarver}}}",
f"\\newcommand\\@{macroname}@star@star{{{twostarsver}}}",
""
            ]

# Simple star version
        elif macroname in STAR_VERSIONS["*"]:
            onestarver  = STAR_VERSIONS["*"][macroname]

            ALL_OPES_DECO += [ALL_OPES_DECO[-1] + "*"]

            newmacros += [
f"\\newcommand\\{macroname}{{\@ifstar{{\@{macroname}@star}}{{\@{macroname}@no@star}}}}",
f"\\newcommand\\@{macroname}@no@star{{{textversion}}}",
f"\\newcommand\\@{macroname}@star{{{onestarver}}}",
""
            ]

# No star version
        else:
            newmacros.append(
f"\\newcommand\\{macroname}{{{textversion}}}"
            )

newmacros = '\n'.join(newmacros[1:])

template_sty = text_start + f"""
{newmacros}
""" + text_end


# ---------------------- #
# -- UPDATING THE DOC -- #
# ---------------------- #

text_start, _, text_end = between(
    text = template_tex,
    seps = [
        "% == All texts - START == %\n",
        "\n% == All texts - END == %"
    ],
    keepseps = True
)

alldecos = [
    d
    for d in INFOS["decorations"]
]
alldecos.sort()

textversions = ["", "\\begin{multicols}{2}"]

for onedeco in alldecos:
    textversions += [
f"    \\verb+\\textop{onedeco}+ donne \\emph{{\\og \\textop{onedeco} \\fg}}",
""
    ]

textversions = textversions[:-1] + [
    "\\vfill\\null"
    "\\end{multicols}",
    ""
]

textversions = "\n".join(textversions)

template_tex = text_start + textversions + text_end


text_start, _, text_end = between(
    text = template_tex,
    seps = [
        "% == Technical infos - Texts - START == %\n",
        "\n% == Technical infos - Texts - END == %"
    ],
    keepseps = True
)

alldecos = [
    f"textop{d}"
    for d in alldecos
]

alldecos = ", ".join(alldecos)

template_tex = text_start + f"""
\\foreach \\k in {{{alldecos}}}{{

	\\IDmacro*{{\k}}{{0}}

}}
""" + text_end


text_start, _, text_end = between(
    text = template_tex,
    seps = [
        "% == Technical infos - Operators - START == %\n",
        "\n% == Technical infos - Operators - END == %"
    ],
    keepseps = True
)

ALL_OPES_DECO = ", ".join(ALL_OPES_DECO)

template_tex = text_start + f"""
\\foreach \\k in {{{ALL_OPES_DECO}}}{{

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
