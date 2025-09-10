# scripts/make_manifest.py
import os, json, shutil, urllib.parse
from pathlib import Path

SRC_DIR  = Path("images_folder")      # <-- your current folder in the repo
DEST_DIR = Path("docs/images")        # <-- GitHub Pages serves from docs/
MANIFEST = DEST_DIR / "manifest.json"

def main():
    if not SRC_DIR.exists():
        raise SystemExit(f"Source folder not found: {SRC_DIR}")

    # Copy images into docs/images (preserve bank folders)
    if DEST_DIR.exists():
        shutil.rmtree(DEST_DIR)
    shutil.copytree(SRC_DIR, DEST_DIR)

    # Build manifest (URL-encode path segments for safe web URLs)
    by_bank = {}
    for bank_dir in sorted(p for p in DEST_DIR.iterdir() if p.is_dir()):
        bank = bank_dir.name   # e.g., "Boston", "Des Moines"
        rel_urls = []
        for img in sorted(bank_dir.glob("*.png")):
            rel = img.relative_to(DEST_DIR)  # e.g., "Boston/ltv_hist.png"
            # URL-encode each path segment to handle spaces like "Des Moines"
            parts = [urllib.parse.quote(p) for p in rel.parts]
            rel_url = "/".join(parts)        # e.g., "Des%20Moines/ltv_hist.png"
            rel_urls.append(rel_url)
        by_bank[bank] = rel_urls

    data = {
        "banks": sorted(by_bank.keys()),
        "images": by_bank,                   # { "Boston": ["Boston/..png", ...], ...}
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(data, indent=2))
    print(f"Wrote manifest with {sum(len(v) for v in by_bank.values())} images -> {MANIFEST}")

if __name__ == "__main__":
    main()
