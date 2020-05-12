
from functools import partial


class TraitMeta(type):
    def __init__(self, name, bases, attrs):
        super().__init__(name, bases, attrs)

        for trait in attrs.get('TRAITS', []):
            attr = f'_{trait}'
            if hasattr(self, trait) or hasattr(self, attr):
                continue

            def getter(self, attr=attr):
                return partial(getattr(self, attr), self)

            def setter(self, value, trait=trait, attr=attr):
                if value is None or callable(value):
                    setattr(self, attr, value)
                elif isinstance(value, str):
                    value = value.lower().replace("-", "_")
                    value = getattr(getattr(self, trait.title()), value)
                    setattr(self, attr, value)
                elif isinstance(value, list):
                    def value(v1, v2): return value[v1][v2]
                    setattr(self, attr, value)
                else:
                    raise TypeError(f'Unexpected type {type(value)}')

            setattr(self, trait, property(getter, setter))


class Trait(object, metaclass=TraitMeta):
    TRAITS = []

    def __init__(self, *args, **kwargs):
        super().__init__()

        for trait in self.TRAITS:
            if trait in kwargs:
                setattr(self, trait, kwargs[trait])
