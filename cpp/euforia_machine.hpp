#pragma once

#include <afsm/fsm.hpp>
#include "euforia_actions.hpp"

using namespace std;

namespace euphoria
{
    // Events
    struct euphoria_event
    {
        int e;
    };
    struct start : euphoria_event
    {
        start() : euphoria_event{10} {}
    };
    struct stop : euphoria_event
    {
        stop() { e = 20; }
    };

    struct euphoria_state
    {
        struct base_state
        {
            int s;
        };
    };
    // State machine definition
    struct euphoria_def : ::afsm::def::state_machine<euphoria_def>, euphoria_state
    {
        struct initial : base_state, state<initial>
        {
            initial() : base_state{1} { }
        };
        struct running : base_state, state<running>
        {
            running() { s = 2; }
        };
        struct terminated : terminal_state<terminated>
        {
            int s;
            terminated() : s(3) {}
        };

        using initial_state = initial;
        using transitions = transition_table<
            /* State       Event    Next        Action      */
            tr<initial,    start,   running,    do_start>,
            tr<running,    stop,    terminated>>;
    };

    // State machine object
    using euphoria_fsm = ::afsm::state_machine<euphoria_def>;

    void use()
    {
        euphoria_fsm fsm;
        fsm.process_event(start{});
        fsm.process_event(stop{});
    }

} /* namespace euphoria */
