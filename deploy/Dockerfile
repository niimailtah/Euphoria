#---Deployment with nginx---
FROM nginx
COPY index.html /usr/share/nginx/html
COPY nginx.default.conf /etc/nginx/conf.d/default.conf
COPY entry-point.sh /bin

ENTRYPOINT ["/bin/bash", "entry-point.sh"]
