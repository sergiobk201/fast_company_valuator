import pandas as pd 
import numpy as np
import os
from fmpapi import fmp_get
from dotenv import load_dotenv
import pyarrow
from datetime import date

load_dotenv()
api_key = os.getenv('FMP_API_KEY')

class StockValuation:
    def __init__(self, ticker, cost):
        self.ticker = ticker
        self.cost = cost

    def get_mos(self):

        bs = fmp_get(
        resource="balance-sheet-statement", 
        symbol=self.ticker, 
        params={"period": "annual", "limit": 5},
        to_pandas=True
        )

        self.bs = bs

        cf = fmp_get(
            resource='cash-flow-statement',
            symbol=self.ticker,
            params={'period':'annual', 'limit':5},
            to_pandas=True
        )
        self.cf = cf

        cf_cfo = cf['operating_cash_flow']
        cf_capex = cf['capital_expenditure']
        cf_net_debt = cf['debt_repayment']
        
        fcf = cf_cfo + cf_capex + cf_net_debt
        fcf_df = pd.DataFrame(fcf)
        fcf_df.columns = ['free_cash_flow']
        today_fcf = np.average(fcf_df['free_cash_flow'])
        roe = cf['net_income'] / bs['total_equity']
        roe = pd.DataFrame(roe)
        roe.columns = ['roe']
        avg_roe = np.average(roe['roe'])

        reinv_rate = (cf['net_income'] + cf ['dividends_paid']) / cf['net_income']
        reinv_rate = pd.DataFrame(reinv_rate)
        reinv_rate.columns = ['reinv_rate']
        reinv_rate_avg = np.average(reinv_rate['reinv_rate'])
        
        growth = avg_roe * reinv_rate_avg
        real_growth = 0
        if growth > 0.05:
            real_growth = 0.05
        else:
            pass

        cost_e = self.cost

        real_growth

        dcf = (today_fcf * (1+real_growth)) + ((today_fcf * ((1+real_growth)**2))/(cost_e - real_growth))

        today = date.today()

        market_cap = fmp_get(
            resource='market-capitalization',
            symbol=self.ticker,
            params= {'date': f'{today.year}-{today.month}-{today.day}'},
            to_pandas=True
        )
        ir = dcf / market_cap['market_cap']
        
        return float(ir.iloc[0])
    
if __name__ == "__main__":
    import sys
    # Example: python fast_company_valuator_class.py 100 5 0.1
    ticker = str(sys.argv[1])
    cost = float(sys.argv[2])
    
    sv = StockValuation(ticker, cost)
    print("Intrinsic Ratio:", sv.get_mos())

