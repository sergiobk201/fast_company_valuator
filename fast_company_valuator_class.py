import pandas as pd 
import numpy as np
import os
import requests
from dotenv import load_dotenv
import pyarrow
from datetime import date

load_dotenv()
api_key = os.getenv('FMP_API_KEY')

class StockValuation:
    def __init__(self, ticker, cost):
        self.ticker = ticker
        self.cost = cost

    def get_ir(self):

        bs_response = requests.get(
            f'https://financialmodelingprep.com/stable/balance-sheet-statement?symbol={self.ticker}&apikey={api_key}'

            )

        bs_json = bs_response.json()
        bs = pd.DataFrame(bs_json)
        self.bs = bs

        cf_response = requests.get(
            f'https://financialmodelingprep.com/stable/cash-flow-statement?symbol={self.ticker}&apikey={api_key}'
            )

        cf_data = cf_response.json()
        cf = pd.DataFrame(cf_data)
        self.cf = cf

        cf_cfo = cf['operatingCashFlow']
        cf_capex = cf['capitalExpenditure']
        cf_net_debt = cf['netDebtIssuance']
        
        fcf = cf_cfo + cf_capex + cf_net_debt
        fcf_df = pd.DataFrame(fcf)
        fcf_df.columns = ['free_cash_flow']
        today_fcf = np.average(fcf_df['free_cash_flow'])
        roe = cf['netIncome'] / bs['totalEquity']
        roe = pd.DataFrame(roe)
        roe.columns = ['roe']
        avg_roe = np.average(roe['roe'])

        reinv_rate = (cf['netIncome'] + cf ['netDividendsPaid']) / cf['netIncome']
        reinv_rate = pd.DataFrame(reinv_rate)
        reinv_rate.columns = ['reinv_rate']
        reinv_rate_avg = np.average(reinv_rate['reinv_rate'])
        
        growth = avg_roe * reinv_rate_avg

        real_growth = 0
        if growth > 0.05:
            real_growth = 0.05
        elif growth < 0:
            real_growth = 0    
        else:
            real_growth = growth

        cost_e = self.cost

        dcf = (today_fcf * (1+real_growth)) + ((today_fcf * ((1+real_growth)**2))/(cost_e - real_growth))

        mk_cap_response = requests.get(
            f'https://financialmodelingprep.com/stable/market-capitalization?symbol={self.ticker}&apikey={api_key}'
        )
        mkcap = mk_cap_response.json()
        market_cap = pd.DataFrame(mkcap)
        ir = dcf / market_cap['marketCap']
        
        return float(ir.iloc[0])
    
if __name__ == "__main__":
    import sys
    # Example: python fast_company_valuator_class.py 100 5 0.1
    ticker = str(sys.argv[1])
    cost = float(sys.argv[2])
    
    sv = StockValuation(ticker, cost)
    print("Intrinsic Ratio:", sv.get_ir())

