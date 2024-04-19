#pragma once

#include "Lock.h"

class LockUser
{
public:
    void procedure1()
    {
        Lock lockA{"A"};
        lockA.acquire();
        lockA.acquire();
        lockA.release();
    }

    void procedure2()
    {
        Lock lockA{"A"};
        lockA.acquire();
        lockA.release();
        lockA.release();
        lockA.acquire();
    }

    void procedure3()
    {
        Lock lockA{"A"};
        Lock lockB{"B"};
        lockA.acquire();
        lockB.acquire();
        lockA.acquire();
        lockA.release();
    }
};
