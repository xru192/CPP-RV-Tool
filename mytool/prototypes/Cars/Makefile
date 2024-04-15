CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra

SRCS = main.cpp monitor.cpp dispatcher.cpp
HDRS = Car.h monitor.h dispatcher.h

# Object files
OBJS = $(SRCS:.cpp=.o)

# Executable name
TARGET = main

# Compile without instrumentation
compile: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) $(OBJS) -o $(TARGET)

# Rule to compile source files into object files
%.o: %.cpp $(HDRS)
	$(CXX) $(CXXFLAGS) -c $< -o $@

run:
	$(MAKE) monitor
	$(MAKE) instrument

monitor:
	../../bin/rv-monitor -c Spec1.mop

instrument: compile
	../../bin/ag++ main.cpp monitor.o -include aspect.ah -o $(TARGET)-instrumented

clean:
	rm -f $(TARGET) $(OBJS) $(TARGET)-instrumented
	rm -f __RVC*
	rm -f *.out
	rm -f *.gch
