#! /usr/bin/env python3

from csv import reader
from datetime import datetime

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


NOW = datetime.now()

THIS_TIME  = NOW.strftime("%H:%M:%S")
THIS_DATE  = NOW.strftime("%Y-%m-%d")
THIS_YEAR  = NOW.strftime("%Y")
THIS_MONTH = NOW.strftime("%m")
THIS_DAY   = NOW.strftime("%d")


DECO = " "*4


# ------------------- #
# -- NO NEW THINGS -- #
# ------------------- #

if not NEWTHINGS:
    print(f"{DECO}* Nothing new to do.")
    exit()


# ----------- #
# -- TOOLS -- #
# ----------- #

def extractchanges(partname, versions):
    global TOC

    content = [
         "",
         "% -------------- %",
        f"% -- {partname} -- %",
         "% -------------- %",
    ]

    notfirstinfo = False

    with cd(PARTS_DIR / partname):
        print(f"{DECO*2}- Working on << {partname} >>.")

        try:
            runthis("git checkout master")

        except Exception as e:
            print(e)
            exit(1)


        for chgedate, versnb in versions:
            texpath = chgedate.replace("-", "/", 1)
            texpath = PARTS_DIR / f"{partname}/factory/99-major-change-log/changes/{texpath}.tex"

            if not texpath.is_file():
                print(
                    f"{DECO*2}- [{partname}] Following LaTeX file is missing."
                )
                print(
                    f"{DECO*2}  << {texpath} >>."
                )
                exit(1)

            with texpath.open(
                mode = "r",
                encoding = "utf-8"
            ) as file:
                chgecontent = file.read().strip()
                chgecontent = chgecontent.split("\n")
                chgecontent = chgecontent[1:]

                chgecontent = "\n".join(chgecontent)

                if not chgecontent:
                    chgecontent += """
\\begin{itemize}[itemsep=.5em]
    \\item Simple migration depuis l'ancien code de \\verb+lymath+.
\\end{itemize}
                    """.strip()


                chgecontent = chgecontent.strip()
                chgecontent = chgecontent.replace('\\separation', '')


                if notfirstinfo:
                    extraline    = ""
                    notfirstinfo = False

                else:
                    extraline ="\n"

                chgecontent = f"""{extraline}
\\begin{{center}}
    \\textbf{{\\textsc{{{TOC[partname]} [{versnb}]}}}}
\\end{{center}}

{chgecontent}
                """.rstrip()

                content.append(chgecontent)

        try:
            runthis("git checkout dev")

        except Exception as e:
            print(e)
            exit(1)


    content = "\n".join(content)

    return content


def resetbugnb(nbver):
    if '-' in nbver:
        _, extra = nbver.split('-')

        nbver = f'0-{extra}'

    else:
        nbver = '0'

    return nbver


# --------------------- #
# -- TOC FOR THE DOC -- #
# --------------------- #

TOC = {}

with TOCDOC_FILE.open(
    mode     = "r",
    encoding = "utf-8"
) as csvfile:
    csvreader = reader(
        csvfile,
        delimiter = '='
    )

    for partname, title in csvreader:
        title    = title.strip()
        partname = partname.strip()

        TOC[partname] = title


# ---------------------- #
# -- MAIN NEW VERSION -- #
# ---------------------- #

print(f"{DECO}* Calculating the new main version number.")

_, mainversion = MAIN_INFOS[PROJECT_NAME]

maj_found = False
min_found = False
bug_found = False

for partname, versions in MAIN_INFOS.items():
    if partname in [':newthings:', PROJECT_NAME]:
        continue

# To be ignored.
    if not partname in (NEWTHINGS):
        print(f"{DECO*2}- << {partname} >> ignored : no new things.")
        continue

    if len(versions) == 1:
        print(f"{DECO*2}- << {partname} >> ignored : only one number version.")
        continue

# Which kind of change have we ?
    (_, newpartnb), (_, prevpartnb) = versions[-2:]
    newpartnb  = newpartnb.split(".")
    prevpartnb = prevpartnb.split(".")

    if prevpartnb[0] != newpartnb[0]:
        maj_found = True

    if prevpartnb[1] != newpartnb[1]:
        min_found = True

    if prevpartnb[2] != newpartnb[2]:
        bug_found = True

    if maj_found:
        continue

