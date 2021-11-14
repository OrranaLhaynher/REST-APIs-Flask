FROM python:3.10
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pip install ./pt_core_news_sm-3.1.0.tar.gz
CMD ["python", "app.py"]