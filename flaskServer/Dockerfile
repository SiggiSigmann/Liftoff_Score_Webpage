FROM tobiassigmann/ip_collector:latest

COPY requirements.txt .
COPY startFlask.sh .
COPY server.py .
COPY excleLoader.py .
COPY dbconnector/* dbconnector/
COPY html/* html/
COPY static/* static/
COPY temp/ temp/
copy creator.py .

EXPOSE 80

ENTRYPOINT [ "./startFlask.sh" ]