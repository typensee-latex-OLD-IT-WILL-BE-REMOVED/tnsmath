#! /usr/bin/env python3

from collections import defaultdict

from mistool.os_use import PPath
from mistool.string_use import between, joinand
from mistool.term_use import ALL_FRAMES, withframe
from orpyste.data import ReadBlock

THIS_DIR = PPath( __file__ ).parent

STY_PATH = THIS_DIR.parent / "lymath" / "lymath.sty"


# ----------------------- #
# -- TOOLS & CONSTANTS -- #
# ----------------------- #

DECO = " "*4

MYFRAME = lambda x: withframe(
    text  = x,
    frame = ALL_FRAMES['latex_pretty']
)

def organize_packages(packages):
    global DECO

    packages_found = defaultdict(list)

    for texpackdef in packages:
        if texpackdef:
            options = between(
                text = texpackdef,
                seps = ["[", "]"]
            )

            if options:
                _, options, texpackdef = options

                options = [x.strip() for x in options.split(",")]

            else:
                options = []

            _, names, _ = between(
                text = texpackdef,
                seps = ["{", "}"]
            )

            for onename in names.split(","):
                packages_found[onename.strip()] += options

    allnames = sorted(packages_found.keys())

    packages_ok = []

    for onename in allnames:
        options = packages_found[onename]

        if options:
            options = f'[{", ".join(options)}]'

        else:
            options = ""

        packages_ok.append(f"\\usepackage{options}{{{onename}}}")


    print(f"{DECO}* Declaration of packages organized.")

    return packages_ok


# ---------------- #
# -- NEW THINGS -- #
# ---------------- #

ALL_PACKAGES = []
ALL_MACROS   = []

for subdir in THIS_DIR.walk("dir::"):
    subdir_name = str(subdir.name)

    if subdir_name in [
        "config",
    ] or subdir_name[:2] == "x-":
        continue

    for latexfile in subdir.walk("file::**.tex"):
        relative_path = latexfile - THIS_DIR

        print(f"{DECO}* Analyzing << {relative_path} >>")

        with open(
            file     = latexfile,
            encoding = "utf-8"
        ) as filetoupdate:
            search = between(
                text = filetoupdate.read(),
                seps = [
                    "% == PACKAGES USED == %",
                    "% == DEFINITIONS == %"
                ],
                keepseps = True
            )

            if search is not None:
                _, packages, after = search

                ALL_PACKAGES += [
                    x.strip()
                    for x in packages.strip().split("\n")
                ]

            _, definitions, _ = between(
                text = after,
                seps = [
                    "% == DEFINITIONS == %",
                    r"\begin{document}"
                ]
            )

            definitions = definitions.split("\n")

            for i in [0, -1]:
                while not definitions[i].strip():
                    definitions.pop(i)

            section = relative_path.stem
            section = section.split("-", 1)
            section = section[1]
            section = section.replace("-", " ")
            section = latexfile.parent.name.split("-", 1)[1] + " - " + section

            definitions = """
{0}

{1}
            """.format(
                MYFRAME(section.upper()),
                "\n".join(definitions)
            ).strip()

            ALL_MACROS.append(definitions)


# --------------------------------- #
# -- ORGANIZING LIST OF PACKAGES -- #
# --------------------------------- #

ALL_PACKAGES = organize_packages(ALL_PACKAGES)


# ------------------------- #
# -- UPDATE THE STY FILE -- #
# ------------------------- #

ALL_PACKAGES = [MYFRAME("PACKAGES REQUIRED"), ""] + ALL_PACKAGES
ALL_PACKAGES = "\n".join(ALL_PACKAGES)

ALL_MACROS = "\n\n\n".join(ALL_MACROS)

STY_PATH.create("file")

with STY_PATH.open(
    mode     = "w",
    encoding = "utf-8"
) as source:
    source.write(f"{ALL_PACKAGES}\n\n\n{ALL_MACROS}")

print(f"{DECO}* Update of << {STY_PATH.name} >> done.")
