a.out: main.cc test.o
	g++ main.cc test.s -lwiringPi

test.o: test.s
	g++ -c test.s
