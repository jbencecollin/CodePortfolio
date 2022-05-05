# Build targets
# lm - link math library library. required if you use math.h functions (commonly
# linked by default on mac).

problem2a: problem2a.o
	gcc -Wall -o problem2a -g -lm problem2a.o

problem2c: problem2c.o
	gcc -Wall -o problem2c -g -lm problem2c.o

problem3: problem3.o
	gcc -Wall -o problem3 -g -lm problem3.o

problem2a.o: problem2a.c
	gcc -c problem2a.c -Wall -g

problem2c.o: problem2c.c
	gcc -c problem2c.c -Wall -g

problem3.o: problem3.c
	gcc -c problem3.c -Wall -g
