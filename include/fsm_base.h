#pragma once
#include <string>
#include "include.h"

class FSM_Base {

    public:

    std::string getName();
    virtual void enter() = 0;
    virtual void exit() = 0;
    virtual void run(int dt) = 0;

    private:
    std::string name = "Base";
    double thruster_values[THRUSTER_COUNT] = {0.0};


};