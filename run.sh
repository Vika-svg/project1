#!/bin/bash
export DATABASE_URL=postgres://sujkmzcxcanudr:78755cbd16e02aff67f6b69761420958fd417906f514f6a645400f8621873a54@ec2-54-75-246-118.eu-west-1.compute.amazonaws.com:5432/d18e3pvm2mtmiv
export FLASK_APP=application.py
export FLASK_DEBUG=1

flask run