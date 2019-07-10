.PHONY: all server

all: data/all.json server

data:
	mkdir -p $@

data/all.json: data
	./main.py > $@

server:
	python -m http.server
