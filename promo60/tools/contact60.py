# 檢查用：線稿 PNG（alpha）疊在白底上，縮到寬 216，五張橫排成一張 jpg
import cv2, numpy as np
tiles = []
for k in ["a1", "a2", "a3", "a4", "a5"]:
    rgba = cv2.imread(f"img/promo/{k}_lines.png", cv2.IMREAD_UNCHANGED)
    a = rgba[..., 3:4].astype(np.float32) / 255.
    bgr = rgba[..., :3].astype(np.float32)
    out = (bgr * a + 255 * (1 - a)).astype(np.uint8)
    h = round(out.shape[0] * 216 / out.shape[1])
    tiles.append(cv2.resize(out, (216, h), interpolation=cv2.INTER_AREA))
sheet = np.hstack(tiles)
cv2.imwrite("tools/check_lines.jpg", sheet, [cv2.IMWRITE_JPEG_QUALITY, 90])
print(sheet.shape)
