#include "Spec1_dispatcher.h"

// This version of the dispatcher is only correct for non-parametric properties.

void Dispatcher::receive_createCar(Car& c) {
    monitor.__RVC_Spec1_reset();
    monitor.__RVC_Spec1_createCar();
}

void Dispatcher::receive_driverEnter(Car& c) {
    monitor.__RVC_Spec1_driverEnter();
}

void Dispatcher::receive_driverExit(Car& c) {
    monitor.__RVC_Spec1_driverExit();
}

void Dispatcher::receive_drive(Car& c) {
    monitor.__RVC_Spec1_drive();
}

