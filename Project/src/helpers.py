
from click import Choice, Tuple


class Dictionary(Choice):
    name = 'dictionary'

    def __init__(self, choices):
        self.__choices = {}
        for k, v in choices.items():
            self.__choices[k.replace('_', '-')] = v

        super().__init__(sorted(self.__choices.keys()), case_sensitive=False)

    def convert(self, value, param, ctx):
        value = value.replace('_', '-')
        value = super().convert(value, param, ctx)

        return self.__choices[value]

    def get_metavar(self, param):
        return '|'.join(self.choices)


class Timewindow(Tuple):
    def __init__(self):
        super().__init__([float, float])

    def convert(self, value, param, ctx):
        hours, minutes = super().convert(value, param, ctx)

        if hours > 23:
            self.fail("Hours should be in the range [00, 23]", param, ctx)

        if minutes > 59:
            self.fail("Minutes should be in the range [00, 59]", param, ctx)

        return hours * 3600 + minutes * 60
