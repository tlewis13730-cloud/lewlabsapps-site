"""Offline structural/content checks; never publish or contact the MCP."""
from pathlib import Path
from html.parser import HTMLParser
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        for key, value in attrs:
            if key == "href":
                self.links.append(value)


class Policies(unittest.TestCase):
    def test_pages_are_local_responsive_and_script_free(self):
        for name in ["privacy.html", "support.html", "terms.html"]:
            text = (ROOT / name).read_text(encoding="utf-8")
            tags = Tags()
            tags.feed(text)
            self.assertIn('name="viewport"', text)
            self.assertIn('lang="en"', text)
            self.assertEqual(tags.tags.count("main"), 1)
            self.assertEqual(tags.tags.count("h1"), 1)
            self.assertNotIn("script", tags.tags)
            self.assertNotIn("form", tags.tags)
            for link in tags.links:
                if not link.startswith(("https:", "mailto:", "#")):
                    self.assertTrue((ROOT / link.split("#")[0]).exists(), link)

    def test_privacy_explains_actual_handoff_limits(self):
        text = (ROOT / "privacy.html").read_text(encoding="utf-8")
        for phrase in ["temporarily validates", "Encoding is not encryption", "normal application logs", "explicitly approve", "no server-side import token", "own terms and retention practices", "30-day"]:
            self.assertIn(phrase, text)

    def test_terms_are_not_pretended_effective(self):
        text = (ROOT / "terms.html").read_text(encoding="utf-8")
        for phrase in ["Not yet effective", 'content="noindex"', "private testing", "No purchase", "consumer rights"]:
            self.assertIn(phrase, text)

    def test_support_does_not_claim_public_installation(self):
        text = (ROOT / "support.html").read_text(encoding="utf-8")
        self.assertIn("not publicly listed yet", text)
        self.assertIn("Do not send complete private handoff links", text)


if __name__ == "__main__":
    unittest.main()
