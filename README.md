# dev-python-web-api-flask-orientdb-simple

## Description
Creates an api of `dog` table.

Remotely tested with *testify*.

## Tech stack
- python
  - flask
  - orientdb
  - testify
  - requests

## Docker stack
- python:latest
- orientdb:latest

## To run
`sudo ./install.sh -u`
- Get all dogs: http://localhost/dogs
  - Schema name, breed, and color
- Query with params: 
  - http://localhost/dogs/name/<name>
  - http://localhost/dogs/breed/<breed>
  - http://localhost/dogs/color/<color>

## To stop
`sudo ./install.sh -d`

## For help
`sudo ./install.sh -h`
