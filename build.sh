#!/bin/bash
set -eo pipefail

PROJECT_NAME='text-improvement'
COMPONENT_NAME='similarity'


docker build . --no-cache -t ${PROJECT_NAME}-${COMPONENT_NAME}
