#!/usr/bin/env python3
from transitions import Machine
from transitions import logger
from pathlib import Path
import time
import configparser
import random
import logging
# -------------------------------------------------------------------------
from rule import Rules

VERSION = '0.0.4'

# ==================================================================================================================================================================
class Exchange(Machine):
    def __init__(self):
        self.states = [
            {'name': 'Begin'},         #
            {'name': 'End'},           #
            {'name': 'Error'}          #
        ]
        self.transitions = [
            {'trigger': 'step', 'source': 'Begin',      'dest': 'End'}
        ]
        Machine.__init__(self, states=self.states, transitions=self.transitions,
                         initial='Begin', send_event=True)
        self.answer = None


# ==================================================================================================================================================================
class War(Machine):
    def __init__(self):
        self.states = [
            {'name': 'Begin'},         #
            {'name': 'End'},           #
            {'name': 'Error'}          #
        ]
        self.transitions = [
            {'trigger': 'step', 'source': 'Begin',      'dest': 'End'}
        ]
        Machine.__init__(self, states=self.states, transitions=self.transitions,
                         initial='Begin', send_event=True)
        self.answer = None


# ==================================================================================================================================================================
class Euphoria(Machine):
    def __init__(self):
        self.states = [
            {'name': 'Begin'},             #
            {'name': 'Node1'},             # after VizirMessage before CaravanProfit
            {'name': 'Node2'},             # after CaravanProfit before Crisis/Exchange
            {'name': 'Node3'},             # after Crisis/Exchange before CaravanSupply
            {'name': 'Node4'},             # after CaravanSupply before CaravanRob
            {'name': 'Node5'},             # after CaravanRob before Metropolitan
            {'name': 'Node6'},             # after Metropolitan before War
            {'name': 'Node7'},             # after War before ...
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
            {'trigger': 'step', 'source': 'PrintState', 'dest': 'VizirMessage', 'unless': 'isFirstYear'},
            {'trigger': 'step', 'source': 'PrintState', 'dest': 'Node1'},
            {'trigger': 'step', 'source': 'VizirMessage', 'dest': 'Node1'},
            {'trigger': 'step', 'source': 'Node1', 'dest': 'CaravanProfit', 'conditions': 'is5YearCaravan'},
            {'trigger': 'step', 'source': 'Node1', 'dest': 'Node2', 'before': 'update_random'},
            {'trigger': 'step', 'source': 'CaravanProfit', 'dest': 'Node2', 'before': 'update_random'},
            {'trigger': 'step', 'source': 'Node2', 'dest': 'Crisis', 'conditions': 'isCrisis'},
            {'trigger': 'step', 'source': 'Crisis', 'dest': 'Node3', 'before': 'update_random'},
            {'trigger': 'step', 'source': 'Node2', 'dest': 'Exchange', 'unless': 'isCrisis'},
            {'trigger': 'step', 'source': 'Exchange', 'dest': 'Node3', 'before': 'update_random'},
            {'trigger': 'step', 'source': 'Node3', 'dest': 'CaravanSupply', 'conditions': 'is0YearCaravan', 'before': 'update_random'},
            {'trigger': 'step', 'source': 'Node3', 'dest': 'Node4', 'before': 'update_random'},
            {'trigger': 'step', 'source': 'CaravanSupply', 'dest': 'Node4', 'before': 'update_random'},
            {'trigger': 'step', 'source': 'Node4', 'dest': 'CaravanRob', 'unless': 'is0YearCaravan', 'before': 'update_random'},
            {'trigger': 'step', 'source': 'Node4', 'dest': 'Node5', 'before': 'update_random'},
            {'trigger': 'step', 'source': 'CaravanRob', 'dest': 'Node5', 'before': 'update_random'},
            {'trigger': 'step', 'source': 'Node5', 'dest': 'Metropolitan', 'conditions': 'isReceiveMetropolitan'},
            {'trigger': 'step', 'source': 'Node5', 'dest': 'Node6', 'before': 'update_random'},
            {'trigger': 'step', 'source': 'Metropolitan', 'dest': 'Node6', 'before': 'update_random'},
            {'trigger': 'step', 'source': 'Node6', 'dest': 'War', 'conditions': 'isReasonWar'},
            {'trigger': 'step', 'source': 'Node6', 'dest': 'Node7', 'before': 'update_random'},
            {'trigger': 'step', 'source': 'War', 'dest': 'Node7', 'before': 'update_random'},
            {'trigger': 'step', 'source': 'Node7', 'dest': 'End'}
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
        self.message = """
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
             Version: """ + VERSION
        print(self.message)

    def on_enter_MainMenu(self, event):
        print('1. Новая игра')
        print('2. Помощь')
        print('3. Выход')
        self.answer = int(input('==> '))

    def on_enter_NewGame(self, event):
        self.current_year = 1
        self.money = 10000  # деньги, руб
        self.gold = 0       # золото, кг
        self.land = 100     # земля, га
        self.grain = 1000   # зерно, тонн
        self.peasant = 100  # крестьяне, душ
        self.guard = 100    # гвардия, чел
        self.caravan_year = 0
        self.caravane_money = 0
        self.is_crisis = False
        self.are_you_married = False
        self.crop_yield_level = None
        self.total_guard_maintenance = None
        self.is_revolution = False
        # средние цены
        self.price_gold = 1000  # руб/кг
        self.price_land = 200   # руб/га
        self.price_grain = 10   # руб/тонн
        self.price_peasant = 50 # руб/душу
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
        profit = self.caravane_money * 6
        print('Вернулся Ваш караван! Получено прибыли на сумму {} руб.!'.format(profit))
        self.money += self.caravane_money
        print('║ Наличность, руб │ {:>10} ║'.format(self.money)) # for test
        self.caravane_money = 0
        self.caravan_year = 0

    def on_enter_Crisis(self, event):
        print('Международный кризис! Торговля невозможна!')
        print('Вашему государству объявлена экономическая блокада!')
        self.is_crisis = True

    def on_enter_Exchange(self, event):
        # TODO: обработать биржу
        print('Желаете торговать на бирже (y/n)?  ==> ')
        exchange = Exchange()
        while exchange.state != 'End':
            exchange.step()
        self.is_crisis = True

    def on_enter_CaravanSupply(self, event):
        logger.info('on_enter_CaravanSupply: self.random_number = {}'.format(self.random_number))
        if self.random_number < 25:
            print('Заморский купец предлагает снарядить караван.\nВы согласны (y/n) ==> ')
            # TODO: добавить обработку
            print('В казне - {} руб, сколько на караван: '.format(self.money))
            self.caravane_money = 0 # TDOD: сдклать запрос и проверку на деньги
            print('Караван отправился за три-девять земель...')
            self.money -= self.caravane_money

        pass

    def on_enter_CaravanRob(self, event):
        logger.info('on_enter_CaravanRob: self.random_number = {}'.format(self.random_number))
        if self.random_number < 20:
            logger.info('on_enter_CaravanRob: rob')
            self.update_random(event)
            if self.random_number < 5:
                printf('Произошло ЧП! Ваш караван полностью разграблен бандитами!!!')
                self.caravan_year = 0
                self.caravane_money = 0
            else:
                self.update_random(event) # TODO: номер должен быть от 0 до 40
                robbed_money = int(self.caravane_money * self.random_number / 100)
                print('Внимание, ЧП! Ваш караван ограблен бандитами на сумму {} руб.!!!'.format(robbed_money))
                self.caravane_money -= robbed_money


    def on_enter_Metropolitan(self, event):
        # TODO: добавить обработку
        pass

    def on_enter_Node5(self, event):
        if self.caravan_year > 0:
            self.caravan_year += 1

    def on_enter_War(self, event):
        war = War()
        while war.state != 'End':
            war.step()

    def on_enter_VizirCatch(self, event):
        # TODO: добавить обработку
        pass

    def on_enter_Inheritance(self, event):
        # TODO: добавить обработку
        pass

    def on_enter_ChildBirthDay(self, event):
        # TODO: добавить обработку
        pass

    def on_enter_Marriage(self, event):
        # TODO: добавить обработку
        pass

    def on_enter_WifeDead(self, event):
        # TODO: добавить обработку
        pass

    def on_enter_WifeIn(self, event):
        # TODO: добавить обработку
        pass

    def on_enter_Sickness(self, event):
        # TODO: добавить обработку
        pass

    def on_enter_GiveGrain(self, event):
        # TODO: добавить обработку
        pass

    def on_enter_MakeTurn(self, event):
        # TODO: добавить обработку
        pass

    def on_enter_NextYear(self, event):
        # TODO: добавить обработку
        print('Будете править в следующем году (y/n)?  ==> ')

    def on_enter_NYParty(self, event):
        # TODO: добавить обработку
        printf('Будете устраивать Новогодний Бал (y/n)?  ==> ')

    def on_enter_EndTurn(self, event):
        # TODO: добавить обработку
        self.current_year += 1

    def on_enter_End(self, event):
        # TODO: добавить обработку
        self.on_enter_PrintState(event)
        if self.is_revolution:
            print('Голодающий народ ВОССТАЛ и свергнул нерадивого правителя!!!')
            print('Поздравляю Вас, батенька, с РЕВОЛЮЦИЕЙ, ха-ха...\n')
        else:
            print('Ваше правление завершилось...')
        # -------------------------------------------------------------------------
        # -------------------------------------------------------------------------
        points = 0
        points += int(self.money / 1000)
        points += int(self.gold * 2)
        points += int(self.land / 5)
        points += int(self.grain / 100)
        points += int(self.peasant / 20)
        points += int(self.guard / 10)
        # points += build_xram * 200
        points += self.current_year * 10
        # -------------------------------------------------------------------------
        print('╔═════════════════╤══════╤═══════════╗')
        print('║    Название     │ Коэф │   Очки    ║')
        print('╠═════════════════╪══════╪═══════════╣')
        print('║ Наличность      │ /1000│{:>10} ║'.format(int(self.money / 1000)))
        print('║ Золото          │    *2│{:>10} ║'.format(int(self.gold * 2)))
        print('║ Земля           │    /5│{:>10} ║'.format(int(self.land / 5)))
        print('║ Зерно           │  /100│{:>10} ║'.format(int(self.grain / 100)))
        print('║ Крестьяне       │   /20│{:>10} ║'.format(int(self.peasant / 20)))
        print('║ Гвардия         │   /10│{:>10} ║'.format(int(self.guard / 10)))
        print('║ Время правления │   *10│{:>10} ║'.format(self.current_year * 10))
        print('╠═════════════════╧══════╪═══════════╣')
        print('║ Общая сумма            │{:>10} ║'.format(points))
        print('╚════════════════════════╧═══════════╝')
        # print('новые храмы - {}; '.format(), build_xram * 200)
        # -------------------------------------------------------------------------
        print('Ну что ж... Поздравляю с успешным (?) окончанием игры.')
        if points > 0 and points <= 100:
            print('P.S. Вам бы лучше гусей пасти... Вместо Ваших крестьян...')
        elif points > 100 and points <= 300:
            print('P.S. Для новичка - сойдет... Хотя, конечно, неважно...')
        elif points > 300 and points <= 500:
            print('P.S. Ну, это уже кое-что... Худо-бедно, да ладно...')
        elif points > 500 and points <= 1000:
            print('P.S. Ну вот, кое-что уже получается. Старайтесь дальше...')
        elif points > 1000 and points <= 3000:
            print('P.S. Неплохо, весьма неплохо... Уважаю...')
        elif points > 3000 and points <= 5000:
            print('P.S. Что ж, видно, играть Вы умеете... Весьма недурственно...')
        elif points > 5000 and points <= 10000:
            print('P.S. Круто, что говорить... Да Вы, батенька, профессионал...')
        elif points > 10000 and points <= 100000:
            print('P.S. Прости их, Господи... Ну Вы, блин, даете!!!')
        elif points > 100000:
            print('P.S. NO pity, NO mercy, NO REGRET!!!!!!!!!!')
        else:
            print('ERROR!!!')
        print('-' * 80)

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

    def isFirstYear(self, event):
        logger.info('isFirstYear: self.current_year = {}'.format(self.current_year))
        if self.current_year == 1:
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

    def isReasonWar(self, event):
        logger.info('isReasonWar: self.random_number = {}'.format(self.random_number))
        # TODO: добавить условие, если Вы отказали жениться
        # print('Разозленный отказом жениться на его дочке, соседний король начал ВОЙНУ!')
        if self.guard < 100:
            if self.random_number > self.guard:
                print('Соседние короли, видя малочисленность Ваших войск, объявили Вам ВОЙНУ!')
                return True
        else:
            if self.random_number < 30:
                print('Есть возможность объявить войну одному из соседей.\nОбъявляете? (y/n) ==> ')
                return False # for test
        return True # for test

    def areYouMarried(self, event):
        return self.are_you_married

    # утилитки
    def update_random(self, event):
        self.random_number = random.randint(0, 100)
        logger.info('update_random: self.random_number = {}'.format(self.random_number))

# ==================================================================================================================================================================
if __name__ == "__main__":
    # -------------------------------------------------------
    # parse ini file
    config = configparser.ConfigParser(allow_no_value=True)
    config.read('euphoria.ini')
    # -------------------------------------------------------
    # logging
    __log_directory = Path('./logs')
    if not __log_directory.is_dir():
        __log_directory.mkdir()
    __log_handler = logging.FileHandler('./logs/{}_euphoria.log'.format(time.strftime('%Y-%m-%d_%H:%M:%S')))
    __log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    __log_handler.setFormatter(__log_formatter)
    logger.addHandler(__log_handler)
    logger.setLevel(logging.INFO)
    logger.info('-' * 80)
    # -------------------------------------------------------
    # game
    euphoria = Euphoria()
    while euphoria.state != 'End':
        euphoria.step()
