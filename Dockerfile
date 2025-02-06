FROM amazonlinux:latest
RUN yum update -y && \
    yum install -y httpd


RUN cd /var/www/html

COPY . /var/www/html

EXPOSE 80

CMD ["-D", "FOREGROUND"]
ENTRYPOINT ["/usr/sbin/httpd"]