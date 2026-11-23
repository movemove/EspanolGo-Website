# EspanolGo — Travel Spanish, 32 Sounds, 100 Video Dialogues & Live Translation Website

Official marketing, interactive studio audio preview, privacy policy, and support website for **EspanolGo** ([AE Interactive](https://appengine.fun)).

- **Live Website:** https://espanolgo.appengine.fun
- **App Store Download:** https://apps.apple.com/app/id6837611917

## Features
- **4 Languages Supported:** English (`/`), Traditional Chinese (`/?lang=zh-Hant`), Simplified Chinese (`/?lang=zh-Hans`), and Japanese (`/?lang=ja`).
- **App Store Conversion:** iOS Safari Smart App Banner (`app-id=6837611917`), App Store CTAs across nav/hero/pricing/footer, `Free Forever` vs. `$3.99 Lifetime Pro` comparison, `hreflang`, and `SoftwareApplication` JSON-LD.
- **Interactive Spanish Studio Audio:** In-browser studio MP3 playback with LatAm/España IPA notes and pronunciation highlights.
- **Localized `/privacy` & `/support`:** Zero-data-collection privacy policy and on-device framework compatibility docs.
- **Cloudflare Worker Edge Bundle:** Single-file deployment serving HTML, WebP screenshots, and MP3 clips on `espanolgo.appengine.fun`.

## Build & Deploy
```bash
python3 prepare_assets.py
python3 build_and_deploy.py
```
