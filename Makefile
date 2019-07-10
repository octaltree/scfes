all: data/all.json

data:
	mkdir -p $@

data/all.json: data
	./main.py > $@
