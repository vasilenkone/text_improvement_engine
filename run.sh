#!/bin/bash
set -eo pipefail


PROJECT_NAME='text-improvement'
COMPONENT_NAME='similarity'


docker run -p 8000:8000 ${PROJECT_NAME}-${COMPONENT_NAME}