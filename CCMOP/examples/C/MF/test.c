
/***
This is the example shows the memory leak property that when x is 0.
***/
#include <stdlib.h>
#include<stdio.h>

int main(){
    int x=0;
    int *p=malloc(sizeof (int));
    if(x)
        free(p);
        return 1;

}
