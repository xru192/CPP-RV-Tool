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

    void print_delta() {
        for (const auto& pair : Delta) {
            auto f = pair.first;
            if (std::get<0>(f) != nullptr) {
                std::cout << "Car: " << std::get<0>(f)->id << "; ";
            } else {
                std::cout << "Car: null; ";
            }
            if (std::get<1>(f) != nullptr) {
                std::cout << "Person: " << std::get<1>(f)->id << "; ";
            } else {
                std::cout << "Person: null; ";
            }
            if (std::get<2>(f) != nullptr) {
                std::cout << "Bridge: " << std::get<2>(f)->id << "; ";
            } else {
                std::cout << "Bridge: null; ";
            }
            std::cout << "State: " << pair.second->__RVC_state;
            std::cout << std::endl;
        }
        std::cout << std::endl;
    }

    bool compatible(const theta_t& theta1, const theta_t& theta2) {
        auto* v0_1 = std::get<0>(theta1);
        auto* v1_1 = std::get<1>(theta1);
        auto* v2_1 = std::get<2>(theta1);
        auto* v0_2 = std::get<0>(theta2);
        auto* v1_2 = std::get<1>(theta2);
        auto* v2_2 = std::get<2>(theta2);

        if (v0_1 != v0_2 && v0_1 != nullptr && v0_2 != nullptr) {
            return false;
        }

        if (v1_1 != v1_2 && v1_1 != nullptr && v1_2 != nullptr) {
            return false;
        }

        if (v2_1 != v2_2 && v2_1 != nullptr && v2_2 != nullptr) {
            return false;
        }
        return true;
    }


    theta_t computeCombine(const theta_t& theta1, const theta_t& theta2) {
        auto* v0 = std::get<0>(theta1);
        auto* v1 = std::get<1>(theta1);
        auto* v2 = std::get<2>(theta1);
        if (std::get<0>(theta2) != nullptr) {
            v0 = std::get<0>(theta2);
        }
        if (std::get<1>(theta2) != nullptr) {
            v1 = std::get<1>(theta2);
        }
        if (std::get<2>(theta2) != nullptr) {
            v2 = std::get<2>(theta2);
        }
        return {v0, v1, v2};
    }

    /**
     * Compute {theta} U Theta
    */
    Theta_t computeCombine(const theta_t& theta) {
        Theta_t all_combine {};
        for (const theta_t& theta_prime : Theta) {
            if (compatible(theta, theta_prime)) {
                theta_t combine = computeCombine(theta, theta_prime);
                all_combine.insert(combine);
            }
        }
        return all_combine;
    };

    /**
     * Performs Theta <-- {bot, theta} U Theta
    */
    void updateTheta(const theta_t& theta) {
        Theta_t combine_theta = computeCombine(theta);
        for (const theta_t& theta_prime : combine_theta) {
            Theta.insert(theta_prime);
        }
    };
    
    /**
     * Computes (theta]_Theta
    */
    Theta_t computeSet(const theta_t& theta) {
        Theta_t set {};
        for (const theta_t& theta_prime : Theta) {
            if (less_informative(theta_prime, theta)) {
                set.insert(theta_prime);
            }
        }
        return set;
    };

    theta_t max(const Theta_t& Theta) {
        theta_t curr_max = {nullptr, nullptr, nullptr};
        for (const theta_t& theta : Theta) {
            if (less_informative(curr_max, theta)) {
                curr_max = theta;
            }
        }
        return curr_max;
    };

    /**
     * Returns whether theta1 is less informative (\sqsubseteq) than theta2.
    */
    bool less_informative(const theta_t& theta1, const theta_t& theta2) {
        auto* v01 = std::get<0>(theta1);
        auto* v11 = std::get<1>(theta1);
        auto* v21 = std::get<2>(theta1);
        auto* v02 = std::get<0>(theta2);
        auto* v12 = std::get<1>(theta2);
        auto* v22 = std::get<2>(theta2);

        if (v01 != nullptr && v01 != v02) {
            return false;
        }
        if (v11 != nullptr && v11 != v12) {
            return false;
        }
        if (v21 != nullptr && v21 != v22) {
            return false;
        }
        return true;
    };

    void receive(int event_id, theta_t& theta) {
        Theta_t domain = computeCombine(theta);
        for (const theta_t& theta_prime : domain) {
            if (Theta.count(theta_prime) > 0) {
                // if theta' is in Theta, max (theta']_Theta = theta' and monitor already is created
                Spec1_Monitor& m = *Delta[theta_prime];
                monitor_receive(m, event_id);
            } else {
                Theta_t set = computeSet(theta_prime);
                theta_t max_theta = max(set);
                Spec1_Monitor* m = new Spec1_Monitor(*Delta[max_theta]);
                monitors.push_back(m);
                Delta[theta_prime] = m;
                monitor_receive(*m, event_id);
            }
        }
        updateTheta(theta);
        // std::cout << "SIZE: " << Theta.size() << std::endl;
        // std::cout << "MONITORS: " << monitors.size() << std::endl;
        // std::cout << "DELTA" << std::endl;
        // print_delta();
    };

    void monitor_receive(Spec1_Monitor& monitor, int event_id) {
        switch (event_id) {
            case 0:
                monitor.__RVC_Spec1_takeBridge();
                break;
            case 1:
                monitor.__RVC_Spec1_exitBridge();
                break;
            case 2:
                monitor.__RVC_Spec1_enterCar();
                break;
            case 3:
                monitor.__RVC_Spec1_exitCar();
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

    void receive_takeBridge(Car& c, OneLaneBridge& b);
    void receive_exitBridge(Car& c, OneLaneBridge& b);
    void receive_enterCar(Car& c, Person& p);
    void receive_exitCar(Car& c, Person& p);
};


