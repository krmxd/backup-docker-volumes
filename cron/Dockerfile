FROM alpine:3.16

RUN apk update && \
    apk add --no-cache docker-cli docker-cli-compose

COPY run_backup.sh /etc/periodic/daily/run_backup

RUN chmod +x /etc/periodic/daily/run_backup

WORKDIR /workdir

CMD ["crond", "-f", "-l", "0"]