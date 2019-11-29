#!/bin/bash

while :; do
  if ping -c1 8.8.8.8 >/dev/null; 
  then
    echo "connect to the internet"
    break
  else
    echo "there is no connection to the internet"
  fi
  sleep 10; 
done

nohup python3 kurs.py
SUB='DISCONNECTED'

while :; do
  STAT=`windscribe status`
  if [[ "$STAT" == *"$SUB"* ]]; then
    echo "there is no connection to the windscribe"
  else
    echo "connected to windscribe"
    break
  fi
  sleep 10; 
done

nohup python3 weather_bot.py
