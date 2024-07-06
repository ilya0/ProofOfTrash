#!/bin/bash
cd /usr/src/app/ && uvicorn server:app --host $CURRENT_HOST --port $PORT --proxy-headers