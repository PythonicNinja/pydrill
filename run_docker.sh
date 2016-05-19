#!/usr/bin/env bash

exists()
{
  command -v "$1" >/dev/null 2>&1
}

if exists docker-machine; then
    if [ "$(docker-machine status)" != "Running" ]; then
        docker-machine start
    fi
    eval "$(docker-machine env default)"
fi

screen -dm bash -c "./docker_drill_embedded.sh"

CID=$(docker ps | grep apache-drill | cut -d ' ' -f 1)
while [ "$CID" == "" ];
do
    CID=$(docker ps | grep apache-drill | cut -d ' ' -f 1)
    echo $(docker ps)
    sleep 0.25
done

echo 'Docker cid' $CID

if exists docker-machine; then
    PYDRILL_HOST=$(docker-machine ip)
    PYDRILL_PORT=8047
else
    PYDRILL_HOST='localhost'
    PYDRILL_PORT=8047
fi

export CID=$CID
export PYDRILL_HOST=$PYDRILL_HOST
export PYDRILL_PORT=$PYDRILL_PORT

echo "PYDRILL_HOST:" $PYDRILL_HOST
echo "PYDRILL_PORT:" $PYDRILL_PORT

