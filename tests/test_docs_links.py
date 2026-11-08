"""Every relative link in the kept docs resolves to a real file."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


class LinksResolve(unittest.TestCase):
    def test_every_relative_link_resolves_to_a_real_file(self):
        files = [ROOT / "README.md", ROOT / "schema" / "README.md"]
        broken = []
        for f in files:
            for target in LINK.findall(f.read_text(encoding="utf-8")):
                target = target.strip()
                if not target or target.startswith("#") or "://" in target:
                    continue
                if not (f.parent / target.split("#")[0]).exists():
                    broken.append(f"{f.relative_to(ROOT)} -> {target}")
        self.assertEqual(broken, [])


if __name__ == "__main__":
    unittest.main()
