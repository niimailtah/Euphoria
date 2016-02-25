#!/usr/bin/env python3
from transitions import Machine
from transitions import logger
import logging
import random

VERSION = '0.0.1'


# ==================================================================================================================================================================
class Rules(Machine):
    def __init__(self):
        self.states = [
            {'name': 'Begin'},         #
            {'name': 'End'},           #
            {'name': 'ChoosePage'},    #
            {'name': 'FirstPage'},     #
            {'name': 'SecondPage'}     #
        ]
        self.transitions = [
            {'trigger': 'step', 'source': 'Begin', 'dest': 'ChoosePage'},
            {'trigger': 'step', 'source': 'ChoosePage', 'dest': 'FirstPage', 'conditions': 'answerIsOne'},
            {'trigger': 'step', 'source': 'FirstPage', 'dest': 'ChoosePage'},
            {'trigger': 'step', 'source': 'ChoosePage', 'dest': 'SecondPage', 'conditions': 'answerIsTwo'},
            {'trigger': 'step', 'source': 'SecondPage', 'dest': 'ChoosePage'},
            {'trigger': 'step', 'source': 'ChoosePage', 'dest': 'End', 'conditions': 'answerIsThree'}
        ]
        Machine.__init__(self, states=self.states, transitions=self.transitions,
                         initial='Begin', send_event=True)
        self.pageNumber = None
        self.answer = None

    def on_enter_ChoosePage(self, event):
        print('1. Первая страница')
        print('2. Вторая страница')
        print('3. Выход')
        self.answer = int(input('==> '))

    def on_enter_FirstPage(self, event):
        if self.pageNumber == 1:
            return
        print("""
            ---------------------------------------------------------------------------------
                  Нехитрые правила игры (рекомендую немного поиграть, а потом читать).
               Первое, вашим подданным нужно кушать . На каждого человека - крестьянина или
            гвардейца - нужно в год 3 тонны зерна (стандартная норма) . Если дадите меньше,
            то может быть 3 варианта последствий: 1) дадите от 70% до 99% . Вас немного по-
            журят и напомнят, что народ нужно кормить . 2) дадите от 40% до 69% . С вероят-
            ностью, обратно пропорциональной выделенной норме, может произойти буннт, и
            Вас свергнут. А может и не произойти. 3) дадите < 40% . Гарантированно произой-
            дет революция, и Вас свергнут.
               Так что перед тем, как купить огромную армию крестьян или солдат, посмотрите
            - а сможете ли Вы ее прокормить.
               Второе, солдатам нужно ежегодно платить жалование. По 10 руб. за год каждому
            солдату. Плюс еще 10 р. начальнику стражи, который всегда на службе , даже если
            под его началом - ни одного гвардейца. Если в казне не хватает денег на выплату
            жалованья, то Ваша верная гвардия может просто-напросто дезертировать...
               Третье, крестьянам для работы нужна земля. Если земли больше , чем крестьян,
            то крестьяне обрабатывают ровно столько земли , сколько их самих. Если крестьян
            больше, чем земли, то они обрабатывают всю землю, а 'лишние', те, которым земли
            не хватило, могут сбежать от Вас. Сбегает обычно часть 'лишних' крестьян.
               Учтите, что урожай может быть получен только с обрабатываемых земель. Каждый
            гектар пашни требует для посева 1 тонну зерна. Дадите меньше, чем обрабатывает-
            ся земли, следовательно, засеете не всю возможную площадь, и часть обрабатывае-
            мой земли простоит год впустую. Дадите больше, чем обрабатывается земли - прос-
            то потратите впустую зерно, так как посеется все равно только необходимое коли-
            чество зерна, а остальное, выделенное для посева, пропадет впустую. Так что мой
            Вам совет - выделяйте на посев именно столько зерна, сколько нужно.
            ---------------------------------------------------------------------------------""")
        self.pageNumber = 1
        self.to_ChoosePage()

    def on_enter_SecondPage(self, event):
        if self.pageNumber == 2:
            return
        print("""
            ---------------------------------------------------------------------------------
               Описывать работу с биржей и всякую дипломатию не имеет смысла - там все эле-
            ментарно. Два слова можно сказать о караванах.
               Караван  -  достаточно редкая возможность быстро разбогатеть, если Вы готовы
            рискнуть. Вложенные в караван деньги приносят прибыль x6. Но не радуйтесь рань-
            ше времени  -  не все так просто.. Ваш караван могут запросто ограбить бандиты,
            отняв у Вас изрядный кусок прибыли. А могут и не просто ограбить , а разграбить
            полностью... И тогда плакали Ваши денежки.
               Не жадничайте, давайте на храм митрополиту - ведь это богоугодное дело. Гля-
            дишь, и действительно новый храм отгрохают... 
               Да, и народу на Новый год выделяйте иногда - пусть повеселится...
               Пара слов насчет войны. Разведка сообщает не точную информацию о численности
            противника, а приблизительную, с ошибкой -25% - +25%. Учитывайте это...
               Война может возникнуть в двух случаях: 1) у Вас мало солдат. Чем малочислен-
            нее Ваша гвардия, тем чаще будут нападать нахальные соседи. 2) Вы оскорбили ка-
            кого-либо соседа отказом жениться на его дочке . Оскорбленный сосед обязательно
            покатит на Вас бочку (то бишь пойдет войной). Хотя, с другой стороны, согласив-
            шись на брак, Вы потратите кучу денег на свадебный пир, а там еще , может быть,
            и на день рождения сына, и на похороны королевы... Решайте сами, что Вам выгод-
            ней...
                                          Originally written by Ponpa Dmitriy, 41PDM. 1998.
                                                     Adapted for Linux by Niimailtah. 2014.
            -------------------------------------------------------------------------------""")
        self.pageNumber = 2
        self.to_ChoosePage()

    def answerIsOne(self, event):
        if self.answer == 1:
            return True
        return False

    def answerIsTwo(self, event):
        if self.answer == 2:
            return True
        return False

    def answerIsThree(self, event):
        if self.answer == 3:
            return True
        return False


