FROM debian:stretch

ENV SPAMASSASSIN_VERSION 3.4.2

# Install spamassassin & # supervisor
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        supervisor \
        spamassassin=${SPAMASSASSIN_VERSION}* 

COPY spamd.sh /

COPY supervisor.conf /

CMD ["/usr/bin/supervisord", "-c", "supervisor.conf"]
