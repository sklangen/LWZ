from dataclasses import dataclass, field
from typing import List
import yaml


class MyYAMLObject(yaml.YAMLObject):
    @classmethod
    def from_yaml(cls, loader, node):
        data = loader.construct_mapping(node, deep=True)
        return cls(**data)
 
    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_mapping(cls.yaml_tag(), vars(data))

    @classmethod
    def yaml_tag(cls):
        return u'!' + cls.__name__


@dataclass
class SeasonPlayer(MyYAMLObject):
    '''Represating a player participating in a season'''

    id: str
    dwz: int = 0
    stateOfMembership: str = 'MEMBER'
    names: List[str] = field(default_factory=list)


@dataclass
class Season(MyYAMLObject):
    '''Represating a season of monthly tournaments played from May, startYear to April, endYear'''

    mode: str
    startYear: int
    parentSeason: str = None
    players: List[SeasonPlayer] = field(default_factory=list)

    @property
    def endYear(self):
        return self.startYear+1


for cls in MyYAMLObject.__subclasses__():
    yaml.SafeDumper.add_multi_representer(cls, cls.to_yaml)
    yaml.SafeLoader.add_constructor(cls.yaml_tag(), cls.from_yaml)
