CC = gcc

default: libadd.a

libadd.a: add.o
	ar rcs $@ $^

add.o: add.c add.h
	$(CC) -c $<

clean:
	rm *.o *.a