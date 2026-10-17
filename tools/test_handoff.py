"""Offline static-site contracts; no dependencies, account or live mutation."""
import functools
import http.server
import json
from pathlib import Path
from html.parser import HTMLParser
import threading
import unittest
from urllib.parse import urlsplit
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "simple-checklist/import.html"
FINGERPRINT = "C1:98:59:A4:33:8C:DB:C6:71:AC:F3:4C:C1:3D:12:6C:67:E0:2C:76:E8:07:81:53:30:21:C9:7A:4A:30:70:50"


class Markup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class PagesHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Model the existing GitHub Pages extensionless .html behavior locally.
        if self.path == "/simple-checklist/import":
            self.path += ".html"
        super().do_GET()

    def log_message(self, *_):
        pass


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.markup = Markup()
        self.html = PAGE.read_text(encoding="utf-8")
        self.markup.feed(self.html)

    def test_all_local_links_resolve(self):
        for _, attrs in self.markup.tags:
            for key in ("href", "src"):
                value = attrs.get(key)
                if value and not urlsplit(value).scheme:
                    self.assertTrue(value.startswith("/"), value)
                    self.assertTrue((ROOT / urlsplit(value).path.lstrip("/")).is_file(), value)

    def test_product_and_play_links(self):
        links = [a.get("href") for t, a in self.markup.tags if t == "a"]
        self.assertIn("/simple-checklist.html", links)
        self.assertIn("https://play.google.com/store/apps/details?id=com.lewlabsapps.simplechecklist", links)
        self.assertNotIn("staging", self.html)

    def test_no_active_content_or_collection(self):
        for tag, attrs in self.markup.tags:
            self.assertNotIn(tag, {"script", "iframe", "form", "input", "object", "embed"})
            self.assertFalse(any(key.startswith("on") for key in attrs))
            if "src" in attrs:
                self.assertTrue(attrs["src"].startswith("/"))
        policies = {a.get("name", a.get("http-equiv")): a.get("content")
                    for t, a in self.markup.tags if t == "meta"}
        self.assertEqual(policies["referrer"], "no-referrer")
        self.assertIn("default-src 'none'", policies["Content-Security-Policy"])

    def test_responsive_shared_branding(self):
        self.assertTrue(any(t == "meta" and a.get("name") == "viewport" for t, a in self.markup.tags))
        self.assertTrue(any(t == "link" and a.get("href") == "/styles.css" for t, a in self.markup.tags))
        self.assertIn('class="btn btn-primary"', self.html)
        self.assertIn("Nothing is imported without your approval", self.html)

    def test_assetlinks_exact_verified_identity(self):
        statements = json.loads((ROOT / ".well-known/assetlinks.json").read_text(encoding="utf-8"))
        self.assertEqual(statements, [{
            "relation": ["delegate_permission/common.handle_all_urls"],
            "target": {"namespace": "android_app", "package_name": "com.lewlabsapps.simplechecklist",
                       "sha256_cert_fingerprints": [FINGERPRINT]},
        }])
        self.assertTrue((ROOT / ".nojekyll").exists())

    def test_local_http_route_and_assetlinks(self):
        handler = functools.partial(PagesHandler, directory=str(ROOT))
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            origin = f"http://127.0.0.1:{server.server_port}"
            for route, content_type in [("/simple-checklist/import", "text/html"),
                                        ("/.well-known/assetlinks.json", "application/json")]:
                with urlopen(origin + route, timeout=5) as response:
                    self.assertEqual(response.status, 200)
                    self.assertEqual(response.headers.get_content_type(), content_type)
                    self.assertTrue(response.read())
        finally:
            server.shutdown()
            server.server_close()
            worker.join(timeout=5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
