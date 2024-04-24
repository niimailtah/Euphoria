#pragma once

#include <ftxui/dom/elements.hpp>
#include <ftxui/screen/screen.hpp>

using namespace std;
using namespace ftxui;

namespace euphoria
{
    // Actions
    struct do_start
    {
        template <typename Event, typename FSM, typename SourceState, typename TargetState>
        void operator()(Event const &e, FSM &, SourceState &s1, TargetState &s2) const
        {
            Element document = border(text("Королевство Эйфория"));

            auto screen = Screen::Create(
                Dimension::Full(),       // Width
                Dimension::Fit(document) // Height
            );
            Render(screen, document);
            screen.Print();
            cout << e.e << endl;
            cout << s1.s << endl;
            cout << s2.s << endl;
        }
    };
} /* namespace euphoria */
