FROM lscr.io/linuxserver/brave:latest

ENV PUID=1000 \
    PGID=1000 \
    TZ=Etc/UTC

EXPOSE 3000
EXPOSE 3001

VOLUME ["/config"]
