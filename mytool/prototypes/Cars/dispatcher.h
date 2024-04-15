#pragma once

#include "Car.h"
#include "monitor.h"

class Dispatcher
{
private:
    Spec1_Monitor monitor {};

public:
    void receive_createCar(Car& c);
    void receive_driverEnter(Car& c);
    void receive_drive(Car& c);
};
