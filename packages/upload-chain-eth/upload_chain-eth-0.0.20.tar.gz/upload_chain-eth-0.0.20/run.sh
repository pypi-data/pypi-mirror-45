#!/bin/bash
cd /HC/GIT/oracle-eth/
source ./venv/bin/activate
exec $1
#exec uploadchain_service
#exec validattion_service
#exec validattion_multiproc_service
