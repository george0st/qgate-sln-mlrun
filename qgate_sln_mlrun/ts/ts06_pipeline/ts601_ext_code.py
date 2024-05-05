import mlrun


class TS601Pipeline:

    def __init__(self, context, name=None, **kw):
        self.context = context
        self.name = name
        self.kw = kw

    def do(self, event):
        if self.name.lower()=="multipl":
            self._multipli(event)
        elif self.name.lower()=="plus":
            self._plus(event)
        return event

    def _multipli(self, event):
        calc = event.body["a"] * event.body["b"]
        event.body = {"calc": calc}

    def _plus(self, event):
        calc = event.body["a"] + event.body["b"]
        event.body = {"calc": calc}

def minus(event):
    calc = event.body["a"] + event.body["b"]
    event.body = {"calc": calc}
    return event
