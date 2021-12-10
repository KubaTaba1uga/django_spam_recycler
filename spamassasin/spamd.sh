#!/bin/bash

spamd --username debian-spamd \
      --nouser-config \
      --syslog stderr \
      --pidfile /var/run/spamd.pid \
      --helper-home-dir /var/lib/spamassassin \
      -i \
      -A 0.0.0.0/0 \
      -p ${PORT}
