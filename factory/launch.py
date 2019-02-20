# gestion de [en] et [fr]

#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from mistool.os_use import PPath, runthis


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_FILE = PPath(__file__)
THIS_DIR  = THIS_FILE.parent


# -------------------------------------- #
# -- LAUNCHING ALL THE BUILDING TOOLS -- #
# -------------------------------------- #

for pattern in [
    "file::**build_*.py",
    "file::build_*.py"
]:
    allpaths = [onepath for onepath in THIS_DIR.walk(pattern)]
    allpaths.sort()

    for onepath in allpaths:
        print('+ Launching "{0}"'.format(onepath - THIS_DIR))

        runthis(
            cmd        = 'python "{0}"'.format(onepath),
            showoutput = True
        )
