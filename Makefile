.PHONY: build run

default: build run

build:
	docker build -t idiamond/docker-demo .

nopersist:
	docker run --rm -it -p 5000:5000 idiamond/docker-demo

persist:
	docker run --rm -it -v `pwd`/_cache:/data/_cache -p 5000:5000 idiamond/docker-demo

run: persist
