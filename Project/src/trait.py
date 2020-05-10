
class TraitMeta(type):
    def __init__(self, name, bases, attrs):
        super().__init__(name, bases, attrs)

        for trait in attrs['traits']:
            attr = f'_{trait}'
            assert not hasattr(self, attr), f'{self}.{attr} already set'
            assert not hasattr(self, trait), f'{self}.{trait} already set'

            def getter(self, attr=attr):
                return getattr(self, attr)

            def setter(self, value, attr=attr):
                if value is None or callable(value):
                    setattr(self, attr, value)
                elif isinstance(value, str):
                    value = value.lower().replace("-", "_")
                    value = getattr(self, value)
                    setattr(self, attr, value)
                elif isinstance(value, list):
                    def value(v1, v2): return value[v1][v2]
                    setattr(self, attr, value)
                else:
                    raise TypeError(f'Unexpected type {type(value)}')

            setattr(self, trait, property(getter, setter))


class Trait(object, metaclass=TraitMeta):
    traits = []

    def __init__(self, *args, **kwargs):
        super().__init__()
