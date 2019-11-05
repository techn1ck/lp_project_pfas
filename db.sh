#!/bin/sh
python utils/db_drop.py
python utils/db_create.py
python utils/db_fill.py