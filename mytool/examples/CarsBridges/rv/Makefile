CXX = g++
CXXFLAGS = -std=c++11

REWRITER = ../../../lib/monitor_rewriter.py

# Name of the .mop file to use
SPECNAME = Spec1

SRCS = ../src/main.cpp $(SPECNAME)_dispatcher.cpp $(SPECNAME)_monitor.cpp
HDRS = ../src/Car.h ../src/Person.h ../src/OneLaneBridge.h $(SPECNAME)_monitor.h $(SPECNAME)_dispatcher.h

OBJS = $(SRCS:.cpp=.o)

TARGET = main


monitor:
	@../../../bin/rv-monitor -c $(SPECNAME).mop
	@python3 $(REWRITER) __RVC_$(SPECNAME)_Monitor.h
	@python3 $(REWRITER) __RVC_$(SPECNAME)_Monitor.cc
	@rm __RVC*
	@echo Monitors for $(SPECNAME) rewritten for my tool


compile: $(OBJS)


%.o: %.cpp $(HDRS)
	@$(CXX) $(CXXFLAGS) -c $< -o $@


instrument: 
	@$(MAKE) monitor
	@$(MAKE) compile --no-print-directory
	@../../../bin/ag++ ../src/main.cpp $(SPECNAME)_dispatcher.o $(SPECNAME)_monitor.o -p . -p "../src" -a $(SPECNAME).ah -o $(TARGET)-instrumented-$(SPECNAME)

	
clean:
	@rm -f $(TARGET) $(OBJS) $(TARGET)-instrumented-*
	@rm -f $(SPECNAME)_monitor.cpp
	@rm -f $(SPECNAME)_monitor.h