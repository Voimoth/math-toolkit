// 置换群枚举核验工具 —— 用于写进 wiki 前核对有限群论断
// 用法: node group_enumeration_verify.js
// 改 N 与下方筛选条件即可扩展到 S_n / A_n / D_{2n} 等小阶群。
// 无外部依赖,秒级完成。2026-09-11 实战定型(A_5 单性 / SO(3) 分类)。

const N = 5; // 改成 4、6 等

// ---------- 基础工具 ----------
function perms(n) {
  const r = [];
  const a = [...Array(n).keys()];
  const rec = (k) => {
    if (k === n) { r.push(a.slice()); return; }
    for (let i = k; i < n; i++) { [a[k], a[i]] = [a[i], a[k]]; rec(k + 1); [a[k], a[i]] = [a[i], a[k]]; }
  };
  rec(0);
  return r;
}
function sign(p) { let s = 1; for (let i = 0; i < p.length; i++) for (let j = i + 1; j < p.length; j++) if (p[i] > p[j]) s = -s; return s; }
function mul(a, b) { return a.map((_, i) => a[b[i]]); }          // a∘b
function inv(a) { const r = []; a.forEach((v, i) => r[v] = i); return r; }
function eql(a, b) { return a.every((v, i) => v === b[i]); }
function key(a) { return a.join(' '); }
function order(a) { let x = a.slice(), o = 1; while (!eql(x, a.map((_, i) => i))) { x = mul(x, a); o++; } return o; }

// ---------- 1. 元素阶分布 ----------
function orderDistribution(G) {
  const d = {};
  for (const g of G) { const o = order(g); d[o] = (d[o] || 0) + 1; }
  return d;
}

// ---------- 2. 共轭类大小(在给定群 G 内) ----------
function conjugacyClasses(G) {
  const seen = new Set(), out = [];
  for (const x of G) {
    if (seen.has(key(x))) continue;
    const cl = new Set();
    for (const g of G) cl.add(key(mul(mul(g, x), inv(g))));
    const arr = [...cl];
    arr.forEach(s => seen.add(s));
    out.push({ size: arr.length, order: order(x), rep: key(x) });
  }
  return out.sort((a, b) => a.order - b.order || a.size - b.size);
}

// ---------- 3. 正规性判定 ----------
function isNormal(H, G) {
  const Hk = new Set(H.map(key));
  for (const g of G) for (const h of H) if (!Hk.has(key(mul(mul(g, h), inv(g))))) return false;
  return true;
}

// ---------- 4. 导群(换位子生成的子群) ----------
function derivedSubgroup(G) {
  const coms = [];
  for (const x of G) for (const y of G) coms.push(mul(mul(x, y), mul(inv(x), inv(y))));
  const gens = [...new Set(coms.map(key))].map(k => k.split(' ').map(Number));
  let H = [G[0].map((_, i) => i)];
  let changed = true;
  while (changed) {
    changed = false;
    for (const g of gens) for (const h of H.slice()) {
      const p = mul(g, h);
      if (!H.some(q => key(q) === key(p))) { H.push(p); changed = true; }
    }
  }
  return H;
}

// ---------- 跑一遍 ----------
const S = perms(N);
const A = S.filter(p => sign(p) === 1);

console.log(`|S_${N}| = ${S.length}   |A_${N}| = ${A.length}`);
console.log('阶分布 (S):', orderDistribution(S));
console.log('阶分布 (A):', orderDistribution(A));

console.log(`\nA_${N} 共轭类 (阶, 大小):`);
for (const c of conjugacyClasses(A)) console.log(`   order ${c.order}  size ${c.size}`);

// 阶数自洽检查(常见坑)
console.log('\n整除自洽检查:');
for (const k of [16, 21, 25]) console.log(`   ${k} | ${A.length} ? ${A.length % k === 0}`);

// N=4 时额外看 Klein 四元群
if (N === 4) {
  const V = A.filter(p => order(p) <= 2);
  console.log(`\nA_4 中阶 ≤2 的子群 V: ${V.length} 个元素; V ◁ A_4 ? ${isNormal(V, A)}; V ◁ S_4 ? ${isNormal(V, S)}`);
  console.log(`A_4 中 2 阶元: ${A.filter(p => order(p) === 2).length}  3 阶元: ${A.filter(p => order(p) === 3).length}`);
}

// 导群
if (N === 4) console.log(`\n|D(S_4)| = ${derivedSubgroup(S).length}  (应 = 12 = |A_4|)`);
if (N === 5) console.log(`\n|D(A_5)| = ${derivedSubgroup(A).length}  (应 = 60,A_5 是完美群)`);
