<!-- Imported from Google Docs 2026-09-20. Source doc retired.
     Original: https://docs.google.com/document/d/1lC3Np_SOu9GxI_1kdhWMZN5v5ZHyWSh97s8TUAmVrjg/edit -->

# Reference screens — GitHub Web

**Source:** Mobbin, GitHub Web app · **Captured:** 21 Aug 2026 · **Screens reviewed:** 17

**Live style guide built from these:** [Stellaris Helper Style Guide](https://claude.ai/code/artifact/8b4f99af-a76c-4f44-84c2-92a208920505)

Each screen links to its Mobbin page. "What it drove" is the specific token, component or
rule in the style guide that came out of that screen — so when a spec is questioned later,
the evidence is one click away.

## 1. Repository & file browsing

The closest analogue to the rift browser: a dense list of named items with metadata columns,
inside a page with persistent chrome.

| Screen | What it drove |
|---|---|
| [Repo file browser with Files sidebar](https://mobbin.com/screens/ee3e030f-ef84-4ad6-b838-9ac06d7607e3) | The two-column shell (content + 296px side rail), the bordered content card with a subtle-grey header strip, and 40px table rows. **Direct model for the rift list.** |
| [Repo home with About sidebar and branch popover](https://mobbin.com/screens/c7bd6794-0b21-417d-ad9b-68db089ff993) | Right-rail metadata pattern (description, links, topic pills, stat rows) — model for a rift's requirements/restrictions panel. Also the floating-overlay shadow spec. |
| [Repo with branch-protection banner](https://mobbin.com/screens/5be4900c-e6df-4a20-8156-bb48ec341cf5) | Flash message anatomy: 1px semantic border, subtle fill, icon, one line of explanation, one action, dismiss. Used for DLC-gating and sync-date notices. |
| [TheAlgorithms/Python — public repo at scale](https://mobbin.com/screens/e6b6c56b-6011-47cf-8ae6-ae93d5a38bcb) | Topic label pills (12px, pill radius, accent-subtle fill) — **direct source of the reward-type badge.** Also the segmented button groups used for filter controls. |
| [File browser with folders and Add file](https://mobbin.com/screens/f24ad9b8-f897-43b6-8e63-e6429fae5c01) | Icon + name + secondary metadata row rhythm; confirmed 14px as table body size, 12px for the timestamp column. |
| [Clone dropdown overlay](https://mobbin.com/screens/d6f80621-09d2-44b5-93f8-8ad7a0005817) | Overlay elevation, tabbed panel inside a menu, warning flash nested inside an overlay. Model for the "how do I reach this reward" popover. |

## 2. Projects — tables, boards and filters

Where GitHub solves the exact problem the reward finder has: filtering a long typed list and
showing state per row.

| Screen | What it drove |
|---|---|
| [Projects table view](https://mobbin.com/screens/26d1818c-01ff-4884-afd7-859d1bc986ed) | Filter bar sitting *inside* the card on canvas.subtle, column headers at 12px muted, status pills inline in cells. **This is the reward finder table, almost unchanged.** |
| [Projects table grouped by priority](https://mobbin.com/screens/231c5ed2-c43c-47e3-82bf-5acdb0f0af82) | Collapsible group headers with a colored dot and a count — the pattern for grouping rewards by type (Relics 8, Edicts 3, …). |
| [Projects board view](https://mobbin.com/screens/640dbc01-1c8a-420d-821c-7c85d58dfbcc) | Card-in-column layout with per-column counts; the card's label row is the ancestor of the rift card's pill row. |
| [Board with an active filter chip](https://mobbin.com/screens/fb42bf1f-b1a6-44c6-90fb-e77ec2ffd654) | Active-filter treatment: the query stays visible and editable with a count and a clear affordance, rather than hiding behind a "Filters (2)" button. |
| [Issues list — empty state](https://mobbin.com/screens/ee2303f9-d88d-480c-a0ec-8bbeaab4205a) | Empty-state spec: centered icon, 20px heading stating the fact, one sentence offering a way out, one button. Also the Filters + search + primary-action bar. |

## 3. Settings — forms and long-form nav

| Screen | What it drove |
|---|---|
| [Public profile settings](https://mobbin.com/screens/6e06aafa-5feb-4405-bbef-1abe791f85b5) | Form field anatomy: 14px semibold label, 32px input, 12px muted help text below. Left nav with grouped, labelled sections. Inline error text in danger red directly under its field. |
| [Profile form with checkboxes](https://mobbin.com/screens/5bcb835f-caad-406d-b911-3697665a011b) | Checkbox + label + help-text stacking, and the "one primary green button ends the form" rule. |
| [Sponsors settings](https://mobbin.com/screens/cf18898e-58b2-48cd-9af5-ce7468763210) | Per-field inline Save — worth stealing if rift notes become editable. Also a bordered empty-state panel nested inside a settings section. |
| [Enterprise settings](https://mobbin.com/screens/80dca4a7-39c7-4c4b-adec-a74e85b41d11) | Two-level left nav (section + sub-items), underline tabs above a form, required-field asterisk, full-width trial banner above the app chrome. |

## 4. Dark theme

| Screen | What it drove |
|---|---|
| [Codespaces / editor, dark](https://mobbin.com/screens/37875e94-9cf7-4164-932f-fdc1ad32d6b3) | Dark canvas values, and the rule that in dark mode a floating shadow is a 1px ring plus a deep drop — a soft shadow alone is invisible on near-black. |
| [Codespaces, second variant](https://mobbin.com/screens/510732c4-c7f7-4df6-99de-47043f943a8a) | Confirms dark-mode border contrast (`#3d444d`) and that dark surfaces step *up* in lightness as they come forward, the inverse of light mode. |

## Notes

- **Why there are no image files mirrored here.** Mobbin serves its screenshots from an
  authenticated CDN, so the files cannot be copied out — only linked. The links resolve for
  anyone with a Mobbin account.
- **Licensing.** Primer, GitHub's design system, is MIT-licensed and its tokens can be used
  freely. GitHub's logo, wordmark and the Octicons brand marks are **not** — the mark used in
  the style guide header is a placeholder and must be replaced before anything ships.
- **What to add next.** The reference set has no pull-request diff view and no command
  palette. If this ever gets a side-by-side path comparison or a keyboard-first jump-to-rift,
  pull those two screens before designing them.
