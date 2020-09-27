# SSRF World

Exploring SSRFs and what the impact can be

* Enumerate the internal network
* Attack another host
* Attack underlying libraries that exist for the purpose of the server-side request (i.e. thumbnailing)
* Attack the server's browser to get a shell


# Basic Usage:
Running the simple thumbnailer application is easy:

    cd thumbnail-server ; sudo docker build -t ssrf . && sudo docker run --rm -t ssrf

