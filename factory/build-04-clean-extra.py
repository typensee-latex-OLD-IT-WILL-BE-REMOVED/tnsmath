#! /usr/bin/env python3

from mistool.latex_use import clean as latexclean
from mistool.os_use import PPath


# ----------------------- #
# -- TOOLS & CONSTANTS -- #
# ----------------------- #

THIS_DIR  = PPath( __file__ ).parent
LYXAM_DIR = THIS_DIR.parent / "lymath"


# ----------------------- #
# -- CLEAN BEFORE PUSH -- #
# ----------------------- #

JSON_DEP_PATH = THIS_DIR / "dep.json"
JSON_DEP_PATH.remove()

for toremove in THIS_DIR.walk("file::**.macros-x.txt"):
    toremove.remove()

for toremove in LYXAM_DIR.walk("file::*.macros-x.txt"):
    toremove.remove()

for toremove in THIS_DIR.walk("file::**.pdf"):
    toremove.remove()

for toremove in THIS_DIR.walk("dir::*"):
    latexclean(toremove)
