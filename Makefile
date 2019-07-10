.PHONY: all server

all: data/all.json

data:
	mkdir -p $@

data/all.json: data
	./main.py > $@

server:
	python -m http.server

open:
	firefox http://localhost:8000/

serve:
	python -m http.server &
	sleep 1
	firefox http://localhost:8000/
