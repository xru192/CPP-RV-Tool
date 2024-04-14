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

void Dispatcher::receive_createCar(Car& c) {
    monitor.__RVC_Spec1_createCar(c);
}

void Dispatcher::receive_driverEnter(Car& c) {
    monitor.__RVC_Spec1_driverEnter(c);
}

void Dispatcher::receive_drive(Car& c) {
    monitor.__RVC_Spec1_drive(c);
}

