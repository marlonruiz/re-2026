import React from 'react';
import {AbsoluteFill, OffthreadVideo, Audio, Img, Sequence, staticFile, useCurrentFrame, useVideoConfig, interpolate, spring, Easing, random} from 'remotion';
import '@fontsource/montserrat/700.css';
import '@fontsource/montserrat/800.css';
import '@fontsource/montserrat/900.css';

// Paleta Clube de Achadinhos (laranja / creme / amarelo)
const C = {bg: '#180E0A', blue: '#E8572A', cyan: '#FFC94D', silver: '#FFE9DC', white: '#FFFFFF', green: '#22C55E'};
const FONT = 'Montserrat, "Noto Color Emoji", sans-serif';
type Word = {t: string; s: number; e: number};
type Zoom = {at: number; scale: number; x?: number; y?: number};
type Broll = {src: string; srcStart?: number; at: number; dur: number};
type Callout = {at: number; dur: number; kind?: 'slam' | 'count' | 'badge'; top?: string; big: string; sub?: string; countTo?: number; prefix?: string; suffix?: string; color?: string};
type Sfx = {file: string; at: number; vol?: number};
export type CriativoProps = {
  duration: number;
  main: {src: string; zooms?: Zoom[]; volume?: number};
  outro?: {at: number; logo: string; line?: string}; broll?: Broll[]; words: Word[]; emph?: string[];
  hook?: {lines: string[]; dur: number; kicker?: string}; tag?: string; tagFrom?: number; callouts?: Callout[]; sfx?: Sfx[];
  captionsY?: number; music?: {src: string; vol: number}; disclaimer?: string;
};

const Background: React.FC = () => {
  const f = useCurrentFrame(); const off = (f * 0.6) % 80;
  return (<AbsoluteFill>
    <Img src={staticFile('assets/bg.png')} style={{position: 'absolute', width: 1080, height: 1920}} />
    <Img src={staticFile('assets/grid.png')} style={{position: 'absolute', width: 1080, height: 2000, top: -80, transform: `translateY(${off}px)`}} />
  </AbsoluteFill>);
};

function zoomAt(zooms: Zoom[] | undefined, frame: number, fps: number) {
  if (!zooms || zooms.length === 0) return {scale: 1, x: 0.5, y: 0.5};
  const t = frame / fps; let i = -1;
  for (let k = 0; k < zooms.length; k++) if (zooms[k].at <= t) i = k;
  if (i < 0) return {scale: zooms[0].scale, x: zooms[0].x ?? 0.5, y: zooms[0].y ?? 0.5};
  const cur = zooms[i]; const prev = i > 0 ? zooms[i - 1] : cur;
  const p = spring({frame: frame - Math.round(cur.at * fps), fps, config: {damping: 18, stiffness: 180}});
  const lerp = (a: number, b: number) => a + (b - a) * p;
  const drift = 1 + 0.012 * Math.sin(frame / 40);
  return {scale: lerp(prev.scale, cur.scale) * drift, x: lerp(prev.x ?? 0.5, cur.x ?? 0.5), y: lerp(prev.y ?? 0.5, cur.y ?? 0.5)};
}

const Main: React.FC<{p: CriativoProps}> = ({p}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig(); const z = zoomAt(p.main.zooms, f, fps);
  return (<AbsoluteFill style={{overflow: 'hidden'}}>
    <AbsoluteFill style={{transform: `scale(${z.scale})`, transformOrigin: `${z.x * 100}% ${z.y * 100}%`}}>
      <OffthreadVideo src={staticFile(p.main.src)} volume={p.main.volume ?? 1} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
    </AbsoluteFill>
    <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0.2) 16%, rgba(0,0,0,0) 28%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.65) 100%)'}} />
  </AbsoluteFill>);
};

