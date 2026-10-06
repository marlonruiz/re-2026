import json,subprocess,sys
n=sys.argv[1]
segs=json.load(open('/root/ads/av/segs.json'))
still={'A':'a2','B':'b1','C':'c2'}[n]
dur={'A':20.48,'B':22.16,'C':22.72}[n]+1.6
clips=[(k.replace('seg','').replace('.mp3',''),s,e) for k,(s,e) in segs.items() if k.startswith(f'seg{n}_')]
inp=['-loop','1','-t',str(dur),'-i',f'/root/ads/av/{still}.png']
for c,_,_ in clips: inp+=['-i',f'/root/ads/clips/{c}.mp4']
inp+=['-i',f'/root/ads/av/voz{n}.mp3']
cover='scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1'
fc=[f'[0:v]{cover}[b0]']; last='b0'
for i,(c,s,e) in enumerate(clips,1):
    fc.append(f'[{i}:v]{cover},trim=0:{e-s:.3f},setpts=PTS-STARTPTS+{s}/TB[c{i}]')
    fc.append(f"[{last}][c{i}]overlay=eof_action=pass:enable='between(t,{s},{e})'[b{i}]"); last=f'b{i}'
a=len(clips)+1
fc.append(f'[{a}:a]apad,atrim=0:{dur}[a]')
cmd=['ffmpeg','-v','error','-y',*inp,'-filter_complex',';'.join(fc),'-map',f'[{last}]','-map','[a]','-t',str(dur),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',f'/root/motion/public/ads/main{n}.mp4']
subprocess.run(cmd,check=True); print('ok',n,clips)
