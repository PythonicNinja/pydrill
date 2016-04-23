#!/usr/bin/env bash

docker_drill_embedded.sh

docker run -it -p 8047:8047 mkieboom/apache-drill-docker /drill-scripts/bootstrap.sh