// Cena gráfica (PNG transparente) sobre o fundo animado
const Scene: React.FC<{b: Broll}> = ({b}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig(); const durF = Math.round(b.dur * fps);
  const inP = spring({frame: f, fps, config: {damping: 15, stiffness: 150}});
  const outP = interpolate(f, [durF - 6, durF], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const kb = interpolate(f, [0, durF], [1.0, 1.06]);
  const float = Math.sin(f / 18) * 6;
  return (<AbsoluteFill style={{opacity: 1 - outP}}>
    <AbsoluteFill style={{transform: `translateY(${(1 - inP) * 1920}px)`}}><Background /></AbsoluteFill>
    <AbsoluteFill style={{transform: `translateY(${(1 - inP) * 300 + float}px) scale(${(0.85 + 0.15 * inP) * kb})`, opacity: inP}}>
      <Img src={staticFile(b.src)} style={{width: 1080, height: 1920}} />
    </AbsoluteFill>
  </AbsoluteFill>);
};

const Rich: React.FC<{text: string; reveal: number; base: React.CSSProperties}> = ({text, reveal, base}) => {
  const parts = text.split(/(\*[^*]+\*)/g).filter(Boolean); let wi = 0;
  return (<span style={base}>{parts.map((part, i) => {
    const em = part.startsWith('*'); const clean = em ? part.slice(1, -1) : part;
    return clean.split(/(\s+)/).map((w, j) => {
      if (/^\s+$/.test(w)) return <span key={`${i}-${j}`}>{w}</span>;
      const k = wi++; const p = Math.max(0, Math.min(1, reveal - k * 0.6));
      return (<span key={`${i}-${j}`} style={{display: 'inline-block', opacity: p, transform: `translateY(${(1 - p) * 40}px) scale(${0.7 + 0.3 * p})`,
        ...(em ? {background: C.blue, color: C.white, padding: '0 14px', borderRadius: 12, boxShadow: `0 0 20px ${C.blue}`, margin: '0 2px'} : {})}}>{w}</span>);
    });
  })}</span>);
};

const Hook: React.FC<{hook: NonNullable<CriativoProps['hook']>}> = ({hook}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig(); const durF = Math.round(hook.dur * fps);
  const out = interpolate(f, [durF - 8, durF], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (<AbsoluteFill style={{alignItems: 'center', paddingTop: 150, opacity: 1 - out, transform: `translateY(${-out * 60}px)`}}>
    {hook.kicker && <div style={{fontFamily: FONT, fontWeight: 800, fontSize: 34, color: C.cyan, letterSpacing: 6, marginBottom: 18, textShadow: '0 3px 0 #000',
      opacity: interpolate(f, [0, 8], [0, 1], {extrapolateRight: 'clamp'})}}>{hook.kicker}</div>}
    <div style={{width: 960, textAlign: 'center', display: 'flex', flexDirection: 'column', gap: 10}}>
      {hook.lines.map((l, i) => (<div key={i}><Rich text={l} reveal={f / 2.2 - i * 2} base={{fontFamily: FONT, fontWeight: 900, fontSize: 74, lineHeight: 1.12, color: C.white,
        textShadow: '0 5px 0 #000', textTransform: 'uppercase'}} /></div>))}
    </div>
  </AbsoluteFill>);
};

const Tag: React.FC<{text: string}> = ({text}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig(); const p = spring({frame: f, fps, config: {damping: 14}});
  return (<div style={{position: 'absolute', top: 120, width: '100%', display: 'flex', justifyContent: 'center', transform: `scale(${p})`}}>
    <div style={{padding: '12px 28px', borderRadius: 999, background: 'rgba(24,14,10,0.8)', border: `2px solid rgba(255,201,77,0.7)`,
      fontFamily: FONT, fontWeight: 800, fontSize: 30, color: C.silver, letterSpacing: 2, boxShadow: '0 0 40px rgba(232,87,42,0.45)'}}>
      <span style={{display: 'inline-block', width: 16, height: 16, borderRadius: 8, background: C.green, marginRight: 14, opacity: 0.5 + 0.5 * Math.sin(f / 5)}} />{text}
    </div>
  </div>);
};

type Chunk = {words: Word[]; s: number; e: number};
function chunkWords(words: Word[]): Chunk[] {
  const out: Chunk[] = []; let cur: Word[] = [];
  const flush = () => { if (cur.length) { out.push({words: cur, s: cur[0].s, e: cur[cur.length - 1].e}); cur = []; } };
  for (const w of words) {
    const prev = cur[cur.length - 1]; const chars = cur.reduce((a, x) => a + x.t.length + 1, 0) + w.t.length;
    if (cur.length && (cur.length >= 3 || chars > 17 || (prev && w.s - prev.e > 0.3))) flush();
    cur.push(w); if (/[.,!?;:]$/.test(w.t) && cur.length >= 2) flush();
  }
  flush();
  for (let i = 0; i < out.length - 1; i++) if (out[i + 1].s - out[i].e < 0.6) out[i].e = out[i + 1].s;
  return out;
}

const Captions: React.FC<{p: CriativoProps; hidden: (t: number) => boolean}> = ({p, hidden}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig(); const t = f / fps;
  const chunks = React.useMemo(() => chunkWords(p.words), [p.words]);
  const emph = (p.emph || []).map((x) => x.toLowerCase());
  const ch = chunks.find((c) => t >= c.s && t < c.e + 0.05);
  if (!ch || hidden(t)) return null;
  const pop = spring({frame: f - Math.round(ch.s * fps), fps, config: {damping: 11, stiffness: 260, mass: 0.6}});
  const total = ch.words.reduce((a, w) => a + w.t.length + 1, 0); const fs = total > 15 ? 70 : total > 11 ? 78 : 86;
  const strip = (s: string) => s.toLowerCase().replace(/[.,!?;:"“”]/g, '');
  return (<div style={{position: 'absolute', top: p.captionsY ?? 1440, width: '100%', display: 'flex', justifyContent: 'center'}}>
    <div style={{width: 1000, textAlign: 'center', transform: `scale(${0.75 + 0.25 * pop}) rotate(${(1 - pop) * -3}deg)`}}>
      {ch.words.map((w, i) => {
        const active = t >= w.s - 0.02 && t < (ch.words[i + 1]?.s ?? ch.e + 1);
        const isEm = emph.some((e) => strip(w.t).includes(e)) || /\d/.test(w.t);
        const wp = spring({frame: f - Math.round(w.s * fps), fps, config: {damping: 10, stiffness: 300, mass: 0.5}});
        return (<span key={i} style={{display: 'inline-block', margin: '0 18px', fontFamily: FONT, fontWeight: 900, fontSize: isEm ? fs * 1.12 : fs,
          textTransform: 'uppercase', color: isEm ? C.cyan : active ? C.white : C.silver, lineHeight: 1.1, transform: `scale(${active ? 1 + 0.12 * wp : 1})`,
          WebkitTextStroke: '3px #000', paintOrder: 'stroke fill', textShadow: active ? `0 0 16px ${C.blue}, 0 7px 0 #000` : '0 7px 0 #000',
          opacity: t >= w.s - 0.05 ? 1 : 0.35}}>{w.t.replace(/[,;:]$/, '')}</span>);
      })}
    </div>
  </div>);
};

const CalloutView: React.FC<{c: Callout}> = ({c}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig(); const durF = Math.round(c.dur * fps);
  const p = spring({frame: f, fps, config: {damping: 9, stiffness: 200, mass: 0.7}});
  const out = interpolate(f, [durF - 6, durF], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const shake = f < 10 ? (random(`s${f}`) - 0.5) * 22 * (1 - f / 10) : 0;
  const flash = interpolate(f, [0, 2, 8], [0, 0.55, 0], {extrapolateRight: 'clamp'});
  let big = c.big;
  if (c.kind === 'count' && c.countTo != null) {
    const cp = interpolate(f, [0, Math.min(durF * 0.55, 30)], [0, 1], {extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
    big = `${c.prefix || ''}${Math.round(c.countTo * cp).toLocaleString('pt-BR')}${c.suffix || ''}`;
  }
  if (c.kind === 'badge') {
    return (<AbsoluteFill style={{alignItems: 'center', justifyContent: 'flex-start', paddingTop: 300, opacity: 1 - out}}>
      <div style={{transform: `scale(${p}) rotate(${-4 + (1 - p) * -10}deg)`, background: C.blue, padding: '22px 44px', borderRadius: 22, boxShadow: `0 0 30px ${C.blue}, 0 14px 0 #6b2310`, textAlign: 'center'}}>
        {c.top && <div style={{fontFamily: FONT, fontWeight: 800, fontSize: 34, color: '#FFE2D3', letterSpacing: 3}}>{c.top}</div>}
        <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 92, color: C.white, lineHeight: 1}}>{big}</div>
        {c.sub && <div style={{fontFamily: FONT, fontWeight: 800, fontSize: 34, color: '#FFE2D3', marginTop: 6}}>{c.sub}</div>}
      </div>
    </AbsoluteFill>);
  }
  const maxLen = Math.max(...big.split('\n').map((l) => l.length));
  return (<AbsoluteFill style={{opacity: 1 - out}}>
    <AbsoluteFill style={{background: 'rgba(24,14,10,0.82)'}} />
    <AbsoluteFill style={{background: `radial-gradient(circle at 50% 48%, rgba(232,87,42,${0.6 * p}), transparent 55%)`}} />
    <AbsoluteFill style={{background: C.white, opacity: flash}} />
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', transform: `translate(${shake}px, ${shake * 0.6}px)`}}>
      <div style={{textAlign: 'center', width: 1000}}>
        {c.top && <div style={{fontFamily: FONT, fontWeight: 800, fontSize: 46, color: C.cyan, letterSpacing: 4, marginBottom: 14, opacity: p}}>{c.top}</div>}
        <div style={{fontFamily: FONT, fontWeight: 900, fontSize: Math.min(170, Math.floor(980 / (maxLen * 0.6))), lineHeight: 1.0, color: c.color || C.white, whiteSpace: 'pre-line',
          transform: `scale(${interpolate(p, [0, 1], [2.4, 1])})`, textTransform: 'uppercase', textShadow: `0 0 24px ${C.blue}, 0 10px 0 #000`, WebkitTextStroke: '3px #000', paintOrder: 'stroke fill'}}>{big}</div>
        {c.sub && <div style={{fontFamily: FONT, fontWeight: 800, fontSize: 50, color: C.silver, marginTop: 24, textTransform: 'uppercase',
          opacity: interpolate(f, [6, 14], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}}>{c.sub}</div>}
      </div>
    </AbsoluteFill>
  </AbsoluteFill>);
};

const Progress: React.FC<{dur: number}> = ({dur}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  return <div style={{position: 'absolute', top: 0, left: 0, height: 12, width: `${(f / (dur * fps)) * 100}%`, background: `linear-gradient(90deg, ${C.blue}, ${C.cyan})`, boxShadow: `0 0 20px ${C.cyan}`}} />;
};

const Outro: React.FC<{o: NonNullable<CriativoProps['outro']>}> = ({o}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig(); const p = spring({frame: f, fps, config: {damping: 14}});
  const bounce = Math.abs(Math.sin(f / 6)) * 18;
  return (<AbsoluteFill style={{opacity: interpolate(f, [0, 6], [0, 1], {extrapolateRight: 'clamp'})}}>
    <Background />
    <AbsoluteFill style={{background: `radial-gradient(circle at 50% 46%, rgba(232,87,42,${0.45 * p}), transparent 50%)`}} />
    <AbsoluteFill style={{transform: `scale(${0.6 + 0.4 * p}) translateY(-160px)`, opacity: p}}><Img src={staticFile(o.logo)} style={{width: 1080, height: 1920}} /></AbsoluteFill>
    {o.line && <div style={{position: 'absolute', top: 1260, width: '100%', textAlign: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 60, color: C.white,
      textTransform: 'uppercase', textShadow: '0 6px 0 #000'}}>{o.line}<div style={{fontSize: 110, transform: `translateY(${bounce}px)`}}>👇</div></div>}
  </AbsoluteFill>);
};

export const Criativo: React.FC<CriativoProps> = (p) => {
  const {fps} = useVideoConfig(); const callouts = p.callouts || [];
  const slamAt = (t: number) => callouts.some((c) => (c.kind ?? 'slam') !== 'badge' && t >= c.at && t < c.at + c.dur);
  const hookDur = p.hook?.dur ?? 0;
  return (<AbsoluteFill style={{background: C.bg}}>
    <Background />
    <Main p={p} />
    {(p.broll || []).map((b, i) => <Sequence key={`b${i}`} from={Math.round(b.at * fps)} durationInFrames={Math.round(b.dur * fps)}><Scene b={b} /></Sequence>)}
    {p.tag && <Sequence from={Math.round((p.tagFrom ?? hookDur) * fps)}><Tag text={p.tag} /></Sequence>}
    {p.hook && <Sequence durationInFrames={Math.round(p.hook.dur * fps)}><Hook hook={p.hook} /></Sequence>}
    <Captions p={p} hidden={slamAt} />
    {callouts.map((c, i) => <Sequence key={`c${i}`} from={Math.round(c.at * fps)} durationInFrames={Math.round(c.dur * fps)}><CalloutView c={c} /></Sequence>)}
    {(p.sfx || []).map((s, i) => <Sequence key={`s${i}`} from={Math.max(0, Math.round(s.at * fps))}><Audio src={staticFile(`sfx/${s.file}.wav`)} volume={s.vol ?? 0.5} /></Sequence>)}
    {p.music && <Audio src={staticFile(p.music.src)} volume={p.music.vol} loop />}
    {p.outro && <Sequence from={Math.round(p.outro.at * fps)}><Outro o={p.outro} /></Sequence>}
    {p.disclaimer && <div style={{position: 'absolute', bottom: 40, width: '100%', textAlign: 'center', fontFamily: FONT, fontWeight: 700, fontSize: 24, color: 'rgba(255,233,220,0.7)'}}>{p.disclaimer}</div>}
    <Progress dur={p.duration} />
  </AbsoluteFill>);
};