# Let's calculate the main version number.
mainversion = mainversion.split(".")

if maj_found:
    newkindmainver    = "major"
    newkindmainver_fr = "majeure"

    mainversion[0] = str(int(mainversion[0]) + 1)
    mainversion[1] = '0'
    mainversion[2] = resetbugnb(mainversion[2])

elif min_found:
    newkindmainver    = "minor"
    newkindmainver_fr = "mineure"

    mainversion[1] = str(int(mainversion[1]) + 1)
    mainversion[2] = resetbugnb(mainversion[2])

elif min_found:
    newkindmainver    = "subminor"
    newkindmainver_fr = "sous mineure"

    mainversion[2] = resetbugnb(mainversion[2])

else:
    mainversion = []

    print(f"{DECO*2}- No new number version.")


mainversion = ".".join(mainversion)


# ------------------- #
# -- TEXT LOG FILE -- #
# ------------------- #

print(f"{DECO}* Managing TXT change log.")

relpath = f"{THIS_YEAR}/{THIS_MONTH}.txt"
logfile = CHANGE_LOGTXT_DIR / relpath

if not logfile.is_file():
    print(f"{DECO*2}- New log file << {relpath} >> added.")
    logfile.create('file')


with logfile.open(
    mode     = "r",
    encoding = "utf-8"
) as txtfile:
    oldcontent = txtfile.read()

titledate = f"""
==========
{THIS_DATE}
==========
""".strip()

if titledate in oldcontent:
    print(
        f"{DECO*2}- No update because {THIS_DATE} has been found "
        f"in << {relpath} >>."
    )
    print(
        f"{DECO*2}  TIP: change this date in << {relpath} >> "
        f"for automatic update."
    )

else:
    newcontent = [
        f"""
// Added : {THIS_DATE} [{THIS_TIME}]
==========
{THIS_DATE}
==========
        """.strip(),
        ""
    ]

    if mainversion:
        newcontent += [
            f"**New {newkindmainver} version version::``{mainversion}``:** "
            "see the changes below.",
            "",
            ""
        ]


    for partname, versions in NEWTHINGS.items():
        aboutversion = []

        if len(versions) == 1:
            aboutversion = (
                f"addition of the version version::``{versions[0][1]}`` "
                f"published at date::``{versions[0][0]}``."
            )

        else:
            aboutversion += [
                "the folowing versions have been added.",
                ""
            ]

            for i, ver in enumerate(versions, 1):
                aboutversion.append(
                    f"{DECO}{i}) Version version::``{ver[1]}`` "
                    f"published at date::``{ver[0]}``."
                )

            aboutversion = "\n".join(aboutversion)


        newcontent += [
            f"**¨{partname}:** {aboutversion}",
            "",
            ""
        ]


    newcontent = "\n".join(newcontent)
    newcontent = f"{newcontent.strip()}\n\n\n{oldcontent.strip()}\n"


    with logfile.open(
    mode     = "w",
    encoding = "utf-8"
    ) as txtfile:
        txtfile.write(newcontent)

    print(f"{DECO*2}- TXT change log file updated.")


# --------------------- #
# -- TEX LOG CHANGES -- #
# --------------------- #

print(f"{DECO}* Managing LaTeX change log.")

relpath = f"{THIS_YEAR}/{THIS_MONTH}-{THIS_DAY}.tex"
logfile = CHANGE_LATEX_DIR / relpath

if logfile.is_file():
    print(
        f"{DECO*2}- No update because << {relpath}.tex << already exists."
    )
    print(
        f"{DECO*2}  TIP: change the name of this file or remove it "
        f"for automatic update."
    )

else:
    print(f"{DECO*2}- New log file << {relpath} >> added.")
    logfile.create('file')

    content = []

    if mainversion:
        content += [
            f"Nouvelle version {newkindmainver_fr} \\verb+{mainversion}+.",
            ""
        ]

    for partname, versions in NEWTHINGS.items():
        content.append(
            extractchanges(
                partname = partname,
                versions = versions
                )
        )

        content.append("\n\n\\separation\n")

    content = "\n".join(content)


    with logfile.open(
        mode     = "w",
        encoding = "utf-8"
    ) as txtfile:
        txtfile.write(content)

    print(f"{DECO*2}- LaTeX change log file updated.")
