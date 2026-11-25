from decimal import Decimal,ROUND_FLOOR
import json
D=Decimal

def size(entry,stop,lot,risk,capital,fee=D(0),slip=D(0)):
 vals=[entry,stop,risk,capital,fee,slip]
 if any(not x.is_finite() for x in vals) or not isinstance(lot,int) or isinstance(lot,bool) or lot<=0 or risk<=0 or capital<=0 or stop<=0 or entry<=stop or fee<0 or slip<0 or stop-slip<=0:
  raise ValueError('Invalid educational long inputs')
 exit=stop-slip
 risk_per_lot=((entry-exit)+fee*(entry+exit))*lot
 cash_per_lot=entry*(1+fee)*lot
 n=min(int((risk/risk_per_lot).to_integral_value(rounding=ROUND_FLOOR)),int((capital/cash_per_lot).to_integral_value(rounding=ROUND_FLOOR)))
 assert n>=0 and n*risk_per_lot<=risk and n*cash_per_lot<=capital
 assert (n+1)*risk_per_lot>risk or (n+1)*cash_per_lot>capital
 return dict(lots=n,shares=n*lot,nominal=str(entry*n*lot),fees=str(fee*(entry+exit)*n*lot),loss=str(n*risk_per_lot),free_capital=str(capital-n*cash_per_lot))
