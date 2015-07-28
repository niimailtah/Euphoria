//
#include <string>
#include <iostream>
#include <sstream>
#include <vector>
#include <stdlib.h>
#include <iomanip>      // std::setw

#ifndef ENGINE_H
#define ENGINE_H

enum Interrupt
{
    StartGame = 0,
    WaitMessage,
    WaitChoice,
    WaitInput,
    EndGame
};

/* описание возможных ресурсов */
struct State
{
    long money;   // деньги, руб
    long gold;    // золото, кг
    long land;    // земля, га
    long grain;   // зерно, тонн
    long peasant; // крестьяне, душ
    long guard;   // гвардия, чел
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

    // караван
    long caravane_money; // деньги, отправленные в караване
    long caravane_year;  // текущий год каравана

    //
    long flag_visir;
    long flag_end;       // окончание игры
    long flag_rebellion; // бунт
    bool flag_crisis;    // международный кризис

    // затраты
    long for_crops;      // на посев
    long for_eat;        // на продовольствие
    long for_temple;     // на храм

    //
    long cur_year;
    long cur_money;
    long cur_gold;
    long cur_land;
    long cur_grain;
    long cur_peasant;
    long cur_guard;

    // торговля
    unsigned int article;
    bool to_buy;
    long cur_pr_gold;
    long cur_pr_land;
    long cur_pr_grain;
    long cur_pr_peasant;
    long cur_pr_guard;
    long pr_gold;
    long pr_land;
    long pr_grain;
    long pr_peasant;
    long pr_guard;

    unsigned short crop_yield_level; // урожайность
};

class Game
{
    public:
        // состояние
        enum Stage
        {
            GameIntro,
            FirstChoice,
            GameRules,
            StartTurn,
            Crisis,
            Trade,
            StartExchange,
            ChooseGoods,
            BuyOrSell,
            GoodsNumber,
            NoMoney,
            EquipCaravane,
            CaravaneMoney,
            RobCaravane,
            RequestMetropolitan,
            MetropolitanMoney,
            Metropolitan,
            FinishGame
        };
        // причина нехватки денег
        enum NoMoneyReason
        {
            ForTrade,
            ForCaravane,
            ForTemple
        };
        enum MessageReason
        {
            Caravane,
            Temple
        };
        
        Game();
        ~Game();
        std::string getMessage();
        std::vector<std::string> getCases();
        void sendChoice(unsigned int choice);
        std::string getInputPrompt();
        void sendInput(std::string input);
        State get_status();
        std::string get_intro();
        std::string get_state();
        std::string get_visir_message();
        std::string get_caravan_arrival();
        std::string get_loot_caravan();
        std::string get_crisis();
        void make_prices();
        std::string get_exchange();
        std::string get_catch_visir();
        std::string get_inherit();
        std::string get_born_son();
        std::string get_wife_has_died();
        std::string get_no_money();
        std::string get_turn();
        std::string legacy();

        std::string get_score();
        Interrupt run();

    private:
        State state;
        Stage stage;
        Stage next_stage; // для последующего перехода после показа сообщения
        NoMoneyReason NMreason; // причина нехватки денег
        MessageReason Mreason;  // причина вывода сообщения после дейстия
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
template <typename T> T StringToNumber(std::string &Text);
unsigned int random(int max);
std::string get_intro();
std::string get_rules(unsigned short page);

#endif // ENGINE_H
