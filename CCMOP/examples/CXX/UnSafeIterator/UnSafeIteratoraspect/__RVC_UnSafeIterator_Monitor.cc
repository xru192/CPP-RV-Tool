#include"__RVC_UnSafeIterator_Monitor.h"
typedef struct monitor{
	int RVC_state=0;
	std::vector<std::pair<std::string,char*>> Trace;
	bool isComplete=false;
	int RVC_UnSafeIterator_match=0;
	std::string* s=nullptr;
	std::string::iterator* it=nullptr;
} __RV_monitor;

struct s_KeyHash {
	std::size_t operator()(const std::string* ptr) const {
		return reinterpret_cast<size_t>(ptr);
	}
};
struct s_Equal {
	bool operator()(const std::string* lhs, const std::string* rhs) const {
		return lhs==rhs;
	}
};
struct it_KeyHash {
	std::size_t operator()(const std::string::iterator* ptr) const {
		return reinterpret_cast<size_t>(ptr);
	}
};
struct it_Equal {
	bool operator()(const std::string::iterator* lhs, const std::string::iterator* rhs) const {
		return lhs==rhs;
	}
};
static std::unordered_map<std::string*, std::vector<__RV_monitor*>*, s_KeyHash, s_Equal> *s_map;
static std::unordered_map<std::string::iterator*, std::vector<__RV_monitor*>*, it_KeyHash, it_Equal> *it_map;
bool isCombine(std::string* s, std::string::iterator* it, __RV_monitor* pM)
{
	if(pM->s!=s&&pM->s!=nullptr&&s!=nullptr)
		return false;
	if(pM->it!=it&&pM->it!=nullptr&&it!=nullptr)
		return false;
	if((pM->s==nullptr||s==nullptr)&&(pM->it==nullptr||it==nullptr))
		return false;
	if((s!=nullptr&&pM->s!=s)||(it!=nullptr&&pM->it!=it))
		return true;
	return false;
}
bool isInclusion(std::string* s, std::string::iterator* it, __RV_monitor* pM)
{
	if(pM->s!=s&&s!=nullptr)
		return false;
	if(pM->it!=it&&it!=nullptr)
		return false;
	return true;
}
bool isUseful(std::string* s, std::string::iterator* it, __RV_monitor* pM, bool inclusion)
{
	if(inclusion)
		return isCombine(s, it, pM);
	else
		return isInclusion(s, it, pM);
}
void getMonitors(std::string* s, std::string::iterator* it, std::vector<__RV_monitor*>* results, bool inclusion)
{
	if(s_map==nullptr)
	{
				s_map=new std::unordered_map<std::string*, std::vector<__RV_monitor*>*, s_KeyHash, s_Equal>;
		it_map=new std::unordered_map<std::string::iterator*, std::vector<__RV_monitor*>*, it_KeyHash, it_Equal>;
	}
	if(s!=nullptr)
	{
		auto iter=s_map->find(s);
		if(iter!=s_map->end())
		{
			auto s_vec=(*iter).second;
			for(auto monitor:*s_vec)
			{
				if(isUseful(s, it, monitor, inclusion))
				{
					results->emplace_back(monitor);
				}
			}
		}
	}
	else if(it!=nullptr)
	{
		auto iter=it_map->find(it);
		if(iter!=it_map->end())
		{
			auto it_vec=(*iter).second;
			for(auto monitor:*it_vec)
			{
				if(isUseful(s, it, monitor, inclusion))
				{
					results->emplace_back(monitor);
				}
			}
		}
	}
}
void combineMonitor(__RV_monitor* cloneMonitor,__RV_monitor* targetMonitor)
{
	if(cloneMonitor->s!=nullptr)
		targetMonitor->s=cloneMonitor->s;
	if(cloneMonitor->it!=nullptr)
		targetMonitor->it=cloneMonitor->it;
}
void updateMap(__RV_monitor* pM)
{
	if(pM->s!=nullptr)
	{
		auto iter=s_map->find(pM->s);
		if(iter!=s_map->end())
		{
			iter->second->emplace_back(pM);
		}
		else
		{
			auto temp=new std::vector<__RV_monitor*>;
			temp->emplace_back(pM);
			(*s_map)[pM->s]=temp;
		}
	}
	if(pM->it!=nullptr)
	{
		auto iter=it_map->find(pM->it);
		if(iter!=it_map->end())
		{
			iter->second->emplace_back(pM);
		}
		else
		{
			auto temp=new std::vector<__RV_monitor*>;
			temp->emplace_back(pM);
			(*it_map)[pM->it]=temp;
		}
	}
}
void try_to_clone(std::string* s, std::string::iterator* it, std::vector<__RV_monitor*>* results)
{
	for(auto monitor:*results)
	{
		if(isCombine(s, it, monitor))
		{
			auto pM=new __RV_monitor;
			pM->Trace=monitor->Trace;
			pM->RVC_state=monitor->RVC_state;
			pM->s=s;
			pM->it=it;
			pM->RVC_UnSafeIterator_match=monitor->RVC_UnSafeIterator_match;
			combineMonitor(monitor,pM);
			if(pM->s!=nullptr&&pM->it!=nullptr)
				pM->isComplete=true;
			updateMap(pM);
		}
	}
}
void printOut(__RV_monitor* monitor)
{
	if(monitor->s!=nullptr)
		std::cout<<"s address:"<<monitor->s<<std::endl;
	if(monitor->it!=nullptr)
		std::cout<<"it address:"<<monitor->it<<std::endl;
	for(auto path:monitor->Trace)
	{
		std::cout<<path.first<<" "<<path.second<<std::endl;
		std::cout<<"|"<<std::endl;
	}
}
void defineNew(std::string* s, std::string::iterator* it)
{
	auto pM=new __RV_monitor;
	pM->RVC_state=0;
	pM->s=s;
	pM->it=it;
	pM->RVC_UnSafeIterator_match=0;
	if(pM->s!=nullptr&&pM->it!=nullptr)
		pM->isComplete=true;
	updateMap(pM);
}




