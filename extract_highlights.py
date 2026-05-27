#!/usr/bin/env python3
"""Convert a YJR annotations file and extract highlights from a KFX book."""

import argparse
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Extract Kindle highlights from a KFX book using its .yjr sidecar.",
    )
    parser.add_argument("book_kfx", help="Path to the .kfx book file")
    parser.add_argument("annotations_yjr", help="Path to the .yjr annotations file (inside the book's .sdr/ folder)")
    parser.add_argument(
        "--markdown", "-m",
        action="store_true",
        help="Emit a .highlights.md file (Markdown grouped by chapter) instead of .highlights.html",
    )
    args = parser.parse_args()

    kfx_file = Path(args.book_kfx)
    yjr_file = Path(args.annotations_yjr)

    if not kfx_file.is_file():
        print(f"KFX file not found: {kfx_file}")
        sys.exit(1)
    if not yjr_file.is_file():
        print(f"YJR file not found: {yjr_file}")
        sys.exit(1)

    script_dir = Path(__file__).parent

    # Convert YJR to JSON using krds.py
    krds_script = script_dir / "krds.py"
    subprocess.run([sys.executable, str(krds_script), str(yjr_file)], check=True)

    json_file = yjr_file.with_suffix(yjr_file.suffix + ".json")

    # Extract highlights using the generated JSON and KFX file
    extract_script = script_dir / "extract_highlights_kfxlib.py"
    cmd = [sys.executable, str(extract_script), str(json_file), str(kfx_file)]
    if args.markdown:
        cmd.append("--markdown")
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
