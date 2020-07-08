from .SeasonDirectory import SeasonPlayer

class Mode:
    def __init__(self, name: str):
        self.name = name

    def get_attr(self, player: SeasonPlayer):
        if player.stateOfMembership != 'MEMBER':
            return 'G'

class RapidMode(Mode):

    def get_attr(self, player):
        return super().get_attr(player) + 'B' if player.dwz < 1600 else ''

modes = {
    'RAPID_15PLUS0': RapidMode('Schnellschach 15+0')
}
