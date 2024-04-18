#include "dispatcher.h"

void Dispatcher::receive_createCar(Car& c) {
    monitor.__RVC_Spec1_reset();
    monitor.__RVC_Spec1_createCar(c);
}

void Dispatcher::receive_driverEnter(Car& c) {
    monitor.__RVC_Spec1_driverEnter(c);
}

void Dispatcher::receive_driverExit(Car& c) {
    monitor.__RVC_Spec1_driverExit(c);
}

void Dispatcher::receive_drive(Car& c) {
    monitor.__RVC_Spec1_drive(c);
}

