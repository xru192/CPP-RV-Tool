#pragma once
#include <string>
#include <iostream>

class Lock {

public:
    std::string id;

    Lock (std::string id) : id(id) {} 

    void acquire() {
        std::cout << id << " acquired" << std::endl;
    }

    void release() {
        std::cout << id << " released" << std::endl;
    }
};
