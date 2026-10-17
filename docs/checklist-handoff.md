# Simple Checklist handoff fallback (Phase 1)

The app receives `https://lewlabsapps.com/simple-checklist/import#sc=<payload>`.
The fragment is UTF-8 V1 JSON in unpadded URL-safe base64. It normally stays out
of HTTP requests; it is not encryption and may remain in browser/history/share
surfaces. The website must not decode or forward it.

`simple-checklist/import.html` is the static fallback. GitHub Pages serves the
extensionless `/simple-checklist/import` path using its existing `.html` routing
(the same behavior as the existing `/simple-checklist` product page). Keep the
root `.nojekyll` file so `.well-known/assetlinks.json` is served unchanged.
There is no JavaScript, analytics, form, account, upload, storage or AI call.
The page reuses existing responsive/light/dark branding without changing CSS.

## Certificate provenance

On 2026-10-16 the owner-connected Samsung Fold4's production package
`com.lewlabsapps.simplechecklist` was checked read-only: version `0.1.16` (25),
installer `com.android.vending`. Its base APK was pulled without changing the
installed app. Android SDK `apksigner verify --verbose --print-certs` verified
APK v3 signing and reported exactly one APK signer with SHA-256:

`C1:98:59:A4:33:8C:DB:C6:71:AC:F3:4C:C1:3D:12:6C:67:E0:2C:76:E8:07:81:53:30:21:C9:7A:4A:30:70:50`

This is the delivered APK signer, not its Source Stamp and not the Codemagic
upload certificate (which begins `B0:15:E8:C2`). The asset statement includes
only this verified signing key and the production package. No debug/staging
certificate is authorized. If Play signing rotation later yields another
legitimate signing certificate, verify it before adding it; do not guess.

## Validation and publication

Run `python tools/test_handoff.py` (standard library only) for HTML links,
privacy constraints, asset-statement validation and local HTTP serving.
The test server simulates Pages' extensionless `.html` resolution; it is a
temporary development check, not a new production backend.

GitHub Pages currently publishes **main / root**. Pushing the feature branch
does **not** publish this page or the asset statement. After owner review and
approval to merge the website branch, verify the live endpoints return 200
directly, with HTML and JSON respectively, over HTTPS:

- `https://lewlabsapps.com/simple-checklist/import`
- `https://lewlabsapps.com/.well-known/assetlinks.json`

The existing Play version 25 predates the receiving code. End-to-end verified
App Link testing needs a separately approved Play-distributed app update with
the matching signing certificate. Do not reinstall a locally signed APK over
the owner's Play installation or weaken verification to demonstrate the link.

Future iOS uses the same URL/fragment/Dart codec with Universal Links and a
separately verified Apple association file; no iOS association is claimed here.
