FROM python:3.10
WORKDIR /usr/src/app_1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["flask", "run"]