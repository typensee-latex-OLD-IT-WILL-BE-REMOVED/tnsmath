#! /usr/bin/env python3

from mistool.os_use import PPath


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = PPath( __file__ ).parent

PROJECT_NAME     = "tnsmath"
PROJECT_PATH     = THIS_DIR.parent.parent / f"{PROJECT_NAME}"
DIR_FACTORY_PATH = PROJECT_PATH / "factory"
DIR_DOC_PATH     = PROJECT_PATH / f"{PROJECT_NAME}"

EXT_FOR_EXTRA = {
    'png'      : ["images"  , "PNG images"],
    'tkz'      : ["tikz"    , "TikZ files"],
    'extra.tex': ["examples", 'TeX "example" files'],
}


DECO = " "*4


# ------------------------- #
# -- COPYING EXTRA FILES -- #
# ------------------------- #

for ext, (reldir, desc) in EXT_FOR_EXTRA.items():
    print(f"{DECO}* Looking for {desc}.")

    for extfile in DIR_FACTORY_PATH.walk(f"file::**.{ext}"):
        if extfile.stem.endswith("-nodoc"):
            continue

        extfile.copy_to(
            dest     = DIR_DOC_PATH / reldir / extfile.name,
            safemode = False
        )

        print(f"{DECO*2}+ Copy of {extfile - DIR_FACTORY_PATH}")
