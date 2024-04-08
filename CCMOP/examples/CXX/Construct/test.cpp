
/***
This example shows the monitor of string contructor behavior.
If you want to monitor the pStr(which uses the new to get the pointer that point to heap memory),
you need to modify the type in MOP file,that add "*" in spec and event parameter.(example: std::string* key)
***/

#include<iostream>

int main() {
    std::string str = "123";
    std::string *pStr=new std::string;
    return 0;
};

