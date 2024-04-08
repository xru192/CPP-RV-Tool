
/***
This example shows the use-after-free property .
We shows two UAF ,which in main and rv::test(),if you want to monitor all behavior in this example .you can use UAF.mop,otherwise use the UAF_within.mop.
***/
/***
Compared with UAF.mop, UAF_within.mop  add within(rv) that limit the AOP scope in namespace rv.
If you want limit in more small scope ,you can add like this "rv::test()",which will limit in test() function body in namespace rv.
***/

#include<iostream>
namespace rv {
    class A
    {
    public:
        A(){};
        int t;
    };
    void test() {
        A *pA=new A;
        int *pTest = new int;
        delete pA;
        int x=0;
        if (!x)
            x=pA->t;
    }
}
int main() {
    rv::test();
    rv::A *pmA=new rv::A;
   delete pmA;
    int x=0;
    if (!x)
        x=pmA->t;
    return 1;
}
