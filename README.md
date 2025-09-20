# 📈 Stock Valuation Class

This project provides a simple **stock valuation tool** using the [Financial Modeling Prep API](https://site.financialmodelingprep.com/developer/docs/).  
It calculates the **Margin of Safety (MoS)** for a given stock based on free cash flow, return on equity, reinvestment rate, and a discounted cash flow (DCF) approach.  

---

## 🚀 Features
- Fetches **balance sheet**, **cash flow**, and **market cap** data via FMP API  
- Computes **Free Cash Flow (FCF)** using operating cash flow, capex, and debt changes  
- Estimates **Return on Equity (ROE)** and **Reinvestment Rate**  
- Caps growth assumptions to a conservative **5% max**  
- Calculates a **Discounted Cash Flow valuation**  
- Returns the **Margin of Safety** relative to current market cap  
- Run directly from the **command line**  

---

## 📂 Project Structure
.
├── stock_valuation.py   # Main class + CLI entry point
├── .env                 # Store your FMP API key here
└── README.md

---

## ⚙️ Installation

1. Clone the repo  
   git clone https://github.com/yourusername/stock-valuation.git  
   cd stock-valuation  

2. Install dependencies  
   pip install pandas numpy python-dotenv pyarrow fmpapi  

3. Set up environment variables  
   Create a `.env` file in the project root:  
   FMP_API_KEY=your_api_key_here  

You can get a free API key from [Financial Modeling Prep](https://site.financialmodelingprep.com/developer/docs/).

---

## 🖥️ Usage

Run from terminal:  
python stock_valuation.py AAPL 0.1  

- `AAPL` → Stock ticker  
- `0.1` → Cost of equity (10%)  

Example output:  
Margin of Safety: 1.18  

A Margin of Safety > 1 means the stock may be undervalued relative to DCF.  
A Margin of Safety < 1 means it may be overvalued.  

---

Use in Python:  
from stock_valuation import StockValuation  

sv = StockValuation("MSFT", 0.08)  # 8% cost of equity  
mos = sv.get_mos()  
print("Margin of Safety:", mos)  

---

## 📊 Formula Highlights
- Free Cash Flow (FCF):  
  FCF = Operating Cash Flow + CapEx + Debt Taken - Debt Repaid  

- Growth Rate:  
  Growth = avg(ROE) * avg(Reinvestment Rate)  
  (capped at 5%)  

- DCF Valuation:  
  Value = (FCF × (1 + g)) + ((FCF × (1 + g)²) / (Cost of Equity – g))  

---

## ✅ Next Steps
- Add holiday/business day adjustments for valuation dates  
- Support quarterly data  
- Extend to multiple valuation methods (e.g., Graham, multiples, etc.)  
