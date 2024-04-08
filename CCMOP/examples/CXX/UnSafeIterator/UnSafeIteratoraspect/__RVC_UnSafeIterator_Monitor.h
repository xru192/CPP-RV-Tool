#include <iostream>

#ifdef __cplusplus
#include <iostream>
#include <unordered_map>
#include <vector>
#endif
#ifdef __cplusplus
extern "C" {
#endif
void
__RVC_UnSafeIterator_derefIterator(std::string::iterator& it,char* loc);
void
__RVC_UnSafeIterator_create(std::string& s, std::string::iterator& it,char* loc);
void
__RVC_UnSafeIterator_update(std::string& s,char* loc);

#ifdef __cplusplus
}
#endif
