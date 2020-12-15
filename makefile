PYTHON = python2.7

.PHONY = help build run clean

FILES = input output


.DEFAULT_GOAL = help

help:
	@echo "---------------HELP-----------------"
	@echo "To run the project type make run"
	@echo "To clean the project type make clean"
	@echo "------------------------------------"

build:
	./dependencies.sh

run:
	${PYTHON} client.py

clean:
	rm -r *.pyc
