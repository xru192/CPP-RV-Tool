#include"monitor.h"

// static int __RVC_state = 0; 



int __RVC_Spec1_fail = 0;

void
Spec1_Monitor::__RVC_Spec1_reset(void)
{
  __RVC_state = 0;
 }

static int __RVC_SPEC1_DRIVERENTER[] = {-1,1, };
static int __RVC_SPEC1_DRIVE[] = {-1,1, };
static int __RVC_SPEC1_CREATECAR[] = {1, 1, };

void
Spec1_Monitor::__RVC_Spec1_createCar(Car& c)
{
{}
__RVC_state = __RVC_SPEC1_CREATECAR[__RVC_state];
  __RVC_Spec1_fail = __RVC_state == -1;
if(__RVC_Spec1_fail)
{
{
		    std::cout << "Spec violated" << std::endl;
        }}
}

void
Spec1_Monitor::__RVC_Spec1_driverEnter(Car& c)
{
{}
__RVC_state = __RVC_SPEC1_DRIVERENTER[__RVC_state];
  __RVC_Spec1_fail = __RVC_state == -1;
if(__RVC_Spec1_fail)
{
{
		    std::cout << "Spec violated" << std::endl;
        }}
}

void
Spec1_Monitor::__RVC_Spec1_drive(Car& c)
{
{}
__RVC_state = __RVC_SPEC1_DRIVE[__RVC_state];
  __RVC_Spec1_fail = __RVC_state == -1;
if(__RVC_Spec1_fail)
{
{
		    std::cout << "Spec violated" << std::endl;
        }}
}


