"""Portable entrypoints for the public workshop. No secrets/config mutation."""
import argparse,json,sys,subprocess,shutil
from pathlib import Path
from decimal import Decimal
from risk import size
ROOT=Path(__file__).resolve().parents[1]


def doctor(require_tv=False):
    node=shutil.which('node');info={'python':sys.version.split()[0],'python_supported':sys.version_info>=(3,10),'node':None,'node_supported_for_tradingview':False,'connections':'Not tested: requires user-selected browser/account and separate real readback'}
    if node:
        r=subprocess.run([node,'--version'],capture_output=True,text=True,timeout=10)
        if r.returncode==0:
            info['node']=r.stdout.strip()
            try:info['node_supported_for_tradingview']=int(r.stdout.strip().lstrip('v').split('.')[0])>=24
            except ValueError:pass
    print(json.dumps(info,ensure_ascii=False,indent=2))
    return 0 if info['python_supported'] and (not require_tv or info['node_supported_for_tradingview']) else 2


def demo(output):
    p=Path(output)
    if p.is_symlink() or (p.exists() and (not p.is_dir() or any(p.iterdir()))):raise ValueError('Use a new empty output directory; existing files are never overwritten')
    p.mkdir(parents=True,exist_ok=True)
    for name in ['dashboard.html','combined-demo.json']:shutil.copyfile(ROOT/'assets'/name,p/name)
    print(json.dumps({'dashboard':str((p/'dashboard.html').resolve()),'data_mode':'synthetic sample, not connected','next':'Open dashboard.html in your browser'},ensure_ascii=False,indent=2))


def main():
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='command',required=True)
    d=sub.add_parser('doctor');d.add_argument('--require-tradingview',action='store_true')
    d=sub.add_parser('demo');d.add_argument('--output',required=True)
    r=sub.add_parser('risk')
    for flag in ['entry','stop','capital','risk']:r.add_argument('--'+flag,required=True)
    r.add_argument('--lot',required=True,type=int);r.add_argument('--fee',default='0');r.add_argument('--slippage',default='0')
    a=p.parse_args()
    try:
        if a.command=='doctor':return doctor(a.require_tradingview)
        if a.command=='demo':demo(a.output)
        else:print(json.dumps(size(Decimal(a.entry),Decimal(a.stop),a.lot,Decimal(a.risk),Decimal(a.capital),Decimal(a.fee),Decimal(a.slippage)),ensure_ascii=False,indent=2))
        return 0
    except (ValueError,ArithmeticError) as e:
        print(str(e),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
