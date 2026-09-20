#!/usr/bin/env python3
"""
Download the wiki images listed in image_manifest.json.

    python3 fetch_images.py            # dry run — shows what it would do
    python3 fetch_images.py --confirm  # actually downloads

READ THIS FIRST
---------------
These files are Paradox Interactive's game assets. They are hosted on the
community wiki to document the game. The wiki's *text* is openly licensed;
the extracted art is not. Using them in a prototype on your own machine is
ordinary fan-tool practice. Putting them behind a public URL, or shipping them
in something other people install, is a decision to make deliberately — not a
default. Paradox is relaxed about fan tools in practice, but that is
forbearance, not a licence.

This script is deliberately polite: one request at a time, a real User-Agent,
a 1-second gap between calls, and it skips anything already downloaded. Do not
raise the rate. A community wiki runs on donated hosting.

It resolves each filename through the MediaWiki API rather than guessing a URL,
so redirects and name normalisation are handled for you. Files that do not
exist are reported, not silently skipped.
"""
import json, os, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
API = "https://stellaris.paradoxwikis.com/api.php"
OUT = os.path.join(HERE, "images")
UA = "StellarisHelperPoC/0.1 (personal prototype; contact: nightowlstudiosus@gmail.com)"
DELAY = 1.0

def api_imageinfo(titles):
    q = urllib.parse.urlencode({"action": "query", "format": "json",
                                "prop": "imageinfo", "iiprop": "url|size|mime",
                                "titles": "|".join(titles)})
    req = urllib.request.Request(f"{API}?{q}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def main():
    confirm = "--confirm" in sys.argv
    man = json.load(open(os.path.join(HERE, "image_manifest.json")))
    wanted, skipped = {}, []
    for it in man["items"]:
        if it["status"] == "unresolved" or not it["wiki_file"]:
            skipped.append(it["subject"]); continue
        wanted.setdefault(it["wiki_file"], it["local_name"])

    print(f"manifest: {len(man['items'])} rows")
    print(f"to download: {len(wanted)} unique files -> {OUT}")
    print(f"skipped (unresolved): {len(skipped)}")
    if not confirm:
        print("\nDRY RUN. Re-run with --confirm to download.")
        print("First 10 targets:")
        for f in list(wanted)[:10]:
            print(f"   File:{f}  ->  images/{wanted[f]}")
        return

    print("\n" + man["licensing"] + "\n")
    os.makedirs(OUT, exist_ok=True)
    titles = [f"File:{f}" for f in wanted]
    urls, missing = {}, []
    for i in range(0, len(titles), 20):                 # API takes 50; 20 is gentler
        data = api_imageinfo(titles[i:i + 20])
        for page in data.get("query", {}).get("pages", {}).values():
            name = page["title"].split("File:", 1)[-1].replace(" ", "_")
            if "imageinfo" in page:
                urls[name] = page["imageinfo"][0]["url"]
            else:
                missing.append(page["title"])
        time.sleep(DELAY)

    ok = fail = 0
    for wf, local in wanted.items():
        url = urls.get(wf)
        if not url:
            continue
        dest = os.path.join(OUT, local)
        if os.path.exists(dest):
            continue
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as fh:
                fh.write(r.read())
            ok += 1
            print(f"  ok   {local}")
        except Exception as exc:
            fail += 1
            print(f"  FAIL {local}: {exc}")
        time.sleep(DELAY)

    print(f"\ndownloaded {ok}, failed {fail}, already present "
          f"{len(wanted) - ok - fail - len(missing)}")
    if missing:
        print(f"\nno such file on the wiki ({len(missing)}) — fix these in the manifest:")
        for m in missing: print("   " + m)

if __name__ == "__main__":
    main()
