# Prompt — "Split tabs" layout (for Claude Code)

Written 2026-09-28. Source design: the "Test build" board of the Rift Nav — Split Browse Prototypes canvas
(https://claude.ai/artifact/HaAgwXd9qWinCuJ5uivkXv). Paste everything below the line into Claude Code.

---

Build a new desktop layout for Rift Nav, "Split tabs", on a new branch. It's based on the
"Test build" board of the Rift Nav — Split Browse Prototypes canvas (claude.ai artifact
HaAgwXd9qWinCuJ5uivkXv). Match that board's behaviour; styling comes from the existing file.

SETUP
- git checkout -b split-tabs
- File: design_handoff_rift_finder/Rift Finder Holo.dc.html
- Add "Split tabs" to the `layout` enum in data-props. Make it the DEFAULT on this branch only
  (main keeps "Notched split"). Derived flag: `tabsLayout = lay === 'Split tabs' && !state.mob`.
- Mobile (state.mob) is completely unchanged: with tabsLayout false, mobile behaves exactly as today.

HOW IT BEHAVES
1. Browse screen (nothing open): same as Notched split's browse today, with the same header,
   search, filter, cards and pin buttons. Opening a rift or dig site no longer changes the page.
   The browse column collapses to the left and the detail loads on the right, inside a tabbed panel.
2. Open tabs: new state `tabs: [{type:'rift'|'dig', name}]` plus `activeTab` (the key
   `type + ':' + name`), max 5.
   - Opening something already open just brings its tab forward.
   - Opening a 6th closes the oldest tab that isn't active.
   - Each tab keeps its own place (reward, cur, railOpen). REUSE the existing `state.progress`
     store: monTabs `go()` already saves and restores it. Factor that into one helper,
     `switchTo(type, name)`, and use it for tabs AND monitoring, so the two stay consistent.
   - Tab: a folder-tab shape above the panel, with the icon tile (see 3), the name
     (ellipsis), an amber dot when a target reward is set, and a close button.
     Active tab: amber top edge, and it merges into the panel.
   - Right of the tabs: "{n} / 5 OPEN" and a ghost "CLOSE ALL" button.
   - Closing the active tab activates the neighbour. Closing the last tab, or CLOSE ALL,
     returns to the browse screen.
   - The rift detail, dig detail AND the step-by-step reader all render INSIDE the panel.
     Size them to the panel's width with container queries (container-type: inline-size on
     the panel), not viewport media queries. The panel is about 1270px wide at 1440, less when
     the list mode is on.
   - Remove the standalone "‹ ABORT / ALL RIFTS" back button in this layout; the tab's close
     button replaces it. ABORT inside the reader still clears the target (goBack).
3. Left column, two modes, with the choice remembered in localStorage 'rf-split-mode':
   a) ICONS (default), 84px wide:
      - Top: a vertical 2-button segmented control (Icons / List), then a RIFT/DIG toggle
        (the existing `browse` state), then a search button that switches to List mode.
      - Tiles: 48px icons with a two-letter code (first letters of the first two words, ignoring
        "The", "A", "in", "on", "of"; one-word names use their first two letters). Ruins-style
        clashes: give "Dimensional Dump" DD. Also check the dig sites for clashes and fix any.
      - Tiles are grouped under small section labels using the existing group keys
        (rifts: Unique / Precursor / General; digs: this.digData.groups).
      - Group dot top-right.
      - An amber ring bottom-right if the item is monitored.
      - A cyan tick on the left edge if it's open in a tab; amber tile plus a longer tick if it's
        the active tab.
      - The tile list scrolls.
      - The name tooltip must render OUTSIDE the scroller, so it isn't clipped. Position it from
        the tile's bounding box relative to the rail, divided by the rail's rendered scale.
        Show it on hover and on focus; hide it on scroll and on blur.
      - While a search or filter is active, show a small amber "{tag} ×" chip under the search
        button that clears it.
   b) LIST, 330px wide:
      - A horizontal Icons/List toggle, "SELECT RIFT" (or "SELECT DIG SITE"), and "{shown}/{total}".
      - The search field matches names AND reward names/categories. When a rift matches only
        through its rewards, its row meta reads "{n} MATCHING" instead of "{n} REWARDS".
      - The type filter, compact.
      - One-line rows: 36px icon tile, name, "{ch} CH · {n} REWARDS", the monitored ring and the
        group dot. States: open (faint cyan fill), active (amber).
   - Both modes share the SAME q / cat state as the browse screen, so switching never loses
     a search.
4. Motion: the left column slides in (railIn, 18px, .3s); tabs rise in (8px, .25s); the panel
   content uses the existing hudIn. Respect prefers-reduced-motion like the rest of the file.

ACCESSIBILITY
- The tab strip is role="tablist" and each tab button is role="tab" with aria-selected.
  Use a roving tabindex, ←/→ to move between tabs and Enter to activate. The close buttons are
  separate buttons with aria-label "Close {name}". The panel is role="tabpanel".
- Rail tiles are buttons, with aria-label "{name}" or "{name}, open in a tab", and
  aria-current on the active one.
- When a tab closes, focus moves to the neighbouring tab, or to the first card when returning
  to browse.
- Type minimums from README "Accessibility and polish" apply: 11px labels, 12px reading text.

DON'T
- Don't touch data/*.json, rift-data.js or dig-data.js.
- Don't change Grid, Split column or Notched split behaviour, apart from the switchTo refactor.
- Don't change mobile.

VERIFY (headless, as in previous passes) at 1440×900, 1280×800 and 1180×820, plus 390×844 to
confirm mobile is untouched:
- Open 3 rifts and 1 dig site, set a target on one, switch tabs, and come back: the target and
  the reader step are preserved.
- Open a 6th item: the oldest inactive tab closes.
- Close all: you're back on browse, with focus on the first card.
- The rail tooltip isn't clipped at the top or bottom of the scroller.
- In List mode, searching "relic" shows only rifts and sites with a relic reward, with MATCHING
  counts.
- No horizontal scroll, and nothing off screen, at any of the four sizes.

Then update README.md (new "Split tabs" section under Variant system), commit to split-tabs,
and push the branch. Don't merge to main.
