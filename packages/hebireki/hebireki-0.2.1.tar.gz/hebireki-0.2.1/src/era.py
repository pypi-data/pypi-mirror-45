from datetime import date


class Era:

    """
    A small data class describing a Japanese era
    """

    def __init__(self, kanji, english, start, end):
        self.kanji = kanji
        self.english = english
        self.short_kanji = kanji[0]
        self.letter = english[0]

        self.start = start
        self.end = end
