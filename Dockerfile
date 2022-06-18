FROM python:latest
ADD src /src
ADD requirements.txt /
RUN python3 -m pip install -r requirements.txt
CMD [ "python", "src/server.py" ]
