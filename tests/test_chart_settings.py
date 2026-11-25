from pathlib import Path
import json,unittest
R=Path(__file__).resolve().parents[1]
class ChartSettingsTests(unittest.TestCase):
 def test_observed_parameters_and_boundaries(self):
  d=json.loads((R/'assets/birzhevik-chart-settings.json').read_text());s=d['observed_settings']
  self.assertFalse(d['method_verified']);self.assertEqual(s['ema']['periods'],[9,50,100,200]);self.assertEqual(s['ema']['source'],'close');self.assertEqual(s['bollinger'],{'length':20,'basis':'SMA','source':'close','multiplier':2});self.assertEqual(s['cci']['source'],'hlc3');self.assertEqual(s['cci']['length'],20);self.assertEqual(s['rsi']['length'],14);self.assertEqual(s['mfi']['length'],14);self.assertFalse(d['visual_reference']['exact_rgb_values_verified']);self.assertEqual(len(d['public_sources']),3)
 def test_installation_is_manual_and_discoverable(self):
  guide=(R/'references/birzhevik-chart.md').read_text()
  for phrase in ['не импортируемый шаблон','только для чтения','ограничивает число индикаторов','chart-setup.md','реконструкция']:self.assertIn(phrase,guide)
  for name in ['README.md','SKILL.md','references/tradingview.md']:self.assertIn('birzhevik-chart.md',(R/name).read_text())
if __name__=='__main__':unittest.main()
