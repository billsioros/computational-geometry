
from click import Choice


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
