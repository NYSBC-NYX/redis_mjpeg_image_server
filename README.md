# redis_to_mjpeg


stream url is localhost:8000/video_feed

virtual_environment is the python virtual_environment

testing has python code to help testing

running with uWSGI
for 5 connections
uwsgi --socket 10.67.147.26:3909 --protocol http --master -p 5 -w wsgi:app 