#pragma once

#include <iostream>
#include <string>

class OneLaneBridge
{
public:
    const std::string id;

    OneLaneBridge(std::string id) : id(id) {
        std::cout << "OneLaneBridge (" << id << ") created" << std::endl;
    }

    void open() {
        std::cout << id << ": opening" << std::endl;
    }

    void close() {
        std::cout << id << ": closing" << std::endl;
    }


};