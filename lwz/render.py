from .Mode import modes
from .SeasonDirectory import SeasonDirectory
from jinja2 import Environment, PackageLoader, select_autoescape


env = Environment(
    loader=PackageLoader('lwz', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


class SeasonDirectoryRenderer:
    def __init__(self, seasonDir: SeasonDirectory):
        self.seasonDir = seasonDir
        self.mode = modes[seasonDir.season.mode]

    @property
    def index(self):
        return env.get_template('season.html').render(
            title=self.mode.name + ' - ' + self.seasonDir.season.name,
            renderer=self
        )
