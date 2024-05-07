//! \file main.cpp
#include <ftxui/dom/elements.hpp>
#include <ftxui/screen/screen.hpp>
#include <ftxui/component/captured_mouse.hpp>     // for ftxui
#include <ftxui/component/component.hpp>          // for Menu
#include <ftxui/component/component_options.hpp>  // for MenuOption
#include <ftxui/component/screen_interactive.hpp> // for ScreenInteractive

// #include "euforia_machine.hpp"

using namespace ftxui;

// MARK:intro
void intro()
{
    Element document = border(text("Королевство Эйфория"));

    auto screen = Screen::Create(
        Dimension::Full(),       // Width
        Dimension::Fit(document) // Height
    );
    Render(screen, document);
    screen.Print();
}

// MARK:new_game
void new_game()
{
    Element document = border(text("Новая игра"));

    auto screen = ScreenInteractive::Fullscreen();
    // auto screen = Screen::Create(
    //     Dimension::Full(),       // Width
    //     Dimension::Fit(document) // Height
    // );
    auto renderer = Renderer([&]
                             { return document; });
    auto component = CatchEvent(renderer, [&](Event event)
                                {
            if (event == Event::Character('q'))
            {
                screen.ExitLoopClosure()();
                return true;
            }
            return false; });
    screen.Loop(component);
}

// MARK:prn_rule
void prn_rule()
{
    std::string p =
        "      Нехитрые правила игры (рекомендую немного поиграть, а потом читать)."
        "   Первое, вашим подданным нужно кушать . На каждого человека - крестьянина или"
        "гвардейца - нужно в год 3 тонны зерна (стандартная норма) . Если дадите меньше,"
        "то может быть 3 варианта последствий: 1) дадите от 70%% до 99%% . Вас немного по-"
        "журят и напомнят, что народ нужно кормить . 2) дадите от 40%% до 69%% . С вероят-"
        "ностью, обратно пропорциональной выделенной норме, может произойти буннт, и"
        "Вас свергнут. А может и не произойти. 3) дадите < 40%% . Гарантированно произой-"
        "дет революция, и Вас свергнут."
        "   Так что перед тем, как купить огромную армию крестьян или солдат, посмотрите"
        "- а сможете ли Вы ее прокормить."
        "   Второе, солдатам нужно ежегодно платить жалование. По 10 руб. за год каждому"
        "солдату. Плюс еще 10 р. начальнику стражи, который всегда на службе , даже если"
        "под его началом - ни одного гвардейца. Если в казне не хватает денег на выплату"
        "жалованья, то Ваша верная гвардия может просто-напросто дезертировать..."
        "   Третье, крестьянам для работы нужна земля. Если земли больше , чем крестьян,"
        "то крестьяне обрабатывают ровно столько земли , сколько их самих. Если крестьян"
        "больше, чем земли, то они обрабатывают всю землю, а 'лишние', те, которым земли"
        "не хватило, могут сбежать от Вас. Сбегает обычно часть 'лишних' крестьян."
        "   Учтите, что урожай может быть получен только с обрабатываемых земель. Каждый"
        "гектар пашни требует для посева 1 тонну зерна. Дадите меньше, чем обрабатывает-"
        "ся земли, следовательно, засеете не всю возможную площадь, и часть обрабатывае-"
        "мой земли простоит год впустую. Дадите больше, чем обрабатывается земли - прос-"
        "то потратите впустую зерно, так как посеется все равно только необходимое коли-"
        "чество зерна, а остальное, выделенное для посева, пропадет впустую. Так что мой"
        "Вам совет - выделяйте на посев именно столько зерна, сколько нужно."
        "   Описывать работу с биржей и всякую дипломатию не имеет смысла - там все эле-"
        "ментарно. Два слова можно сказать о караванах."
        "   Караван  -  достаточно редкая возможность быстро разбогатеть, если Вы готовы"
        "рискнуть. Вложенные в караван деньги приносят прибыль x6. Но не радуйтесь рань-"
        "ше времени  -  не все так просто.. Ваш караван могут запросто ограбить бандиты,"
        "отняв у Вас изрядный кусок прибыли. А могут и не просто ограбить , а разграбить"
        "полностью... И тогда плакали Ваши денежки."
        "   Не жадничайте, давайте на храм митрополиту - ведь это богоугодное дело. Гля-"
        "дишь, и действительно новый храм отгрохают... "
        "   Да, и народу на Новый год выделяйте иногда - пусть повеселится..."
        "   Пара слов насчет войны. Разведка сообщает не точную информацию о численности"
        "противника, а приблизительную, с ошибкой -25%% - +25%%. Учитывайте это..."
        "   Война может возникнуть в двух случаях: 1) у Вас мало солдат. Чем малочислен-"
        "нее Ваша гвардия, тем чаще будут нападать нахальные соседи. 2) Вы оскорбили ка-"
        "кого-либо соседа отказом жениться на его дочке . Оскорбленный сосед обязательно"
        "покатит на Вас бочку (то бишь пойдет войной). Хотя, с другой стороны, согласив-"
        "шись на брак, Вы потратите кучу денег на свадебный пир, а там еще , может быть,"
        "и на день рождения сына, и на похороны королевы... Решайте сами, что Вам выгод-"
        "ней..."
        "                              Originally written by Ponpa Dmitriy, 41PDM. 1998."
        "                                         Adapted for Linux by Niimailtah. 2014.";
    auto document = vbox({window(text("Align left:"), paragraphAlignLeft(p))}) |
                    vscroll_indicator | yframe | flex;
    auto screen = ScreenInteractive::Fullscreen();
    auto renderer = Renderer([&]
                             { return document; });
    auto component = CatchEvent(renderer, [&](Event event)
                                {
            if (event == Event::Character('q'))
            {
                screen.ExitLoopClosure()();
                return true;
            }
            return false; });
    screen.Loop(component);
}

// MARK:main
int main(int argc, char *argv[])
{
    intro();
    getchar();
    auto screen = ScreenInteractive::Fullscreen();
    screen.SetCursor(Screen::Cursor{.shape = Screen::Cursor::Shape::Hidden});

    std::vector<std::string> entries = {
        "Новая Игра",
        "Помощь",
        "Выход",
    };
    int selected = 0;

    MenuOption option;
    option.on_enter = screen.ExitLoopClosure();
    auto menu = Menu(&entries, &selected, option);

    while (selected != 2)
    {
        screen.Loop(menu);
        switch (selected)
        {
        case 0:
            new_game();
            break;
        case 1:
            prn_rule();
            break;
        case 2:
            break;
        }
    }

    return EXIT_SUCCESS;
}
