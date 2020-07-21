# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR=$(dirname "$0")

PROJECT_DIR="$THIS_DIR/../"
cd "$PROJECT_DIR"
# The trick `...` was found (again ?) in
# https://stackoverflow.com/a/1744613/4589608
PROJECT_NAME=$(basename "`pwd`")
TYPENSEE_DIR=$(dirname "`pwd`")

PARTS_DIR="$TYPENSEE_DIR/$PROJECT_NAME-parts"

TNS_PREFIX="tns"

FACTORY_CHANGE_LOG="99-major-change-log"
TEX_CHANGE_LOG="factory/$FACTORY_CHANGE_LOG/changes"

CSV_FILE="$PROJECT_DIR""factory/x-change-log-parts-x.csv"


# ----------- #
# -- TOOLS -- #
# ----------- #

function analyze {
    for chgelog in $(find $1/$TEX_CHANGE_LOG -name '*.tex')
    do
        year=$(basename "`dirname $chgelog`")

# Source: https://stackoverflow.com/a/965072/4589608
        monthday=$(basename $chgelog)
        monthday="${monthday%.*}"

        version=$(cat $chgelog | grep version.*verb)
# Source: https://linuxhint.com/trim_string_bash/
        version="${version%*+*}"
        version="${version#*+*}"

        echo "$1, $year-$monthday, $version" >> "$CSV_FILE"
    done
}


# -------------------- #
# -- RESET CSV FILE -- #
# -------------------- #

thisyear=$(date +'%Y')
thismonthday=$(date +'%m-%d')
hournco=$(date +'%kh%Mm%S')

echo "Last update, $thisyear-$thismonthday, $hournco" > "$CSV_FILE"


# ------------------- #
# -- ANALYZE PARTS -- #
# ------------------- #

cd "$PARTS_DIR"

for onepart in $(ls -d tns*)
do
    echo "    * Searching inside << $onepart >>."
    analyze $onepart
done


# --------------------- #
# -- ANALYZE tnsmath -- #
# --------------------- #

cd "$TYPENSEE_DIR"

echo "    * Searching inside << tnsmath >>."
analyze tnsmath
