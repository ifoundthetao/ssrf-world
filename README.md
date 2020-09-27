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
The thumbnail-server will teach about basic SSRFs and how they can be used.
This has a built-in "admin" page, with weak credentials.

The niave mitigation thumbnail server will teach simple bypasses for an attacker to work on.
The mitigation here is to now allow an attacker to directly request a thumbnail from an internal server.
The goal of this is to encourage an attacker to elevate their perspective and go from
using the SSRF as its own point of attack for enumation, but to leverage JS from external resources.

The allow-list mitigation thumbnail server will teach an attacker how they can use protocol
formats, and insecure validation routines to bypass allow-list mitigations.
The mitigation here is to only allow thumbnails of allowed domains. 
This scenario makes it more difficult to leverage an external server, though not impossible.

# Basic Usage:
## Running the simple thumbnailer application:

    cd thumbnail-server ; sudo docker build -t ssrf . && sudo docker run --rm -t ssrf

## Running the thumbnail server with niave mitigations:

    cd thumbnail-server-with-niave-remediation ; sudo docker build -t ssrf-niave . && sudo docker run --rm -t ssrf-niave

## Running the thumbnail server with allow-list mitigations:

    cd thumbnail-server-with-allowlist-remediation ; sudo docker build -t ssrf-allowlist . && sudo docker run --rm -t ssrf-allowlist

