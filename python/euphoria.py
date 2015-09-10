#!/usr/bin/env python3
from transitions import Machine
import random


# ===========================================================
class WidgetInfo(object):
    def __init__(self):
        pass


class MessageInfo(WidgetInfo):
    def __init__(self, message=''):
        super(MessageInfo, self).__init__()
        self.message = message

    def get_message(self):
        return self.message


class InputInfo(WidgetInfo):
    def __init__(self, message=''):
        super(InputInfo, self).__init__()
        self.message = message
        self.prompt = '==> '
        self.response = ''

    def get_message(self):
        return self.message

    def get_prompt(self):
        return self.prompt

    def get_response(self):
        return self.response

    def set_response(self, response=''):
        self.response = response


class ChoiceInfo(WidgetInfo):
    def __init__(self, message='', choices=[]):
        super(ChoiceInfo, self).__init__()
        self.message = message
        self.choices = choices
        self.response = -1

    def get_message(self):
        return self.message

    def get_choices(self):
        return self.choices

    def get_response(self):
        return self.response

    def set_choices(self, choices=[]):
        self.choices = choices


# ===========================================================
class Game(object):
    """
    """
    def __init__(self):
        self.euphoria = Euphoria()

    """
    """
    def run(self):
        print('Current state: {}'.format(self.euphoria.state))
        while self.euphoria.state != 'finish':
            self.euphoria.response = self.__process()
            prev_state = self.euphoria.state
            self.euphoria.StepMessage()
            if self.euphoria.state == prev_state:
                self.euphoria.StepInput()
                if self.euphoria.state == prev_state:
                    self.euphoria.StepChoice()
                    if self.euphoria.state == prev_state:
                        self.euphoria.Step()
                    else:
                        print('Current state: {}'.format(self.euphoria.state))
                else:
                    print('Current state: {}'.format(self.euphoria.state))
            else:
                print('Current state: {}'.format(self.euphoria.state))
        print('Current state: {}'.format(self.euphoria.state))

    """
    """
    def __process(self):
        if type(self.euphoria.widget_info).__name__ == 'MessageInfo':
            print(self.euphoria.widget_info.message)
            return None
        elif type(self.euphoria.widget_info).__name__ == 'InputInfo':
            print(self.euphoria.widget_info.message)
            response = input(self.euphoria.widget_info.prompt)
            self.euphoria.widget_info.set_response = response
            return response
        elif type(self.euphoria.widget_info).__name__ == 'ChoiceInfo':
            print(self.euphoria.widget_info.message)
            for i in range(len(self.euphoria.widget_info.choices)):
                print('{}. {}'.format(i, self.euphoria.widget_info.choices[i]))
            # TODO: add validation
            response = input('==> ')
            self.euphoria.widget_info.set_response = response
            return response


# ===========================================================
class Euphoria(object):
    def __init__(self):
        random.seed()
        self.widget_info = WidgetInfo()
        self._init_machine()

    """
    """
    @staticmethod
    def _fork():
        # print('fork')
        if random.randint(0, 1) == 1:
            return False
        return True

    """
    """
    def _init_machine(self):
        self.states = ['GameIntro', 'GameMenu', 'StartTurn', 'GameRules', 'Crisis',
                       'Trade', 'StartExchange', 'ChooseGoods', 'BuyOrSell', 'GoodsQuantity',
                       'EquipCaravan', 'CaravanMoney', 'RobCaravan',
                       'RequestMetropolitan', 'SpendMoney', 'WarReason', 'CatchVizier', 'Inherit', 'BornSon',
                       'WarChoice', 'GetMarried', 'DeadWifeMessenger', 'WarBegin', 'AskWife', 'Sick', 'Shaman',
                       'EndTurn', 'Revolution', 'Result', 'FinishGame',
                       'start', 'message', 'input', 'choice', 'finish']  # for test
        self.transitions = [
            {'trigger': 'ShowIntro', 'source': 'GameIntro', 'dest': 'GameMenu', 'after': '_intro'},
            {'trigger': 'GameMenu', 'source': 'GameMenu', 'dest': 'StartTurn', 'after': '_game_menu'},
            {'trigger': 'GameMenu', 'source': 'GameRules', 'dest': 'GameMenu', 'after': '_game_menu'},
            {'trigger': 'GameRules', 'source': 'GameMenu', 'dest': 'GameRules', 'after': '_game_rules'},
            {'trigger': 'FinishGame', 'source': 'GameMenu', 'dest': 'FinishGame', 'after': '_finish_game'},
            {'trigger': 'StepMessage', 'source': 'start', 'dest': 'message', 'conditions': '_fork',
             'after': '_message'},
            {'trigger': 'StepInput', 'source': 'start', 'dest': 'input', 'conditions': '_fork', 'after': '_input'},
            {'trigger': 'StepChoice', 'source': 'start', 'dest': 'choice', 'after': '_choice'},
            {'trigger': 'Step', 'source': 'message', 'dest': 'finish'},
            {'trigger': 'Step', 'source': 'input', 'dest': 'finish'},
            {'trigger': 'Step', 'source': 'choice', 'dest': 'finish'}
        ]
        self.machine = Machine(model=self, states=self.states, transitions=self.transitions, initial='start',
                               ignore_invalid_triggers=True)

    def _message(self):
        self.widget_info = MessageInfo(message='Message. Current state: {}'.format(self.state))

    def _input(self):
        self.widget_info = InputInfo(message='Input. Current state: {}'.format(self.state))

    def _choice(self):
        l = ['First', 'Second', 'Third']
        self.widget_info = ChoiceInfo(message='Choice. Current state: {}'.format(self.state), choices=l)

    """
    """
    @staticmethod
    def _intro():
        text = """
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
        ╚═══════════════════════════════════════════════════════════════════╝"""

    """
    """
    def _game_menu(self):
        l = ['Новая игра', 'Помощь (правила)', 'Выход']
        self.__choice(title='Главное меню', l=l)
        self._choice = input('==> ')

    """
    """
    def _game_rules(self):
        pass

    """
    """
    def _finish_game(self):
        pass


# ===========================================================
if __name__ == "__main__":
    game = Game()
    game.run()
