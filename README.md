# 📈 Stock Valuation Class

This project provides a simple **stock valuation tool** using the [Financial Modeling Prep API](https://site.financialmodelingprep.com/developer/docs).  
It calculates the **Intrinsic Ratio** for a given stock based on free cash flow, return on equity, reinvestment rate, and a discounted cash flow (DCF) approach.  

---

## 🚀 Features
- Fetches **balance sheet**, **cash flow**, and **market cap** data via FMP API  
- Computes **Free Cash Flow (FCF)** using operating cash flow, capex, and debt changes  
- Estimates **Return on Equity (ROE)** and **Reinvestment Rate**  
- Caps growth assumptions to a conservative **5% max**  
- Calculates a **Discounted Cash Flow valuation**  
- Returns the **Intrinsic Ratio** which is the DCF market value relative to current market cap  
- Run directly from the **command line**  
- You can also run a **docker container** for ease of reproduction

---

## 📂 Project Structure

| File | Description |
|----------|-------------|
| `fast_company_valuator_class.py` | # Main class + CLI entry point
| `fast_company_valuator.ipynb` | # Step by step thought process
| `.env` | # Store your FMP API key here
| `.gitignore` | # Add .env to avoid sharing API key
| `Dockerfile` | #Use this to create a docker image and container
| `requirements.txt` | #All project dependencies and packages
| `.dockerignore` | #Add files that don't need to be considered when creating container
|| `README.md` |


---

## ⚙️ Installation (Option 1)

1. Clone the repo
   ```bash  
   git clone https://github.com/sergiobk201/fast_company_valuator.git
   cd fast_company_valuator
   ```
2. Install dependencies  
   ```bash
   pip install pandas numpy python-dotenv pyarrow fmpapi  
   ```
3. Set up environment variables  
   Create a `.env` file in the project root:  
   FMP_API_KEY=your_api_key_here  

You can get a free API key from [Financial Modeling Prep API](https://site.financialmodelingprep.com/developer/docs)

---

## ⚙️ Installation (Option 2)

1. Clone the repo
   ```bash  
   git clone https://github.com/sergiobk201/fast_company_valuator.git
   cd fast_company_valuator
   ```
2. Build your docker container
   ```bash
   docker build -t choose_name .
   ```
3. Run docker container with API, stock ticker and discount rate 
   Create a `.env` file in the project root:  
   FMP_API_KEY=your_api_key_here
   ```bash
   docker run --env-file .env choose_name 'TICKER' 0.1
   ```  

You can get a free API key from [Financial Modeling Prep API](https://site.financialmodelingprep.com/developer/docs)

---

## 🖥️ Usage

Run from terminal:
```bash
python fast_company_valuator_class.py AAPL 0.1  
```
- `AAPL` → Stock ticker  
- `0.1` → Cost of equity (10%)  

Example output:  
Intrinsic Ratio: 1.18  

An Instrinsic Ratio > 1 means the stock may be undervalued relative to DCF.  
An Intrinsic Ratio < 1 means it may be overvalued.  

---

Use in Python:  
```python
from fast_company_valuator_class import StockValuation  

sv = StockValuation("MSFT", 0.08)  # 8% cost of equity  
ir = sv.get_ir()  
print("Intrinsic Ratio:", ir)  
```
---

## 📊 Formula Highlights
- Free Cash Flow (FCF):  
  FCF = Operating Cash Flow + CapEx + Debt Taken - Debt Paid 

- Growth Rate:  
  Growth = avg(ROE) * avg(Reinvestment Rate)  
  (capped at 5%)  

- DCF Valuation:  
  Value = (FCF × (1 + g)) + ((FCF × (1 + g)²) / (Cost of Equity – g))  

---

