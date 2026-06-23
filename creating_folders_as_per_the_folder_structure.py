#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
from pathlib import Path
from typing import List

# ------------------------------------------------------------------
# CONFIG – change only these two lines
# ------------------------------------------------------------------
MP3_LIST_FILE   = r"D:\python\Vara Prasad\mp3_paths.txt"   # Your .mp3 paths
JSON_SOURCE_DIR = r"D:\python\Vara Prasad\Python Script For Audio Output CSV To JSON File Conversion & Word Count Summary\output_jsons"  # Where JSONs are
# ------------------------------------------------------------------


def win_long_path(p: Path) -> Path:
    """Add \\?\ prefix on Windows for long paths."""
    if os.name == "nt" and not str(p).startswith("\\\\?\\"):
        return Path("\\\\?\\" + str(p))
    return p


def load_mp3_paths(file_path: str) -> List[Path]:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip().lower().endswith(".mp3")]
    return [Path(p) for p in lines]


def main():
    mp3_paths = load_mp3_paths(MP3_LIST_FILE)
    json_root = Path(JSON_SOURCE_DIR)

    if not json_root.exists():
        print(f"[ERROR] JSON source folder not found: {json_root}")
        return

    # Index all .json files (flat or nested)
    print(f"Scanning JSONs in: {json_root}")
    json_map = {f.name: f for f in json_root.rglob("*.json")}
    print(f"Found {len(json_map)} JSON file(s)\n")

    copied = 0
    missing = 0
    skipped = 0

    for mp3_path in mp3_paths:
        folder = win_long_path(mp3_path.parent)
        json_name = mp3_path.stem + ".json"
        target_json = folder / json_name

        if json_name in json_map:
            src_json = json_map[json_name]
            if target_json.exists():
                print(f"[ ] SKIP   → {target_json} (already exists)")
                skipped += 1
            else:
                try:
                    shutil.copy2(src_json, target_json)
                    print(f"[->] COPIED → {json_name} → {folder}")
                    copied += 1
                except Exception as e:
                    print(f"[!] ERROR  → {json_name} | {e}")
        else:
            print(f"[X] MISSING → {json_name}")
            missing += 1

    # Summary
    print("\n" + "="*50)
    print("JSON COPY SUMMARY")
    print("="*50)
    print(f"Copied    : {copied}")
    print(f"Missing   : {missing}")
    print(f"Skipped   : {skipped}")
    print("="*50)


if __name__ == "__main__":
    main()


!/usr/bin/env python3
-*- coding: utf-8 -*-