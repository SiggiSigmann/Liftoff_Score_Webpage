FROM tobiassigmann/ip_collector:latest

COPY requirements.txt .
COPY startFlask.sh .
COPY server.py .
COPY dbconnector/* dbconnector/

EXPOSE 80

ENTRYPOINT [ "./startFlask.sh" ]