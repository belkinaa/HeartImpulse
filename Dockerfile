FROM python:3.9
WORKDIR /app
RUN pip3 install -r req.txt
EXPOSE 5000