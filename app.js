import { competitors, workloads, aiPaths, strategicQuestions, sources, glossary } from './data.js';
import { computeEnergyScenario } from './economics.js';
const $ = (selector) => document.querySelector(selector);
const escapeText = (value) => String(value).replace(/[&<>"']/g, ch => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }[ch]));
const sourceFor = id => sources.find(source => source.id === id);

let activeCompetitor = 'amd';
function renderCompetitors() {
  $('#competitorGrid').innerHTML = competitors.map(item => `
    <button class="competitor-card tone-${item.tone} ${item.id === activeCompetitor ? 'selected' : ''}" type="button" data-competitor="${item.id}" aria-pressed="${item.id === activeCompetitor}">
      <div class="competitor-top"><span class="competitor-logo">${item.mark}</span><span class="competitor-title"><strong>${escapeText(item.name)}</strong><small>${escapeText(item.category)}</small></span></div>
      <h3 class="competitor-headline">${escapeText(item.headline)}</h3><p class="competitor-description">${escapeText(item.summary)}</p>
      <span class="competitor-more">VIEW STRATEGIC POSITION <span>↗</span></span>
    </button>`).join('');
  const item = competitors.find(x=> x.id === activeCompetitor);
  $('#competitorDetail').innerHTML = `<div class="detail-title"><span>DEEP DIVE</span> ${escapeText(item.name)} / ${escapeText(item.product)}</div><div class="detail-columns"><div class="detail-col"><h4>POSITIONING STRENGTHS</h4><ul>${item.strength.map(s=> `<li>${escapeText(s)}</li>`).join('')}</ul></div><div class="detail-col"><h4>WHAT TO VERIFY</h4><ul>${item.watch.map(s=> `<li>${escapeText(s)}</li>`).join('')}</ul></div></div><div class="detail-source">SOURCE TRAIL: ${item.sources.map(id=>`<a href="${sourceFor(id).url}" target="_blank" rel="noopener noreferrer">${id} ↗</a>`).join(' &nbsp;·&nbsp; ')}</div>`;
  document.querySelectorAll('[data-competitor]').forEach(button=> button.addEventListener('click', ()=> {activeCompetitor=button.dataset.competitor;renderCompetitors();}));
}

let activeWorkload = 'cloud';
const workIcons = {cloud:'☁',building:'▥',cpu:'▦',brain:'✳'};
function renderWorkloads() {
  $('#workloadOptions').innerHTML = workloads.map(item=> `<button class="workload-tab ${item.id===activeWorkload?'active':''}" type="button" role="tab" aria-selected="${item.id===activeWorkload}" data-workload="${item.id}"><span class="workload-ico">${workIcons[item.icon]}</span><span><strong>${escapeText(item.label)}</strong><small>${escapeText(item.theme)}</small></span><span class="chevron">↗</span></button>`).join('');
  const item=workloads.find(x=> x.id===activeWorkload);
  $('#workloadDetail').innerHTML = `<div class="mini">BUYER DECISION LENS / ${escapeText(item.label.toUpperCase())}</div><h3>${escapeText(item.question)}</h3><p>${escapeText(item.insight)}</p><div class="label-small">THREE METRICS TO TEST</div><div class="metric-tags">${item.metrics.map(m=>`<span>${escapeText(m)}</span>`).join('')}</div><div class="buyer-meta">TYPICAL BUYER: <strong>${escapeText(item.buyer)}</strong></div>`;
  document.querySelectorAll('[data-workload]').forEach(button=> button.addEventListener('click',()=>{activeWorkload=button.dataset.workload;renderWorkloads();}));
}

let activeAi = 'cpu';
function renderAi() {
  $('#aiPaths').innerHTML = aiPaths.map(item=>`<button class="ai-path ${activeAi === item.id ? 'active':''}" type="button" data-ai="${item.id}" aria-pressed="${activeAi === item.id}"><span class="ai-number">${item.n} / 03</span><strong>${escapeText(item.label)}</strong><span class="ai-bottom">${escapeText(item.tag)} <span>↗</span></span></button>`).join('');
  const item=aiPaths.find(x=>x.id===activeAi);
  $('#aiDetail').innerHTML=`<div><span class="mini">THE CPU ROLE / ${item.n}</span><h3>${escapeText(item.title)}</h3></div><div class="ai-body"><p>${escapeText(item.statement)}</p><div><b>Track:</b> ${escapeText(item.bottleneck)}</div><div class="ai-caution"><b>Don't assume:</b> ${escapeText(item.caution)}</div></div>`;
  document.querySelectorAll('[data-ai]').forEach(button=>button.addEventListener('click',()=>{activeAi=button.dataset.ai;renderAi();}));
}

function renderBriefing() {
  $('#briefingList').innerHTML=strategicQuestions.map((item,i)=> `<details class="brief-item" ${i===0?'open':''}><summary><span class="brief-index">0${i+1}</span><span class="brief-question">${escapeText(item.q)}</span><span class="brief-plus">＋</span></summary><div class="brief-answer"><p>${escapeText(item.a)}</p><a href="${sourceFor(item.source).url}" target="_blank" rel="noopener noreferrer">REVIEW RELATED PUBLIC SOURCE ↗</a></div></details>`).join('');
}
function renderSources() {
  $('#sourceList').innerHTML=sources.map(item=>`<a class="source-item" href="${item.url}" target="_blank" rel="noopener noreferrer"><span class="source-id">${escapeText(item.id)}</span><span class="source-title">${escapeText(item.title)}<small>${escapeText(item.owner)} · ${escapeText(item.kind)} — ${escapeText(item.insight)}</small></span><span class="source-date">${escapeText(item.date)}</span><span class="source-trust ${item.trust==='Vendor claim'?'vendor':''}">${escapeText(item.trust)}</span><span class="source-arrow">↗</span></a>`).join('');
}
function renderGlossary(){ $('#glossaryGrid').innerHTML=glossary.map(([term,meaning])=>`<article class="glossary-item"><strong>${escapeText(term)}</strong><p>${escapeText(meaning)}</p></article>`).join(''); }

const defaults={servers:500,watts:500,rate:0.15,pue:1.3,improvement:20};
const euro=new Intl.NumberFormat('en-IE',{style:'currency',currency:'EUR',maximumFractionDigits:0});
const dec=new Intl.NumberFormat('en-IE');
function syncEconomics(){
  const values=Object.fromEntries(Object.keys(defaults).map(id=>[id,Number(document.getElementById(id).value)]));
  $('#serversOut').textContent=dec.format(values.servers);
  $('#wattsOut').textContent=`${values.watts} W`;
  $('#rateOut').textContent=`€${values.rate.toFixed(2)} / kWh`;
  $('#pueOut').textContent=values.pue.toFixed(2);
  $('#improvementOut').textContent=`${values.improvement}%`;
  const result=computeEnergyScenario(values);
  $('#annualCost').textContent=euro.format(result.base);
  $('#annualSavings').textContent=euro.format(result.savings);
  $('#scenarioBarValue').textContent=`${result.percentRemaining}%`;
  $('#scenarioBar').style.width=`${result.percentRemaining}%`;
}
function setupEconomics(){Object.keys(defaults).forEach(id=>document.getElementById(id).addEventListener('input',syncEconomics));$('#resetEconomics').addEventListener('click',()=>{Object.entries(defaults).forEach(([id,value])=>document.getElementById(id).value=String(value));syncEconomics();});syncEconomics();}

function setupNavigation(){
 const menu=$('#menuButton'),rail=$('#sidebar');
 const closeMenu=()=>{rail.classList.remove('open');menu.setAttribute('aria-expanded','false');};
 menu.addEventListener('click',()=>{rail.classList.toggle('open');menu.setAttribute('aria-expanded',String(rail.classList.contains('open')));});
 document.querySelectorAll('a[href^="#"]').forEach(a=>a.addEventListener('click',closeMenu));
 const links=[...document.querySelectorAll('.nav-link')];
 const labelFor=id=>links.find(a=>a.dataset.section===id)?.textContent.trim().replace(/^[^\w]+/,'').replace(/06$/,'').trim()||'Overview';
 const observer=new IntersectionObserver(entries=>{
   for(const entry of entries){if(entry.isIntersecting){const id=entry.target.id;links.forEach(a=>a.classList.toggle('active',a.dataset.section===id));$('#currentLocation').textContent=labelFor(id);}}
 },{rootMargin:'-20% 0px -65% 0px',threshold:0});
 document.querySelectorAll('main > section').forEach(s=>observer.observe(s));
 document.addEventListener('keydown',event=>{if(event.key==='Escape')closeMenu();});
}

renderCompetitors();renderWorkloads();renderAi();renderBriefing();renderSources();renderGlossary();setupEconomics();setupNavigation();