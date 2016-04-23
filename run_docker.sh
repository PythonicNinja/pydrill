#!/usr/bin/env bash
set -e

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
echo 'Docker cid' $CID
while [ "$CID" == "" ];
do
    CID=$(docker ps | grep apache-drill | cut -d ' ' -f 1)
done


if exists docker-machine; then
    PYDRILL_HOST=$(docker-machine ip)
    PYDRILL_PORT=8047
else
    echo "You don't use docker-machine"
    PYDRILL_HOST=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' ${CID})
    PYDRILL_PORT=8047
fi

export CID=$CID
export PYDRILL_HOST=$PYDRILL_HOST
export PYDRILL_PORT=$PYDRILL_PORT

echo "PYDRILL_HOST:" $PYDRILL_HOST
echo "PYDRILL_PORT:" $PYDRILL_PORT

