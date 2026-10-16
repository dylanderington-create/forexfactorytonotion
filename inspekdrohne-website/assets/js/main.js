(()=>{
const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
if(window.gsap&&window.ScrollTrigger)gsap.registerPlugin(ScrollTrigger);
const $ = (s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];

/* ---------- Ironbow-Farbskala ---------- */
const STOPS=[[0,[18,5,46]],[.18,[58,15,122]],[.38,[154,18,131]],[.58,[224,50,30]],[.74,[255,125,0]],[.88,[255,194,26]],[1,[255,246,216]]];
const LUT=new Uint8ClampedArray(256*3);
for(let i=0;i<256;i++){const t=i/255;let a=STOPS[0],b=STOPS[STOPS.length-1];for(let k=0;k<STOPS.length-1;k++){if(t>=STOPS[k][0]&&t<=STOPS[k+1][0]){a=STOPS[k];b=STOPS[k+1];break}}const f=(t-a[0])/((b[0]-a[0])||1);for(let c=0;c<3;c++)LUT[i*3+c]=a[1][c]+(b[1][c]-a[1][c])*f}
const idx=(T,a,b)=>Math.max(0,Math.min(255,Math.round((T-a)/(b-a)*255)));

/* Zufall mit Seed, damit jede Karte gleich aussieht */
function rng(seed){return()=>{seed|=0;seed=seed+0x6D2B79F5|0;let t=Math.imul(seed^seed>>>15,1|seed);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}

/* ---------- Heatfield-Hilfen ---------- */
function Field(w,h,base){const f=new Float32Array(w*h).fill(base);return{w,h,f,
  rect(x,y,rw,rh,T,mode){x|=0;y|=0;for(let j=Math.max(0,y);j<Math.min(h,y+rh);j++)for(let i=Math.max(0,x);i<Math.min(w,x+rw);i++){const k=j*w+i;f[k]=mode==='max'?Math.max(f[k],T):T}},
  spot(cx,cy,r,dT){const r2=r*r;for(let j=Math.max(0,cy-r*2|0);j<Math.min(h,cy+r*2);j++)for(let i=Math.max(0,cx-r*2|0);i<Math.min(w,cx+r*2);i++){const d=(i-cx)**2+(j-cy)**2;f[j*w+i]+=dT*Math.exp(-d/r2)}},
  noise(rand,amp){for(let k=0;k<f.length;k++)f[k]+=(rand()-.5)*amp},
  toCanvas(a,b){const c=document.createElement('canvas');c.width=w;c.height=h;const x=c.getContext('2d');const im=x.createImageData(w,h);for(let k=0;k<f.length;k++){const n=idx(f[k],a,b)*3;im.data[k*4]=LUT[n];im.data[k*4+1]=LUT[n+1];im.data[k*4+2]=LUT[n+2];im.data[k*4+3]=255}x.putImageData(im,0,0);return c},
  at(x,y){x=((x%w)+w)%w|0;y=((y%h)+h)%h|0;return f[y*w+x]}
}}

/* ---------- HERO: Wärmebild-Überflug einer Siedlung ---------- */
function buildCity(){
  const S=512, B=128, R=rng(7);
  const F=Field(S,S,6.5);
  F.noise(R,1.2);
  // Wiesen/Gärten mit leichter Struktur
  for(let n=0;n<90;n++)F.spot(R()*S,R()*S,6+R()*14,-1.5+R()*2);
  // Straßen (periodisch, damit die Kachel nahtlos ist)
  for(let s=0;s<S;s+=B){F.rect(s,0,12,S,11.5);F.rect(0,s,S,12,11.5)}
  // Autos
  for(let n=0;n<26;n++){const onX=R()<.5,lane=(R()*4|0)*B+3+(R()*5|0),p=R()*S|0;onX?F.rect(p,lane,11,5,24+R()*10):F.rect(lane,p,5,11,24+R()*10)}
  // Häuser je Block
  for(let by=0;by<S;by+=B)for(let bx=0;bx<S;bx+=B){
    const inner=B-12, ox=bx+12, oy=by+12;
    const cols=2, rows=2;
    for(let r=0;r<rows;r++)for(let c=0;c<cols;c++){
      if(R()<.12){ // Baum-Gruppe statt Haus
        for(let t=0;t<4;t++)F.spot(ox+c*inner/2+10+R()*36,oy+r*inner/2+10+R()*36,6+R()*5,2.2);continue}
      const cw=inner/2, ch=inner/2;
      const hw=24+R()*18|0, hh=20+R()*16|0;
      const hx=ox+c*cw+(cw-hw)/2+(R()-.5)*6|0, hy=oy+r*ch+(ch-hh)/2+(R()-.5)*6|0;
      const roof=2.5+R()*4, vert=R()<.5;
      // zwei Dachflächen mit First
      if(vert){F.rect(hx,hy,hw/2|0,hh,roof);F.rect(hx+(hw/2|0),hy,hw-(hw/2|0),hh,roof+1.4);F.rect(hx+(hw/2|0)-1,hy,2,hh,roof+5)}
      else{F.rect(hx,hy,hw,hh/2|0,roof);F.rect(hx,hy+(hh/2|0),hw,hh-(hh/2|0),roof+1.4);F.rect(hx,hy+(hh/2|0)-1,hw,2,roof+5)}
      // Traufe/Umrandung (warme Wand unten)
      F.rect(hx-1,hy-1,hw+2,1,12,'max');F.rect(hx-1,hy+hh,hw+2,1,12,'max');F.rect(hx-1,hy,1,hh,12,'max');F.rect(hx+hw,hy,1,hh,12,'max');
      // Kamin
      if(R()<.75){const kx=hx+4+R()*(hw-8)|0,ky=hy+3+R()*(hh-8)|0;F.rect(kx,ky,4,4,44+R()*14)}
      // Dachfenster mit Wärmeverlust
      if(R()<.6){const wx=hx+3+R()*(hw-9)|0,wy=hy+3+R()*(hh-8)|0;F.rect(wx,wy,5,4,16+R()*6);F.spot(wx+2,wy+2,3.5,5)}
      // Wärmeleck in Dämmung
      if(R()<.45)F.spot(hx+R()*hw,hy+R()*hh,4+R()*5,7+R()*9);
      // PV-Feld mit Hotspot
      if(R()<.3){const pw=Math.min(hw-6,18),ph=Math.min(hh/2-3,9)|0,px=hx+3,py=hy+2;for(let a=0;a<pw;a+=4)for(let b=0;b<ph;b+=4)F.rect(px+a,py+b,3,3,26+R()*4);if(R()<.7)F.rect(px+(R()*(pw/4)|0)*4,py,3,3,68)}
    }
  }
  return F;
}

function hero(){
  const cv=$('#thermal'), ctx=cv.getContext('2d');
  const F=buildCity(), S=F.w;
  // 3x3 kacheln, weichzeichnen, Mitte ausschneiden → nahtlos
  const raw=F.toCanvas(-2,36);
  const big=document.createElement('canvas');big.width=S*3;big.height=S*3;const bx=big.getContext('2d');
  for(let j=0;j<3;j++)for(let i=0;i<3;i++)bx.drawImage(raw,i*S,j*S);
  const tile=document.createElement('canvas');tile.width=S;tile.height=S;const tx=tile.getContext('2d');
  tx.filter='blur(1.4px)';tx.drawImage(big,-S,-S);tx.filter='none';
  let W,H,dpr,scale;
  function size(){dpr=Math.min(devicePixelRatio||1,2);W=cv.clientWidth;H=cv.clientHeight;cv.width=W*dpr|0;cv.height=H*dpr|0;scale=Math.max(W,H)/380}
  size();addEventListener('resize',size);
  let ox=40,oy=60,t0=performance.now(),mx=-1,my=-1,visible=true,scanY=0;
  const probe=$('#probe'),pv=$('#probe-val'),alt=$('#t-alt'),spd=$('#t-spd');
  const hero=$('#hero');
  hero.addEventListener('pointermove',e=>{const r=cv.getBoundingClientRect();mx=e.clientX-r.left;my=e.clientY-r.top;probe.style.transform=`translate(${mx}px,${my}px)`;probe.classList.add('on')});
  hero.addEventListener('pointerleave',()=>{probe.classList.remove('on');mx=-1});
  new IntersectionObserver(es=>{visible=es[0].isIntersecting}).observe(hero);
  function draw(now){
    const dt=Math.min(.05,(now-t0)/1000);t0=now;
    if(!RM){ox+=dt*7.5;oy+=dt*4.2}
    ctx.setTransform(dpr,0,0,dpr,0,0);ctx.imageSmoothingEnabled=true;
    const ts=S*scale;
    const sx=-((ox*scale)%ts), sy=-((oy*scale)%ts);
    for(let y=sy;y<H;y+=ts)for(let x=sx;x<W;x+=ts)ctx.drawImage(tile,x,y,ts,ts);
    // Scanlinie
    if(!RM){scanY=(scanY+dt*H*.22)%(H+120);const g=ctx.createLinearGradient(0,scanY-120,0,scanY);g.addColorStop(0,'rgba(255,246,216,0)');g.addColorStop(1,'rgba(255,246,216,.13)');ctx.fillStyle=g;ctx.fillRect(0,scanY-120,W,120);ctx.fillStyle='rgba(255,246,216,.5)';ctx.fillRect(0,scanY,W,1)}
    if(mx>=0){const T=F.at(ox+mx/scale,oy+my/scale);pv.textContent=T.toFixed(1).replace('.',',')+' °C'}
    if(!RM&&((now/400)|0)%2===0){alt.textContent=(58+Math.sin(now/1700)*1.6).toFixed(1);spd.textContent=(4.2+Math.sin(now/900)*.4).toFixed(1)}
  }
  function loop(now){if(visible)draw(now);requestAnimationFrame(loop)}
  draw(performance.now());
  if(!RM)requestAnimationFrame(loop);else addEventListener('resize',()=>draw(performance.now()));
  if(RM){hero.addEventListener('pointermove',()=>draw(performance.now()))}
}

/* ---------- Vergleich: Dach bei Tageslicht vs. Wärmebild ---------- */
function roofCompare(){
  const W=600,H=350;
  // Geometrie (in 600x350)
  const house={x:120,y:70,w:340,h:210}; // Grundriss von oben
  const ridge=house.y+house.h*.46;
  const sky1={x:212,y:92,w:30,h:24}, sky2={x:340,y:92,w:30,h:24};
  const chim={x:350,y:64,w:20,h:18};
  const pv={x:300,y:190,cols:6,rows:3,cw:22,ch:15,gap:2};
  const hot={c:4,r:2};
  const gap={x:170,y:136,r:22};
  // --- Tageslicht ---
  const v=$('#c-vis'), vc=v.getContext('2d');v.width=W*2;v.height=H*2;vc.scale(2,2);
  const R=rng(3);
  vc.fillStyle='#4f6b3a';vc.fillRect(0,0,W,H);
  for(let i=0;i<1400;i++){vc.fillStyle=`rgba(${60+R()*40|0},${90+R()*50|0},${40+R()*30|0},.5)`;vc.fillRect(R()*W,R()*H,2,2)}
  vc.fillStyle='#b7ada0';vc.fillRect(260,280,70,70); // Weg
  vc.fillStyle='#8f8a82';vc.fillRect(0,300,W,50); // Straße
  vc.fillStyle='#6f6a63';for(let x=0;x<W;x+=40)vc.fillRect(x,323,22,3);
  // Baum
  for(let i=0;i<9;i++){vc.fillStyle=`rgba(${34+R()*20|0},${70+R()*30|0},${30+R()*15|0},.85)`;vc.beginPath();vc.arc(530+(R()-.5)*50,120+(R()-.5)*50,20+R()*16,0,7);vc.fill()}
  // Schatten
  vc.fillStyle='rgba(0,0,0,.28)';vc.fillRect(house.x+10,house.y+10,house.w,house.h);
  // Dachflächen
  const tile=(y0,y1,base)=>{vc.fillStyle=base;vc.fillRect(house.x,y0,house.w,y1-y0);for(let y=y0;y<y1;y+=7){vc.fillStyle='rgba(0,0,0,.22)';vc.fillRect(house.x,y,house.w,1.3);for(let x=house.x+((y/7|0)%2)*6;x<house.x+house.w;x+=12){vc.fillStyle='rgba(0,0,0,.14)';vc.fillRect(x,y,1,7)}}};
  tile(house.y,ridge,'#8e3b2a');tile(ridge,house.y+house.h,'#7a3123');
  vc.fillStyle='#5a2419';vc.fillRect(house.x,ridge-3,house.w,6); // First
  vc.fillStyle='#9aa0a6';vc.fillRect(house.x-4,house.y-4,house.w+8,4);vc.fillRect(house.x-4,house.y+house.h,house.w+8,4); // Rinnen
  const skyl=s=>{vc.fillStyle='#39414a';vc.fillRect(s.x,s.y,s.w,s.h);vc.fillStyle='rgba(160,190,220,.55)';vc.fillRect(s.x+3,s.y+3,s.w-6,s.h-6);vc.fillStyle='rgba(255,255,255,.35)';vc.fillRect(s.x+4,s.y+4,6,s.h-8)};
  skyl(sky1);skyl(sky2);
  vc.fillStyle='#5b5752';vc.fillRect(chim.x,chim.y,chim.w,chim.h);vc.fillStyle='#2b2926';vc.fillRect(chim.x+4,chim.y+4,chim.w-8,chim.h-8);
  for(let r=0;r<pv.rows;r++)for(let c=0;c<pv.cols;c++){const x=pv.x+c*(pv.cw+pv.gap),y=pv.y+r*(pv.ch+pv.gap);vc.fillStyle='#1b2536';vc.fillRect(x,y,pv.cw,pv.ch);vc.strokeStyle='rgba(140,170,210,.35)';vc.lineWidth=.6;for(let k=1;k<4;k++){vc.beginPath();vc.moveTo(x+k*pv.cw/4,y);vc.lineTo(x+k*pv.cw/4,y+pv.ch);vc.stroke()}vc.fillStyle='rgba(255,255,255,.07)';vc.fillRect(x,y,pv.cw,3)}
  // --- Wärmebild ---
  const G=Field(W,H,7);const R2=rng(11);G.noise(R2,1);
  for(let i=0;i<60;i++)G.spot(R2()*W,R2()*H,10+R2()*20,-1.2+R2()*1.6);
  G.rect(0,300,W,50,9.5);G.rect(260,280,70,20,10.5);
  G.spot(530,120,40,-2.5);
  G.rect(house.x-4,house.y-4,house.w+8,house.h+8,14); // warme Wand/Traufe
  G.rect(house.x,house.y,house.w,ridge-house.y,3.2);G.rect(house.x,ridge,house.w,house.y+house.h-ridge,4.1);
  G.rect(house.x,ridge-3,house.w,6,9.5);
  G.spot(house.x+house.w*.8,ridge,10,3);
  // Wärmebrücke Dachfenster 1 stark, 2 schwach
  G.rect(sky1.x,sky1.y,sky1.w,sky1.h,15);G.spot(sky1.x+sky1.w/2,sky1.y+sky1.h/2,20,8);
  G.rect(sky2.x,sky2.y,sky2.w,sky2.h,12);G.spot(sky2.x+sky2.w/2,sky2.y+sky2.h/2,10,2);
  // Dämmungs-Fehlstelle
  G.spot(gap.x,gap.y,gap.r,9);G.spot(gap.x+8,gap.y-4,gap.r*.5,3);
  // Kamin
  G.rect(chim.x,chim.y,chim.w,chim.h,34);G.rect(chim.x+4,chim.y+4,chim.w-8,chim.h-8,52);G.spot(chim.x+chim.w/2,chim.y+chim.h,14,12);
  // PV (Winter: Module etwas wärmer durch Sonne)
  for(let r=0;r<pv.rows;r++)for(let c=0;c<pv.cols;c++){const x=pv.x+c*(pv.cw+pv.gap),y=pv.y+r*(pv.ch+pv.gap);G.rect(x,y,pv.cw,pv.ch,19+R2()*2.5)}
  {const x=pv.x+hot.c*(pv.cw+pv.gap),y=pv.y+hot.r*(pv.ch+pv.gap);G.rect(x,y,pv.cw,pv.ch,27);G.rect(x+pv.cw*.55|0,y+4,6,6,74);G.spot(x+pv.cw*.55+3,y+7,4,12)}
  const irRaw=G.toCanvas(0,34);
  const ir=$('#c-ir'),ic=ir.getContext('2d');ir.width=W*2;ir.height=H*2;ic.filter='blur(2.2px)';ic.drawImage(irRaw,0,0,W*2,H*2);ic.filter='none';
  // Scanlinien fürs IR-Gefühl
  ic.fillStyle='rgba(0,0,0,.08)';for(let y=0;y<H*2;y+=3)ic.fillRect(0,y,W*2,1);
  // Regler
  const box=$('#compare'),rng_=$('#cmp-range');
  const set=v=>box.style.setProperty('--pos',v+'%');
  rng_.addEventListener('input',e=>set(e.target.value));
  // Intro-Wisch, wenn sichtbar
  if(!RM&&window.gsap){const o={v:88};gsap.to(o,{v:24,duration:1.8,ease:'power3.inOut',scrollTrigger:{trigger:box,start:'top 75%'},onUpdate:()=>{set(o.v);rng_.value=o.v}});set(88);rng_.value=88}
}

/* ---------- Radar Einsatzgebiet ---------- */
function radar(){
  const cv=$('#radar');if(!cv)return;const ctx=cv.getContext('2d');
  const base={n:'Neulußheim',lat:49.2972,lon:8.5197};
  // [Name, Breite, Länge, Label-Ausrichtung, Label-Versatz y]
  const C=[['Hockenheim',49.322,8.547,'l',-6],['Mannheim',49.487,8.466,'l',0],['Heidelberg',49.398,8.672,'l',-8],['Schwetzingen',49.383,8.572,'l',0],['Speyer',49.317,8.431,'r',0],['Walldorf',49.306,8.642,'l',0],['Wiesloch',49.294,8.698,'l',16],['Ludwigshafen',49.477,8.445,'r',6],['Weinheim',49.550,8.667,'l',0],['Sinsheim',49.253,8.879,'c',16]];
  const km=(la,lo)=>[(lo-base.lon)*72.6,-(la-base.lat)*111.2]; // km Ost/Süd
  const RANGE=33; // km bis Rand
  let S,dpr,hl=null;
  const css=getComputedStyle(document.documentElement);
  const col={fg:css.getPropertyValue('--fg').trim(),mute:css.getPropertyValue('--mute').trim(),hot:css.getPropertyValue('--hot').trim()};
  function size(){dpr=Math.min(devicePixelRatio||1,2);S=cv.clientWidth;cv.width=S*dpr;cv.height=S*dpr}
  size();addEventListener('resize',size);
  $$('#cities li').forEach(li=>{li.addEventListener('mouseenter',()=>hl=li.dataset.c);li.addEventListener('mouseleave',()=>hl=null)});
  let a=0,last=performance.now(),vis=true;
  new IntersectionObserver(es=>vis=es[0].isIntersecting).observe(cv);
  function draw(now){
    const dt=(now-last)/1000;last=now;if(!RM)a=(a+dt*.9)%(Math.PI*2);
    ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,S,S);
    const c=S/2,r=S/2-24,k=r/RANGE,small=S<480;
    ctx.strokeStyle='rgba(190,210,230,.16)';ctx.lineWidth=1;
    for(let i=1;i<=3;i++){ctx.beginPath();ctx.arc(c,c,10*i*k,0,7);ctx.stroke()}
    ctx.beginPath();ctx.moveTo(c-r,c);ctx.lineTo(c+r,c);ctx.moveTo(c,c-r);ctx.lineTo(c,c+r);ctx.stroke();
    ctx.fillStyle=col.mute;ctx.font='10px "JetBrains Mono",monospace';ctx.textAlign='left';
    for(let i=1;i<=3;i++)ctx.fillText(10*i+' km',c+5,c+10*i*k-5); // Beschriftung nach Süden, dort liegen keine Orte
    ctx.textAlign='center';ctx.fillText('N',c,14);
    const g=ctx.createConicGradient?ctx.createConicGradient(a-Math.PI/2.2,c,c):null;
    if(g){g.addColorStop(0,'rgba(255,125,0,0)');g.addColorStop(.12,'rgba(255,125,0,.28)');g.addColorStop(.121,'rgba(255,125,0,0)');ctx.fillStyle=g;ctx.beginPath();ctx.arc(c,c,r,0,7);ctx.fill()}
    ctx.strokeStyle='rgba(255,194,26,.8)';ctx.beginPath();ctx.moveTo(c,c);ctx.lineTo(c+Math.cos(a-Math.PI/2.2+.75)*r,c+Math.sin(a-Math.PI/2.2+.75)*r);ctx.stroke();
    ctx.font=(small?'600 9px':'600 11px')+' "JetBrains Mono",monospace';
    C.forEach(([n,la,lo,al,oy])=>{const [x,y]=km(la,lo);const px=c+x*k,py=c+y*k;const ang=Math.atan2(py-c,px-c);let d=((a-Math.PI/2.2+.75)-ang)%(Math.PI*2);if(d<0)d+=Math.PI*2;const glow=RM?1:Math.max(0,1-d/2.2);const on=hl===n;
      ctx.fillStyle=on?col.hot:`rgba(255,${150+glow*90|0},${40+glow*150|0},${.45+glow*.55})`;ctx.beginPath();ctx.arc(px,py,on?6:3.5+glow*2,0,7);ctx.fill();
      if(on){ctx.strokeStyle=col.hot;ctx.beginPath();ctx.moveTo(c,c);ctx.lineTo(px,py);ctx.stroke()}
      ctx.fillStyle=on?col.hot:`rgba(238,241,244,${.6+glow*.4})`;ctx.textAlign=al==='r'?'right':al==='c'?'center':'left';ctx.fillText(n.toUpperCase(),al==='r'?px-8:al==='c'?px:px+8,py+4+oy)});
    ctx.textAlign='center';
    const pulse=RM?0:(now/1400)%1;
    ctx.strokeStyle=`rgba(255,194,26,${1-pulse})`;ctx.lineWidth=2;ctx.beginPath();ctx.arc(c,c,8+pulse*38,0,7);ctx.stroke();
    ctx.fillStyle=col.hot;ctx.beginPath();ctx.arc(c,c,7,0,7);ctx.fill();
    ctx.fillStyle=col.fg;ctx.font=(small?'700 10px':'700 12px')+' "JetBrains Mono",monospace';ctx.fillText('NEULUSSHEIM · BASIS',c,c+30);
  }
  function loop(now){if(vis||hl)draw(now);requestAnimationFrame(loop)}
  draw(performance.now());if(!RM)requestAnimationFrame(loop);else addEventListener('resize',()=>draw(performance.now()));
  if(document.fonts)document.fonts.ready.then(()=>draw(performance.now()));
}

/* ---------- Navigation & Mobile-CTA ---------- */
function nav(){
  const n=$('#nav'),b=$('#burger'),m=$('#menu');if(!n)return;
  const mc=$('.mobile-cta'),hero=$('.hero'),kontakt=$('#kontakt');
  const on=()=>{n.classList.toggle('solid',scrollY>40||!hero);
    if(mc){const past=hero?scrollY>hero.offsetHeight*.6:scrollY>200;const atForm=kontakt&&kontakt.getBoundingClientRect().top<innerHeight*.8;mc.classList.toggle('on',past&&!atForm)}};
  on();addEventListener('scroll',on,{passive:true});
  if(mc)document.body.classList.add('has-mcta');
  const close=()=>{m.classList.remove('open');b.setAttribute('aria-expanded','false');b.setAttribute('aria-label','Menü öffnen')};
  b.addEventListener('click',()=>{const o=m.classList.toggle('open');b.setAttribute('aria-expanded',String(o));b.setAttribute('aria-label',o?'Menü schließen':'Menü öffnen')});
  $$('#menu a').forEach(a=>a.addEventListener('click',close));
  addEventListener('keydown',e=>{if(e.key==='Escape'&&m.classList.contains('open')){close();b.focus()}});
}

/* ---------- Cursor ---------- */
function cursor(){
  const c=$('.cursor');if(!c||RM||!matchMedia('(pointer:fine)').matches)return;
  let x=innerWidth/2,y=innerHeight/2,cx=x,cy=y;
  addEventListener('pointermove',e=>{x=e.clientX;y=e.clientY});
  $$('a,button,.svc,input,select,textarea,summary,.compare').forEach(el=>{el.addEventListener('mouseenter',()=>c.classList.add('big'));el.addEventListener('mouseleave',()=>c.classList.remove('big'))});
  (function f(){cx+=(x-cx)*.22;cy+=(y-cy)*.22;c.style.transform=`translate(${cx}px,${cy}px)`;requestAnimationFrame(f)})();
}

/* ---------- Formular ----------
   FORM_ENDPOINT leer  → Anfrage wird als fertige E-Mail im Mailprogramm geöffnet.
   FORM_ENDPOINT gesetzt (z. B. Web3Forms) → Anfrage wird direkt gesendet, danach /danke.
   Spamschutz: verstecktes Honeypot-Feld + Mindest-Ausfüllzeit. */
const FORM_ENDPOINT='';
const FORM_KEY='';   // z. B. Web3Forms access_key
function form(){
  const f=$('#form');if(!f)return;
  const msg=$('#form-msg'),t0=Date.now();
  const fields={name:$('#f-name'),contact:$('#f-contact'),consent:$('#f-consent')};
  const setErr=(el,text)=>{const id=el.id+'-err';let e=document.getElementById(id);
    if(text){el.setAttribute('aria-invalid','true');el.setAttribute('aria-describedby',id);if(!e){e=document.createElement('span');e.id=id;e.className='field-err';(el.type==='checkbox'?el.closest('label'):el).insertAdjacentElement('afterend',e)}e.textContent=text}
    else{el.removeAttribute('aria-invalid');if(e)e.remove()}};
  const validate=()=>{let first=null;
    const nm=fields.name.value.trim();setErr(fields.name,nm?'':'Bitte geben Sie Ihren Namen an.');if(!nm)first=first||fields.name;
    const c=fields.contact.value.trim();const ok=/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(c)||/^[+()\d\s/-]{6,}$/.test(c);
    setErr(fields.contact,ok?'':'Bitte eine gültige E-Mail-Adresse oder Telefonnummer angeben.');if(!ok)first=first||fields.contact;
    setErr(fields.consent,fields.consent.checked?'':'Bitte bestätigen Sie die Datenschutzhinweise.');if(!fields.consent.checked)first=first||fields.consent;
    return first};
  Object.values(fields).forEach(el=>el.addEventListener(el.type==='checkbox'?'change':'blur',()=>{if(el.hasAttribute('aria-invalid'))validate()}));
  f.addEventListener('submit',async e=>{
    e.preventDefault();
    const bad=validate();
    if(bad){msg.hidden=false;msg.textContent='Bitte prüfen Sie die markierten Felder.';bad.focus();return}
    // Spam: Honeypot ausgefüllt oder in unter 3 Sekunden abgeschickt → still ignorieren
    if($('#f-website').value||Date.now()-t0<3000){location.href='/danke';return}
    const ls=$$('input[name=leistung]:checked').map(i=>i.value).join(', ')||'–';
    const data={name:fields.name.value.trim(),kontakt:fields.contact.value.trim(),objekt:$('#f-obj').value,ort:$('#f-ort').value.trim()||'–',leistung:ls,nachricht:$('#f-msg').value.trim()};
    const btn=f.querySelector('button[type=submit]');btn.disabled=true;btn.setAttribute('aria-busy','true');
    if(FORM_ENDPOINT){
      msg.hidden=false;msg.textContent='Anfrage wird gesendet …';
      try{const r=await fetch(FORM_ENDPOINT,{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify({access_key:FORM_KEY,subject:'Anfrage Drohnenflug – '+data.objekt,from_name:'inspekdrohne.de',...data})});
        if(!r.ok)throw new Error(r.status);location.href='/danke';return}
      catch(err){msg.textContent='Die Anfrage konnte gerade nicht gesendet werden. Bitte schreiben Sie uns an info@inspekdrohne.de oder rufen Sie an: 06205 3646528.';btn.disabled=false;btn.removeAttribute('aria-busy');return}
    }
    const body=`Name: ${data.name}\nKontakt: ${data.kontakt}\nObjekt: ${data.objekt}\nOrt: ${data.ort}\nLeistung: ${data.leistung}\n\n${data.nachricht}`;
    location.href=`mailto:info@inspekdrohne.de?subject=${encodeURIComponent('Anfrage Drohnenflug – '+data.objekt)}&body=${encodeURIComponent(body)}`;
    setTimeout(()=>{location.href='/danke?via=mail'},900);
  });
}

/* ---------- Animationen ---------- */
function motion(){
  const pre=$('#pre');if(!$('.hero'))return;
  const noAnim=RM||!window.gsap;
  if(noAnim){if(pre)pre.remove();$$('.statement h2').forEach(h=>h.classList.add('struck'));return}
  gsap.registerPlugin(ScrollTrigger);
  function intro(){
    gsap.from('.hero h1 .ln>span',{yPercent:45,opacity:0,duration:1.1,ease:'expo.out',stagger:.09});
    gsap.from('.hero .eyebrow,.hero-sub p,.hero-cta .btn',{y:24,opacity:0,duration:.9,ease:'power3.out',stagger:.08,delay:.35});
    gsap.from('.hud .c',{scale:2.4,opacity:0,duration:.9,ease:'expo.out',stagger:.05,delay:.2});
  }
  // Vorflug-Check nur beim Einstieg von außen
  // (ohne Speicherung im Browser: übersprungen, wenn man von einer eigenen Unterseite kommt)
  let seen=false;try{seen=!!document.referrer&&new URL(document.referrer).host===location.host}catch(e){}
  if(pre&&!seen){
    const rows=$$('#pre .row'),bar=$('#pre .bar i');
    rows.forEach((r,i)=>setTimeout(()=>{r.classList.add('on');bar.style.width=((i+1)/rows.length*100)+'%'},80+i*120));
    setTimeout(()=>{pre.classList.add('done');intro();setTimeout(()=>pre.remove(),700)},80+rows.length*120+180);
  }else{if(pre)pre.remove();intro()}
  ScrollTrigger.create({trigger:'#strikeh',start:'top 70%',onEnter:()=>{$$('#strikeh .strike').forEach((el,i)=>setTimeout(()=>el.style.setProperty('--s',1),i*260))}});
  $$('.reveal').forEach(el=>gsap.from(el,{y:50,opacity:0,duration:1,ease:'power3.out',scrollTrigger:{trigger:el,start:'top 90%',once:true}}));
  $$('section h2').forEach(h=>{if(h.closest('.hero,.consent'))return;gsap.from(h,{y:70,opacity:0,duration:1.1,ease:'expo.out',scrollTrigger:{trigger:h,start:'top 88%',once:true}})});
  const p=$('#fp'),dot=$('#dronedot');
  if(p&&getComputedStyle($('.steps svg.path')).display!=='none'){
    const L=p.getTotalLength();
    gsap.fromTo(p,{strokeDashoffset:L,strokeDasharray:`${L} ${L}`},{strokeDashoffset:0,ease:'none',scrollTrigger:{trigger:'#steps',start:'top 80%',end:'bottom 60%',scrub:.6,onUpdate:s=>{const pt=p.getPointAtLength(L*s.progress);dot.setAttribute('cx',pt.x);dot.setAttribute('cy',pt.y)}}});
  }
  gsap.from('.cta .big',{xPercent:-8,ease:'none',scrollTrigger:{trigger:'.cta',start:'top bottom',end:'top 20%',scrub:true}});
}

/* ---------- Cookie-Banner / Einwilligung ----------
   Speichert nur die eigene Entscheidung (localStorage, technisch notwendig nach § 25 Abs. 2 TDDDG).
   Optionale Dienste werden erst nach Zustimmung geladen. Neuen Dienst eintragen:
   SERVICES.statistik.load = () => { ...Skript laden... }   und in der Datenschutzerklärung nennen. */
const CONSENT_KEY='inspek-consent',CONSENT_VERSION=1;
const SERVICES={
  statistik:{label:'Statistik',desc:'Hilft uns zu verstehen, wie die Website genutzt wird, damit wir sie verbessern können. Aktuell ist kein Statistikdienst aktiv.',load:null}
};
function consent(){
  const read=()=>{try{const v=JSON.parse(localStorage.getItem(CONSENT_KEY));return v&&v.v===CONSENT_VERSION?v:null}catch(e){return null}};
  const apply=c=>{Object.keys(SERVICES).forEach(k=>{const sv=SERVICES[k];if(c&&c[k]&&sv.load&&!sv.loaded){sv.loaded=true;try{sv.load()}catch(e){}}})};
  const save=c=>{c.v=CONSENT_VERSION;c.date=new Date().toISOString();try{localStorage.setItem(CONSENT_KEY,JSON.stringify(c))}catch(e){}apply(c)};
  const el=document.createElement('section');el.className='consent';el.id='consent';el.hidden=true;
  el.setAttribute('role','dialog');el.setAttribute('aria-labelledby','consent-title');el.setAttribute('aria-describedby','consent-text');
  el.innerHTML=`<div class="consent-in">
    <div class="consent-copy"><h2 id="consent-title">Datenschutz-Einstellungen</h2>
    <p id="consent-text">Wir verwenden nur technisch notwendige Speicherungen. Optionale Dienste wie Statistik laden wir erst, wenn Sie zustimmen. Ihre Wahl können Sie jederzeit unter „Cookie-Einstellungen“ im Seitenfuß ändern. Mehr in der <a href="/datenschutz">Datenschutzerklärung</a>.</p></div>
    <div class="consent-opts" id="consent-opts" hidden>
      <label class="opt"><input type="checkbox" checked disabled> <span><strong>Notwendig</strong> · immer aktiv<br><small>Speichert Ihre Auswahl in diesem Banner. Keine Weitergabe an Dritte.</small></span></label>
      ${Object.entries(SERVICES).map(([k,sv])=>`<label class="opt"><input type="checkbox" id="consent-${k}" data-k="${k}"> <span><strong>${sv.label}</strong><br><small>${sv.desc}</small></span></label>`).join('')}
    </div>
    <div class="consent-btns">
      <button type="button" class="cbtn" data-a="deny">Nur notwendige</button>
      <button type="button" class="cbtn" data-a="settings" aria-expanded="false" aria-controls="consent-opts">Einstellungen</button>
      <button type="button" class="cbtn" data-a="save" hidden>Auswahl speichern</button>
      <button type="button" class="cbtn" data-a="all">Alle akzeptieren</button>
    </div></div>`;
  document.body.appendChild(el);
  const opts=el.querySelector('#consent-opts'),bSet=el.querySelector('[data-a=settings]'),bSave=el.querySelector('[data-a=save]');
  const open=(withOpts)=>{const c=read()||{};Object.keys(SERVICES).forEach(k=>{el.querySelector('#consent-'+k).checked=!!c[k]});
    opts.hidden=!withOpts;bSave.hidden=!withOpts;bSet.hidden=!!withOpts;bSet.setAttribute('aria-expanded',String(!!withOpts));
    el.hidden=false;document.body.classList.add('consent-open');requestAnimationFrame(()=>el.classList.add('on'))};
  const close=()=>{el.classList.remove('on');document.body.classList.remove('consent-open');setTimeout(()=>{el.hidden=true},250)};
  el.addEventListener('click',e=>{const a=e.target.closest('[data-a]');if(!a)return;const act=a.dataset.a;const c={};
    if(act==='settings'){open(true);el.querySelector('#consent-opts input:not([disabled])')?.focus();return}
    Object.keys(SERVICES).forEach(k=>{c[k]=act==='all'?true:act==='deny'?false:el.querySelector('#consent-'+k).checked});
    save(c);close();if(opener){opener.focus();opener=null}});
  let opener=null;
  $$('.consent-link').forEach(b=>b.addEventListener('click',()=>{opener=b;open(true);el.querySelector('.cbtn')?.focus()}));
  const c=read();if(c)apply(c);else open(false);
}

/* ---------- Danke-Seite: Hinweis bei Versand über Mailprogramm ---------- */
function thanks(){const el=$('#via-mail');if(el&&/via=mail/.test(location.search))el.hidden=false}

nav();consent();if($('#thermal'))hero();if($('#compare'))roofCompare();radar();form();cursor();motion();thanks();
})();
