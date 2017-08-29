from random import randrange

from tombola import Tombola

@Tombola.register
class TomboList(list):
    def pick(self):
        try:
            position = randrange(len(self))
            return self.pop(position)
        except ValueError:
            raise LookupError('pop from empty TomboList')

    load = list.extend

    def loaded(self):
        return bool(self)

    def inspect(self):
        return tuple(sorted(self))
