const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),C=require(path.join(root,'scripts/portfolio_core.js')),d=JSON.parse(fs.readFileSync(path.join(root,'assets/combined-demo.json'),'utf8'));
let r=C.calculate(d);assert.equal(r.rows.length,5);assert.equal(r.byCurrency.USD.gross,12400);assert.equal(r.byCurrency.USD.pnl,400);assert.equal(r.byCurrency.USD.stress,-372);assert.equal(r.byCurrency.RUB.gross,190000);assert.equal(r.byCurrency.RUB.pnl,2000);assert.equal(r.byCurrency.RUB.stress,-5700);
assert.equal(C.calculate(d,{shift:0}).byCurrency.USD.stress,0);assert.equal(C.calculate(d,{shift:3}).byCurrency.RUB.stress,5700);
const a=structuredClone(d);a.accounts.push(a.accounts[0]);assert.throws(()=>C.validate(a));const b=structuredClone(d);b.accounts[1].positions[0].multiplier=10;assert.throws(()=>C.validate(b));const c=structuredClone(d);c.accounts[0].positions[0].mark_price=null;assert.equal(C.calculate(c).byCurrency.USD.prices_complete,false);
const f={kind:'future',signed_size:-2,mark_price:100,entry_price:120,multiplier:5};assert.equal(C.position(f).notional,-1000);assert.equal(C.position(f).pnl,200);
console.log('Synthetic portfolio math: 5 rows; native USD/RUB; 0/−3/+3%; shorts; contract multiplier; null and invalid cases passed');
