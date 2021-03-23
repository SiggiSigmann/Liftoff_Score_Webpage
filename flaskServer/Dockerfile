FROM tobiassigmann/ip_collector:latest

COPY requirements.txt .
COPY startFlask.sh .
COPY server.py .
COPY dbconnector/* dbconnector/
COPY html/* html/
COPY static/* static/
COPY temp/ temp/

EXPOSE 80

ENTRYPOINT [ "./startFlask.sh" ]