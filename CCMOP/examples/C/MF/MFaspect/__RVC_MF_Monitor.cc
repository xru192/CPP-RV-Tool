#include"__RVC_MF_Monitor.h"
typedef struct monitor{
	int RVC_state=0;
	std::vector<std::pair<std::string,char*>> Trace;
	bool isComplete=false;
	int RVC_MF_match=0;
	void* key=nullptr;
} __RV_monitor;

struct key_KeyHash {
	std::size_t operator()(const void* ptr) const {
		return reinterpret_cast<size_t>(ptr);
	}
};
struct key_Equal {
	bool operator()(const void* lhs, const void* rhs) const {
		return lhs==rhs;
	}
};
static std::unordered_map<void*, std::vector<__RV_monitor*>*, key_KeyHash, key_Equal> *key_map;
bool isCombine(void* key, __RV_monitor* pM)
{
	if(pM->key!=key&&pM->key!=nullptr&&key!=nullptr)
		return false;
	if((pM->key==nullptr||key==nullptr))
		return false;
	if((key!=nullptr&&pM->key!=key))
		return true;
	return false;
}
bool isInclusion(void* key, __RV_monitor* pM)
{
	if(pM->key!=key&&key!=nullptr)
		return false;
	return true;
}
bool isUseful(void* key, __RV_monitor* pM, bool inclusion)
{
	if(inclusion)
		return isCombine(key, pM);
	else
		return isInclusion(key, pM);
}
void getMonitors(void* key, std::vector<__RV_monitor*>* results, bool inclusion)
{
	if(key_map==nullptr)
	{
				key_map=new std::unordered_map<void*, std::vector<__RV_monitor*>*, key_KeyHash, key_Equal> ;
	}
	if(key!=nullptr)
	{
		auto iter=key_map->find(key);
		if(iter!=key_map->end())
		{
			auto key_vec=(*iter).second;
			for(auto monitor:*key_vec)
			{
				if(isUseful(key, monitor, inclusion))
				{
					results->emplace_back(monitor);
				}
			}
		}
	}
}
void combineMonitor(__RV_monitor* cloneMonitor,__RV_monitor* targetMonitor)
{
	if(cloneMonitor->key!=nullptr)
		targetMonitor->key=cloneMonitor->key;
}
void updateMap(__RV_monitor* pM)
{
	if(pM->key!=nullptr)
	{
		auto iter=key_map->find(pM->key);
		if(iter!=key_map->end())
		{
			iter->second->emplace_back(pM);
		}
		else
		{
			auto temp=new std::vector<__RV_monitor*>;
			temp->emplace_back(pM);
			(*key_map)[pM->key]=temp;
		}
	}
}
void try_to_clone(void* key, std::vector<__RV_monitor*>* results)
{
	for(auto monitor:*results)
	{
		if(isCombine(key, monitor))
		{
			auto pM=new __RV_monitor;
			pM->Trace=monitor->Trace;
			pM->RVC_state=monitor->RVC_state;
			pM->key=key;
			pM->RVC_MF_match=monitor->RVC_MF_match;
			combineMonitor(monitor,pM);
			if(pM->key!=nullptr)
				pM->isComplete=true;
			updateMap(pM);
		}
	}
}
void printOut(__RV_monitor* monitor)
{
	if(monitor->key!=nullptr)
		std::cout<<"key address:"<<monitor->key<<std::endl;
	for(auto path:monitor->Trace)
	{
		std::cout<<path.first<<" "<<path.second<<std::endl;
		std::cout<<"|"<<std::endl;
	}
}
void defineNew(void* key)
{
	auto pM=new __RV_monitor;
	pM->RVC_state=0;
	pM->key=key;
	pM->RVC_MF_match=0;
	if(pM->key!=nullptr)
		pM->isComplete=true;
	updateMap(pM);
}




void
__RVC_MF_reset(__RV_monitor *pM)
{
	if(pM != nullptr){
		pM->RVC_state = 0;
		pM->Trace.clear();
	}
}

static int __RVC_MF_ENDPROG[] = {-1,-1,1, };
static int __RVC_MF_FREE[] = {-1,-1,0, };
static int __RVC_MF_MALLOC[] = {2, -1,-1,};

void
__RVC_MF_malloc(void* key,char* loc)
{
	if(loc==nullptr||key==nullptr)
	{
		return;
	}
	std::vector<__RV_monitor*> results;
	getMonitors(key,&results,false);
	if(results.empty()){
		defineNew(key);
		getMonitors(key,&results,false);
	}
	if(results.empty())
		return;
	for(auto monitor:results){
		if(monitor->RVC_state>=0){
			{}
			int old_state2=monitor->RVC_state;
			monitor->RVC_state = __RVC_MF_MALLOC[monitor->RVC_state];
			if(old_state2!=monitor->RVC_state) {
				std::string eventname="malloc";
				monitor->Trace.emplace_back(std::pair<std::string ,char*>(eventname,loc));
			}
			  monitor->RVC_MF_match = monitor->RVC_state == 1;
			if(monitor->RVC_MF_match) {
				printOut(monitor);
				std::cout<<"V"<<std::endl;
				{
		printf("object not free at address %p\n",monitor->key);

	}
			}
		}
	}
}
void
__RVC_MF_endProg(char *loc)
{
	if(key_map==nullptr)
	 return;
	for(auto pairs:*key_map)
	{
		for(auto monitor:*pairs.second)
		{
			if(monitor->isComplete)
			{
				if (monitor->RVC_state >= 0) {
					{}
					int old_state2 = monitor->RVC_state;
					monitor->RVC_state = __RVC_MF_ENDPROG[monitor->RVC_state];
					if(old_state2!=monitor->RVC_state) {
						std::string eventname="endProg";
						monitor->Trace.emplace_back(std::pair<std::string ,char*>(eventname,loc));
					}
					  monitor->RVC_MF_match = monitor->RVC_state == 1;
					if(monitor->RVC_MF_match) {
						printOut(monitor);
						std::cout<<"V"<<std::endl;
						{
		printf("object not free at address %p\n",monitor->key);

	}
					}
				}
			}
		}
	}
}
void
__RVC_MF_free(void* key,char* loc)
{
	if(loc==nullptr||key==nullptr)
	{
		return;
	}
	std::vector<__RV_monitor*> results;
	getMonitors(key,&results,false);
	if(results.empty())
		return;
	for(auto monitor:results){
		if(monitor->RVC_state>=0){
			{}
			int old_state2=monitor->RVC_state;
			monitor->RVC_state = __RVC_MF_FREE[monitor->RVC_state];
			if(old_state2!=monitor->RVC_state) {
				std::string eventname="free";
				monitor->Trace.emplace_back(std::pair<std::string ,char*>(eventname,loc));
			}
			  monitor->RVC_MF_match = monitor->RVC_state == 1;
			if(monitor->RVC_MF_match) {
				printOut(monitor);
				std::cout<<"V"<<std::endl;
				{
		printf("object not free at address %p\n",monitor->key);

	}
			}
		}
	}
}

