# Reward imagery

**Nothing here is an image.** This folder holds a *manifest* — filenames and wiki
page URLs — plus a script you run yourself to fetch them. No artwork has been
downloaded or redistributed by building this.

## Before you download anything

These are Paradox Interactive's game assets, hosted on the community wiki to
document the game. The wiki's **text** is openly licensed; the extracted **art is
not**. On your own machine for a prototype, this is ordinary fan-tool practice.
Behind a public URL, or shipped in something other people install, it is a
decision worth making on purpose. Paradox is famously relaxed about fan tools,
but that is forbearance, not a licence.

That is the whole caveat. It is your call, and it is a reasonable one for a PoC.

## Running it

```
cd resources
python3 fetch_images.py            # dry run, shows the plan
python3 fetch_images.py --confirm  # downloads into resources/images/
```

It resolves every name through the MediaWiki API rather than guessing URLs, so
redirects and capitalisation are handled. It is rate-limited to one request a
second with a real User-Agent, skips files already present, and reports names
that do not exist rather than failing silently. **Don't raise the rate** — a
community wiki runs on donated hosting.

## What the manifest actually covers

| | |
|---|---|
| rows | 138 |
| resolved, ready to fetch | 133 (89 unique files — many sites share event art) |
| needs verification | 3 |
| unresolved | 2 |
| entity art coverage | 111 of 142 entities |

`image_manifest.json` rows carry `category`, `subject`, `wiki_file`, `file_page`,
`local_name`, `entity_uids` (joins to the v2.1 datasets) and `status`.

### Three real gaps, stated rather than papered over

1. **The 24 general astral rifts have no event art mapped.** The wiki's
   `Astral_rift` page only exposes File: references for the 8 unique and
   precursor rifts. The rest need a per-rift pass.
2. **All 63 specimen icons are unresolved.** The rift and site pages link
   specimens as *anchors on the Collection page*, not as File: references, so
   there is nothing to extract without a separate pass over `Collection`.
3. **Advisor Core has no icon.** It is a rift relic in the dataset but does not
   appear in the wiki's Relics table under that name. Worth checking whether it
   is listed differently before assuming an icon exists.

The 3 "needs verification" rows are shared resource icons (astral threads,
minor artifacts, Grand Archive) whose filenames are inferred from usage rather
than read from a File: link. The fetch script will tell you if they 404.

## A design note, since this is for a helper UI

Event splash art is 400×200-ish key art — it reads as *illustration*, not as
*information*. At the sizes a reward table actually uses, 89 near-identical
sci-fi vistas will make rows harder to scan, not easier: eleven different sites
share `Evt_frozen.png` and `Evt_ship_in_orbit.png` alone, so the picture stops
being a distinguishing signal.

What carries meaning at UI scale is **reward type** — is this a relic, a specimen,
a tech, a modifier, a risk? That is a dozen glyphs you control, they stay legible
at 16px, they theme with the rest of your system, and they sidestep the licensing
question entirely. Your v2.1 `reward_finder[].category` field is already exactly
that taxonomy.

Suggested split: your own category glyphs in the dense views (tables, finder,
chips), game art only on entity detail pages where a single large image is the
point and there is room for it to be illustration. That way the download is
~35 hero images rather than 89 thumbnails, and the IP surface shrinks to the
one place it actually buys something.

Worth pressure-testing: I have not seen your PoC, so I am guessing at how dense
your reward views are. If the UI is already card-based with one entity per
screen, game art earns its place much earlier than I am implying here.
