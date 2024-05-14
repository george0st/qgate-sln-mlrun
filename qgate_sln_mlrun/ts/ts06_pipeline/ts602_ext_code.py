import mlrun


class TS602Pipeline:

    def __init__(self, context, name=None, **kw):
        self.context = context
        self.name = name
        self.kw = kw

    def do(self, event):

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
        return event

def second(event):
    if isinstance(event, mlrun.serving.server.MockEvent):
        data=event.body
    else:
        data=event
    calc = data["a"] + data["b"]
#        data = {"calc": calc}
    data.clear()
    data['calc']=calc
    return event
