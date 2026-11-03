(function(){
'use strict';
var d=document,de=d.documentElement,$=function(s,r){return(r||d).querySelector(s)},$$=function(s,r){return Array.prototype.slice.call((r||d).querySelectorAll(s))};
var ES=de.lang==='es',DAY={Mon:'lun',Tue:'mar',Wed:'mié',Thu:'jue',Fri:'vie',Sat:'sáb',Sun:'dom'};
var fold=function(x){return x.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/&amp;/g,'&')};
var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
/* header shrink */
var hdr=$('.hdr');
function onScroll(){if(hdr)hdr.classList.toggle('is-scrolled',window.scrollY>12)}
onScroll();window.addEventListener('scroll',onScroll,{passive:true});
/* mobile nav + mega menu */
var burger=$('.burger'),nav=$('#nav');
if(burger&&nav){burger.addEventListener('click',function(){var o=nav.classList.toggle('open');burger.setAttribute('aria-expanded',o);burger.setAttribute('aria-label',o?(ES?'Cerrar menú':'Close menu'):(ES?'Abrir menú':'Open menu'));d.body.style.overflow=o?'hidden':''})}
var mb=$('.has-mega>button'),mega=$('.mega');
if(mb&&mega){
 var setM=function(o){mega.classList.toggle('open',o);mb.setAttribute('aria-expanded',o)};
 mb.addEventListener('click',function(){setM(!mega.classList.contains('open'))});
 var hm=$('.has-mega'),t;
 hm.addEventListener('mouseenter',function(){if(window.innerWidth>1060){clearTimeout(t);setM(true)}});
 hm.addEventListener('mouseleave',function(){if(window.innerWidth>1060){t=setTimeout(function(){setM(false)},160)}});
 d.addEventListener('keydown',function(e){if(e.key==='Escape'){setM(false)}});
 d.addEventListener('click',function(e){if(!hm.contains(e.target))setM(false)});
 hm.addEventListener('focusout',function(e){if(window.innerWidth>1060&&!hm.contains(e.relatedTarget))setM(false)});
}
/* back-to-home button */
var th=$('.to-home');
if(th){
 th.hidden=false;
 var tick=false,upd=function(){tick=false;th.classList.toggle('show',window.scrollY>400)};
 window.addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(upd)}},{passive:true});upd();
 th.addEventListener('click',function(e){
  if(th.pathname===location.pathname){e.preventDefault();window.scrollTo({top:0,behavior:reduce?'auto':'smooth'})}
 });
}
/* reveal */
var rv=$$('.rv');
if('IntersectionObserver' in window&&!reduce){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});rv.forEach(function(el){io.observe(el)})}else{rv.forEach(function(el){el.classList.add('in')})}
/* spotlight */
if(!reduce&&window.matchMedia('(hover:hover)').matches){$$('.card').forEach(function(c){c.addEventListener('pointermove',function(e){var r=c.getBoundingClientRect();c.style.setProperty('--mx',(e.clientX-r.left)+'px');c.style.setProperty('--my',(e.clientY-r.top)+'px')})})}
/* scroll spy */
var links=$$('[data-spy] a');
if(links.length&&'IntersectionObserver' in window){
 var map={};links.forEach(function(a){var id=a.getAttribute('href').slice(1);(map[id]=map[id]||[]).push(a)});
 var secs=Object.keys(map).map(function(id){return d.getElementById(id)}).filter(Boolean);
 var so=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(a){a.removeAttribute('aria-current')});map[e.target.id].forEach(function(a){a.setAttribute('aria-current','true');if(a.closest('.chips')){var c=a.closest('.chips');c.scrollTo({left:a.offsetLeft-16,behavior:reduce?'auto':'smooth'})}})}})},{rootMargin:'-30% 0px -60% 0px'});
 secs.forEach(function(s){so.observe(s)});
}
/* open-now */
function etNow(){var p=new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',weekday:'short',hour:'numeric',minute:'numeric',hour12:false}).formatToParts(new Date()),o={};p.forEach(function(x){o[x.type]=x.value});return{wd:o.weekday,h:parseInt(o.hour,10)%24,m:parseInt(o.minute,10)}}
try{
 var n=etNow(),mins=n.h*60+n.m,H=window.__HOURS||[],D=H.map(function(x){return x[0]});
 function mm(x){var q=x.split(':');return +q[0]*60+ +q[1]}
 function fmt(x){var h=+x.split(':')[0],m=+x.split(':')[1],s=h>=12?'PM':'AM';h=h%12||12;return h+(m?':'+(m<10?'0':'')+m:'')+' '+s}
 var i=D.indexOf(n.wd),td=H[i]||[n.wd,null,null],open=!!(td[1]&&mins>=mm(td[1])&&mins<mm(td[2]));
 $$('[data-status]').forEach(function(el){var t=$('.t',el);el.classList.toggle('open',open);
  if(open){t.textContent=(ES?'Abierto · cierra a las ':'Open now · closes ')+fmt(td[2])}else{var lbl,nx=null;if(td[1]&&mins<mm(td[1])){lbl=ES?'hoy':'today';nx=td}else{for(var k=1;k<8;k++){var c=H[(i+k)%7];if(c&&c[1]){nx=c;lbl=k===1?(ES?'mañana':'tomorrow'):(ES?DAY[c[0]]:c[0]);break}}}
   t.textContent=nx?(ES?'Cerrado · abre '+lbl+' a las ':'Closed · opens '+lbl+' ')+fmt(nx[1]):(ES?'Cerrado':'Closed')}});
 var row=$('.hours tr[data-d="'+n.wd+'"]');if(row)row.classList.add('today');
}catch(e){}
/* map facade */
var mf=$('[data-map]');
if(mf){var btn=$('button',mf);btn.addEventListener('click',function(){var f=d.createElement('iframe');f.src=mf.getAttribute('data-map');f.title=mf.getAttribute('data-title')||'Map';f.loading='lazy';f.referrerPolicy='no-referrer-when-downgrade';mf.appendChild(f);$('.inner',mf).remove()})}
/* command palette */
var pal=$('#pal'),idx=window.__SERVICES||[];
if(pal&&idx.length&&typeof pal.showModal==='function'){
 var inp=$('input',pal),list=$('.pal-list',pal),sel=0,cur=[];
 var base=de.getAttribute('data-base')||'';
 var render=function(q){q=q.trim().toLowerCase();cur=idx.filter(function(s){return!q||fold(s.n+' '+s.c).indexOf(fold(q))>-1});sel=0;
  list.innerHTML=cur.length?cur.map(function(s,i){return'<li><a href="'+base+s.u+'"'+(i===0?' class="sel"':'')+'><span>'+s.n+'</span><small>'+s.c+'</small></a></li>'}).join(''):'<li class="pal-empty">'+(ES?'Sin resultados. Llámenos al número de arriba y pregunte.':'No match. Call us at the number above and ask.')+'</li>'};
 var openP=function(){pal.showModal();inp.value='';render('');inp.focus()};
 $$('[data-open-pal]').forEach(function(b){b.addEventListener('click',openP)});
 inp.addEventListener('input',function(){render(inp.value)});
 inp.addEventListener('keydown',function(e){var as=$$('a',list);if(!as.length)return;if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();as[sel]&&as[sel].classList.remove('sel');sel=(sel+(e.key==='ArrowDown'?1:-1)+as.length)%as.length;as[sel].classList.add('sel');as[sel].scrollIntoView({block:'nearest'})}else if(e.key==='Enter'){e.preventDefault();location.href=as[sel].href}});
 pal.addEventListener('click',function(e){if(e.target===pal)pal.close()});
 d.addEventListener('keydown',function(e){var t=e.target,typing=t&&(/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName)||t.isContentEditable);if(e.key==='/'&&!typing&&!pal.open){e.preventDefault();openP()}});
}
/* inline finder (services hub) */
var fi=$('#finder-in'),fo=$('#finder-out');
if(fi&&fo&&idx.length){var base2=de.getAttribute('data-base')||'';fi.addEventListener('input',function(){var q=fi.value.trim().toLowerCase();if(!q){fo.innerHTML='';return}var r=idx.filter(function(s){return fold(s.n+' '+s.c).indexOf(fold(q))>-1}).slice(0,8);fo.innerHTML=r.length?r.map(function(s){return'<a href="'+base2+s.u+'"><span>'+s.n+'</span><small>'+s.c+'</small></a>'}).join(''):'<p class="note">'+(ES?'Sin resultados. Llame y pregunte. La lista muestra parte de lo que hacemos.':'No match. Call and ask. The list shows some of what we do.')+'</p>'})}
})();
