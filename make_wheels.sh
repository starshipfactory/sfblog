#!/bin/bash
rm ./wheels/*.whl
pip wheel -w ./wheels/ -r requirements.txt
