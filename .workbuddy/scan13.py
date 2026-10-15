# -*- coding: utf-8 -*-
"""纯 PIL 像素扫描：定位橙色滑块 / 仪表盘数字 / 浅橙分段滑块。"""
import sys
from PIL import Image

im = Image.open(sys.argv[1]).convert('RGB')
W, H = im.size
px = im.load()
print('size', im.size)

regions = {}
for y in range(H):
    for x in range(W):
        r, g, b = px[x, y]
        if r > 220 and 50 < g < 130 and b < 60:          # 信号橙 #fa520f 系
            key = 'orange_left' if x < 600 else ('orange_right' if x > 1150 else 'orange_mid')
        elif r >= 250 and 244 <= g <= 250 and 232 <= b <= 242:  # #FFF7ED 系
            if 150 < y < 520 and x < 700:
                key = 'cream_left'
            elif x > 1150:
                key = 'cream_right'
            else:
                continue
        else:
            continue
        reg = regions.setdefault(key, [10**9, -1, 10**9, -1])  # xmin xmax ymin ymax
        reg[0] = min(reg[0], x); reg[1] = max(reg[1], x)
        reg[2] = min(reg[2], y); reg[3] = max(reg[3], y)

for k in sorted(regions):
    xmin, xmax, ymin, ymax = regions[k]
    print('%-13s x %4d..%4d  y %4d..%4d' % (k, xmin, xmax, ymin, ymax))
