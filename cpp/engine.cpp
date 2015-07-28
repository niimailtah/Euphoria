//
#include "engine.h"

/* расход зерна на единицу */
static const long ed_posev = 1; // на посев на 1 га
static const long ed_eat = 3;   // на еду на 1 душу (krest+guard)

Game::Game()
{
    /* initialize random seed: */
    srand(time(NULL));
    
    /* начальные значения */
    state.money = 10000; // деньги, руб
    state.gold = 0;      // золото, кг
    state.land = 100;    // земля, га
    state.grain = 1000;  // зерно, тонн
    state.peasant= 100;   // крестьяне, душ
    state.guard = 100;   // гвардия, чел
    state.cur_money = state.money;
    state.cur_gold = state.gold;
    state.cur_land = state.land;
    state.cur_grain = state.grain;
    state.cur_peasant = state.peasant;
    state.cur_guard = state.guard;
    /* средние цены */
    state.pr_gold = 1000; // руб/кг
    state.pr_land = 200;  // руб/га
    state.pr_grain = 10;  // руб/тонн
    state.pr_peasant = 50;  // руб/душу
    state.pr_guard = 100; // руб/чел
    state.cur_year = 1;
    state.crop_yield_level = random(5);
    state.caravane_year = 0;
    state.caravane_money = 0;
    state.flag_crisis = false;
    stage = GameIntro;

}

Game::~Game()
{

}

State Game::get_status()
{
    return state;
}

Interrupt Game::run()
{
    Interrupt ret = WaitMessage;
    switch (stage)
    {
        case GameIntro:
        case GameRules:
        case StartTurn:
        case Crisis:
        case StartExchange:
        case NoMoney:
        case RobCaravane:
            ret = WaitMessage;
            break;
        case FirstChoice:
        case Trade:
        case ChooseGoods:
        case BuyOrSell:
        case EquipCaravane:
            ret = WaitChoice;
            break;
        case GoodsNumber:
        case CaravaneMoney:
        case RequestMetropolitan:
            ret = WaitInput;
            break;
        case FinishGame:
            ret = EndGame;
            break;
        default:
            break;
    }
    return ret;
}

std::string Game::getMessage()
{
    std::string ret = "";
    switch (stage)
    {
        case GameIntro:
            ret = get_intro();
            stage = FirstChoice;
            break;
        case GameRules:
            ret = get_rules(1);
            ret += get_rules(2);
            stage = FirstChoice;
            break;
        case StartTurn:
            ret = get_state();
            if (state.cur_year > 1)
            {
                ret += get_visir_message();
            }
            if (state.caravane_year == 5)
            {
                ret += get_caravan_arrival();
                state.caravane_year = 0;
            }
            if (random(100) < 25)
            {
                stage = Crisis;
            }
            else
            {
                stage = Trade;
            }
            break;
        case StartExchange:
            make_prices();
            ret = get_exchange();
            stage = ChooseGoods;
            break;
        case NoMoney:
            ret = get_no_money();
            stage = next_stage;
            break;
        case Crisis:
            ret = get_crisis();
            stage = EquipCaravane;
            break;
        case RobCaravane:
            if (state.caravane_year > 1 && random(100) < 20)
            {
                ret = get_loot_caravan();
            }
            stage = RequestMetropolitan;
//            stage = FinishGame;
            break;
        default:
            break;
    }
    return ret;
}

void Game::sendChoice(unsigned int choice)
{
    switch (stage)
    {
        case FirstChoice:
            switch (choice)
            {
                case 1:
                    stage = StartTurn;
                    break;
                case 2:
                    stage = GameRules;
                    break;
                case 3:
                    stage = FinishGame;
                    break;
                default:
                    break;
            }
            break;
        case Trade:
            switch (choice)
            {
                case 1:
                    stage = StartExchange;
                    break;
                case 2:
                    if (random(100) < 25)
                    {
                        stage = EquipCaravane;
                        break;
                    }
                    stage = RobCaravane;
                    break;
                default:
                    break;
            }
            break;
        case ChooseGoods:
            switch (choice)
            {
                case 1:
                case 2:
                case 3:
                case 4:
                case 5:
                    state.article = choice;
                    stage = BuyOrSell;
                    break;
                case 6:
                    if (random(100) < 25)
                    {
                        stage = EquipCaravane;
                        break;
                    }
                    stage = RobCaravane;
                    break;
                default:
                    break;
            }
            break;
        case BuyOrSell:
            switch (choice)
            {
                case 1:
                    state.to_buy = true;
                    stage = GoodsNumber;
                    break;
                case 2:
                    state.to_buy = false;
                    stage = GoodsNumber;
                    break;
                default:
                    break;
            }
            break;
        case EquipCaravane:
            switch (choice)
            {
                case 1:
                    stage = CaravaneMoney;
                    break;
                case 2:
                    stage = RobCaravane;
                    break;
                default:
                    break;
            }
            break;
        default:
            break;
    }
    return;
}

