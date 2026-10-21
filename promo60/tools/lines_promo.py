# 宣傳片主圖的「鉛筆線稿」v2：用 XDoG（兩個模糊相減）取線，線有粗細與濃淡，像手畫；去掉碎點
import cv2, numpy as np
rng = np.random.default_rng(3)
for k in ["a1","a2","a3","a4","a5"]:
    im = cv2.imread(f"img/promo/{k}.png"); im = cv2.resize(im, (1080, 1620), interpolation=cv2.INTER_AREA)
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.
    g = cv2.bilateralFilter(g, 7, .08, 5)
    s1, s2 = 1.4, 2.4
    d = cv2.GaussianBlur(g, (0, 0), s1) - 0.985 * cv2.GaussianBlur(g, (0, 0), s2)
    e = 1 - np.tanh(np.clip(d, -1, 1) * 40)            # 0 白 ~ 2 黑
    e = np.clip((e - 0.7) / 0.9, 0, 1)                 # 門檻
    # 去碎點
    m = (e > .35).astype(np.uint8); n, lab, st, _ = cv2.connectedComponentsWithStats(m, connectivity=8)
    keep = np.zeros(n, bool); keep[1:] = st[1:, cv2.CC_STAT_AREA] >= 28; e = e * keep[lab]
    # 筆壓濃淡：低頻雜訊
    pr = cv2.GaussianBlur(rng.random((1620, 1080)).astype(np.float32), (0, 0), 30); pr = .78 + .22 * (pr - pr.min()) / (pr.max() - pr.min())
    a = np.clip(e * pr, 0, 1); a = cv2.GaussianBlur(a, (0, 0), .6)
    rgba = np.zeros((1620, 1080, 4), np.uint8); rgba[..., 0] = 0x22; rgba[..., 1] = 0x26; rgba[..., 2] = 0x2c; rgba[..., 3] = (a * 255).astype(np.uint8)
    cv2.imwrite(f"img/promo/{k}_lines.png", rgba); print(k, round(float((a > .25).mean() * 100), 1), "% 線")
