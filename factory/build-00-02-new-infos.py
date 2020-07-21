#! /usr/bin/env python3

from collections import defaultdict
from csv import reader
import json

from mistool.os_use import PPath


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = PPath(__file__).parent

PROJECT_NAME = "tnsmath"

CSV_PARTS_INFOS_PATH = THIS_DIR / "x-change-log-parts-x.csv"
JSON_MAIN_INFOS_PATH = THIS_DIR / f"x-change-log-{PROJECT_NAME}-x.json"

SOMETHING_NEW = False
NEW_THING_TAG = ':newthings:'

DECO = " "*4


# ----------- #
# -- TOOLS -- #
# ----------- #

def updateinfos(maininfos, partsinfos):
    return sorted(
        list(
            set(tuple(x) for x in partsinfos)
            -
            set(tuple(x) for x in maininfos)
        )
    )


# --------------------- #
# -- TNS(MAIN) INFOS -- #
# --------------------- #

if JSON_MAIN_INFOS_PATH.is_file():
    with JSON_MAIN_INFOS_PATH.open(
        mode     = "r",
        encoding = "utf-8"
    ) as jsonfile:
        MAIN_INFOS = json.load(jsonfile)

else:
    JSON_MAIN_INFOS_PATH.create('file')
    MAIN_INFOS = {}

    print(f"{DECO}* Missing JSON file added.")

MAIN_INFOS[NEW_THING_TAG] = {}


# ------------------ #
# -- NEW THINGS ? -- #
# ------------------ #

allinfos = defaultdict(list)

with CSV_PARTS_INFOS_PATH.open(
    mode     = "r",
    encoding = "utf-8"
) as csvfile:
    csvreader = reader(
        csvfile,
        skipinitialspace = True
    )

# Ignore the first internal info.
    next(csvreader)

# For the whole project we just want the older version.
    maindate    = "0-0-0"
    maniversion = ""

    for partname, verdate, version in csvreader:
        if partname == PROJECT_NAME:
            version = version.strip()

            if version:
                verdate = verdate.replace("_", "")

                if verdate > maindate:
                    maindate    = verdate
                    mainversion = version

        else:
            allinfos[partname].append([verdate, version])


for partname in sorted(allinfos.keys()):
    infos = allinfos[partname]
    infos.sort()

# New part ?
    if partname not in MAIN_INFOS\
    or not MAIN_INFOS[partname]:
        SOMETHING_NEW = True

        MAIN_INFOS[partname]                = infos
        MAIN_INFOS[NEW_THING_TAG][partname] = infos

# Known part - New versions ?
# ["2020-07-15", "0.2.0-beta"], ["2020-07-17", "0.3.0-beta"]
    else:
        newinfos = updateinfos(
            maininfos  = MAIN_INFOS[partname],
            partsinfos = infos
        )

        if newinfos:
            SOMETHING_NEW = True

            MAIN_INFOS[NEW_THING_TAG][partname] = newinfos
            MAIN_INFOS[partname]                = infos


MAIN_INFOS[PROJECT_NAME] = [maindate, mainversion]


# ------------------ #
# -- NEW THINGS ? -- #
# ------------------ #

if SOMETHING_NEW:
    with JSON_MAIN_INFOS_PATH.open(
        mode     = "w",
        encoding = "utf-8"
    ) as jsonfile:
        jsonfile.write(
            json.dumps(MAIN_INFOS)
        )

    print(f"{DECO}* New things added to the JSON file.")


else:
    print(f"{DECO}* Nothing new found.")
