tmper : temp file sharing
=========================

A very simple file sharing utility that launches quickly and allows sharing
files between many people with a set number of downloads (default 1, max 10).

If there is an existing server then you can easily interact with it through
the command line interface. In this case, set the global url option then
upload and download::

    tmper c --url=http://some.url.com/       # configure a global url
    tmper u /some/file                       # upload a file and receive code
    tmper d <code>                           # download file code

For more information, look into tmper --help. If there is no server you can
easily start one yourself. In the basic form, simply run::

    tmper s      # 's' is short for serve, see tmper --help

and point your browser to http://127.0.0.1:8888.  From there, you can follow
the directions to upload and download files.  By default, it only runs on the
local interface. 

nginx setup
===========

It is recommended that if you wish the server to be available remotely to run
it behind a webserver such as nginx or apache with forwarding set up between
the two (so root privileges are not required).  Here is a sample setup,
especially for larger max file sizes and rate-limiting requests::

    limit_req_zone $binary_remote_addr zone=tmper:10m rate=1r/s;

    server {
        listen 80;

        root /var/www/;
        index index.html index.htm;
        server_name <server-url>;

        location / {
            client_body_buffer_size    1M;
            client_max_body_size       128M;
            error_page 413 /error-size;
            limit_req zone=tmper burst=3;

            proxy_pass http://localhost:3333;
            proxy_set_header Host $http_host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }

Additionally, it is always recommended to employ SSL, however we do not cover
that topic here. For information about obtaining certificates and using them,
please refer to https://letsencrypt.org/
