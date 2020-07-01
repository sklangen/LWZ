import yaml


class MyYAMLObject(yaml.YAMLObject):
    @classmethod
    def from_yaml(cls, loader, node):
        data = loader.construct_mapping(node, deep=True)
        return cls(**data)
 
    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_mapping(cls.yaml_tag, vars(data))


class SeasonPlayer(MyYAMLObject):
    yaml_tag = u'!SeasonPlayer'

    def __init__(self, id, dwz=0, stateOfMembership='MEMBER', names=None):
        self.id = id
        self.dwz = dwz
        self.stateOfMembership = stateOfMembership
        self.names = names or []


class Season(MyYAMLObject):
    yaml_tag = u'!Season'

    def __init__(self, mode, startYear, parentSeason=None, players=None):
        print('PLAYERS', players)
        self.mode = mode
        self.startYear = startYear
        self.parentSeason = parentSeason
        self.players = players or []


for cls in MyYAMLObject.__subclasses__():
    yaml.SafeDumper.add_multi_representer(cls, cls.to_yaml)
    yaml.SafeLoader.add_constructor(cls.yaml_tag, cls.from_yaml)
