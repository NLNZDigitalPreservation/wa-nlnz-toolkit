#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-.venv/bin/python}"
TWINE_BIN="${TWINE_BIN:-.venv/bin/twine}"
PACKAGE_DIR="wa_nlnz_toolkit"
SOURCELESS="${SOURCELESS:-0}"

if [[ ! -x "$PYTHON_BIN" ]]; then
	PYTHON_BIN="python"
fi

if [[ ! -x "$TWINE_BIN" ]]; then
	TWINE_BIN="twine"
fi

# clean previous builds
rm -rf dist/

# build wheel only (no source distribution)
"$PYTHON_BIN" -m build --wheel

if [[ "$SOURCELESS" == "1" ]]; then
	ORIG_WHEEL="$(ls dist/*.whl | head -n 1)"
	TMP_DIR="$(mktemp -d)"

	# Sourceless wheels are tied to the Python bytecode version that built them.
	"$PYTHON_BIN" -m wheel unpack "$ORIG_WHEEL" --dest "$TMP_DIR"
	UNPACKED_DIR="$(find "$TMP_DIR" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
	PKG_PATH="$UNPACKED_DIR/$PACKAGE_DIR"

	"$PYTHON_BIN" -m compileall -b "$PKG_PATH"
	find "$PKG_PATH" -name "*.py" -delete

	WHEEL_META="$(find "$UNPACKED_DIR" -path "*/WHEEL" | head -n 1)"
	WHEEL_TAG="$($PYTHON_BIN - <<'PY'
import sys
print(f"cp{sys.version_info.major}{sys.version_info.minor}-none-any")
PY
)"
	sed -i "s/^Tag: .*/Tag: ${WHEEL_TAG}/" "$WHEEL_META"

	rm -f "$ORIG_WHEEL"
	"$PYTHON_BIN" -m wheel pack "$UNPACKED_DIR" --dest-dir dist
	rm -rf "$TMP_DIR"
fi

# upload the wheel to testpypi
"$TWINE_BIN" upload --repository testpypi dist/*.whl

