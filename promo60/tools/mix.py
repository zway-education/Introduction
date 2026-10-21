# 疊配樂（warm）＋每次換場的鉛筆聲，整體調到 -16 LUFS：python3 tools/mix.py 影格資料夾 pencil.json 輸出.mp4
import json,subprocess,sys
fr,pj,out=sys.argv[1:4]; A="/home/user/Introduction/promo60/audio"; P=json.load(open(pj))
ins=["-framerate","30","-i",f"{fr}/f_%05d.jpg","-i",f"{A}/"+__import__("os").environ.get("MUSIC","reelpool_warm.mp3")+""]
fc="[1:a]atrim=0:60,asetpts=N/SR/TB,volume=0.6,afade=t=in:d=1,afade=t=out:st=57:d=3[m];"
for k,t in enumerate(P):
    ins+=["-i",f"{A}/promo_pencil.wav"]; fc+=f"[{k+2}:a]volume=0.8,adelay={int(t*1000)}|{int(t*1000)}[p{k}];"
fc+="[m]"+"".join(f"[p{k}]" for k in range(len(P)))+f"amix=inputs={len(P)+1}:normalize=0,atrim=0:60[mx];[mx]loudnorm=I=-16:TP=-1.5:LRA=11[a]"
subprocess.run(["ffmpeg","-y","-loglevel","error",*ins,"-filter_complex",fc,"-map","0:v","-map","[a]","-c:v","libx264","-pix_fmt","yuv420p","-crf","19","-preset","medium","-c:a","aac","-b:a","192k","-ar","48000","-t","60","-movflags","+faststart",out],check=True)
# 第二次：量實際響度，補差到 -16 LUFS（只重編音軌）
import re, os, shutil
m = subprocess.run(["ffmpeg","-hide_banner","-nostats","-i",out,"-af","ebur128","-f","null","-"],capture_output=True,text=True).stderr
I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", m)[-1]); g = -16 - I
if abs(g) > .3:
    tmp = out + ".tmp.mp4"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",out,"-c:v","copy","-af",f"volume={g:.2f}dB,alimiter=limit=0.84:level=false","-c:a","aac","-b:a","192k",tmp],check=True); shutil.move(tmp, out)
print("響度", I, "→ 補", round(g, 2), "dB")
