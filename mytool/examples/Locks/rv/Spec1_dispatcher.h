#pragma once

#include "../src/Lock.h"
#include "Spec1_monitor.h"

class Dispatcher
{
private:
    Spec1_Monitor monitor{};

public:
    void receive_begin();
    void receive_end();
    void receive_acquire(Lock &l);
    void receive_release(Lock &l);
};
