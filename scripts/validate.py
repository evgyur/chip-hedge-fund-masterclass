"""Focused public-layer validation; no access to credential stores."""
from pathlib import Path
import argparse,hashlib,json,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
PATTERNS={
 'private-key':r'-----BEGIN [A-Z ]*PRIVATE KEY-----',
 'credential-shaped':r'(?:gh[pousr]_|sk-proj-|sk-or-v1-)[A-Za-z0-9_-]{20,}',
 'jwt-shaped':r'eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}',
 'operator-home':r'/(?:home|Users)/[^/\s<>]+/\.(?:hermes|openclaw)/',
 'private-chat-link':r'https?://t\.me/c/\d+',
 'literal-wallet':r'0x[a-fA-F0-9]{40}\b',
}

def validate(root=ROOT):
 root=Path(root);problems=[];s=(root/'SKILL.md').read_text();desc=re.search(r'^description: (.+)$',s,re.M)
 if not desc or len(desc[1])>60 or not desc[1].endswith('.'):problems.append(('SKILL.md','description'))
 for needle in ['references/tradingview.md','references/alfa-mcp.md','references/parallel.md','references/dashboard.md','references/risk.md','references/permissions.md','SKILL_ROOT','Только чтение','не инвестиционная рекомендация']:
  if needle not in s:problems.append(('SKILL.md','missing '+needle))
 for p in [root/'SKILL.md',*sorted((root/'references').glob('*.md'))]:
  for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
   if target.startswith(('https://','http://','#')):continue
   q=(p.parent/target.split('#')[0]).resolve()
   if not q.is_relative_to(root.resolve()) or not q.exists():problems.append((str(p.relative_to(root)),'broken link '+target))
 own=[p for p in root.rglob('*') if p.is_file() and not any(x in p.relative_to(root).parts for x in ['.git','vendor','__pycache__','output','runtime']) and p.suffix not in ['.pyc','.png','.jpg','.webp']]
 for p in own:
  text=p.read_text(errors='strict')
  for label,rx in PATTERNS.items():
   if re.search(rx,text):problems.append((str(p.relative_to(root)),label))
 prov=json.loads((root/'PROVENANCE.json').read_text())['tradingview-chip']
 for f,h in prov['files'].items():
  p=root/'vendor/tradingview-chip'/f
  if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=h:problems.append(('vendor/'+f,'pin changed'))
 if (root/'.github').exists():problems.append(('.github','hosted automation not assigned'))
 return problems

if __name__=='__main__':
 failures=validate();print(json.dumps({'public_layer_findings':failures,'vendor':'byte pins checked separately against public source'},ensure_ascii=False,indent=2));raise SystemExit(bool(failures))