class Exchange(Machine):
    def __init__(self):
        pass


class War(Machine):
    def __init__(self):
        pass


# ==================================================================================================================================================================
class Euphoria(Machine):
    def __init__(self):
        self.states = [
            {'name': 'Begin'},             #
            {'name': 'TrunkPoint1'},       #
            {'name': 'TrunkPoint2'},       #
            {'name': 'TrunkPoint3'},       #
            {'name': 'TrunkPoint4'},       #
            {'name': 'TrunkPoint5'},       #
            {'name': 'TrunkPoint6'},       #
            {'name': 'End'},               #
            {'name': 'Intro'},             #
            {'name': 'MainMenu'},          #
            {'name': 'Rules'},             #
            {'name': 'NewGame'},           #
            {'name': 'StartTurn'},         #
            {'name': 'PrintState'},        #
            {'name': 'VizirMessage'},      #
            {'name': 'CaravanProfit'},     #
            {'name': 'Crisis'},            #
            {'name': 'Exchange'},          #
            {'name': 'CaravanSupply'},     #
            {'name': 'CaravanRob'},        #
            {'name': 'Metropolitan'},      #
            {'name': 'War'},               #
            {'name': 'VizirCatch'},        #
            {'name': 'Inheritance'},       #
            {'name': 'ChildBirthDay'},     #
            {'name': 'Marriage'},          #
            {'name': 'WifeDead'},          #
            {'name': 'WifeIn'},            #
            {'name': 'Sickness'},          #
            {'name': 'GiveGrain'},         #
            {'name': 'MakeTurn'},          #
            {'name': 'NextYear'},          #
            {'name': 'NYParty'},           #
            {'name': 'EndTurn'},           #
            {'name': 'EndGame'}            #
        ]
        self.transitions = [
            {'trigger': 'step', 'source': 'Begin', 'dest': 'Intro'},
            {'trigger': 'step', 'source': 'Intro', 'dest': 'MainMenu'},
            {'trigger': 'step', 'source': 'MainMenu', 'dest': 'Rules', 'conditions': 'answerIsTwo'},
            {'trigger': 'step', 'source': 'Rules', 'dest': 'MainMenu'},
            {'trigger': 'step', 'source': 'MainMenu', 'dest': 'End', 'conditions': 'answerIsThree'},
            {'trigger': 'step', 'source': 'MainMenu', 'dest': 'NewGame', 'conditions': 'answerIsOne'},
            {'trigger': 'step', 'source': 'NewGame', 'dest': 'PrintState'},
            {'trigger': 'step', 'source': 'PrintState', 'dest': 'VizirMessage', 'conditions': 'isNotFirstYear'},
            {'trigger': 'step', 'source': 'PrintState', 'dest': 'TrunkPoint1'},
            {'trigger': 'step', 'source': 'VizirMessage', 'dest': 'TrunkPoint1'},
            {'trigger': 'step', 'source': 'TrunkPoint1', 'dest': 'CaravanProfit', 'conditions': 'is5YearCaravan'},
            {'trigger': 'step', 'source': 'TrunkPoint1', 'dest': 'TrunkPoint2', 'before': 'update_random'},
            {'trigger': 'step', 'source': 'CaravanProfit', 'dest': 'TrunkPoint2', 'before': 'update_random'},
            {'trigger': 'step', 'source': 'TrunkPoint2', 'dest': 'Crisis', 'conditions': 'isCrisis'},
            {'trigger': 'step', 'source': 'Crisis', 'dest': 'TrunkPoint3', 'before': 'update_random'},
            {'trigger': 'step', 'source': 'TrunkPoint2', 'dest': 'Exchange', 'unless': 'isCrisis'},
            {'trigger': 'step', 'source': 'Exchange', 'dest': 'TrunkPoint3', 'before': 'update_random'},
            {'trigger': 'step', 'source': 'TrunkPoint3', 'dest': 'CaravanSupply', 'conditions': 'is0YearCaravan'},
            {'trigger': 'step', 'source': 'TrunkPoint3', 'dest': 'TrunkPoint4', 'before': 'update_random'},
            {'trigger': 'step', 'source': 'CaravanSupply', 'dest': 'TrunkPoint4', 'before': 'update_random'},
            {'trigger': 'step', 'source': 'TrunkPoint4', 'dest': 'CaravanRob', 'unless': 'is0YearCaravan'},
            {'trigger': 'step', 'source': 'TrunkPoint4', 'dest': 'TrunkPoint5', 'before': 'update_random'},
            {'trigger': 'step', 'source': 'TrunkPoint5', 'dest': 'Metropolitan', 'conditions': 'isReceiveMetropolitan'},
            {'trigger': 'step', 'source': 'TrunkPoint5', 'dest': 'War'},
            {'trigger': 'step', 'source': 'War', 'dest': 'TrunkPoint6'},
            {'trigger': 'step', 'source': 'TrunkPoint6', 'dest': 'End'}
        ]
        Machine.__init__(self, states=self.states, transitions=self.transitions,
                         initial='Begin', send_event=True)
        random.seed()
        self.random_number = None
        self.answer = 0

    def on_enter_Rules(self, event):
        rule = Rules()
        while rule.state != 'End':
            rule.step()

    def on_enter_Intro(self, event):
        print("""
        ╔═══════════════════════════════════════════════════════════════════╗
        ║ █   █ ▄▀▀▀▄ █▀▀▀▄ ▄▀▀▀▄   ▄▀█ █▀▀▀█ █▀▀▀▄ ▄▀▀▀▄ ▀▀█▀▀ █▀▀▀▄ ▄▀▀▀▄ ║
        ║ █ ▄▀  █   █ █   █ █   █ ▄▀  █ █     █   █ █   ▀   █   █   █ █   █ ║
        ║ █▀▄   █   █ █▄▄▄▀ █   █ █   █ █▀▀   █▀▀▀▄ █       █   █▀▀▀▄ █   █ ║
        ║ █  █  █   █ █     █   █ █   █ █     █   █ █   ▄   █   █   █ █   █ ║
        ║ █   █ ▀▄▄▄▀ █     ▀▄▄▄▀ █   █ █▄▄▄█ █▄▄▄▀ ▀▄▄▄▀   █   █▄▄▄▀ ▀▄▄▄▀ ║
        ║                 ▄                                                 ║
        ║       ▄▀▀▀▄  █     █ ▄▀▀█▀▀▄ ▄▀▀▀▀▀▄ █▀▀▀▀▀▄ █     █ ▄▀▀▀▀▀█      ║
        ║      ▀     █ █   ▄██ █  █  █ █     █ █     █ █   ▄██ █     █      ║
        ║         ▄▄▄█ █ ▄█▀ █ ▀▄▄█▄▄▀ █     █ █▄▄▄▄▄▀ █ ▄█▀ █ ▀▄▄▄▄▄█      ║
        ║      ▄     █ ██▀   █    █    █     █ █       ██▀   █   ▄▀  █      ║
        ║       ▀▄▄▄▀  █     █    █    ▀▄▄▄▄▄▀ █       █     █ ▄▀    █      ║
        ╚═══════════════════════════════════════════════════════════════════╝
        Version: """ + VERSION)

    def on_enter_MainMenu(self, event):
        print('1. Новая игра')
        print('2. Помощь')
        print('3. Выход')
        self.answer = int(input('==> '))

    def on_enter_NewGame(self, event):
        self.current_year = 1
        self.money = 10000  # деньги, руб
        self.gold = 0  # золото, кг
        self.land = 100  # земля, га
        self.grain = 1000  # зерно, тонн
        self.peasant = 100  # крестьяне, душ
        self.guard = 100  # гвардия, чел
        self.caravan_year = 0
        self.caravane_money = 0
        self.is_crisis = False
        self.crop_yield_level = None
        self.total_guard_maintenance = None
        # средние цены
        self.price_gold = 1000  # руб/кг
        self.price_land = 200  # руб/га
        self.price_grain = 10  # руб/тонн
        self.price_peasant = 50  # руб/душу
        self.guard_maintenance = 100  # руб/чел

    def on_enter_PrintState(self, event):
        print('-' * 80)
        print('                   Состояние Ваших дел на {}-й год правления.'.format(self.current_year))
        print('╔═════════════════╤════════════╗')
        print('║    Название     │   Запасы   ║')
        print('╠═════════════════╪════════════╣')
        print('║ Наличность, руб │ {:>10} ║'.format(self.money))
        print('║ Золото, кг.     │ {:>10} ║'.format(self.gold))
        print('║ Земля, га       │ {:>10} ║'.format(self.land))
        print('║ Зерно, тонн     │ {:>10} ║'.format(self.grain))
        print('║ Крестьяне, душ  │ {:>10} ║'.format(self.peasant))
        print('║ Гвардия, чел.   │ {:>10} ║'.format(self.guard))
        print('╚═════════════════╧════════════╝')

    def on_enter_VizirMessage(self, event):
        print('Ваше Величество, прибыл Главный Визирь с докладом.')
        print('Визирь сообщает:')
        print('Жалованье гвардии за прошлый год составило {} рублей.'.format(self.total_guard_maintenance))
        # TODO: добавить больше информации

    def on_enter_CaravanProfit(self, event):
        # TODO: показать доход каравана
        pass

    def on_enter_Crisis(self, event):
        # TODO: показать информацию о кризисе
        pass

    def on_enter_Exchange(self, event):
        # TODO: обработать биржу
        pass

    def on_enter_CaravanSupply(self, event):
        # TODO: добавить обработку
        pass

    def on_enter_CaravanRob(self, event):
        # TODO: добавить обработку
        pass

    def on_enter_Metropolitan(self, event):
        # TODO: добавить обработку
        pass

    def on_enter_TrunkPoint5(self, event):
        self.caravan_year += 1

    # условия
    def answerIsOne(self, event):
        logger.info('answerIsOne: self.answer = {}'.format(self.answer))
        if self.answer == 1:
            return True
        return False

    def answerIsTwo(self, event):
        logger.info('answerIsTwo: self.answer = {}'.format(self.answer))
        if self.answer == 2:
            return True
        return False

    def answerIsThree(self, event):
        logger.info('answerIsThree: self.answer = {}'.format(self.answer))
        if self.answer == 3:
            return True
        return False

    def isNotFirstYear(self, event):
        logger.info('isNotFirstYear: self.current_year = {}'.format(self.current_year))
        if self.current_year != 1:
            return True
        return False

    def is5YearCaravan(self, event):
        logger.info('is5YearCaravan: self.caravan_year = {}'.format(self.caravan_year))
        if self.caravan_year == 5:
            self.caravan_year = 0
            return True
        return False

    def is0YearCaravan(self, event):
        logger.info('is0YearCaravan: self.caravan_year = {}'.format(self.caravan_year))
        if self.caravan_year == 0:
            return True
        return False

    def isCrisis(self, event):
        logger.info('isCrisis: self.random_number = {}'.format(self.random_number))
        self.is_crisis = False
        if self.random_number < 25:
            self.is_crisis = True
        return self.is_crisis

    def isReceiveMetropolitan(self, event):
        logger.info('isReceiveMetropolitan: self.random_number = {}'.format(self.random_number))
        if self.random_number < 20:
            return True
        return False

    # утилитки
    def update_random(self, event):
        self.random_number = random.randint(0, 100)
        logger.info('update_random: self.random_number = {}'.format(self.random_number))

# ==================================================================================================================================================================
if __name__ == "__main__":
    handler = logging.FileHandler('euphoria.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.info('-' * 80)
    euphoria = Euphoria()
    while euphoria.state != 'End':
        euphoria.step()
