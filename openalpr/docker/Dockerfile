# openalpr image
FROM parkearly/openalpr

# install aws cli
RUN apt-get update && apt-get install -y awscli

COPY init.sh /usr/local/bin/init.sh
RUN chmod +x /usr/local/bin/init.sh

ENTRYPOINT ["/usr/local/bin/init.sh"]