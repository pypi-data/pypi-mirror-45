#!/usr/bin/python3

from datetime import *
from .era import *
import string
import re


class Wareki:

    """
    A class which wraps around a datetime object (dt), extending functionality
    to work with the traditional Japanese calendar format as well as Japanese time and date formats
    """

    # A hard-coded list of Japanese eras
    eras = [
        Era("令和", "Reiwa", datetime(2019, 5, 1), None),  # A 'None' as an end date means it's the current era
        Era("平成", "Heisei", datetime(1989, 8, 1), datetime(2019, 4, 30)),
        Era("昭和", "Showa", datetime(1926, 12, 25), datetime(1989, 1, 7)),
        Era("大正", "Taisho", datetime(1912, 7, 30), datetime(1926, 12, 24)),
        Era("明治", "Meiji", datetime(1867, 2, 3), datetime(1912, 7, 29)),  # Eras before Meiji were not well defined
    ]

    def __init__(self, dt=None):
        if dt is None:
            dt = datetime.now()
        self.dt = dt

    def __str__(self):
        """
        :return: Returns a string representation using the Japanese calendar format of the date and time with kanji
        """
        return str(self.strftime("%@EE%@N年%-m月%d日 (%@A) %-H時%M分%S秒"))

    def era(self):
        """
        :return: the Japanese era (as an instance of Era) of the given datetime
        """

        # Find the latest era which started before the datetime
        for era in self.eras:
            if self.dt >= era.start:
                return era
        return self.eras[-1]

    def era_year(self, gannen=False):
        """
        :param gannen: (default=False) use the tradition of using the kanji "元" instead of "1" for the first year
        :return: the year within the Japanese era of the datetime
        """
        greg_year = self.dt.year
        japan_year = greg_year - self.era().start.year + 1
        if gannen:
            return "元" if japan_year == 1 else str(japan_year)
        else:
            return japan_year

    def strftime(self, format_spec, modifier="%@"):
        """
        A wrapper on top of datetime.strftime() which implements a number of Japanese formatting options for
        dates and times. The prefix symbol is given by "modifier" and by default is "%@".

        The list of symbols are as follows:
            E       Short kanji representation of the era (E.g. 平)
            EE      Full kanji representation of the era (E.g. 平成)
            e       Short romanised representation of the era (E.g. H)
            ee      Full kanji representation of the era (E.g. Heisei)
            n       The year within the era (E.g. 31 for 2019)
            N       The year within the era, using gannen (E.g. 元 for Mar 1 2019)
            a       Short kanji representation of the day of the week (金 for Friday)
            A       Full kanji representation of the day of the week (金曜日 for Friday)

        :param format_spec: The strftime string to be formatted
        :param modifier: (default="%@") the prefix to each symbol (as to not conflict with normal strftime)
        :return: the result of the above strftime conversions on top of regular strftime
        """
        code_conversion = {
            "E": self.era().short_kanji,
            "EE": self.era().kanji,
            "e": self.era().letter,
            "ee": self.era().english,
            "n": self.era_year(),
            "N": self.era_year(True),
            "a": self.kanji_weekday(),
            "A": self.full_kanji_weekday()
        }
        new_string = self.dt.strftime(format_spec)
        for code, value in code_conversion.items():
            if len(code) == 1:
                new_string = re.sub(r"{1}{0}(?!{0})".format(code, modifier), str(value), new_string)
            else:
                new_string = new_string.replace(modifier + code, value)
        return new_string

    def kanji_weekday(self):
        """
        :return: A short kanji representation of the day of the week
        """
        weekdays = ["日", "月", "火", "水", "木", "金", "土"]
        return weekdays[self.dt.weekday()]

    def full_kanji_weekday(self):
        """
        :return: A full kanji representation of the day of the week
        """
        return self.kanji_weekday() + "曜日"
