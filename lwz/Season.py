import yaml

class YAMLObject(yaml.YAMLObject):
    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            raise ValueError('Position argument are not supported')
        self.__setstate__(kwargs)


class SeasonPlayer(YAMLObject):
    yaml_tag = u'!SeasonPlayer'

    def __setstate__(self, d):
        self.id = d['id']
        self.dwz = d.get('dwz', 0)
        self.stateOfMembership = d.get('stateOfMembership', 'MEMBER')
        self.names = d['names']


class Season(YAMLObject):
    yaml_tag = u'!Season'

    def __setstate__(self, d):
        self.mode = d['mode']
        self.startYear = d['startYear']
        self.parentSeason = d.get('parentSeason')
        self.players = d.get('players', [])
