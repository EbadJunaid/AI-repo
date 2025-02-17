CC=g++

all : bin/source

bin/source : source.cpp
	@mkdir -p bin
	${CC} source.cpp -o bin/source

run : bin/source
	@bin/source

clean : 
	rm -rf bin/*
