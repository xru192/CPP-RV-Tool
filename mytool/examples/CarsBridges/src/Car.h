#pragma once

#include <iostream>
#include <string>
#include "OneLaneBridge.h"

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

    void enterBridgeEast(OneLaneBridge bridge) {
        std::cout << id << ": entering bridge " << bridge.id << " from East" << std::endl;
    }

    void enterBridgeWest(OneLaneBridge bridge) {
        std::cout << id << ": entering bridge " << bridge.id << " from West" << std::endl;
    }

    void exitBridge(OneLaneBridge bridge) {
        // TODO: remove bridge param
        std::cout << id << ": exiting bridge " << bridge.id << std::endl;
    }

};