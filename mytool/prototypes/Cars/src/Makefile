CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra

SRCS = main.cpp
HDRS = Car.h Person.h

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

clean:
	rm -f $(TARGET) $(OBJS)
