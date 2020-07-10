from .SeasonDirectory import SeasonPlayer

class Mode:
    def __init__(self, name: str):
        self.name = name

    def get_attr(self, player: SeasonPlayer) -> str:
        if player.stateOfMembership != 'MEMBER':
            return 'G'
        return ''

class RapidMode(Mode):

    def get_attr(self, player: SeasonPlayer) -> str:
        return super().get_attr(player) + 'B' if player.dwz < 1600 else ''

modes = {
    'RAPID_15PLUS0_A': RapidMode('Schnellschach 15+0 A'),
    'RAPID_15PLUS0_B': RapidMode('Schnellschach 15+0 B')
}
