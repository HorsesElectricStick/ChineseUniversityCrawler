

class BaseTask:
    @property
    def is_done(self) -> bool:
        return self._is_done

    @is_done.setter
    def is_done(self, value: bool) -> None:
        if type(value) != bool:
            raise TypeError("类{0}的is_done属性必须为bool类型，而不能为{1}类型".format(
                type(self).__name__, type(value).__name__))
        else:
            self._is_done = value

    def done(self) -> None:
        self.is_done = True

    def not_done(self) -> None:
        self.is_done = False
