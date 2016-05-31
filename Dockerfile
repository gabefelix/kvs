FROM python:2.7
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt requests==2.10.0
EXPOSE 49160
EXPOSE 49161
EXPOSE 49612
EXPOSE 12345
EXPOSE 12346
EXPOSE 12347
ENTRYPOINT ["python"]
CMD ["hello.py"]