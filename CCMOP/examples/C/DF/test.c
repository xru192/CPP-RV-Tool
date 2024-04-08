
/***
This is a simple example which may lead to double free error,when you type 1 to x.
***/
#include <stdlib.h>
#include<stdio.h>

int main(){

    void *T;
    T=((void *)malloc(1));
    free(T);
    int x;
    scanf("%d",&x);
    if(x)
        free(T);
    return 0;
}
