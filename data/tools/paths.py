# -*- coding: utf-8 -*-
"""Where the repo is. Defaults to this file's location, so the tools run from any checkout on
any machine; STELLARIS_ROOT overrides it (the Cowork mount used ~/mnt/Stellaris)."""
import os
ROOT = os.environ.get("STELLARIS_ROOT") or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA = os.path.join(ROOT, "data")
TOOLS = os.path.join(DATA, "tools")
UI = os.path.join(ROOT, "design_handoff_rift_finder")
