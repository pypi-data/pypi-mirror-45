#!/bin/bash
cd /HC/GIT/upload-chain-eth/
source ./venv/bin/activate
exec $1
#exec uploadchain_service
#exec validation_service
#exec validation_multiproc_service
