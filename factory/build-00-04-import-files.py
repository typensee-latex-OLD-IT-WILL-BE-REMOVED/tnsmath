#! /usr/bin/env python3

from csv import reader
from collections import defaultdict
import json

from mistool.os_use import PPath, cd , runthis


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = PPath(__file__).parent

PROJECT_NAME = "tnsmath"


PARTS_DIR = THIS_DIR.parent.parent / "tnsmath-parts"


TOCDOC_FILE = THIS_DIR / f"tocdoc[fr].txt"


CHANGE_LOGTXT_DIR = THIS_DIR.parent / "change-log"
CHANGE_LATEX_DIR  = THIS_DIR / "99-major-change-log" / "changes"

JSON_MAIN_INFOS_PATH = (THIS_DIR / f"x-change-log-{PROJECT_NAME}-x.json")

with JSON_MAIN_INFOS_PATH.open(
    mode     = "r",
    encoding = "utf-8"
) as jsonfile:
    MAIN_INFOS = json.load(jsonfile)

NEW_THING_TAG = ':newthings:'
NEWTHINGS     = MAIN_INFOS[NEW_THING_TAG]


EXT_FOR_EXTRA = {
    'png': "PNG images",
    'tkz': "TikZ files",
}


DECO = " "*4


def extractcontent(ppath):
    with ppath.open(
        mode     = "r",
        encoding = "utf-8"
    ) as file:
        content = file.read()

    return content


def updatecontent(ppath, content):
    with ppath.open(
        mode     = "w",
        encoding = "utf-8"
    ) as file:
        file.write(content)


# ------------------- #
# -- NO NEW THINGS -- #
# ------------------- #

if not NEWTHINGS:
    print(f"{DECO}* Nothing new to do.")
    exit()

print(f"{DECO}* Copying files in << tnsmath >> folder.")


# ----------------------------- #
# -- META INFOS OF THE PARTS -- #
# ----------------------------- #

META_PARTS = {}

with TOCDOC_FILE.open(
    mode     = "r",
    encoding = "utf-8"
) as csvfile:
    csvreader = reader(
        csvfile,
        delimiter = '='
    )

    position = 0

    for partname, title in csvreader:
        position += 1

        partname = partname.strip()
        title    = title.strip()

        META_PARTS[partname] = {
            'dirname': f"{position:02}-{partname}",
            'title'  : title
        }


# ----------------------------- #
# -- META INFOS OF THE PARTS -- #
# ----------------------------- #

for partname, versions in MAIN_INFOS.items():
    if partname in [':newthings:', PROJECT_NAME]:
        continue

# To be ignored.
    if not partname in (NEWTHINGS):
        print(f"{DECO*2}- << {partname} >> ignored : no new things.")
        continue

# Copy only the sty, png and tkz files.
    print(f"{DECO*2}- << {partname} >> : copying files.")

    destdir = THIS_DIR / META_PARTS[partname]['dirname']
    title   = META_PARTS[partname]['title']

# Destination dir. musts not exist.
    if destdir.is_dir():
        print(f"{DECO*3}--> Deletion of << {destdir.stem} >>.")
        # TODO
        continue

# Let's copy all the usefull dir. No builder here !
    partdirfactory = PARTS_DIR / partname / 'factory'

    texpaths = []

    for ext in ['tex', 'sty'] + list(EXT_FOR_EXTRA):
        for srcpath in partdirfactory.walk(f"file::**.{ext}"):
            if "nodoc" in srcpath.stem \
            or srcpath.parent.stem in ["00-intro", "99-major-change-log", "config"] \
            or srcpath.parent.parent.parent.stem == "99-major-change-log":
                continue

            destpath = destdir / (srcpath - partdirfactory)

            srcpath.copy_to(destpath)

# \input{../config/header ---> \input{../../config/header
            if ext == "tex":
                texpaths.append(destpath)

                content = extractcontent(destpath)
                content = content.replace(
                    "\\input{../config/header",
                    "\\input{../../config/header"
                )

                updatecontent(destpath, content)

# Add the chapter.
        if ext == "tex":
            texpaths.sort()
            firstpath = texpaths[0]

            content = extractcontent(firstpath)
            content = content.replace(
                "\\begin{document}",
                f"""
\\begin{{document}}

\\chapter{{{title}}}
                """.strip()
            )

            updatecontent(firstpath, content)
