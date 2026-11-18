/* Check current exported prices against browser optimizer and saved default plans. */
const fs=require('fs'), opt=require('../app/optimizer.js');
const systems=JSON.parse(fs.readFileSync('app/data/systems.json'));
const summary=JSON.parse(fs.readFileSync('app/data/summary.json'));
const raw=systems.map(s=>{const a=s.eq.filter(v=>v!==null);return a.length?a.reduce((x,y)=>x+y,0)/a.length:null});
const sorted=raw.filter(v=>v!==null).sort((a,b)=>a-b), mid=sorted.length>>1;
const med=sorted.length%2?sorted[mid]:(sorted[mid-1]+sorted[mid])/2;
const costs=systems.map(s=>s.cost), conns=systems.map(s=>s.conn);
const benefits=systems.map((s,i)=>s.pop*(s.failing?1:1-Math.pow(1-s.pf,5))*(1+(raw[i]??med)));
for(const row of summary.comparison){const chosen=opt.optimize(costs,benefits,conns,row.budget_musd*1e6);const people=chosen.reduce((n,i)=>n+systems[i].pop,0);const spent=chosen.reduce((n,i)=>n+costs[i],0);if(people!==row.optimizer.people||Math.round(spent/1e5)/10!==row.optimizer.spent_musd)throw Error('Default plan mismatch '+row.budget_musd);}
console.log(JSON.stringify({matched:summary.comparison.length}));
