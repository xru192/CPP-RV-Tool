
/***
This example shows the UnSafe iterator for container in C++ programs.
***/
#include<iostream>
#include<map>
using namespace std;

int main()
{
    std::map<int,std::string> maps;
    maps.insert(std::pair<int,string>(1,"hello"));
    std::map<int,std::string>::iterator it=maps.begin();
    maps.clear();
    std::cout<<(*it).second<<endl;
    return 0;
}
