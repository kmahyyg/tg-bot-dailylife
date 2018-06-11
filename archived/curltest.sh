#!/bin/bash
#curl -H 'Content-Type: application/json' -X POST -d '{"name":"yyg2","tel":"111211"}' http://127.0.0.1:5000
curl -X DELETE 'http://127.0.0.1:5000/api/checktel?name=yyg3'
exit 0
