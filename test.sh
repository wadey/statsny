#!/bin/bash

set -e
set -o pipefail

HOST="${1:-localhost}"
PORT="${2:-9026}"

if [ "$(uname)" = "Darwin" ]
then NC="nc -4u -w1"
else NC="nc -4u -q1"
fi

_payload() {
    cat <<EOF
    {
        "endpoint":  "/users/:user",
        "method":    "GET",
        "code":      $1,
        "elapsed":   $2,

        "stats": {
            "load-user-from-db": 1000,
            "validate-token":    50
        },

        "groups": {
            "product": "users"
        },

        "timestamp": 1234567890000,
        "path":      "/users/alice",
        "ip":        "127.0.0.1",

        "request_id": "ABCDEF012345"
    }
EOF
}

set -x
_payload 200 100 | $NC "$HOST" "$PORT"
_payload 200 500 | $NC "$HOST" "$PORT"
_payload 500 3000 | $NC "$HOST" "$PORT"
