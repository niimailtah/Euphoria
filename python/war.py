
#!/usr/bin/env python3
from transitions import Machine
from transitions import logger

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
if __name__ == "__main__":
    # -------------------------------------------------------
    pass
