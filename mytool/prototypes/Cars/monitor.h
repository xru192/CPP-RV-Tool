#include<iostream>
#include "main.cpp"


#include <iostream>
#include <unordered_map>
#include <vector>

class Spec1_Monitor {
public:
void
__RVC_Spec1_reset(void);
void
__RVC_Spec1_createCar(Car& c);
void
__RVC_Spec1_driverEnter(Car& c);
void
__RVC_Spec1_drive(Car& c);

int __RVC_state = 0; 
};

