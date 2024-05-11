#pragma once

#include <iostream>
#include <string>
#include "Car.h"

class Person
{
public:
    const std::string id;
    Car* myCar = nullptr; // Car this person is in 

    Person(std::string name) : id(name) {}

    // if not in car/already put on does nothing
    void putOnSeatBelt()
    {
        std::cout << id << ": Putting on seat belt" << std::endl;
    }

    // if not in car/already taken off does nothing
    void takeOffSeatBelt()
    {
        std::cout << id << ": Taking off seat belt" << std::endl;
    }

    void enterCarAsDriver(Car &c)
    {
        std::cout << id << ": entering Car (" << c.id << ") as driver" << std::endl;
        myCar = &c;
    }

    void enterCarAsPassenger(Car &c) {
        std::cout << id << ": entering Car (" << c.id << ") as passenger" << std::endl;
        myCar = &c;
    }

    void exitCar() {
        std::cout << id << ": exiting Car" << std::endl;
        myCar = nullptr;
    }
};