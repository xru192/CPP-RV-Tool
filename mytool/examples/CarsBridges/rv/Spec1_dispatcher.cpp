#include "Spec1_dispatcher.h"

void Dispatcher::receive_takeBridge(Car& c, OneLaneBridge& b) {
    theta_t theta = {&c, nullptr, &b};
    receive(0, theta);
}

void Dispatcher::receive_exitBridge(Car& c, OneLaneBridge& b) {
    theta_t theta = {&c, nullptr, &b};
    receive(1, theta);
}

void Dispatcher::receive_enterCar(Car& c, Person& p) {
    theta_t theta = {&c, &p, nullptr};
    receive(2, theta);
};

void Dispatcher::receive_exitCar(Car& c, Person& p) {
    theta_t theta = {&c, &p, nullptr};
    receive(3, theta);
};