void
__RVC_UnSafeIterator_reset(__RV_monitor *pM)
{
	if(pM != nullptr){
		pM->RVC_state = 0;
		pM->Trace.clear();
	}
}

static int __RVC_UNSAFEITERATOR_DEREFITERATOR[] = {-1,1, -1,2, };
static int __RVC_UNSAFEITERATOR_CREATE[] = {1, -1,-1,-1,};
static int __RVC_UNSAFEITERATOR_UPDATE[] = {-1,3, -1,3, };

void
__RVC_UnSafeIterator_derefIterator(std::string::iterator& it,char* loc)
{
	if(loc==nullptr)
	{
		return;
	}
	std::vector<__RV_monitor*> results;
	getMonitors(nullptr,&it,&results,true);
	if(!results.empty()){
		try_to_clone(nullptr,&it,&results);
	}
	results.clear();
	getMonitors(nullptr,&it,&results,false);
	if(results.empty())
		return;
	for(auto monitor:results){
		if(monitor->RVC_state>=0){
			{}
			int old_state2=monitor->RVC_state;
			monitor->RVC_state = __RVC_UNSAFEITERATOR_DEREFITERATOR[monitor->RVC_state];
			if(old_state2!=monitor->RVC_state) {
				std::string eventname="derefIterator";
				monitor->Trace.emplace_back(std::pair<std::string ,char*>(eventname,loc));
			}
			  monitor->RVC_UnSafeIterator_match = monitor->RVC_state == 2;
			if(monitor->RVC_UnSafeIterator_match) {
				printOut(monitor);
				std::cout<<"V"<<std::endl;
				{
		std::cout<<"improper iterator usage!"<<std::endl;
	}
			}
		}
	}
}
void
__RVC_UnSafeIterator_create(std::string& s, std::string::iterator& it,char* loc)
{
	if(loc==nullptr)
	{
		return;
	}
	std::vector<__RV_monitor*> results;
	getMonitors(&s,&it,&results,false);
	if(results.empty()){
		defineNew(&s,&it);
		getMonitors(&s,&it,&results,false);
	}
	if(results.empty())
		return;
	for(auto monitor:results){
		if(monitor->RVC_state>=0){
			{}
			int old_state2=monitor->RVC_state;
			monitor->RVC_state = __RVC_UNSAFEITERATOR_CREATE[monitor->RVC_state];
			if(old_state2!=monitor->RVC_state) {
				std::string eventname="create";
				monitor->Trace.emplace_back(std::pair<std::string ,char*>(eventname,loc));
			}
			  monitor->RVC_UnSafeIterator_match = monitor->RVC_state == 2;
			if(monitor->RVC_UnSafeIterator_match) {
				printOut(monitor);
				std::cout<<"V"<<std::endl;
				{
		std::cout<<"improper iterator usage!"<<std::endl;
	}
			}
		}
	}
}
void
__RVC_UnSafeIterator_update(std::string& s,char* loc)
{
	if(loc==nullptr)
	{
		return;
	}
	std::vector<__RV_monitor*> results;
	getMonitors(&s,nullptr,&results,true);
	if(!results.empty()){
		try_to_clone(&s,nullptr,&results);
	}
	results.clear();
	getMonitors(&s,nullptr,&results,false);
	if(results.empty())
		return;
	for(auto monitor:results){
		if(monitor->RVC_state>=0){
			{}
			int old_state2=monitor->RVC_state;
			monitor->RVC_state = __RVC_UNSAFEITERATOR_UPDATE[monitor->RVC_state];
			if(old_state2!=monitor->RVC_state) {
				std::string eventname="update";
				monitor->Trace.emplace_back(std::pair<std::string ,char*>(eventname,loc));
			}
			  monitor->RVC_UnSafeIterator_match = monitor->RVC_state == 2;
			if(monitor->RVC_UnSafeIterator_match) {
				printOut(monitor);
				std::cout<<"V"<<std::endl;
				{
		std::cout<<"improper iterator usage!"<<std::endl;
	}
			}
		}
	}
}