std::vector<std::string> Game::getCases()
{
    std::vector<std::string> ret;
    std::string topic;
    switch (stage)
    {
        case FirstChoice:
            ret.push_back("");
            ret.push_back("Новая Игра");
            ret.push_back("Помощь");
            ret.push_back("Выход");
            break;
        case Trade:
            ret.push_back("\n\nЖелаете торговать на бирже?");
            ret.push_back("Да");
            ret.push_back("Нет");
            break;
        case ChooseGoods:
            ret.push_back("\nВыберите товар, с которым проводить операции:");
            ret.push_back("Золото");
            ret.push_back("Земля");
            ret.push_back("Зерно");
            ret.push_back("Крестьяне");
            ret.push_back("Гвардия");
            ret.push_back("Выход с биржи");
            break;
        case BuyOrSell:
            topic = "Выберите тип операций";
            switch (state.article)
            {
                case 1:
                    topic += " с золотом:\n";
                    break;
                case 2:
                    topic += " с землей:\n";
                    break;
                case 3:
                    topic += " с зерном:\n";
                    break;
                case 4:
                    topic += " с крестьянами:\n";
                    break;
                case 5:
                    topic += " с гвардией:\n";
                    break;
            }
            ret.push_back(topic);
            ret.push_back("Покупать");
            ret.push_back("Продавать");
            break;
        case EquipCaravane:
            ret.push_back("\n\nЗаморский купец предлагает снарядить караван.\nВы согласны?");
            ret.push_back("Да");
            ret.push_back("Нет");
            break;
        default:
            break;
    }
    return ret;
}

void Game::sendInput(std::string input)
{
    long count;
    switch (stage)
    {
        case GoodsNumber:
            count = StringToNumber<long>(input);
            if (state.to_buy)
            {
                switch (state.article)
                {
                    case 1:
                        if (count * state.cur_pr_gold > state.cur_money)
                        {
                            stage = NoMoney;
                            NMreason = ForTrade;
                            next_stage = ChooseGoods;
                        }
                        else
                        {
                            state.cur_gold += count;
                            state.cur_money -= count * state.cur_pr_gold;
                            stage = StartExchange;
                        }
                        break;
                    case 2:
                        if (count * state.cur_pr_land > state.cur_money)
                        {
                            stage = NoMoney;
                            NMreason = ForTrade;
                            next_stage = ChooseGoods;
                        }
                        else
                        {
                            state.cur_land += count;
                            state.cur_money -= count * state.cur_pr_land;
                            stage = StartExchange;
                        }
                        break;
                    case 3:
                        if (count * state.cur_pr_grain > state.cur_money)
                        {
                            stage = NoMoney;
                            NMreason = ForTrade;
                            next_stage = ChooseGoods;
                        }
                        else
                        {
                            state.cur_grain += count;
                            state.cur_money -= count * state.cur_pr_grain;
                            stage = StartExchange;
                        }
                        break;
                    case 4:
                        if (count * state.cur_pr_peasant > state.cur_money)
                        {
                            stage = NoMoney;
                            NMreason = ForTrade;
                            next_stage = ChooseGoods;
                        }
                        else
                        {
                            state.cur_peasant += count;
                            state.cur_money -= count * state.cur_pr_peasant;
                            stage = StartExchange;
                        }
                        break;
                    case 5:
                        if (count * state.cur_pr_guard > state.cur_money)
                        {
                            stage = NoMoney;
                            NMreason = ForTrade;
                            next_stage = ChooseGoods;
                        }
                        else
                        {
                            state.cur_guard += count;
                            state.cur_money -= count * state.cur_pr_guard;
                            stage = StartExchange;
                        }
                        break;
                    default:
                        break;
                }
            }
            else
            {
                switch (state.article)
                {
                    case 1:
                        state.cur_gold -= count;
                        state.cur_money += count * state.cur_pr_gold;
                        break;
                    case 2:
                        state.cur_land -= count;
                        state.cur_money += count * state.cur_pr_land;
                        break;
                    case 3:
                        state.cur_grain -= count;
                        state.cur_money += count * state.cur_pr_grain;
                        break;
                    case 4:
                        state.cur_peasant -= count;
                        state.cur_money += count * state.cur_pr_peasant;
                        break;
                    case 5:
                        state.cur_guard -= count;
                        state.cur_money += count * state.cur_pr_guard;
                        break;
                    default:
                        break;
                }
            }
            break;
        case CaravaneMoney:
            count = StringToNumber<long>(input);
            if (count > state.money)
            {
                stage = NoMoney;
                NMreason = ForCaravane;
            }
            else
            {
                state.money -= count;
                state.caravane_money = count;
                // TODO: сообщение об отправке каравана
                Mreason = Caravane;
                stage = RequestMetropolitan;
//                stage = FinishGame;
            }
            break;
        case RequestMetropolitan:
            count = StringToNumber<long>(input);
            if (count > state.money)
            {
                stage = NoMoney;
                NMreason = ForTemple;
            }
            else
            {
                state.for_temple += count;
                Mreason = Temple;
            }
            break;
        default:
            break;
    }
    return;
}

