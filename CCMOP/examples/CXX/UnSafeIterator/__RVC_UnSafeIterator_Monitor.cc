#include"__RVC_UnSafeIterator_Monitor.h"
static int __RVC_state = 0; 



int __RVC_UnSafeIterator_match = 0;

void
__RVC_UnSafeIterator_reset(void)
{
  __RVC_state = 0;
 }

static int __RVC_UNSAFEITERATOR_DEREFITERATOR[] = {-1,1, -1,2, };
static int __RVC_UNSAFEITERATOR_CREATE[] = {1, -1,-1,-1,};
static int __RVC_UNSAFEITERATOR_UPDATE[] = {-1,3, -1,3, };

void
__RVC_UnSafeIterator_derefIterator(std::string::iterator& it)
{
{}
__RVC_state = __RVC_UNSAFEITERATOR_DEREFITERATOR[__RVC_state];
  __RVC_UnSafeIterator_match = __RVC_state == 2;
if(__RVC_UnSafeIterator_match)
{
{
		std::cout<<"improper iterator usage!"<<std::endl;
        }}
}

void
__RVC_UnSafeIterator_create(std::string& s, std::string::iterator& it)
{
{}
__RVC_state = __RVC_UNSAFEITERATOR_CREATE[__RVC_state];
  __RVC_UnSafeIterator_match = __RVC_state == 2;
if(__RVC_UnSafeIterator_match)
{
{
		std::cout<<"improper iterator usage!"<<std::endl;
        }}
}

void
__RVC_UnSafeIterator_update(std::string& s)
{
{}
__RVC_state = __RVC_UNSAFEITERATOR_UPDATE[__RVC_state];
  __RVC_UnSafeIterator_match = __RVC_state == 2;
if(__RVC_UnSafeIterator_match)
{
{
		std::cout<<"improper iterator usage!"<<std::endl;
        }}
}


