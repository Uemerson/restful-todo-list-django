#!/bin/bash
function trap_ctrlc ()
{
    # perform cleanup here
    docker compose -f docker-compose.dev.yml down
 
    # exit shell script with error code 2
    # if omitted, shell script will continue execution
    exit 2
}

trap "trap_ctrlc" 2
docker compose -f docker-compose.dev.yml --env-file .env.dev up -d --build --remove-orphans
docker compose -f docker-compose.dev.yml logs -f --tail=15 api