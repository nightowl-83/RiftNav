# Archive — retired Google Drive sync setup

**Retired 2026-09-20.** Superseded by the Git repository.

Between 2026-08-22 and 2026-09-20, the local folder `~/Desktop/Projects/Stellaris` was the
source of truth and a Google Drive folder ("Stellaris Helper",
`1fasaDAjT6Yvqo58fdlUmVctGeLaT6cqi`) was maintained as a mirror, with a daily scheduled
parity audit.

That arrangement is no longer in force. The files here are kept for history only — do not
follow their instructions.

Two things to be aware of:

- The Drive folder still holds two **Google Docs** that have no true file form. Their `.docx`
  and `.pdf` snapshots are in `reference/`. If those Docs are still being edited in Drive,
  Drive is authoritative for them and the snapshots will drift.
- If Google Drive for desktop was ever installed and pointed at this folder, uninstall it or
  unlink this folder. Two sync systems fighting over one directory is how you get conflict
  copies.
