#include <iostream>
#include "Person.h"
#include "Car.h"
#include "OneLaneBridge.h"

void scenario1()
{
    std::cout << "Scenario 1 (Non-violating): " << std::endl;
    OneLaneBridge bridge {"Bridge 1"};
    Car car1 {"BMW"};
    Car car2 {"Toyota"};
    Person person1 {"Alice"};
    Person person2 {"Bob"};

    bridge.open();
    
    person1.enterCarAsDriver(car1);
    car1.enterBridgeEast(bridge);

    person2.enterCarAsDriver(car2);
    car2.enterBridgeEast(bridge);
}

void scenario2()
{
    std::cout << "Scenario 2 (Violating): " << std::endl;
    OneLaneBridge bridge {"Bridge 1"};
    Car car1 {"BMW"};
    Person person1 {"Alice"};
    person1.enterCarAsDriver(car1);
    car1.enterBridgeEast(bridge);
    car1.exitBridge(bridge);
    car1.enterBridgeEast(bridge);
}

void scenario3()
{
    std::cout << "Scenario 3 (Violating - needs parameterization to detect): " << std::endl;
    OneLaneBridge bridge {"Bridge 1"};
    OneLaneBridge bridge2 {"Bridge 2"};
    Car car1 {"BMW"};
    Car car2 {"Toyota"};
    Person person1 {"Alice"};
    Person person2 {"Bob"};

    person1.enterCarAsDriver(car1);
    car1.enterBridgeEast(bridge);
    car1.exitBridge(bridge);

    person2.enterCarAsDriver(car2);
    person2.exitCar();
    car1.enterBridgeEast(bridge);
}

int main(int argc, char **argv)
{
    if (argc < 2)
    {
        std::cout << "Pass in a scenario (1-3) to execute." << std::endl;
        return 0;
    }

    int x = atoi(argv[1]);
    switch (x)
    {
    case 1:
        scenario1();
        break;
    case 2:
        scenario2();
        break;
    case 3:
        scenario3();
        break;
    default:
        std::cout << "Invalid option. Must be in 1-3" << std::endl;
    }
    return 0;
}
