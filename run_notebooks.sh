#!/bin/bash

cd /workspace/notebooks && \
ls *.ipynb | sort -V | xargs jupyter nbconvert --execute --to notebook --inplace
ls *.ipynb | sort -V | xargs jupyter nbconvert --clear-output --inplace 
cd /workspace


