
/***
This example shows the UnSafe Iterator for string.
***/
/***
UnSafeIterator.mop is the UnSafe Iterator property.
The within(main()) will limit the scope to main function body,that not influence the result for test.cpp.We just want to show the usage of within.
***/
#include <iostream>
int main() {
    std::string s = "hello";
    std::string::iterator it=s.begin();
    s.clear();
    std::cout<<*it<<std::endl;
    return 0;
};

