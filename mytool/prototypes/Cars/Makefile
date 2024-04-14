all: run

run:
	$(MAKE) monitor
	$(MAKE) instrument

monitor:
	../../bin/rv-monitor -c Spec1.mop

instrument:
	../../bin/ag++ main.cpp -include aspect.ah

clean:
	rm -f __RVC*
	rm -f *.out