# 宣傳片主圖的深度估計（Depth Anything V2 small，onnx）：輸出 img/promo/aN_d.png（越亮越靠近鏡頭）
import numpy as np, onnxruntime as ort
from PIL import Image, ImageFilter
sess = ort.InferenceSession("models_dl/depth_anything_v2_small.onnx", providers=["CPUExecutionProvider"])
inp = sess.get_inputs()[0]; print(inp.name, inp.shape)
S = 518
for k in ["a1", "a2", "a3", "a4", "a5"]:
    im = Image.open(f"img/promo/{k}.png").convert("RGB")
    x = np.asarray(im.resize((S, S), Image.BICUBIC)).astype(np.float32) / 255.
    x = (x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    x = x.transpose(2, 0, 1)[None].astype(np.float32)
    d = sess.run(None, {inp.name: x})[0].squeeze()
    d = (d - d.min()) / (d.max() - d.min() + 1e-6)
    out = Image.fromarray((d * 255).astype(np.uint8), "L").resize((1080, 1620), Image.BICUBIC).filter(ImageFilter.GaussianBlur(2))
    out.save(f"img/promo/{k}_d.png"); print(k, "ok", float(d.mean()))
