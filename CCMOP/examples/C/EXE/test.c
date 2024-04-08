
/***
This is a exampe which shows that out tool have the ability whish supports the execution pointcut.
***/
#include<stdio.h>
#include <stdlib.h>

int* exe_before(int* x)
{
    if(*x>0)
        return x;
    else
        return x;
}
int* exe_after(int *x)
{
    if(*x>0)
        return x;
    return x;

}
int main()
{
    int *x=(int *)malloc(sizeof(int));
    exe_after(x);
    exe_before(x);
    return 1;
}
