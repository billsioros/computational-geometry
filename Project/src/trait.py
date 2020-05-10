
class TraitMeta(type):
    def __init__(self, name, bases, attrs):
        super().__init__(name, bases, attrs)

        for field in attrs['traits']:
            assert not hasattr(
                self, f'_{field}'
            ), f'{self}._{field} already set'
            assert not hasattr(
                self, field
            ), f'{self}.{field} already set'

            def getter(self, field=field):
                return getattr(self, f'_{field}')

            def setter(self, value, field=field):
                if value is None or callable(value):
                    setattr(self, f'_{field}', value)
                elif isinstance(value, str):
                    value = value.lower().replace("-", "_")
                    value = getattr(self, value)
                    setattr(self, f'_{field}', value)
                elif isinstance(value, list):
                    def value(v1, v2): return value[v1][v2]
                    setattr(self, f'_{field}', value)
                else:
                    raise TypeError(f'Unexpected type {type(value)}')

            setattr(self, field, property(getter, setter))


class Trait(object, metaclass=TraitMeta):
    traits = []

    def __init__(self, *args, **kwargs):
        super().__init__()
