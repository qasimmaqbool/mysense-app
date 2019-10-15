FROM python:3.7

RUN pip install boto3

ADD load.py /

ADD Predict.csv /

CMD ["python", "./load.py"]