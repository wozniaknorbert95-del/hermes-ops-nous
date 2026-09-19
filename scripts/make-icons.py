#!/usr/bin/env python3
"""Generate PWA raster icons from the same design as icons/icon.svg.

Why: Chrome needs PNG 192/512 for installability; iOS ignores SVG
apple-touch-icon and needs a 180x180 PNG (no transparency, full bleed).

Dev-only tool (Pillow). Not run at deploy time.

    python scripts/make-icons.py

Outputs:
    icons/icon-192.png
    icons/icon-512.png
    icons/icon-maskable-512.png
    icons/apple-touch-icon-180.png
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover
    print("FAIL: Pillow required -> pip install Pillow")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
ICONS = ROOT / "icons"

BG = "#0b1020"
RING = "#22d3ee"
HAND = "#34d399"
TXT = "#f8fafc"

VIEWBOX = 512
FONT_CANDIDATES = (
    r"C:\Windows\Fonts\seguisb.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
    r"C:\Windows\Fonts\arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
)


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def render(size: int, *, rounded: bool) -> Image.Image:
    """Draw the Akademia mark at `size` px. `rounded=False` = full bleed (iOS)."""
    scale = size / VIEWBOX
    ss = 4  # supersample for smooth curves
    canvas = size * ss
    img = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def s(v: float) -> float:
        return v * scale * ss

    if rounded:
        d.rounded_rectangle([0, 0, canvas - 1, canvas - 1], radius=s(96), fill=BG)
    else:
        d.rectangle([0, 0, canvas - 1, canvas - 1], fill=BG)

    cx = cy = s(256)
    r = s(168)
    ring_w = max(2, int(s(28)))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RING, width=ring_w)

    # clock hand: 12 o'clock -> centre -> 4 o'clock
    pts = [(s(256), s(128)), (s(256), s(256)), (s(352), s(304))]
    d.line(pts, fill=HAND, width=ring_w, joint="curve")
    for px, py in (pts[0], pts[2]):
        d.ellipse([px - ring_w / 2, py - ring_w / 2, px + ring_w / 2, py + ring_w / 2], fill=HAND)

    font = load_font(int(s(72)))
    try:
        d.text((cx, s(420)), "A", font=font, fill=TXT, anchor="mm")
    except (ValueError, AttributeError):  # bitmap fallback font has no anchor
        d.text((cx, s(420)), "A", font=font, fill=TXT)

    final = Image.LANCZOS if hasattr(Image, "LANCZOS") else Image.Resampling.LANCZOS
    out = img.resize((size, size), final)
    if not rounded:  # iOS composites on black; flatten to remove alpha
        flat = Image.new("RGB", (size, size), BG)
        flat.paste(out, (0, 0), out)
        return flat
    return out


def main() -> int:
    ICONS.mkdir(parents=True, exist_ok=True)
    targets = (
        ("icon-192.png", 192, True),
        ("icon-512.png", 512, True),
        ("icon-maskable-512.png", 512, False),
        ("apple-touch-icon-180.png", 180, False),
    )
    for name, size, rounded in targets:
        path = ICONS / name
        render(size, rounded=rounded).save(path, format="PNG", optimize=True)
        print(f"OK {path.relative_to(ROOT)} ({size}x{size}, {'rounded' if rounded else 'full-bleed'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
