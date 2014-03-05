#include <string>
#include <iostream>
#include <sstream>
#include <stdlib.h>
#include <iomanip>      // std::setw

#ifndef ENGINE_H
#define ENGINE_H

class Screen
{
public:
    Screen();
    virtual ~Screen();
    void virtual show();
};

class Choice : public Screen
{
public:
    Choice();
    virtual ~Choice();
    void virtual show();
};

class Menu : public Screen
{
public:
    Menu();
    virtual ~Menu();
    void virtual show();
};

class Message : public Screen
{
public:
    Message();
    virtual ~Message();
    void virtual show();
};

/* описание возможных ресурсов */
struct State
{
    long money; // деньги, руб
    long gold;  // золото, кг
    long land;  // земля, га
    long grain; // зерно, тонн
    long peasant; // крестьяне, душ
    long guard; // гвардия, чел
    long abs_guard_maintenance;
    long guard_maintenance;
    long add_grain;
    long eat_rat;
    long add_peasant;
    long run_peasant;
    long run_guard;
    long grab_gold;
    long grab_money;
    long grab_money2;

    long pr_gold;
    long pr_land;
    long pr_grain;
    long pr_peasant;
    long pr_guard;

    // караван
    long for_caravane;
    long flag_caravane;

    long flag_visir;
    long flag_end;   // окончание игры
    long flag_rebellion; // бунт

    long for_crops; // на посев

    long for_eat;

    long cur_money;
    long cur_gold;
    long cur_land;
    long cur_grain;
    long cur_peasant;
    long cur_guard;

    long cur_pr_gold;
    long cur_pr_land;
    long cur_pr_grain;
    long cur_pr_peasant;
    long cur_pr_guard;

    unsigned short crop_yield_level; // урожайность
};

class Game
{
    public:
//        enum Interrupt {Choice=0, Menu, Message};
        enum Stage {Start=0, End};
        
        Game();
        ~Game();
        State get_status();
        std::string get_state();
        std::string get_visir_message();
        std::string get_caravan_arrival();
        std::string get_loot_caravan();
        std::string get_exchange();
        std::string get_catch_visir();
        std::string get_inherit();
        std::string get_born_son();
        std::string get_wife_has_died();
        std::string get_turn();
        std::string legacy();

        std::string get_score();
        Screen* run();

    private:
        State state;
        Stage stage;
        long calc_scores();
};

class MakeString {
public:
    template<class T>
    MakeString& operator<< (const T& arg)
    {
        m_stream << arg;
        return *this;
    }
    operator std::string() const
    {
        return m_stream.str();
    }
protected:
    std::stringstream m_stream;
};

template<class T> std::string t_to_string(T i);
unsigned int random(int max);
std::string get_intro();
std::string get_rules(unsigned short page);

#endif // ENGINE_H