std::string Game::getInputPrompt()
{
    std::string ret;
    switch (stage)
    {
        case GoodsNumber:
            if (state.to_buy)
            {
                switch (state.article)
                {
                    case 1:
                        ret = "\nСколько килограммов золота желаете купить: ";
                        break;
                    case 2:
                        ret = "\nСколько гектаров земли желаете купить: ";
                        break;
                    case 3:
                        ret = "\nСколько тонн зерна желаете купить: ";
                        break;
                    case 4:
                        ret = "\nСколько душ крестьян желаете купить: ";
                        break;
                    case 5:
                        ret = "\nСколько гвардейцев желаете нанять: ";
                        break;
                    default:
                        break;
                }
            }
            else
            {
                switch (state.article)
                {
                    case 1:
                        ret = "\nСколько килограммов золота желаете продать: ";
                        break;
                    case 2:
                        ret = "\nСколько гектаров земли желаете продать: ";
                        break;
                    case 3:
                        ret = "\nСколько тонн зерна желаете продать: ";
                        break;
                    case 4:
                        ret = "\nСколько душ крестьян желаете продать: ";
                        break;
                    case 5:
                        ret = "\nСколько гвардейцев желаете продать: ";
                        break;
                    default:
                        break;
                }
            }
            break;
        case CaravaneMoney:
            ret = MakeString() << "\nВ казне - " << state.money << " руб, сколько на караван:";
            break;
        case RequestMetropolitan:
            ret = MakeString() << "\n\nМитрополит Вашего государства просит денег на новый храм."
                               << "\nСколько выделяте (в казне " << state.money << " руб.): ";
            break;
        default:
            break;
    }
    return ret;
}

std::string Game::get_state() //long god)
{
    std::string ret;

/*    if (fl_end == 1)
    {
        printf("---------------------------------------------------------------------------------\n");
        printf("                   Состояние Ваших дел после %li лет правления.", god);
    }
    else
    {
*/
    ret = MakeString() << "---------------------------------------------------------------------------------\n"
        << "                   Состояние Ваших дел на " << state.cur_year << "-й год правления."
//    }
        << "\nНаличность в казне: " << state.money << " руб."
        << "\n╔════════════════╤════════════╗"
        << "\n║    Название    │   Запасы   ║"
        << "\n╠════════════════╪════════════╣"
        << "\n║ Золото, кг     │ " << std::setw(10) << state.gold  << " ║"
        << "\n║ Земля, га      │ " << std::setw(10) << state.land  << " ║"
        << "\n║ Зерно, тонн    │ " << std::setw(10) << state.grain << " ║"
        << "\n║ Крестьяне, душ │ " << std::setw(10) << state.peasant << " ║"
        << "\n║ Гвардия, чел.  │ " << std::setw(10) << state.guard << " ║"
        << "\n╚════════════════╧════════════╝\n";
    return ret;
/*    if (MENTOR)
    {
        long int difference = cur_guard * 3 + cur_krest * 3 +cur_land;
        printf("\nНадо %li зерна\nМожно продать %li", difference, cur_zerno - difference);
    }*/
}

std::string Game::get_visir_message()
{
    std::string ret;
    ret = MakeString() << "\n\nВаше Величество, прибыл Главный Визирь с докладом."
        << "\nВизирь сообщает:"
        << "\nЖалованье гвардии за прошлый год составило " << state.abs_guard_maintenance << " рублей.";
    switch (state.crop_yield_level)
    {
        case 0:
            ret += MakeString() << "\nСтрашная засуха поразила посевы. Очень неурожайный год."
                << "\nСобрано всего " << state.add_grain << " тонн зерна.";
            break;
        case 1:
            ret += MakeString() << "\nУрожайность была низкая. Собрано " << state.add_grain << " тонн зерна.";
            break;
        case 2:
            ret += MakeString() << "\nСредний по урожайности год."
                << "\nНаши крестьяне собрали " << state.add_grain << " тонн зерна.";
            break;
        case 3:
            ret += MakeString() << "\nУрожайный год. Собрано " << state.add_grain << " тонн зерна.";
            break;
        case 4:
            ret += MakeString() << "\nПролившиеся вовремя дожди обеспечили невиданно высокий урожай."
                << "\nАмбары ломятся от зерна - собрано " << state.add_grain << " тонн!";
            break;
    }
    if (state.eat_rat > 0)
    {
        ret += MakeString() << "\nПреступная халатность! Крысы сожрали " << state.eat_rat << " тонн зерна!";
    }
    if (state.add_peasant > 0)
    {
        ret += MakeString() << "\nЧисло Ваших подданных увеличилось. Родилось " << state.add_peasant << " детей.";
    }
    if (state.run_peasant != -1)
    {
        ret += MakeString() << "\nВашим крестьянам не хватает земли. Сбежало " << state.run_peasant << " человек.";
    }
    if (state.run_guard != -1)
    {
        ret += MakeString() << "\nНе хватило денег на выплату денежного довольствия Вашей гвардии."
            << "\nДезертировало " << state.run_guard << " солдат.";
    }
    if (state.grab_gold > 0)
    {
        ret += MakeString() << "\nСкандал! Из сокровищницы похищено " << state.grab_gold << " кг золота!";
    }
    if (state.grab_money > 0)
    {
        ret += MakeString() << "\nКража! Визирь похитил " << state.grab_money << " руб. и скрылся!..";
    }
    return ret;
}

