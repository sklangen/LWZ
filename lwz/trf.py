import io

class Player(object):
    def __init__(self):
        self.startrank = 0
        self.sex = 'm'
        self.title = ''
        self.name = ''
        self.fide = 0
        self.fed = ''
        self.id = ''
        self.birthdate = ''
        self.points = ''
        self.rank = ''

    def __repr__(self):
        return '%s (%s) FIDE-ID: %s FIDE-Rat: %s' % (self.name,
            self.fed,
            self.id,
            self.fide
        )


class Tournament(object):

    def __init__(self):
        self.name = u''
        self.city = u''
        self.federation = u''
        self.startdate = u''
        self.enddate = u''
        self.numplayers = 0
        self.numratedplayers = 0
        self.numteams = 0  # unsupported yet
        self.type = 0
        self.chiefarbiter = u''
        self.deputyarbiters = u''
        self.rateofplay = u''
        self.rounddates = []
        self.players = []
        self.teams = []
        self.xx_fields = {}

    def __repr__(self):
        return '%s (%s) from %s to %s' % (self.name,
          self.federation,
          self.startdate,
          self.enddate)


def dump(fp, tournament):
    _dump_tournament(fp, tournament)


def dumps(tournament):
    fp = io.StringIO()
    _dump_tournament(fp, tournament)
    return fp.getvalue()


def _dump_tournament(fp, tournament):
    fp.write(f'012 {tournament.name}\n')
    fp.write(f'022 {tournament.city}\n')
    fp.write(f'032 {tournament.federation}\n')
    fp.write(f'042 {tournament.startdate}\n')
    fp.write(f'052 {tournament.enddate}\n')
    fp.write(f'062 {tournament.numplayers}\n')
    fp.write(f'072 {tournament.numratedplayers}\n')
    fp.write(f'082 {tournament.numteams}\n')
    fp.write(f'092 {tournament.type}\n')
    fp.write(f'102 {tournament.chiefarbiter}\n')
    fp.write(f'112 {tournament.deputyarbiters}\n')
    fp.write(f'122 {tournament.rateofplay}\n')

    for field, value in tournament.xx_fields.items():
        fp.write(f'{field} {value}\n')

    for player in tournament.players:
        _dump_player(fp, player)
        fp.write('\n')


def _dump_player(fp, player):
    fp.write('001')
    fp.write(f' {player.startrank:>4}')
    fp.write(f' {player.sex:1}')
    fp.write(f' {player.title:>2}')
    fp.write(f' {player.name:<33}')
    fp.write(f' {player.fide:>4}')
    fp.write(f' {player.fed:<3}')
    fp.write(f' {player.id:>11}')
    fp.write(f' {player.birthdate:>10}')
    fp.write(f' {player.points:>4}')
    fp.write(f' {player.rank:>4}')

    for opponent in player.opponents:
        fp.write('  {id:>4} {color:1} {result:1}'.format(**opponent))


def load(fp):
    return _parse_tournament(fp.readlines())


def loads(s):
    return _parse_tournament(s.split('\n'))


def _parse_tournament(lines):
    tournament = Tournament()

    for line in lines:
        data = line[4:].strip()

        if line.startswith('012 '):
            tournament.name = data
        elif line.startswith('022 '):
            tournament.city = data
        elif line.startswith('032 '):
            tournament.federation = data
        elif line.startswith('042 '):
            tournament.startdate = data
        elif line.startswith('052 '):
            tournament.enddate = data
        elif line.startswith('062 '):
            tournament.numplayers = int(data)
        elif line.startswith('072 '):
            tournament.numratedplayers = int(data)
        elif line.startswith('082 '):
            tournament.numteams = int(data)
        elif line.startswith('092 '):
            tournament.type = data
        elif line.startswith('102 '):
            tournament.chiefarbiter = data
        elif line.startswith('112 '):
            tournament.deputyarbiters = data
        elif line.startswith('122 '):
            tournament.rateofplay = data
        elif line.startswith('132 '):
            tournament.rounddates = _group_string(data, 10)
        elif line.startswith('001 '):
            player = _parse_player(line)
            tournament.players.append(player)
        elif line.startswith('013 '):
            team = tournament._parse_team(data)
            tournament.teams.append(team)
        elif line.startswith('XX'):
            name = line[:3]
            tournament.xx_fields[name] = data
    return tournament


def _parse_player(line):
    player = Player()
    player.startrank = line[4:8].strip()
    player.sex = line[9].strip()
    player.title = line[10:13].strip()
    player.name = line[14:47].strip()
    player.fide = line[48:52].strip()
    player.fed = line[53:56].strip()
    player.id = line[57:68].strip()
    player.birthdate = line[69:79].strip()
    player.points = line[80:84].strip()
    player.rank = line[85:89].strip()
    player.opponents = list(_parse_opponents(line[91:].rstrip()))
    return player


def _parse_opponents(string):
    round = 1
    while len(string) >= 7:
        yield {
            'id': string[:4].strip(),
            'color': string[5],
            'result': string[7],
            'round': round
        }
        round += 1
        string = string[10:]

def _parse_team(data):
    pass


def _group_string(string, n):
    items = zip(*[string[i::n] for i in range(n)])
    return [''.join(item).rstrip() for item in items]
