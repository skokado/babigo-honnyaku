FROM nginx:1.17

RUN rm -f /etc/nginx/conf.d/*.conf

COPY ./nginx/ /etc/nginx/
COPY ./static/ /static/

EXPOSE 80