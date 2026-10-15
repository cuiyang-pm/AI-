# -*- coding: utf-8 -*-
"""像素级横向溢出诊断：找出 375px 视口下贴到右缘的内容行"""
import sys
from PIL import Image, ImageChops

path = sys.argv[1]
im = Image.open(path).convert("RGB")
W, H = im.size
BG = (255, 250, 235)
THR = 24

bg = Image.new("RGB", im.size, BG)
diff = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > THR else 0)
px = diff.load()

rows = []
for y in range(H):
    mx = -1
    for x in range(W - 1, -1, -1):
        if px[x, y]:
            mx = x
            break
    if mx >= 0:
        rows.append((y, mx))

over = [(y, mx) for y, mx in rows if mx >= W - 3]
print("image %dx%d, non-bg rows=%d, rows touching right edge=%d" % (W, H, len(rows), len(over)))
if over:
    ys = [y for y, _ in over]
    print("overflow y range: %d -> %d" % (min(ys), max(ys)))
    segs = []
    start = prev = None
    for y, _ in over:
        if start is None:
            start = prev = y
        elif y - prev <= 2:
            prev = y
        else:
            segs.append((start, prev))
            start = prev = y
    segs.append((start, prev))
    for a, b in segs:
        m = max(mx for y, mx in over if a <= y <= b)
        print("  band y=%d..%d  max_x=%d" % (a, b, m))
