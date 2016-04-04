FROM python:2.7
ADD . / 
WORKDIR /
RUN pip install -r requirements.txt
CMD python -m "SimpleHTTPServer" 8124
EXPOSE 8124
