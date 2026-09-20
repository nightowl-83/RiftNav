# Setting up Google Drive for desktop (one-time, ~10 minutes)

This is the piece that does the actual continuous syncing. The scheduled Claude
task audits parity; it does not replace this.

## Read this constraint first

Google Drive for desktop offers two modes, and **neither one lets you point an
arbitrary existing folder at an arbitrary existing My Drive folder.** That is
the single awkward fact in this setup:

- **Mirror My Drive** — bidirectional, real-time. But it mirrors *all* of My
  Drive to one location that Drive controls (e.g. `~/Google Drive/My Drive/…`).
  You don't get to choose per-folder mount points.
- **Sync folders from your computer** — bidirectional for that folder, and you
  keep your existing path. But the folder lands under **Computers →
  mikes-macbook-pro** in Drive, *not* inside My Drive. It can't be merged into
  the existing "Stellaris Helper" folder.

So: pick one. Option A gives you literal parity with `Stellaris Helper` at the
cost of moving the folder. Option B keeps your path at the cost of the Drive
copy living somewhere new.

---

## Option A — Mirror My Drive, relocate the project (recommended)

Gives you true parity with the existing `Stellaris Helper` folder.

1. Download Google Drive for desktop: https://www.google.com/drive/download/
2. Install it and sign in as **mcball83@gmail.com** (the account that owns
   `Stellaris Helper`).
3. Open Drive preferences → **Google Drive** (left sidebar) → choose
   **Mirror files**. Note the local folder path it shows you.
4. Let it finish the initial sync. You'll now have a real local folder at
   something like `~/Google Drive/My Drive/…/Stellaris Helper`.
5. Move your working files into that `Stellaris Helper` folder.
6. Leave a shortcut at your old path so muscle memory still works. In Terminal:

   ```
   rm -rf ~/Desktop/Projects/Stellaris
   ln -s "$HOME/Google Drive/My Drive/Stellaris Helper" ~/Desktop/Projects/Stellaris
   ```

   (Adjust the Drive path to whatever step 3 showed. The `rm -rf` only removes
   the old folder — make sure step 5 moved everything first.)

7. In the Claude desktop app, re-add the folder as a connected folder so this
   session's tools follow the new real path rather than the symlink.

**Trade-off to pressure-test:** mirroring My Drive pulls *everything* in that
Drive account down to the laptop, not just Stellaris. If that account has a lot
in it, check the disk cost before committing. Drive's "Stream files" mode avoids
that but then files aren't truly local, which breaks the source-of-truth premise.

---

## Option B — Sync the folder in place

Keeps `~/Desktop/Projects/Stellaris` exactly where it is.

1. Install Drive for desktop and sign in (same as above).
2. Preferences → **My Computer** → **Add folder** → select
   `~/Desktop/Projects/Stellaris`.
3. Check **Sync with Google Drive**. (The "Back up to Google Photos" option is
   for media backup only — leave it off.)
4. The folder now appears in Drive under **Computers → mikes-macbook-pro →
   Stellaris**.

**Trade-off:** you now have two Drive locations — the new `Computers` one, and
the old `Stellaris Helper` in My Drive. You'd want to move the two existing Docs
into the synced folder and retire `Stellaris Helper`, or accept that the Docs
live separately and are reachable only via `DRIVE_MANIFEST.md`.

---

## After either option

Tell Claude which one you picked. The daily parity audit needs to know the Drive
folder ID it should be comparing against, and Option B changes it.
