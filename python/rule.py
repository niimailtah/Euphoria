# ==================================================================================================================================================================
class Rules(Machine):
    def __init__(self):
        self.states = [
            {'name': 'Begin'},         #
            {'name': 'End'},           #
            {'name': 'ChoosePage'},    #
            {'name': 'FirstPage'},     #
            {'name': 'SecondPage'},    #
            {'name': 'Error'}          #
        ]
        self.transitions = [
            {'trigger': 'step', 'source': 'Begin',      'dest': 'ChoosePage'},
            {'trigger': 'step', 'source': 'ChoosePage', 'dest': 'FirstPage',  'conditions': ['verify', 'answerIsOne'], 'after': 'to_ChoosePage'},
            # {'trigger': 'step', 'source': 'ChoosePage', 'dest': 'Error',  'after': 'err'},
            # {'trigger': 'step', 'source': 'ChoosePage', 'dest': 'FirstPage',  'conditions': 'verify', 'after': 'to_ChoosePage'},
            {'trigger': 'step', 'source': 'FirstPage',  'dest': 'ChoosePage'},
            # {'trigger': 'step', 'source': 'FirstPage',  'dest': 'Error',  'after': 'err'},
            {'trigger': 'step', 'source': 'ChoosePage', 'dest': 'SecondPage', 'conditions': ['verify', 'answerIsTwo'], 'after': 'to_ChoosePage'},
            # {'trigger': 'step', 'source': 'ChoosePage', 'dest': 'SecondPage', 'conditions': 'verify', 'after': 'to_ChoosePage'},
            {'trigger': 'step', 'source': 'SecondPage', 'dest': 'ChoosePage'},
            {'trigger': 'step', 'source': 'SecondPage', 'dest': 'Error',  'after': 'err'},
            # {'trigger': 'step', 'source': 'ChoosePage', 'dest': 'End',        'conditions': ['verify', 'answerIsThree']},
            # {'trigger': 'step', 'source': 'ChoosePage', 'dest': 'End',        'conditions': 'verify'}
            # {'trigger': 'step', 'source': 'ChoosePage', 'dest': 'End'},
            {'trigger': 'step', 'source': '*', 'dest': 'End'}
        ]
        Machine.__init__(self, states=self.states, transitions=self.transitions,
                         initial='Begin', send_event=True)
        self.pageNumber = None
        self.answer = None

    def verify(self, event):
        if self.answer in [1, 2, 3]:
            return True
        # TODO: raise an Exception
        return False

    # TODO: An error should raise an Exaption
    def err(self, event):
        print('ERROR')

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
        logger.info('answerIsTree: self.answer = {}'.format(self.answer))
        if self.answer == 3:
            return True
        return False

    def on_enter_ChoosePage(self, event):
        print('1. Первая страница')
        print('2. Вторая страница')
        print('3. Выход')
        self.answer = int(input('==> '))

    def on_enter_FirstPage(self, event):
        if self.pageNumber == 1:
            return
        self.message = """
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
            ---------------------------------------------------------------------------------
            """
        print(self.message)
        self.pageNumber = 1

    def on_enter_SecondPage(self, event):
        if self.pageNumber == 2:
            return
        self.message = """
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
                                                       Adopted for *NIX by Niimailtah. 2014.
            ---------------------------------------------------------------------------------
            """
        print(self.message)
        self.pageNumber = 2


# ==================================================================================================================================================================
if __name__ == "__main__":
    rule = Rules()
    while rule.state != 'End':
        rule.step()
