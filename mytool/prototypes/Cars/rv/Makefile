CXX = g++
CXXFLAGS = -std=c++11

REWRITER = ../../../lib/monitor_rewriter.py

SRCS = ../src/main.cpp dispatcher.cpp Spec1_monitor.cpp
HDRS = ../src/Car.h Spec1_monitor.h dispatcher.h

OBJS = $(SRCS:.cpp=.o)

TARGET = main


monitor:
	@../../../bin/rv-monitor -c Spec1.mop
	@python3 $(REWRITER) __RVC_Spec1_Monitor.h
	@python3 $(REWRITER) __RVC_Spec1_Monitor.cc
	@rm __RVC*


compile: $(OBJS)


%.o: %.cpp $(HDRS)
	$(CXX) $(CXXFLAGS) -c $< -o $@


instrument: monitor
	@$(MAKE) compile --no-print-directory
	@../../../bin/ag++ ../src/main.cpp dispatcher.o Spec1_monitor.o -p . -p "../src" -o $(TARGET)-instrumented

	
clean:
	@rm -f $(TARGET) $(OBJS) $(TARGET)-instrumented
	@rm -f Spec1_monitor.cpp
	@rm -f Spec1_monitor.h