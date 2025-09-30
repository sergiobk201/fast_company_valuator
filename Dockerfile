FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY fast_company_valuator_class.py .

ENTRYPOINT [ "python", "fast_company_valuator_class.py"]

