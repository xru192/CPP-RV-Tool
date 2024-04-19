#pragma once

#include <iostream>
#include <string>

class Car
{
public:
    const std::string id;

    Car(std::string id) : id(id) {
        std::cout << "Car (" << id << ") created" << std::endl;
    }

    void drive() {
        std::cout << id << ": driving" << std::endl;
    }

    void park() {
        std::cout << id << ": parking" << std::endl;
    }


};