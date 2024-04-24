//! \file main.cpp
#include <iostream>
#include "euforia_machine.hpp"

int main(int argc, char *argv[])
{
    try {
        euphoria::use();
        return EXIT_SUCCESS;
    } catch (::std::exception const& e) {
        ::std::cerr << "Exception: " << e.what() << "\n";
        return EXIT_FAILURE;
    } catch (...) {
        ::std::cerr << "Unexpected exception\n";
        return 2;
    }
}