std::string Game::get_caravan_arrival()
{
    long profit = state.caravane_money * 6; // прибыль
    state.cur_money += profit;
    return MakeString() << "\n\nВернулся Ваш караван! Получено прибыли на сумму " << profit << " руб.!";
}

std::string Game::get_loot_caravan()
{
    std::string ret;
    long n, grab;
    n = random(100);
    if (n < 5)
    {
        ret = "\n\nПроизошло ЧП! Ваш караван полностью разграблен бандитами!!!";
        state.caravane_year = 0;
        state.caravane_money = 0;
    }
    else
    {
        n = random(40);
        grab = (state.caravane_money * n) / 100;
        ret += MakeString() << "\n\nВнимание, ЧП! Ваш караван ограблен бандитами на сумму " << grab << " руб.!!!";
        state.caravane_money -= grab;
    }
    return ret;
}

std::string Game::get_crisis()
{
    std::string ret;
    ret = "\n\nМеждународный кризис! Торговля невозможна!" \
          "\nВашему государству объявлена экономическая блокада!\n";
    state.flag_crisis = true;
    return ret;
}

std::string Game::get_catch_visir()
{
    long cur;
    std::string ret;
    cur = (random(50) + 50) * state.grab_money2 / 100;
    ret = MakeString() << "\n\nВаша полиция поймала сбежавшего визиря!"
        << "\nУ него конфисковано все имущество, а его самого посадили на кол!"
        << "\nВ казну возвращено " << cur << " руб.";
    state.cur_money += cur;
    state.flag_visir = 0;
    return ret;
}

std::string Game::get_inherit()
{
    long cur;
    long n;
    std::string ret;
    ret = "\n\nУмер Ваш дальний родственник. Вы получили наследство в размере:";
    n = random(90) + 10;
    cur = state.cur_money * n / 100;
    state.cur_money += cur;
    ret += MakeString() << "\nДеньги - " << cur << " руб.";
    n = random(90) + 10;
    cur = state.cur_gold * n / 100;
    state.cur_gold += cur;
    ret += MakeString() << "\nЗолото - " << cur << " кг.";
    n = random(90) + 10;
    cur = state.cur_land * n / 100;
    state.cur_land += cur;
    ret += MakeString() << "\nЗемля - " << cur << " га.";
    n = random(90) + 10;
    cur = state.cur_grain * n / 100;
    state.cur_grain += cur;
    ret += MakeString() << "\nЗерно - " << cur << " тонн.";
    n = random(90) + 10;
    cur = state.cur_peasant * n / 100;
    state.cur_peasant += cur;
    ret += MakeString() << "\nКрестьяне - " << cur << " душ.";
    n = random(90) + 10;
    cur = state.cur_guard * n / 100;
    state.cur_guard += cur;
    ret += MakeString() << "\nСолдаты - " << cur << " чел.";
    return ret;
}

void Game::make_prices()
{
    state.cur_pr_gold  = ((state.pr_gold * 75) / 100)  + (random(50) * state.pr_gold / 100);
    state.cur_pr_land  = ((state.pr_land * 75) / 100)  + (random(50) * state.pr_land / 100);
    state.cur_pr_grain = ((state.pr_grain * 75) / 100) + (random(50) * state.pr_grain / 100);
    state.cur_pr_peasant = ((state.pr_peasant * 75) / 100) + (random(50) * state.pr_peasant / 100);
    state.cur_pr_guard = ((state.pr_guard * 75) / 100) + (random(50) * state.pr_guard / 100);
}

