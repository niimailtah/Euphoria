
CC:=gcc

SRC=$(wildcard *.cpp)

#DEPS=
#CFLAGS+=-O0 -g3 -Wall -export-dynamic -I./ $(shell pkg-config $(DEPS) --cflags)

CFLAGS+=-O0 -g3 -Wall -export-dynamic -I./

#LDFLAGS:=$(shell pkg-config $(DEPS) --libs)
LDFLAGS=-lstdc++

OBJ=$(SRC:%.cpp=%.o)

EXEC:=./bin/eiforia

all: $(EXEC)

%.o: %.cpp
	$(CC) -c -o $@ $< $(CFLAGS)

$(EXEC): $(OBJ)
	gcc -o $@ $^ $(CFLAGS) $(LDFLAGS)

clean:
	rm -f *.o $(EXEC)
