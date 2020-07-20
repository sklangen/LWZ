from .SeasonDirectory import SeasonPlayer
from .trf import Player, Tournament

class Mode:
    score_header = 'Punkte'

    def __init__(self, name: str):
        self.name = name

    def get_attr(self, player: SeasonPlayer) -> str:
        if player.stateOfMembership != 'MEMBER':
            return 'G'
        return ''

    def format_score(self, score):
        return str(score)

class RapidMode(Mode):

    def get_attr(self, player: SeasonPlayer) -> str:
        return super().get_attr(player) + ('B' if player.dwz < 1600 else '')

    def get_score(self, player: Player, tourmanent: Tournament) -> str: 
        return player.points

class BlitzMode(Mode):
    score_header = 'Prozent'

    def get_score(self, player: Player, tourmanent: Tournament) -> str:
        return 100 * player.points/tourmanent.numrounds

    def format_score(self, score):
        return f'{score:.2f}'

modes = {
    'RAPID_15PLUS0_A': RapidMode('Schnellschach 15+0 A'),
    'RAPID_15PLUS0_B': RapidMode('Schnellschach 15+0 B'),
    'BLITZ_5PLUS0': BlitzMode('Blitzschach 5+0'),
    'BLITZ_3PLUS2': BlitzMode('Blitzschach 3+2'),
}
