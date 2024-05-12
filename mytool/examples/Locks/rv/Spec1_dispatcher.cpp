#include "Spec1_dispatcher.h"

// This version of the dispatcher is only correct for non-parametric properties.

void Dispatcher::receive_begin()
{
    monitor.__RVC_Spec1_reset();
    monitor.__RVC_Spec1_begin();
}

void Dispatcher::receive_end()
{
    monitor.__RVC_Spec1_end();
}

void Dispatcher::receive_acquire(Lock &l)
{
    monitor.__RVC_Spec1_acquire();
}

void Dispatcher::receive_release(Lock &l)
{
    monitor.__RVC_Spec1_release();
}
