import importlib.util,json,subprocess,sys,tempfile,unittest,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'scripts'))
from risk import size
from decimal import Decimal as D
from portfolio_model import from_alfa,combine
from validate import validate

class PublicBundleTests(unittest.TestCase):
 def test_risk_cases(self):
  for entry,fee,slip,count in [('300','0','0',50),('302','0','0',37),('300','.0005','.1',46),('302','.0005','.1',35)]:
   self.assertEqual(size(D(entry),D(294),10,D(3000),D(1000000),D(fee),D(slip))['lots'],count)
  with self.assertRaises(ValueError):size(D(290),D(294),10,D(3000),D(1000000))
 def test_real_cli_other_cwd_and_conflict(self):
  with tempfile.TemporaryDirectory() as temp:
   out=Path(temp)/'demo';cmd=[sys.executable,str(R/'scripts/workshop.py'),'demo','--output',str(out)]
   r=subprocess.run(cmd,cwd=temp,capture_output=True,text=True);self.assertEqual(r.returncode,0,r.stderr);self.assertTrue((out/'dashboard.html').exists());before=(out/'dashboard.html').read_bytes()
   r=subprocess.run(cmd,cwd=temp,capture_output=True,text=True);self.assertEqual(r.returncode,2);self.assertEqual((out/'dashboard.html').read_bytes(),before)
   r=subprocess.run([sys.executable,str(R/'scripts/workshop.py'),'risk','--entry','300','--stop','294','--lot','10','--capital','1000000','--risk','3000'],cwd=temp,capture_output=True,text=True);self.assertEqual(r.returncode,0,r.stderr);self.assertEqual(json.loads(r.stdout)['lots'],50)
 def test_synthetic_fixture(self):
  d=json.loads((R/'assets/combined-demo.json').read_text());self.assertEqual(len(d['accounts']),2)
  for a in d['accounts']:self.assertEqual(a['mode'],'sample');self.assertNotIn('wallet',a)
  self.assertEqual({a['currency'] for a in d['accounts']},{'USD','RUB'})
 def test_adapter_selected_account_and_units(self):
  raw={'as_of':'2026-01-01T00:00:00Z','positions':[{'accountId':7,'balanceGroup':'Papers','instrumentId':1,'instrumentType':'Stock','quantity':300,'price':300,'averagePrice':290,'profitLoss':3000}],'balances':[{'accountId':7,'balanceGroup':'Papers','currentBalance':1000000,'money':910000,'marginRequirement':0}],'instruments':[{'id':1,'ticker':'SBER','currencyId':0}]}
  a=from_alfa(raw,7)['accounts'][0];self.assertEqual(a['positions'][0]['signed_size'],300);self.assertEqual(a['equity'],1000000);self.assertIsNone(a['positions'][0]['liquidation_price']);self.assertNotIn('accountId',json.dumps(a))
  raw['balances'].append(dict(raw['balances'][0],balanceGroup='Unified'))
  with self.assertRaises(ValueError):from_alfa(raw,7)
 def test_no_default_wallet(self):
  r=subprocess.run([sys.executable,str(R/'scripts/build_snapshot.py')],capture_output=True,text=True);self.assertNotEqual(r.returncode,0);self.assertIn('--wallet',r.stderr)
 def test_validation_and_negative(self):
  self.assertEqual(validate(),[])
  with tempfile.TemporaryDirectory() as temp:
   x=Path(temp)/'repo';shutil.copytree(R,x,ignore=shutil.ignore_patterns('.git','__pycache__','output','runtime'));p=x/'SKILL.md';p.write_text(p.read_text().replace('Только чтение','Удалено'));self.assertTrue(any('missing Только чтение' in str(v) for v in validate(x)))
 def test_code_embedded_exactly(self):
  self.assertIn((R/'scripts/portfolio_core.js').read_text(),(R/'assets/dashboard.html').read_text())
 def test_no_hidden_runtime_or_workflow(self):
  self.assertFalse((R/'.github').exists());self.assertFalse((R/'runtime').exists());self.assertTrue((R/'licenses/manrope-OFL.txt').is_file());self.assertTrue((R/'licenses/dejavu-LICENSE.txt').is_file())

if __name__=='__main__':unittest.main()
