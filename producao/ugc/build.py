import json,subprocess,sys
n=sys.argv[1]
props=json.load(open(f'/root/motion/props/ad{n}.json'))
words=props['words']; dur={'A':20.48,'B':22.16,'C':22.72}[n]
order={'A':[('A_hook',0,7.67),('A_mid',7.67,17.43),('A_cta',17.43,20.48)],
       'B':[('B_hook',0,4.72),('B_mid',4.72,16.8),('B_cta',16.8,22.16)],
       'C':[('C_hook',0,5.99),('C_mid1',5.99,11.27),('C_perg',11.27,14.72),('C_mid2',14.72,18.6),('C_cta',18.6,22.72)]}[n]
# jump cuts: sub-split long clips at sentence ends, alternate zoom
ends=[w['e'] for w in words if w['t'][-1] in '.!?,']
pieces=[]
for c,s,e in order:
    cuts=[s]+[t for t in ends if s+2.2<t<e-1.6]
    # keep cuts at least 2.2s apart
    cc=[cuts[0]]
    for t in cuts[1:]:
        if t-cc[-1]>=2.2: cc.append(t)
    cc.append(e)
    for a,b in zip(cc,cc[1:]): pieces.append((c,s,a,b))
fc=[];inp=[]
for i,(c,s,a,b) in enumerate(pieces):
    z=[1.0,1.12,1.05,1.16][i%4]
    inp+=['-i',f'/root/ads/clips/{c}.mp4']
    w=int(1080*z)//2*2; h=int(1920*z)//2*2
    fc.append(f'[{i}:v]trim={a-s:.3f}:{b-s:.3f},setpts=PTS-STARTPTS,scale={w}:{h}:force_original_aspect_ratio=increase,crop=1080:1920:(iw-1080)/2:(ih-1920)*0.3,fps=30,setsar=1[v{i}]')
fc.append(''.join(f'[v{i}]' for i in range(len(pieces)))+f'concat=n={len(pieces)}:v=1:a=0[cat]')
# captions ASS
def ts(t): h=int(t//3600); m=int(t%3600//60); s=t%60; return f'{h}:{m:02d}:{s:05.2f}'
chunks=[];cur=[]
for w in words:
    cur.append(w)
    if len(cur)>=3 or w['t'][-1] in '.!?,': chunks.append(cur); cur=[]
if cur: chunks.append(cur)
ass=['[Script Info]','PlayResX: 1080','PlayResY: 1920','','[V4+ Styles]',
 'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
 'Style: C,Poppins,88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,6,2,2,60,60,560,1','','[Events]','Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
for i,ch in enumerate(chunks):
    st=ch[0]['s']; en=chunks[i+1][0]['s'] if i+1<len(chunks) else dur
    en=min(en,ch[-1]['e']+0.6)
    txt=' '.join(w['t'].strip('.,') for w in ch).lower() if False else ' '.join(w['t'].rstrip(',.') for w in ch)
    ass.append(f'Dialogue: 0,{ts(st)},{ts(en)},C,,0,0,0,,{{\\fscx88\\fscy88\\t(0,90,\\fscx100\\fscy100)}}{txt}')
open(f'/root/ads/ugc/cap{n}.ass','w').write('\n'.join(ass))
k=len(pieces)
inp+=['-loop','1','-i',f'/root/ads/ugc/head{n}.png','-i',f'/root/ads/av/voz{n}.mp3']
fc.append(f'[cat]ass=/root/ads/ugc/cap{n}.ass[cap]')
fc.append(f'[cap][{k}:v]overlay=0:0:shortest=1[vo]')
cmd=['ffmpeg','-v','error','-y',*inp,'-filter_complex',';'.join(fc),'-map','[vo]','-map',f'{k+1}:a','-t',str(dur),
     '-s','720x1280','-c:v','libx264','-crf','21','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k',f'/root/ads/ugc/UGC_{n}.mp4']
subprocess.run(cmd,check=True); print('ok',n,len(pieces),[(round(a,2),round(b,2)) for _,_,a,b in pieces])