std::string Game::get_exchange()
{
    double f;
    std::string ret;
    ret = MakeString() << "Наличность в казне: " << state.cur_money << " руб."
        << "\n╔════════════════╤══════════════╤══════════════╤══════════════╗"
        << "\n║    Название    │    Запасы    │ Текущая цена │ Текущий курс ║"
        << "\n╠════════════════╪══════════════╪══════════════╪══════════════╣";
    f = state.cur_pr_gold * 100 / state.pr_gold;
    ret += MakeString() << "\n║ Золото, кг     │ " << std::setw(12) << state.cur_gold <<  " │ " << std::setw(12) << state.cur_pr_gold <<  " │ " << std::setw(12) << f << " ║";
    f = state.cur_pr_land * 100 / state.pr_land;
    ret += MakeString() << "\n║ Земля, га      │ " << std::setw(12) << state.cur_land <<  " │ " << std::setw(12) << state.cur_pr_land <<  " │ " << std::setw(12) << f << " ║";
    f = state.cur_pr_grain * 100 / state.pr_grain;
    ret += MakeString() << "\n║ Зерно, тонн    │ " << std::setw(12) << state.cur_grain << " │ " << std::setw(12) << state.cur_pr_grain << " │ " << std::setw(12) << f << " ║";
    f = state.cur_pr_peasant * 100 / state.pr_peasant;
    ret += MakeString() << "\n║ Крестьяне, душ │ " << std::setw(12) << state.cur_peasant << " │ " << std::setw(12) << state.cur_pr_peasant << " │ " << std::setw(12) << f << " ║";
    f = state.cur_pr_guard * 100 / state.pr_guard;
    ret += MakeString() << "\n║ Гвардия, чел.  │ " << std::setw(12) << state.cur_guard << " │ " << std::setw(12) << state.cur_pr_guard << " │ " << std::setw(12) << f << " ║";
    ret += "\n╚════════════════╧══════════════╧══════════════╧══════════════╝\n";
    return ret;
}

std::string Game::get_born_son()
{
    long cur;
    std::string ret;
    cur = (random(40) + 20) * state.cur_money / 100;
    state.cur_money -= cur;
    ret = MakeString() << "\n\nУ Вас родился сын! Поздравляю! Ваша династия не угаснет в веках!"
        << "\nНа праздничный банкет по случаю рождения сына потрачено " << cur << " руб.";
    return ret;
}

std::string Game::get_wife_has_died()
{
/*    long cur;
    long n;
*/    
    std::string ret;
    ret = "\n\nПрибыл гонец от королевы. Впустить (y/n)? ";
/*    n = get_choice();
    if (n == 0)
    {
        printf("\nХоть Вы и не приняли гонца, но печальная весть все равно дошла до Вас.");
    }
    printf("\nВеликое несчастье! Умерла королева! Овдовевший монарх безутешен!");
    cur = (random(40) + 20) * cur_money / 100;
    printf("\nНа похороны королевы потрачено %li руб.", cur);
    cur_money -= cur;
    fl_marry = 0;
*/
    return ret;
}

std::string Game::get_no_money()
{
    std::string ret = "";
    switch (NMreason)
    {
        case ForTrade:
            ret = "\nУ вас не хватает денег чтобы оплатить покупку!";
            next_stage = ChooseGoods;
            break;
        case ForCaravane:
            ret = MakeString() << "\nУ Вас столько нету. Вы можете отправить от 0 до " << state.money << " руб.";
            if (random(100) < 25)
            {
                next_stage = EquipCaravane;
                break;
            }
            next_stage = RobCaravane;
            break;
        case ForTemple:
            ret = MakeString() << "\nУ Вас столько нету. Вы можете пожертвовать от 0 до " << state.money << " руб.";
            next_stage = RequestMetropolitan;
            break;
        default:
            break;
    }
    return ret;
}

