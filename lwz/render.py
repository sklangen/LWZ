from .Mode import modes
from .SeasonDirectory import SeasonDirectory
from babel.dates import format_date
from jinja2 import Environment, PackageLoader, select_autoescape
import calendar


env = Environment(
    loader=PackageLoader('lwz', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

month_names = calendar.month_abbr[5:] + calendar.month_abbr[1:5]


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

    @property
    def headers(self):
        yield 'Name'
        yield 'DWZ'
        yield 'Attr'
        yield 'Punkte'

        for month in month_names:
            d = self.seasonDir.as_date(month)
            yield format_date(d, 'MMM YYYY', locale='de_DE')

    @property
    def rows(self):
        for player, score, months in sorted(self.rows_calculated, key=lambda t: t[1], reverse=True):
            yield [player.name, player.dwz, self.mode.get_attr(player), score] + months

    @property
    def rows_calculated(self):
        for player in self.seasonDir.season.players:
            months_played = dict(self.seasonDir.months_played(player))

            if months_played:
                score = sum(sorted((p.points for p in months_played.values()), reverse=True)[:6])
                months = [getattr(months_played.get(m), 'points', '') for m in month_names]

                yield player, score, months
