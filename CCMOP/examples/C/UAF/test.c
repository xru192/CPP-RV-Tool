/***
This is a example shows the use after free property.
***/
#include <stdio.h>
#include <stdlib.h>
typedef struct {
    int t;
} test;

static test *x;

int main(){

    x=malloc(sizeof (test));
    free(x);
    x->t=1;
    return 1;

}