std::string Game::get_turn()
{
    long n;
    long a, b;
    double f, f1, f2, f3;
    std::string ret;
// обработка (крестьяне+гвардия) - зерно
    f1 = state.for_eat;
    f2 = ed_eat;
    f3 = state.cur_peasant + state.cur_guard;
    f = (f1 / f2) / f3;
    ret = MakeString() << "\n\nНорма продуктов на год на 1 человека составляет " << f * 100 << " от необходимой.";
    if (f >= 1.)
    {
        ret += "\nНарод доволен таким щедрым правитетем.";
    }
    if ((f < 1.) && (f >= 0.7))
    {
        ret += "\nКормите народ получше, не то получите РЕВОЛЮЦИЮ...";
    }
    if ((f < 0.7) && (f >= 0.4))
    {
        n = random(100);
        if (n < 100 - (f * 100))
        {
            ret += "\nВы доигрались... Народ не стал терпеть такие унижения и сверг Вас!!!";
            ret += "\nНе доводите больше свой народ до БУНТА!!!";
            return "1";
        }
        else
        {
            ret += "\nНедовольство вами резко возросло. Вы сильно рискуете...";
            ret += "\nТолько случай спас Вас в этот раз от БУНТА...";
        }
    }
    if (f < 0.4)
    {
        ret += "\nДа Вы что, издеваетесь?!! Так морить голодом свой народ!..";
        ret += "\nПродали бы лишних крестьян, изверг, если прокормить не можете...";
        ret += "\nЕстественно, умирающий от голода народ сверг такого тирана...";
        ret += "\nПолучите БУНТ!!!";
        return "1";
    }
// обработка урожая
    state.crop_yield_level = random(5);
    a = state.cur_peasant < state.cur_land ? state.cur_peasant : state.cur_land;
    b = a < state.for_crops ? a : state.for_crops;
    state.add_grain = (state.crop_yield_level * 2 + 3) * b;
    state.cur_grain += state.add_grain;
// обработка крыс
    n = random(100);
    if (n < 20)
    {
        state.eat_rat = (random(20) * state.cur_grain) / 100;
        state.cur_grain -= state.eat_rat;
    }
    else
    {
        state.eat_rat = -1;
    }
// обработка земля - крестьяне
    if (state.cur_peasant > state.cur_land)
    {
        state.run_peasant = random(state.cur_peasant - state.cur_land);
        state.cur_peasant -= state.run_peasant;
    }
    else
    {
        state.run_peasant = -1;
    }
    n = random(10) + 6;
    state.add_peasant = (state.cur_peasant * n) / 100;
    state.cur_peasant += state.add_peasant;
// обработка гвардия - деньги
    state.abs_guard_maintenance = (state.cur_guard + 1) * state.guard_maintenance;
    if (state.abs_guard_maintenance > state.cur_money)
    {
        n = random(10) + 6;
        state.run_guard = (state.cur_guard * n) / 100;
        state.cur_guard -= state.run_guard;
        state.abs_guard_maintenance = (state.cur_guard + 1) * state.guard_maintenance;
        if (state.abs_guard_maintenance > state.cur_money)
        {
            state.abs_guard_maintenance = state.cur_money;
        }
    }
    else
    {
        state.run_guard = -1;
    }
    state.cur_money -= state.abs_guard_maintenance;
// обработка похищения золота
    if (state.cur_gold > 0)
    {
        n = random(100);
        if (n < 20)
        {
            state.grab_gold = (random(25) * state.cur_gold) / 100;
            state.cur_gold -= state.grab_gold;
        }
        else
        {
            state.grab_gold = -1;
        }
    }
    else
    {
        state.grab_gold = -1;
    }
// обработка визирь - деньги
    if (state.cur_money > 0)
    {
        n = random(100);
        if (n < 10)
        {
            state.grab_money = (random(25) * state.cur_money) / 100;
            state.grab_money2 = state.grab_money;
            state.cur_money -= state.grab_money;
            state.flag_visir = 1;
        }
        else
        {
            state.grab_money = -1;
        }
    }
    else
    {
        state.grab_money = -1;
    }
    if (state.caravane_year > 0)
    {
        ++state.caravane_year;
    }
    return "0";
}

std::string Game::legacy()
{
    long cur;
    long n;
    std::string ret;
    ret = "\n\nУмер Ваш дальний родственник. Вы получили наследство в размере:";
    n = random(90) + 10;
    cur = state.cur_money * n / 100;
    state.cur_money += cur;
    ret += MakeString() << "\nДеньги - " << cur << " руб.";
    n = random(90) + 10;
    cur = state.cur_gold * n / 100;
    state.cur_gold += cur;
    ret += MakeString() << "\nЗолото - " << cur << " кг.";
    n = random(90) + 10;
    cur = state.cur_land * n / 100;
    state.cur_land += cur;
    ret += MakeString() << "\nЗемля - " << cur << " га.";
    n = random(90) + 10;
    cur = state.cur_grain * n / 100;
    state.cur_grain += cur;
    ret += MakeString() << "\nЗерно - " << cur << " тонн.";
    n = random(90) + 10;
    cur = state.cur_peasant * n / 100;
    state.cur_peasant += cur;
    ret += MakeString() << "\nКрестьяне - " << cur << " душ.";
    n = random(90) + 10;
    cur = state.cur_guard * n / 100;
    state.cur_guard += cur;
    ret += MakeString() << "\nСолдаты - " << cur << " чел.";
    return ret;
}






