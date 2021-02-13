#!/bin/bash
curl -X POST -H 'Accept:application/json' -H 'Content-Type: application/json' --data @configs/postgres-source.json http://localhost:8083/connectors
echo "Config successfully posted"