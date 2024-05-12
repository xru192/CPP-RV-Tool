#pragma once

#include <unordered_set>
#include <unordered_map>
#include <tuple>
#include "../src/Car.h"
#include "../src/Person.h"
#include "../src/OneLaneBridge.h"
#include "Spec1_monitor.h"

// Hash function for pointers
template<typename T>
std::size_t hash_pointer(const T* ptr) {
    return reinterpret_cast<std::size_t>(ptr);
}

// Custom hash function for tuple of pointers
struct tuple_hash {
    template <std::size_t N>
    std::size_t operator()(const std::tuple<Car*, Person*, OneLaneBridge*>& tuple) const {
        std::size_t seed = 0;
        hash_combine(seed, std::get<N>(tuple));
        return seed;
    }

    std::size_t operator()(const std::tuple<Car*, Person*, OneLaneBridge*>& tuple) const {
        return hash_combine<0>(tuple);
    }

    template <std::size_t N>
    std::size_t hash_combine(const std::tuple<Car*, Person*, OneLaneBridge*>& tuple) const {
        std::size_t seed = 0;
        seed ^= hash_pointer(std::get<N>(tuple)) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        return seed;
    }

    template <std::size_t N, std::size_t M, typename... Ts>
    std::size_t hash_combine(const std::tuple<Car*, Person*, OneLaneBridge*>& tuple) const {
        std::size_t seed = hash_combine<N>(tuple);
        seed = hash_combine<M, Ts...>(tuple);
        return seed;
    }
};

class Dispatcher
{
using theta_t = std::tuple<Car*, Person*, OneLaneBridge*>;
using Theta_t = std::unordered_set<theta_t, tuple_hash>;

private:
    std::vector<Spec1_Monitor*> monitors {};
    Theta_t Theta {};
    std::unordered_map<theta_t, Spec1_Monitor*, tuple_hash> Delta {};

    /**
     * Compute {theta} U Theta
    */
    Theta_t computeCombine(const theta_t& theta);

    /**
     * Performs Theta <-- {bot, theta} U Theta
    */
    void updateTheta(const theta_t& theta);
    
    /**
     * Computes (theta]_Theta
    */
    Theta_t computeSet(const theta_t& theta);
    theta_t max(Theta_t& Theta);

    /**
     * Returns whether theta1 is less informative (\sqsubseteq) than theta2.
    */
    bool less_informative(theta_t theta1, theta_t theta2);

    void receive(int event_id, theta_t theta) {
        Theta_t domain = computeCombine(theta);
        for (theta_t theta_prime : domain) {
            if (Theta.count(theta_prime) > 0) {
                // if theta' is in Theta, max (theta']_Theta = theta' and monitor already is created
                Spec1_Monitor m = *Delta[theta_prime];
            } else {
                Theta_t set = computeSet(theta_prime);
                theta_t max_theta = max(set);
                Spec1_Monitor* m = new Spec1_Monitor(*Delta[max_theta]);
                monitors.push_back(m);
                Delta[theta_prime] = m;
            }
        }
    };

    void monitor_receive(Spec1_Monitor& monitor, int event_id) {
        switch (event_id) {
            case 0:
                monitor.__RVC_Spec1_takeBridge();
                break;
        }
    }


public:
    Dispatcher () {
        Spec1_Monitor* m = new Spec1_Monitor();
        monitors.push_back(m);
        theta_t bot = {nullptr, nullptr, nullptr};
        Delta[bot] = m;
        Theta.insert(bot);
    }

    void receive_takeBridge(Car& c, Person& p, OneLaneBridge& b);
    void receive_exitBridge(Car& c, Person& p, OneLaneBridge& b);
};


