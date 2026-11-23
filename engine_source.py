# tiny-chess-01 engine: 0x88 board, negamax + quiescence, PST eval, embedded opening book.
# Readable source of the entry; main.py is produced from this file by the kit's own compress.
import json as j,os,sys,urllib.request as u,base64 as b,zlib as z
V=[0,100,320,330,500,900,0]
P=bytes(x for v in b.b85decode('h=}g)nXH+ch>DkZnU;u%BSbccNSaBiNUBMiHi;udXLoprc$s;bc$s;bd5C9sh=`e)c!+q2c!+q2c!-FJXLoprc$s*ah?#krc$jB*Lo!1$Lo!1$WJ7jls)($Z') for x in (v//16*8,v%16*8))
E=[[0]*128 for _ in range(13)]
for c in range(1,7):
 t=(c-1)*32
 for s in range(128):
  if s&136:continue
  f=s&7;r=s>>4;m=f if f<4 else 7-f
  E[c][s]=V[c]+P[t+(7-r)*4+m]-64;E[c+6][s]=-V[c]-P[t+r*4+m]+64
KN=(-33,-31,-18,-14,14,18,31,33);KD=(-17,-16,-15,-1,1,15,16,17);BD=(-17,-15,15,17);RD=(-16,-1,1,16)
M=100000;F=M*10
B=bytearray(128);L=[];I=[-1]*128;W=True;CR=0;EP=-1;KW=4;KB=116;EV=0;U=[];N=0;BM=[0];LM=150000
A=type('A',(Exception,),{})
a=int.from_bytes(b.b85decode('9|I;UqYwhXLwp4Q1Xt6ofzyyj)(C(oXvz}+S}Iscd3xZ(N$=dVo&*qJ5&;oV=}?aZF^FXjMhP}t;YnzPG8_OXLIp_GL~6Zk-b9}O6`KMO0iY0100@l$1k^nkkp}{R*Km^qn%YKMMF5~nfFw|pBmgj5;egJGK>!>CHX@_KZIV(wgtb+M!cmt41VaD>4HX#@b5H@ofz^j#hao5wG6_f+0Lf=a%)tl-S0F>s5ETGyRZszzMMMZCRnamiKtNo|#j`4w15pFl0D$!Y!jV?nP)X1M0GSq1L&Zdd5@-v60e}J)lrkYhWFA975l<56Jwa1j%s^yUVMyW@jmz_O#=u-n7yy*ACBV=@iH8Nx5}1|%fMmu^i!@<RqEw484g&!M3IYNEa7bT;Sr;{R-#`E'),'little');BKL=[]
while a:
 c=a&0xffffff;h=a>>24&255;o=h>>7;n=h&127;a>>=32;ix=[a>>6*i&63 for i in range(n)];a>>=6*n
 BKL.append((c,o,ix))
BL=-1;BP=0;BS=None
def bk():
 global BL,BP,BS
 cur=(bytes(B),W,CR)
 if BL>=0 and cur!=BS:BL=-1
 if BL<0:
  cc=z.crc32(cur[0]+bytes([W,CR]))&0xffffff
  for i,x in enumerate(BKL):
   if x[0]==cc:BL=i;BP=x[1];BS=cur;break
  else:return 0
 ix=BKL[BL][2]
 if BP>=len(ix):BL=-1;return 0
 m=gn()[ix[BP]];mk(m);k=BP+1<len(ix)
 if k:mk(gn()[ix[BP+1]])
 BS=(bytes(B),W,CR);BP+=2 if k else 1
 if k:um()
 um();return m
def qf(n):return(ord(n[1])-49)*16+ord(n[0])-97
def uf(m):
 f=m&127;t=m>>7&127;p=m>>14&7
 return chr(97+(f&7))+chr(49+(f>>4))+chr(97+(t&7))+chr(49+(t>>4))+('nbrq'[p-2] if p else '')
def mf(u):
 f=qf(u[:2]);t=qf(u[2:4]);p='nbrq'.index(u[4])+2 if len(u)==5 else 0;return f|t<<7|p<<14
def pf(fn):
 global W,CR,EP,KW,KB,EV,L,I
 B[:]=bytes(128)
 L=[];I=[-1]*128;a=fn.split();EV=0;s=112
 for h in a[0]:
  if h=='/':s-=24
  elif h.isdigit():s+=int(h)
  else:
   d='PNBRQK'.index(h.upper())+1
   if h.islower():d+=6
   B[s]=d;I[s]=len(L);L.append(s);EV+=E[d][s]
   if d==6:KW=s
   elif d==12:KB=s
   s+=1
 W=a[1]=='w';CR=0
 if len(a)>2:
  for k,v in zip('KQkq',(1,2,4,8)):
   if k in a[2]:CR|=v
 EP=qf(a[3]) if len(a)>3 and a[3]!='-' else -1;U.clear()
def at(s,w):
 b=B
 for t in(s-15,s-17) if w else(s+15,s+17):
  if not t&136 and b[t]==7-6*w:return 1
 for d in KN:
  t=s+d
  if not t&136 and b[t]==8-6*w:return 1
 for d in KD:
  t=s+d
  if not t&136 and b[t]==12-6*w:return 1
 for d in BD+RD:
  t=s+d
  while not t&136:
   v=b[t]
   if v:
    if v==11-6*w or v==9-6*w+(d not in BD):return 1
    break
   t+=d
 return 0
def mv(m):
 t=B[m>>7&127];v=V[t if t<=6 else t-6] if t else 100;a=B[m&127];return v*16-V[a if a<=6 else a-6]
def gn(o=False):
 c=[];y=[];b=B;ek=12 if W else 6
 for f in L:
  v=b[f]
  if(v<=6)!=W:continue
  d=v if v<=6 else v-6
  if d==1:
   r=16 if W else -16;st=1 if W else 6;pr=7 if W else 0;t=f+r
   if not t&136 and not b[t]:
    if t>>4==pr:
     for p in(5,4,3,2):c.append(f|t<<7|p<<14)
    elif not o:
     y.append(f|t<<7)
     if f>>4==st:
      x=f+2*r
      if not b[x]:y.append(f|x<<7)
   for g in(r-1,r+1):
    t=f+g
    if t&136:continue
    tv=b[t]
    if tv and tv!=ek and(tv<=6)!=W:
     if t>>4==pr:
      for p in(5,4,3,2):c.append(f|t<<7|p<<14)
     else:c.append(f|t<<7)
    elif t==EP and EP>=0:c.append(f|t<<7)
  elif d==2 or d==6:
   for g in(KN if d==2 else KD):
    t=f+g
    if t&136:continue
    tv=b[t]
    if not tv:
     if not o:y.append(f|t<<7)
    elif tv!=ek and(tv<=6)!=W:c.append(f|t<<7)
  else:
   for g in(BD if d==3 else RD if d==4 else BD+RD):
    t=f+g
    while not t&136:
     tv=b[t]
     if not tv:
      if not o:y.append(f|t<<7)
     else:
      if tv!=ek and(tv<=6)!=W:c.append(f|t<<7)
      break
     t+=g
 if not o:
  for ks,rs,es,bt,aq,ds in((4,7,(5,6),1,(4,5,6),6),(4,0,(3,2,1),2,(4,3,2),2),(116,119,(117,118),4,(116,117,118),118),(116,112,(115,114,113),8,(116,115,114),114)):
   if(ks<16)==W and CR&bt and b[ks]==(6 if ks<16 else 12) and b[rs]==(4 if ks<16 else 10) and all(not b[x] for x in es) and all(not at(x,ks>16) for x in aq):y.append(ks|(ds<<7))
 c.sort(key=mv,reverse=True);return c+y if not o else c
def pm(a,z):
 i=I[a];L[i]=z;I[z]=i;I[a]=-1
def pr(s):
 i=I[s];x=L.pop()
 if x!=s:L[i]=x;I[x]=i
 I[s]=-1
def pa(s):I[s]=len(L);L.append(s)
def mk(m):
 global W,CR,EP,KW,KB,EV
 f=m&127;t=m>>7&127;p=m>>14&7;v=B[f];cp=B[t];s=t
 if v in(1,7) and t==EP and not cp:s=t-16 if W else t+16;cp=B[s]
 U.append((m,cp,s,CR,EP,EV,KW,KB));EV-=E[v][f]
 if cp:
  EV-=E[cp][s];pr(s)
 n=v
 if p:
  n=p if W else p+6
 EV+=E[n][t];B[f]=0;B[t]=n;pm(f,t)
 if s!=t:B[s]=0
 if v==6:KW=t
 elif v==12:KB=t
 if v in(6,12) and abs(t-f)==2:
  rf,rt=(f+3,f+1) if t>f else(f-4,f-1);rv=B[rf];EV-=E[rv][rf];EV+=E[rv][rt];B[rf]=0;B[rt]=rv;pm(rf,rt)
 for sq,bt in((4,3),(0,2),(7,1),(116,12),(112,8),(119,4)):
  if f==sq or t==sq:CR&=~bt
 EP=(f+t)//2 if v in(1,7) and abs(t-f)==32 else -1;W=not W
def um():
 global W,CR,EP,KW,KB,EV
 m,cp,s,CR,EP,EV,KW,KB=U.pop();f=m&127;t=m>>7&127;v=B[t];p=m>>14&7
 if p:v=1 if not W else 7
 if v in(6,12) and abs(t-f)==2:
  rf,rt=(f+3,f+1) if t>f else(f-4,f-1);pm(rt,rf);B[rf]=B[rt];B[rt]=0
 pm(t,f);B[f]=v;B[t]=0
 if cp:B[s]=cp;pa(s)
 W=not W
def S(d,a,b,pl):
 global N
 N+=1
 if N>LM:raise A()
 if d<=0:
  s=EV if W else -EV
  if at(KW if W else KB,not W):
   if not gn():return -M+pl
   return s
  if s>=b:return b
  if s>a:a=s
  for m in gn(1):
   mk(m)
   if at(KW if not W else KB,W):um();continue
   s2=-S(0,-b,-a,pl+1);um()
   if s2>a:a=s2
   if a>=b:break
  return a
 z=-F;bm=0
 for m in gn():
  mk(m)
  if at(KW if not W else KB,W):um();continue
  s=-S(d-1,-b,-a,pl+1);um()
  if s>z:z=s;bm=m
  if s>a:a=s
  if a>=b:break
 if z==-F:return -M+pl if at(KW if W else KB,not W) else 0
 if pl==0:BM[0]=bm
 return z
def rt():
 global N
 N=0;BM[0]=0;b=0
 try:
  for d in range(1,65):
   S(d,-F,F,0)
   if BM[0]:b=BM[0]
 except A:pass
 return b
def ch(fn,lg):
 pf(fn)
 lg=[mf(u) for u in lg];ls=set(lg)
 m=bk()
 if m and m in ls:return uf(m)
 b=rt()
 return uf(b if b in ls else lg[0])
def pt(u,pa,bo):
 q=u.Request(u2+pa,data=j.dumps(bo).encode())
 with u.urlopen(q,timeout=120) as r:return j.load(r)
u2=os.environ.get('MAKEFUN_ENV_URL') or sys.exit('MAKEFUN_ENV_URL is not set')
while True:
 g=pt(u,'/game',{})
 if g['status']=='done':break
 while g['status']=='your_move':
  w=ch(g['fen'],g['legal_moves'])
  g=pt(u,'/move',{'game':g['game'],'move':w})
