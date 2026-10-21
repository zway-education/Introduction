# 孩子版主圖：縮成 1080×1350 放在 1080×1620 紙上（下方留紙色），再算鉛筆線稿與畫的順序
import cv2, numpy as np, sys
rng = np.random.default_rng(3)
H, W, IH = 1620, 1080, 1350
for k in [f"{s}{i}" for s in "cd" for i in range(1, 6)]:
    src = cv2.imread(f"img/kids/{k}.jpg"); im = cv2.resize(src, (W, IH), interpolation=cv2.INTER_AREA)
    pad = np.full((H, W, 3), (240, 246, 249), np.uint8); pad[:IH] = im
    cv2.imwrite(f"img/kids/{k}_p.jpg", pad, [cv2.IMWRITE_JPEG_QUALITY, 94])
    g = cv2.cvtColor(pad, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.
    g = cv2.bilateralFilter(g, 7, .08, 5)
    d = cv2.GaussianBlur(g, (0, 0), 1.4) - 0.985 * cv2.GaussianBlur(g, (0, 0), 2.4)
    e = 1 - np.tanh(np.clip(d, -1, 1) * 40); e = np.clip((e - 0.7) / 0.9, 0, 1); e[IH - 12:] = 0
    m = (e > .35).astype(np.uint8); n, lab, st, _ = cv2.connectedComponentsWithStats(m, connectivity=8)
    keep = np.zeros(n, bool); keep[1:] = st[1:, cv2.CC_STAT_AREA] >= 28; e = e * keep[lab]
    pr = cv2.GaussianBlur(rng.random((H, W)).astype(np.float32), (0, 0), 30); pr = .78 + .22 * (pr - pr.min()) / (pr.max() - pr.min())
    a = cv2.GaussianBlur(np.clip(e * pr, 0, 1), (0, 0), .6)
    rgba = np.zeros((H, W, 4), np.uint8); rgba[..., 0] = 0x22; rgba[..., 1] = 0x26; rgba[..., 2] = 0x2c; rgba[..., 3] = (a * 255).astype(np.uint8)
    cv2.imwrite(f"img/kids/{k}_lines.png", rgba)
    al = rgba[..., 3]; m = (al > 40).astype(np.uint8)
    n, lab, stats, cent = cv2.connectedComponentsWithStats(m, connectivity=8)
    order = np.full(n, 1.0, np.float32); row = np.floor(cent[1:, 1] / 160); x = cent[1:, 0] / W; x = np.where(row % 2 == 0, x, 1 - x)
    key = row + x * .9 + rng.random(n - 1) * .25; key = np.where(stats[1:, cv2.CC_STAT_AREA] >= 60, key, key + 1.5)
    order[1:] = np.argsort(np.argsort(key)) / max(1, n - 2)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); om = order[lab].astype(np.float32)
    x0 = stats[:, cv2.CC_STAT_LEFT][lab]; y0 = stats[:, cv2.CC_STAT_TOP][lab]; w = np.maximum(1, stats[:, cv2.CC_STAT_WIDTH][lab]); h = np.maximum(1, stats[:, cv2.CC_STAT_HEIGHT][lab])
    om = om + ((xx - x0) / w + (yy - y0) / h) / 2 * (1.0 / max(1, n - 1)) * 1.6; om[lab == 0] = 1.0
    cv2.imwrite(f"img/kids/{k}_order.png", (np.clip(om, 0, 1) * 254).astype(np.uint8)); print(k, round(float((a > .25).mean() * 100), 1), "% 線", n, "筆")
