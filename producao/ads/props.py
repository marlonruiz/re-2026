import json,copy
W=lambda n: json.load(open(f'/root/ads/av/words{n}.json'))
def fix(words,rep):
    out=[]
    for w in words:
        t=w['t']
        if t in rep:
            r=rep[t]
            if isinstance(r,list):
                d=(w['e']-w['s'])/len(r)
                for i,x in enumerate(r): out.append({'t':x,'s':round(w['s']+i*d,2),'e':round(w['s']+(i+1)*d,2)})
                continue
            t=r
        out.append({**w,'t':t})
    return out
def sfx_for(trans, hook_at=0, slams=(), outro=None, badges=()):
    s=[{'file':'pop','at':hook_at,'vol':0.4}]
    s+= [{'file':'whoosh','at':max(0,t-0.15),'vol':0.4} for t in trans]
    s+= [{'file':'impact','at':t,'vol':0.5} for t in slams]
    s+= [{'file':'pop','at':t,'vol':0.45} for t in badges]
    if outro: s.append({'file':'ding','at':outro,'vol':0.45})
    return s
ADS={
 'A':dict(dur=20.48,rep={'para':'Para','Shopify,':'Shopee,','Toquem':['Toca','em'],'saiba':'Saiba','mais':'Mais'},
   emph=['graça','shopee','recebe','celular','mais'],
   hook={'kicker':'VOCÊ FAZ ISSO?','lines':['Para de mandar','*link de graça!*'],'dur':2.3},
   broll=[('lojas',7.67,4.43),('sem',12.1,5.33)],
   zooms=[{'at':0,'scale':1.0,'y':0.35},{'at':2.4,'scale':1.13,'y':0.35},{'at':5.9,'scale':1.0,'y':0.35},{'at':17.43,'scale':1.06,'y':0.35},{'at':18.6,'scale':1.14,'y':0.35}],
   callouts=[{'kind':'badge','at':3.9,'dur':1.7,'top':'TODO DIA ALGUÉM PERGUNTA','big':'“Onde você comprou?”'},
             {'kind':'slam','at':12.14,'dur':1.9,'top':'CADA COMPRA','big':'VOCÊ\nRECEBE'}],
   outro_line='Toque em Saiba mais'),
 'B':dict(dur=22.16,rep={'Chopi':'Shopee'},
   emph=['sabe','shopee','revenda','nada','recebe','simples'],
   hook={'kicker':'🤫 SEGREDO','lines':['Pouca gente','*sabe disso...*'],'dur':2.0},
   broll=[('lojas',4.72,2.83),('sem',7.55,4.5),('conversas',12.05,4.75)],
   zooms=[{'at':0,'scale':1.05,'y':0.35},{'at':1.9,'scale':1.16,'y':0.35},{'at':16.8,'scale':1.0,'y':0.35},{'at':20.9,'scale':1.12,'y':0.35}],
   callouts=[{'kind':'slam','at':14.7,'dur':1.9,'top':'E RECEBE POR','big':'CADA\nCOMPRA'}],
   outro_line='Toque aqui embaixo'),
 'C':dict(dur=22.72,rep={'Mais!':'Mais!'},
   emph=['black','friday','natal','barato','link','celular','agora'],
   hook={'kicker':'BLACK FRIDAY · NATAL','lines':['Todo mundo vai','*te pedir indicação*'],'dur':2.9},
   broll=[('conversas',5.99,5.28),('sem',14.72,3.88)],
   zooms=[{'at':0,'scale':1.0,'y':0.35},{'at':3.0,'scale':1.12,'y':0.35},{'at':11.27,'scale':1.05,'y':0.35},{'at':12.6,'scale':1.16,'y':0.35},{'at':18.6,'scale':1.0,'y':0.35},{'at':20.1,'scale':1.12,'y':0.35}],
   callouts=[{'kind':'badge','at':0.6,'dur':1.8,'top':'FALTA POUCO','big':'27/11 · 25/12'},
             {'kind':'badge','at':12.62,'dur':1.9,'top':'A PERGUNTA É','big':'Pelo SEU link?'}],
   outro_line='Toque em Saiba mais'),
}
for n,a in ADS.items():
    words=fix(W(n),a['rep'])
    tot=round(a['dur']+1.6,2)
    trans=[b[1] for b in a['broll']]+[b[1]+b[2] for b in a['broll']]
    p={'duration':tot,'captionsY':1440,'emph':a['emph'],
       'main':{'src':f'ads/main{n}.mp4','zooms':a['zooms']},
       'broll':[{'src':f'assets/cena-{s}.png','at':at,'dur':d} for s,at,d in a['broll']],
       'callouts':a['callouts'],
       'sfx':sfx_for(trans,slams=[c['at'] for c in a['callouts'] if c['kind']=='slam'],badges=[c['at'] for c in a['callouts'] if c['kind']=='badge'],outro=a['dur']),
       'hook':a['hook'],'tag':'CLUBE DE ACHADINHOS','tagFrom':a['hook']['dur'],
       'outro':{'at':a['dur'],'logo':'assets/logo-outro.png','line':a['outro_line']},
       'words':words}
    json.dump(p,open(f'/root/motion/props/ad{n}.json','w'),ensure_ascii=False)
    print(n,tot,' '.join(w['t'] for w in words))
