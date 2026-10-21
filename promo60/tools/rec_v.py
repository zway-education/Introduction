# 直式逐格錄影：python rec_v.py 頁面名 起秒 迄秒 配樂(或none) 輸出.mp4（需要本機伺服器 http://localhost:8766）
import sys, pathlib, asyncio, subprocess, tempfile, shutil
from playwright.async_api import async_playwright
page, t0, t1, music, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4], pathlib.Path(sys.argv[5])
Q = ("&" + sys.argv[6]) if len(sys.argv) > 6 else ""
FPS = 30; N = int(round((t1 - t0) * FPS))
async def main(tmp):
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome", args=["--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist"])
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.goto(f"http://localhost:8766/{page}.html?rec=1{Q}", timeout=120000)
        await pg.wait_for_function("window.__ready === true", timeout=180000)
        await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(500)
        for i in range(N):
            await pg.evaluate("t=>window.__render(t)", t0 + i / FPS)
            await pg.screenshot(path=str(tmp / f"f_{i:05d}.jpg"), type="jpeg", quality=95)
            if (i + 1) % 300 == 0: print(f"{i+1}/{N}", flush=True)
        await b.close()
tmp = pathlib.Path(tempfile.mkdtemp(prefix=f"trf_{page}_"))
try:
    asyncio.run(main(tmp))
    dur = N / FPS
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(tmp / "f_%05d.jpg")]
    if music != "none":
        cmd += ["-i", music, "-filter_complex", f"[1:a]volume=0.55,afade=t=in:d=1,afade=t=out:st={max(0, dur-2.5):.2f}:d=2.5[a]", "-map", "0:v", "-map", "[a]", "-c:a", "aac", "-b:a", "160k"]
    cmd += ["-t", f"{dur:.2f}", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True); print("輸出", out)
finally:
    shutil.rmtree(tmp, ignore_errors=True)
