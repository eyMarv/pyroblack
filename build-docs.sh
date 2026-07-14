#!/bin/bash
# Build Sphinx docs from this repo and publish into eyMarv/pyroblack-docs.
# Hardened so a failed/empty build can never wipe the live main/ tree again.
set -euo pipefail

export DOCS_KEY
VENV="$(pwd)"/venv
export VENV

branch="main"
HTML_DIR="docs/build/html"
DOCS_REPO_DIR="pyroblack-docs"

cleanup() {
    # Avoid leaving a partial clone in the workspace if the job fails mid-way.
    if [ -d "$DOCS_REPO_DIR" ]; then
        rm -rf "$DOCS_REPO_DIR"
    fi
}
trap cleanup EXIT

make clean
make clean-docs
make venv
make api
"$VENV"/bin/pip install -e '.[docs]'
cd compiler/docs || exit 1
"$VENV"/bin/python compiler.py
cd ../.. || exit 1

"$VENV"/bin/sphinx-build -b html "docs/source" "$HTML_DIR" -j auto

# --- Safety gates: never wipe the published branch without a good build ---
if [ ! -d "$HTML_DIR" ]; then
    echo "ERROR: Sphinx output directory missing: $HTML_DIR" >&2
    exit 1
fi
if [ ! -f "$HTML_DIR/index.html" ]; then
    echo "ERROR: Sphinx did not produce $HTML_DIR/index.html — aborting publish" >&2
    exit 1
fi
# Require a non-trivial build (avoid publishing an empty/partial tree).
html_count="$(find "$HTML_DIR" -type f | wc -l | tr -d ' ')"
if [ "${html_count:-0}" -lt 20 ]; then
    echo "ERROR: Sphinx output looks empty ($html_count files) — aborting publish" >&2
    exit 1
fi

if [ -z "${DOCS_KEY:-}" ]; then
    echo "ERROR: DOCS_KEY is not set; cannot push to pyroblack-docs" >&2
    exit 1
fi

rm -rf "$DOCS_REPO_DIR"
git clone "https://eyMarv:${DOCS_KEY}@github.com/eyMarv/pyroblack-docs.git" "$DOCS_REPO_DIR"
cd "$DOCS_REPO_DIR" || exit 1

mkdir -p "$branch"

# Stage new HTML in a temporary directory, then swap into place.
# This way a failed cp never leaves main/ half-deleted.
stage_dir="$(mktemp -d "${branch}.XXXXXX")"
# shellcheck disable=SC2064
trap 'rm -rf "$stage_dir"; cleanup' EXIT

cp -a "../${HTML_DIR}/." "$stage_dir/"
if [ ! -f "$stage_dir/index.html" ]; then
    echo "ERROR: copy into staging dir failed (no index.html)" >&2
    exit 1
fi

# Replace branch content atomically from the caller's perspective:
# remove old tracked files under $branch, then move staged tree in.
rm -rf "$branch"
mkdir -p "$branch"
# Move contents (including hidden files) into branch/
cp -a "$stage_dir/." "$branch/"
rm -rf "$stage_dir"

# Ensure project Pages keep working without a wrong custom domain.
# (eyMarv.github.io/pyroblack-docs does not need CNAME; a bad CNAME breaks routing.)
rm -f CNAME
# Root redirect to the branch folder (preserve existing convention).
if [ ! -f index.html ]; then
    cat > index.html <<EOF
<!doctype html>
<html lang="en" class="no-js">
    <body>
        <meta http-equiv="Refresh" content="0; url='/pyroblack-docs/${branch}'" />
    </body>
</html>
EOF
fi
touch .nojekyll

git config --local user.name "eyMarv"
git config --local user.email "eyMarv07@gmail.com"
git add --all

if git diff --cached --quiet; then
    echo "No docs changes to publish."
    exit 0
fi

# Final guard: refuse to commit a branch tree that lost its index.
if [ ! -f "$branch/index.html" ]; then
    echo "ERROR: refusing to publish — $branch/index.html missing after staging" >&2
    exit 1
fi

git commit -a -m "docs: $branch: Update docs $(date '+%Y-%m-%d | %H:%M:%S %p %Z')" --signoff

# Pull with rebase before pushing to handle concurrent docs runs (e.g. tag + main).
# If the remote has moved ahead, replay our commit on top instead of failing.
git pull --rebase origin main || true
git push -u origin HEAD:main
