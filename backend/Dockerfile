FROM python:3

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 3001

CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "3001", "--reload"]

