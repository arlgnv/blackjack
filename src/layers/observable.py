class Observable:
    def __init__(self):
        self._observers = {}

    def subscribe(self, event_name, callback):
        if event_name in self._observers:
            self._observers[event_name].append(callback)
        else:
            self._observers[event_name] = [callback]

    def notify(self, event_name, args=None):
        for callback in self._observers[event_name]:
            if args:
                callback(args)
            else:
                callback()
