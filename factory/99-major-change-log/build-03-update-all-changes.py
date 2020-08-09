
#! /usr/bin/env python3

from mistool.os_use import PPath
from mistool.string_use import between, joinand


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR    = PPath(__file__).parent
CHANGES_DIR = THIS_DIR / 'changes'

CHANGE_LOG_TEX_FILE = THIS_DIR / "02-all-changes-nodoc[fr].tex"

DECO = " "*4


# ----------------------- #
# -- ALL CHANGES SHOWN -- #
# ----------------------- #

with CHANGE_LOG_TEX_FILE.open(
    mode     = "r",
    encoding = "utf-8"
) as f:
    text_start, _, text_end = between(
        text = f.read(),
        seps = [
            "% All changes - START",
            "% All changes - END"
        ],
        keepseps = True
    )


allppaths = [p for p in CHANGES_DIR.walk("file::**.tex")]
allppaths.sort(
    key     = lambda x: str(x).replace("_", ""),
    reverse = True
)


lastyear = "9"*4
content  = []

for ppath in allppaths:
    year = ppath.parent.name.replace("_", "")

    if year < lastyear:
        lastyear = year

        content.append(
        f"""

% ------------------------ %


\\section{{{year}}}

        """
        )


    with ppath.open(
        mode     = "r",
        encoding = "utf-8"
    ) as f:
        firstline = True

        content.append("\\begin{description}\n")

        for line in f.readlines():
            if firstline:
                line = f"\\medskip\n" \
                     + f"\\item[{ppath.parent.stem}-{ppath.stem}] {line}"
                line = line.replace("_", "")

                firstline = False

            content.append(line)

        content.append("\n\\end{description}")



content = "".join(content)

with CHANGE_LOG_TEX_FILE.open(
    mode     = 'w',
    encoding = 'utf-8'
) as f:
    f.write(f"{text_start}{content}\n\n{text_end}")
