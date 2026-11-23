#!/usr/bin/env python3
"""Prepare optimized WebP screenshots, icons, OG social banner, and sample Spanish MP3s for EspanolGo-Website."""
from __future__ import annotations

import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SITE_DIR = Path("/Users/kevin/.gemini/antigravity/scratch/EspanolGo-Website")
PUB_IMG = SITE_DIR / "public/images"
PUB_AUD = SITE_DIR / "public/audio"

SHOTS_ROOT = Path("/Users/kevin/Desktop/EspanolGo Hub/Screenshots")
ICON_SRC = Path("/Users/kevin/Desktop/EspanolGo Hub/AppIcon/EspanolGo_AppIcon_1024x1024.png")
AUDIO_SRC = Path("/Users/kevin/.gemini/antigravity/scratch/EspanolGo.swiftpm/Resources/Audio")

LANG_MAP = {
    "en": "en-US",
    "zh-Hant": "zh-Hant",
    "zh-Hans": "zh-Hans",
    "ja": "ja",
}

SCENES = [
    ("01_LearnPath.png", "s01"),
    ("02_VoiceTutor.png", "s02"),
    ("03_Interpreter.png", "s03"),
    ("04_VideoScenarios.png", "s04"),
    ("05_PhonicsLab.png", "s05"),
]

AUDIO_SAMPLES = [
    ("vocab_ex_v_split_bill.mp3", "split.mp3"),
    ("vocab_ex_v_oat_milk.mp3", "oatmilk.mp3"),
    ("vocab_ex_v_credit_card.mp3", "card.mp3"),
    ("vocab_ex_v_check_in.mp3", "checkin.mp3"),
]


def round_icon(im: Image.Image, radius_ratio: float = 0.22) -> Image.Image:
    w, h = im.size
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w, h), radius=int(w * radius_ratio), fill=255)
    out = im.convert("RGBA")
    out.putalpha(mask)
    return out


def build_og_image(icon_img: Image.Image) -> None:
    w, h = 1200, 630
    bg = Image.new("RGB", (w, h), (10, 12, 24))
    px = bg.load()
    for y in range(h):
        ty = y / (h - 1)
        for x in range(w):
            tx = x / (w - 1)
            r = int(28 + 70 * (1 - tx) * 0.55 + 16 * ty)
            g = int(16 + 24 * ty + 38 * tx * 0.4)
            b = int(26 + 44 * tx + 22 * (1 - ty))
            px[x, y] = (min(255, r), min(255, g), min(255, b))

    canvas = bg.convert("RGBA")
    ic = round_icon(icon_img.resize((220, 220), Image.Resampling.LANCZOS), 0.22)
    canvas.paste(ic, (96, (h - 220) // 2), ic)

    draw = ImageDraw.Draw(canvas)
    f_title = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 76, index=1)
    f_sub = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 33, index=0)
    f_pill = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 24, index=1)

    tx_x = 368
    draw.text((tx_x, 174), "EspanolGo", font=f_title, fill=(255, 255, 255, 255))
    draw.text((tx_x, 272), "100 Real Spanish Video Dialogues", font=f_sub, fill=(253, 186, 116, 248))
    draw.text((tx_x, 322), "32 IPA Sounds · Voice Practice · Live Translation", font=f_sub, fill=(203, 213, 225, 238))
    draw.text((tx_x, 404), "iOS  ·  iPadOS  ·  iPhone Duo  |  AE Interactive", font=f_pill, fill=(94, 234, 212, 245))

    canvas.convert("RGB").save(PUB_IMG / "og.png", format="PNG", optimize=True)


def main() -> None:
    PUB_IMG.mkdir(parents=True, exist_ok=True)
    PUB_AUD.mkdir(parents=True, exist_ok=True)

    icon = Image.open(ICON_SRC).convert("RGB")
    round_icon(icon.resize((256, 256), Image.Resampling.LANCZOS)).save(PUB_IMG / "icon.webp", format="WEBP", quality=88)
    round_icon(icon.resize((512, 512), Image.Resampling.LANCZOS)).save(PUB_IMG / "icon.png", format="PNG", optimize=True)
    build_og_image(icon)

    for site_lang, rel_folder in LANG_MAP.items():
        for src_name, short in SCENES:
            src = SHOTS_ROOT / rel_folder / "iPhone_6.9" / src_name
            im = Image.open(src).convert("RGB")
            im_s = im.resize((640, 1390), Image.Resampling.LANCZOS)
            im_s.save(PUB_IMG / f"{site_lang}_{short}.webp", format="WEBP", quality=84)

        ipad_src = SHOTS_ROOT / rel_folder / "iPad_13" / "02_VoiceTutor.png"
        ipad_im = Image.open(ipad_src).convert("RGB").resize((760, 1013), Image.Resampling.LANCZOS)
        ipad_im.save(PUB_IMG / f"{site_lang}_ipad.webp", format="WEBP", quality=84)

    for src_name, dst_name in AUDIO_SAMPLES:
        shutil.copy2(AUDIO_SRC / src_name, PUB_AUD / dst_name)

    total_img = sum(p.stat().st_size for p in PUB_IMG.glob("*"))
    total_aud = sum(p.stat().st_size for p in PUB_AUD.glob("*"))
    print(f"ASSETS_READY: images={len(list(PUB_IMG.glob('*')))} ({total_img/1024:.1f} KB), audio={len(list(PUB_AUD.glob('*')))} ({total_aud/1024:.1f} KB)")


if __name__ == "__main__":
    main()
