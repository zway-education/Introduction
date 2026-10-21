# 轉場「用畫的」順序圖：線稿每一筆（連通的線段）依手畫順序出現；上色依畫筆一道一道的順序出現
import cv2, numpy as np
rng = np.random.default_rng(5)
H, W = 1620, 1080
# 上色順序：一道約 110px 高的橫筆，蛇行左右來回，邊緣帶一點雜訊
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
noise = cv2.GaussianBlur(rng.random((H, W)).astype(np.float32), (0, 0), 18); noise = (noise - noise.min()) / (noise.max() - noise.min())
band = np.floor((yy + (noise - .5) * 70) / 110); nb = band.max() + 1
xfrac = np.where(band % 2 == 0, xx / W, 1 - xx / W)
paint = (band + xfrac * .92) / nb; paint = np.clip(paint, 0, 1)
cv2.imwrite("img/promo/paint_order.png", (paint * 255).astype(np.uint8))
for k in ["a1", "a2", "a3", "a4", "a5"]:
    a = cv2.imread(f"img/promo/{k}_lines.png", cv2.IMREAD_UNCHANGED)[..., 3]
    m = (a > 40).astype(np.uint8)
    n, lab, stats, cent = cv2.connectedComponentsWithStats(m, connectivity=8)
    # 手畫順序：大致由上往下、每 160px 一列內由左到右（蛇行），大筆先畫、小碎點後補
    order = np.full(n, 1.0, np.float32)
    row = np.floor(cent[1:, 1] / 160); x = cent[1:, 0] / W; x = np.where(row % 2 == 0, x, 1 - x)
    key = row + x * .9 + rng.random(n - 1) * .25
    big = stats[1:, cv2.CC_STAT_AREA] >= 60
    key = np.where(big, key, key + 1.5)   # 小碎點最後補
    rank = np.argsort(np.argsort(key)); order[1:] = rank / max(1, n - 2)
    # 每一筆自己也要從一端畫到另一端：用該筆外框內的對角線進度
    om = order[lab].astype(np.float32)
    x0 = stats[:, cv2.CC_STAT_LEFT][lab]; y0 = stats[:, cv2.CC_STAT_TOP][lab]; w = np.maximum(1, stats[:, cv2.CC_STAT_WIDTH][lab]); h = np.maximum(1, stats[:, cv2.CC_STAT_HEIGHT][lab])
    prog = ((xx - x0) / w + (yy - y0) / h) / 2
    om = om + prog * (1.0 / max(1, n - 1)) * 1.6; om[lab == 0] = 1.0
    cv2.imwrite(f"img/promo/{k}_order.png", (np.clip(om, 0, 1) * 254).astype(np.uint8)); print(k, n, "筆")
