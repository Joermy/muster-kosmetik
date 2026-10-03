#!/usr/bin/env python3
import pathlib
import subprocess

WURZEL = pathlib.Path(__file__).resolve().parent.parent
ZIEL = WURZEL / "assets" / "fonts"

SCHRIFTEN = {
    "Syne-Variabel.woff2":
        "https://fonts.gstatic.com/s/syne/v24/8vIH7w4qzmVxm2BL9A.woff2",
    "Outfit-Variabel.woff2":
        "https://fonts.gstatic.com/s/outfit/v15/QGYvz_MVcBeNP4NJtEtq.woff2",
}

LIZENZEN = {
    "OFL-Syne.txt":
        "https://raw.githubusercontent.com/google/fonts/main/ofl/"
        "syne/OFL.txt",
    "OFL-Outfit.txt":
        "https://raw.githubusercontent.com/google/fonts/main/ofl/"
        "outfit/OFL.txt",
}

def laden(url, ziel, mindestens):
    erg = subprocess.run(
        ["curl", "-sL", "--max-time", "60", "--retry", "2", url],
        capture_output=True)
    if erg.returncode != 0 or len(erg.stdout) < mindestens:
        raise RuntimeError(f"{url}: nur {len(erg.stdout)} Bytes")
    ziel.write_bytes(erg.stdout)
    return len(erg.stdout)

def main():
    ZIEL.mkdir(parents=True, exist_ok=True)
    gesamt = 0
    for name, url in SCHRIFTEN.items():
        groesse = laden(url, ZIEL / name, 4000)
        gesamt += groesse
        print(f"  {name:34s} {groesse / 1024:6.1f} KB")
    for name, url in LIZENZEN.items():
        laden(url, ZIEL / name, 1000)
        print(f"  {name:34s} Lizenztext")
    print(f"\n{gesamt / 1024:.1f} KB Schriften unter assets/fonts/")

if __name__ == "__main__":
    main()
