class Emitter:
    def __init__(self):
        self._notifications = []

    @property
    def valid(self):
        return len(self.notifications) == 0

    @property
    def invalid(self):
        return len(self.notifications) > 0

    @property
    def notifications(self):
        return self._notifications

    @notifications.setter
    def notifications(self, value):
        return self._notifications.append(value)

    @property
    def clear(self):
        self._notifications = []
