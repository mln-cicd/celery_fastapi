
set -e

function ping:redis() {
    docker compose exec -it redis redis-cli ping
}

TIMEFORMAT="Task completed in %3lR"
time ${@:-help}
