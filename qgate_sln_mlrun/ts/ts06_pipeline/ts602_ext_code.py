import mlrun


class TS602Pipeline:

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

    def first(self, event):

        if isinstance(event, mlrun.serving.server.MockEvent):
            data=event.body
        else:
            data=event
        calc = data['a'] * data['b']

#        data = {"calc": calc}
        data.clear()
        data['calc']=calc

    def second(self, event):
        if isinstance(event, mlrun.serving.server.MockEvent):
            data=event.body
        else:
            data=event
        calc = data["a"] + data["b"]
#        data = {"calc": calc}
        data.clear()
        data['calc']=calc