/* Game report */
std::string Game::get_score()
{
    std::string ret;
/*    if (i > 50)
    {
        i = 50;
    }
    clrscr();
*/  
    state.flag_end = 1;
    if (state.flag_rebellion == 0)
    {
        ret += "Ваше правление завершилось...\n";
    }
    else
    {
        ret += "Голодающий народ ВОССТАЛ и свергнул нерадивого правителя!!!";
        ret += "\nПоздравляю Вас, батенька, с БУНТОМ, ха-ха...\n";
    }
//    prn_sost(i);
    ret += "\n\nЗа ваше состояние Вам даются следующее количество очков:";
//    score = make_score(i);
//    prn_score(i);
    long score;
    score = calc_scores();
    ret += MakeString() << "\nОбщая сумма Ваших очков: " << score;
    ret += "\n\nНу что ж... Поздравляю с успешным (?) окончанием игры.";
    if ((score >= 0) && (score <= 100) )
    {
        ret += "\nP.S. Вам бы лучше гусей пасти... Вместо Ваших крестьян...";
    }
    if ((score > 100) && (score <= 300))
    {
        ret += "\nP.S. Для новичка - сойдет... Хотя, конечно, неважно...";
    }
    if ((score > 300) && (score <= 500))
    {
        ret += "\nP.S. Ну, это уже кое-что... Худо-бедно, да ладно...";
    }
    if ((score > 500) && (score <= 1000))
    {
        ret += "\nP.S. Ну вот, кое-что уже получается. Старайтесь дальше...";
    }
    if ((score > 1000) && (score <= 3000))
    {
        ret += "\nP.S. Неплохо, весьма неплохо... Уважаю...";
    }
    if ((score > 3000) && (score <= 5000))
    {
        ret += "\nP.S. Что ж, видно, играть Вы умеете... Весьма недурственно...";
    }
    if ((score > 5000) && (score <= 10000))
    {
        ret += "\nP.S. Круто, что говорить... Да Вы, батенька, профессионал...";
    }
    if ((score > 10000) && (score <= 100000))
    {
        ret += "\nP.S. Прости их, Господи... Ну Вы, блин, даете!!!";
    }
    if (score > 100000)
    {
        ret += "\nP.S. NO pity, NO mercy, NO REGRET!!!!!!!!!!";
    }
    return ret;
}

long Game::calc_scores()
{
    long score = 0;
    score += (state.cur_money / 1000);
    score += (state.cur_gold * 2);
    score += (state.cur_land / 5);
    score += (state.cur_grain / 100);
    score += (state.cur_peasant / 20);
    score += (state.cur_guard / 10);
//    score += build_xram * 200; храм
//    score += i * 10; год
    return score;
}

template<class T>
std::string t_to_string(T i)
{
    std::stringstream ss;
    std::string s;
    ss << i;
    s = ss.str();

    return s;
}

template <typename T>
T StringToNumber(std::string &Text) //Text not by const reference so that the function can be used with a 
{                                   //character array as argument
    std::stringstream ss(Text);
    T result;
    return ss >> result ? result : 0;
}

unsigned int random(int max)
{
    return rand() % max;
}

std::string Game::get_intro()
{
    return std::string("╔═══════════════════════════════════════════════════════════════════╗\n" \
                  "║ █   █ ▄▀▀▀▄ █▀▀▀▄ ▄▀▀▀▄   ▄▀█ █▀▀▀█ █▀▀▀▄ ▄▀▀▀▄ ▀▀█▀▀ █▀▀▀▄ ▄▀▀▀▄ ║\n" \
                  "║ █ ▄▀  █   █ █   █ █   █ ▄▀  █ █     █   █ █   ▀   █   █   █ █   █ ║\n" \
                  "║ █▀▄   █   █ █▄▄▄▀ █   █ █   █ █▀▀   █▀▀▀▄ █       █   █▀▀▀▄ █   █ ║\n" \
                  "║ █  █  █   █ █     █   █ █   █ █     █   █ █   ▄   █   █   █ █   █ ║\n" \
                  "║ █   █ ▀▄▄▄▀ █     ▀▄▄▄▀ █   █ █▄▄▄█ █▄▄▄▀ ▀▄▄▄▀   █   █▄▄▄▀ ▀▄▄▄▀ ║\n" \
                  "║                 ▄                                                 ║\n" \
                  "║       ▄▀▀▀▄  █     █ ▄▀▀█▀▀▄ ▄▀▀▀▀▀▄ █▀▀▀▀▀▄ █     █ ▄▀▀▀▀▀█      ║\n" \
                  "║      ▀     █ █   ▄██ █  █  █ █     █ █     █ █   ▄██ █     █      ║\n" \
                  "║         ▄▄▄█ █ ▄█▀ █ ▀▄▄█▄▄▀ █     █ █▄▄▄▄▄▀ █ ▄█▀ █ ▀▄▄▄▄▄█      ║\n" \
                  "║      ▄     █ ██▀   █    █    █     █ █       ██▀   █   ▄▀  █      ║\n" \
                  "║       ▀▄▄▄▀  █     █    █    ▀▄▄▄▄▄▀ █       █     █ ▄▀    █      ║\n" \
                  "╚═══════════════════════════════════════════════════════════════════╝\n");
}

