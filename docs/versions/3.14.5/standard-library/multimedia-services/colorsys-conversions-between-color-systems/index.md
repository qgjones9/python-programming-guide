# [colorsys — Conversions between color systems](https://docs.python.org/3/library/colorsys.html)

The [`colorsys`](https://docs.python.org/3/library/colorsys.html) module converts color coordinates between **RGB** (monitor space) and three other models: **YIQ** (broadcast), **HLS** (hue–lightness–saturation), and **HSV** (hue–saturation–value). All functions are pure math — no image objects, no file I/O. Coordinates are **floating-point**; in RGB, HLS, and HSV every component lies in **0.0–1.0**. In YIQ, **Y** is 0–1 while **I** and **Q** may be negative. Full definitions remain on [docs.python.org](https://docs.python.org/3/library/colorsys.html).

Background reading: [Charles Poynton's Color FAQ](https://poynton.ca/ColorFAQ.html) and [Cambridge in Colour — color spaces](https://www.cambridgeincolour.com/tutorials/color-spaces.htm).

---

## Function pairs — [Module contents](https://docs.python.org/3/library/colorsys.html#module-colorsys)

| Direction | Functions |
|-----------|-----------|
| RGB ↔ YIQ | `rgb_to_yiq`, `yiq_to_rgb` |
| RGB ↔ HLS | `rgb_to_hls`, `hls_to_rgb` |
| RGB ↔ HSV | `rgb_to_hsv`, `hsv_to_rgb` |

Each conversion is **bidirectional** but not always bit-identical after a round trip because of floating-point rounding.

```python
# Goal: official docs example — HSV round trip
import colorsys

h, s, v = colorsys.rgb_to_hsv(0.2, 0.4, 0.4)
assert (round(h, 1), round(s, 1), round(v, 1)) == (0.5, 0.5, 0.4)
back = colorsys.hsv_to_rgb(h, s, v)
assert all(abs(a - b) < 1e-9 for a, b in zip(back, (0.2, 0.4, 0.4)))
```

```python
# Goal: convert 8-bit sRGB bytes to HLS and back
import colorsys

def byte_rgb_to_unit(r, g, b):
    return r / 255.0, g / 255.0, b / 255.0

def unit_to_byte_rgb(r, g, b):
    return tuple(min(255, max(0, int(round(c * 255)))) for c in (r, g, b))

r, g, b = byte_rgb_to_unit(255, 128, 64)
h, lightness, s = colorsys.rgb_to_hls(r, g, b)
r2, g2, b2 = colorsys.hls_to_rgb(h, lightness, s)
assert unit_to_byte_rgb(r2, g2, b2) == (255, 128, 64)
```

```python
# Goal: YIQ path (I and Q may be negative)
import colorsys

y, i, q = colorsys.rgb_to_yiq(1.0, 0.0, 0.0)
assert 0.0 <= y <= 1.0
r, g, b = colorsys.yiq_to_rgb(y, i, q)
assert all(abs(c - e) < 1e-9 for c, e in zip((r, g, b), (1.0, 0.0, 0.0)))
```

---

## Coordinate conventions

| Space | Component ranges | Typical use |
|-------|------------------|-------------|
| RGB | R, G, B each 0–1 | Web/CSS after scaling from 0–255 |
| HSV | H 0–1 (fraction of circle), S and V 0–1 | Color pickers, segmentation by hue |
| HLS | H 0–1, L and S 0–1 | Adjust lightness without shifting hue |
| YIQ | Y 0–1; I, Q signed | Legacy TV / luma-chroma separation |

**Hue** in this module is **not** degrees: multiply by 360 for CSS `hsl()` angles. **Saturation** and **lightness/value** are unit intervals, not percentages.

```python
# Goal: map colorsys hue fraction to CSS degrees
import colorsys

h, s, v = colorsys.rgb_to_hsv(1.0, 0.0, 0.0)  # pure red
css_h = round(h * 360)
assert css_h == 0
```

---

## Practical patterns

| Pattern | Approach |
|---------|----------|
| Lighten a swatch | Raise **L** in HLS or **V** in HSV, then convert back to RGB |
| Desaturate toward gray | Drive **S** toward 0 in HLS/HSV |
| Compare two hex colors | Normalize to 0–1 RGB, convert to HSV, compare **H** with tolerance |
| Per-pixel image work | Prefer **Pillow**, **OpenCV**, or **numpy** — `colorsys` is scalar-only |

```python
# Goal: lighten by boosting HLS lightness
import colorsys

def lighten(r, g, b, amount=0.15):
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return colorsys.hls_to_rgb(h, min(1.0, l + amount), s)

r, g, b = (0.2, 0.4, 0.6)
lr, lg, lb = lighten(r, g, b)
assert lr >= r and lg >= g and lb >= b
```

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Passing 0–255 integers directly | Divide by 255 first (values > 1 clamp unpredictably in downstream math) |
| Expecting hue in degrees | Multiply `h` by 360 for CSS; keep 0–1 for `colorsys` |
| Assuming exact round trips | Compare with tolerance (`abs(a - b) < 1e-9`) |
| Using for alpha compositing | `colorsys` ignores alpha; handle transparency separately |
| Confusing HLS and HSV lightness | Same RGB yields different H/L/S vs H/S/V triples — pick one model per feature |

---

## Best practices

| Practice | Why |
|----------|-----|
| Normalize inputs once at UI boundaries | Keeps internal math in documented 0–1 range |
| Round only when emitting bytes or CSS | Avoid compounding error across chained transforms |
| Document which model your theme uses | HLS “lightness” ≠ HSV “value” for the same color name |
| Use vectorized libraries for images | One `colorsys` call per pixel is slow in Python loops |
