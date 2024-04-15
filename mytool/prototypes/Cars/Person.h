#pragma once

#include "Car.h"

class Person
{
    public:
    void putOnSeatBelt() {}   // if not in car/already put on does nothing
    void takeOffSeatBelt() {} // if not in car/already taken off does nothing

    void enterCarAsDriver(Car& c) {}
    void enterCarAsPassenger(Car& c) {}
    void exitCar() {}
};