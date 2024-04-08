
/***
This example shows the memory leak property,when you types 0 to "X".
***/
#include<iostream>


int main() {
    std::string *ps = new std::string;
    int x;
    std::cout<<"please input a number:";
    std::cin>>x;
    if (x)
        return 0;
    else
        delete ps;
    return 1;
}
