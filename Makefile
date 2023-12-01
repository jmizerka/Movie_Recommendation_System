.PHONY: run clean

first_run:
    python3 source/processing/clean.py
    python3 source/database/db_creator.py
    python3 source/machine_learning/vectorizers.py

run: main.py
    python3 main.pyg