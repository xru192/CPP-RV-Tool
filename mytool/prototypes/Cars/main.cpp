#include <iostream>

class Car
{
    public:
    void drive() {}

    void park() {}
};

class Person
{
    public:
    void putOnSeatBelt() {}   // if not in car/already put on does nothing
    void takeOffSeatBelt() {} // if not in car/already taken off does nothing

    void enterCarAsDriver(Car c) {}
    void enterCarAsPassenger(Car c) {}
    void exitCar() {}
};

void scenario1()
{
    std::cout << "Scenario 1 (Non-violating): " << std::endl;
    Car car{};
    Person person{};
    person.enterCarAsDriver(car);
    car.drive(); 
}

void scenario2()
{
    std::cout << "Scenario 2 (Violating): " << std::endl;
    Car car{};
    car.drive(); 
}

void scenario3()
{
    std::cout << "Scenario 3 (Violating - needs parameterization to detect): " << std::endl;
    Car car1{};
    Car car2{};
    Person person{};
    person.enterCarAsDriver(car1);
    car1.drive(); 
    car2.drive();
}

int main(int argc, char **argv)
{
    if (argc < 2)
    {
        std::cout << "Pass in a scenario (1-1) to execute." << std::endl;
        return 0;
    }

    int x = atoi(argv[1]);
    switch (x)
    {
    case 1:
        scenario1();
        break;
    default:
        std::cout << "Invalid option" << std::endl;
    }
    return 0;
}