std::string get_rules(unsigned short page)
{
    std::string ret;
    switch (page)
    {
        case 1:
            ret = "---------------------------------------------------------------------------------\n" \
                  "      Нехитрые правила игры (рекомендую немного поиграть, а потом читать).\n" \
                  "   Первое, вашим подданным нужно кушать . На каждого человека - крестьянина или\n" \
                  "гвардейца - нужно в год 3 тонны зерна (стандартная норма) . Если дадите меньше,\n" \
                  "то может быть 3 варианта последствий: 1) дадите от 70%% до 99%% . Вас немного по-\n" \
                  "журят и напомнят, что народ нужно кормить . 2) дадите от 40%% до 69%% . С вероят-\n" \
                  "ностью, обратно пропорциональной выделенной норме, может произойти бунт, и\n" \
                  "Вас свергнут. А может и не произойти. 3) дадите < 40%% . Гарантированно произой-\n" \
                  "дет бунт, и Вас свергнут.\n" \
                  "   Так что перед тем, как купить огромную армию крестьян или солдат, посмотрите\n" \
                  "- а сможете ли Вы ее прокормить.\n" \
                  "   Второе, солдатам нужно ежегодно платить жалование. По 10 руб. за год каждому\n" \
                  "солдату. Плюс еще 10 р. начальнику стражи, который всегда на службе , даже если\n" \
                  "под его началом - ни одного гвардейца. Если в казне не хватает денег на выплату\n" \
                  "жалованья, то Ваша верная гвардия может просто-напросто дезертировать...\n" \
                  "   Третье, крестьянам для работы нужна земля. Если земли больше , чем крестьян,\n" \
                  "то крестьяне обрабатывают ровно столько земли , сколько их самих. Если крестьян\n" \
                  "больше, чем земли, то они обрабатывают всю землю, а 'лишние', те, которым земли\n" \
                  "не хватило, могут сбежать от Вас. Сбегает обычно часть 'лишних' крестьян.\n" \
                  "   Учтите, что урожай может быть получен только с обрабатываемых земель. Каждый\n" \
                  "гектар пашни требует для посева 1 тонну зерна. Дадите меньше, чем обрабатывает-\n" \
                  "ся земли, следовательно, засеете не всю возможную площадь, и часть обрабатывае-\n" \
                  "мой земли простоит год впустую. Дадите больше, чем обрабатывается земли - прос-\n" \
                  "то потратите впустую зерно, так как посеется все равно только необходимое коли-\n" \
                  "чество зерна, а остальное, выделенное для посева, пропадет впустую. Так что мой\n" \
                  "Вам совет - выделяйте на посев именно столько зерна, сколько нужно.\n";
            break;
        case 2:
            ret = "   Описывать работу с биржей и всякую дипломатию не имеет смысла - там все эле-\n" \
                  "ментарно. Два слова можно сказать о караванах.\n" \
                  "   Караван  -  достаточно редкая возможность быстро разбогатеть, если Вы готовы\n" \
                  "рискнуть. Вложенные в караван деньги приносят прибыль x6. Но не радуйтесь рань-\n" \
                  "ше времени  -  не все так просто.. Ваш караван могут запросто ограбить бандиты,\n" \
                  "отняв у Вас изрядный кусок прибыли. А могут и не просто ограбить , а разграбить\n" \
                  "полностью... И тогда плакали Ваши денежки.\n" \
                  "   Не жадничайте, давайте на храм митрополиту - ведь это богоугодное дело. Гля-\n" \
                  "дишь, и действительно новый храм отгрохают... \n" \
                  "   Да, и народу на Новый год выделяйте иногда - пусть повеселится...\n" \
                  "   Пара слов насчет войны. Разведка сообщает не точную информацию о численности\n" \
                  "противника, а приблизительную, с ошибкой -25%% - +25%%. Учитывайте это...\n" \
                  "   Война может возникнуть в двух случаях: 1) у Вас мало солдат. Чем малочислен-\n" \
                  "нее Ваша гвардия, тем чаще будут нападать нахальные соседи. 2) Вы оскорбили ка-\n" \
                  "кого-либо соседа отказом жениться на его дочке . Оскорбленный сосед обязательно\n" \
                  "покатит на Вас бочку (то бишь пойдет войной). Хотя, с другой стороны, согласив-\n" \
                  "шись на брак, Вы потратите кучу денег на свадебный пир, а там еще , может быть,\n" \
                  "и на день рождения сына, и на похороны королевы... Решайте сами, что Вам выгод-\n" \
                  "ней...\n" \
                  "                              Originally written by Ponpa Dmitriy, 41PDM. 1998.\n" \
                  "                                         Adapted for Linux by Niimailtah. 2014.\n" \
                  "-------------------------------------------------------------------------------\n";
        default:
            break;
    }
    return ret;
}
