#include "LockUser.h"

void scenario1()
{
    std::cout << "Scenario 1 (Non-violating): " << std::endl;
    LockUser lockUser{};
    lockUser.procedure1();
}

void scenario2()
{
    std::cout << "Scenario 2 (Violating): " << std::endl;
    LockUser lockUser{};
    lockUser.procedure2();
}

void scenario3()
{
    std::cout << "Scenario 3 (Violating - needs parameterization to detect): " << std::endl;
    LockUser lockUser{};
    lockUser.procedure3();
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