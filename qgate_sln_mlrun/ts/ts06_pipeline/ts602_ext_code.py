import mlrun


class TS602Pipeline:

    def __init__(self, context, name=None, **kw):
        self.context = context
        self.name = name
        self.kw = kw

    def do(self, event):
        if self.name=="step1":
            self.step1(event)
        elif self.name=="step2":
            self.step2(event)
        elif self.name=="step3":
            self.step3(event)
        elif self.name=="step4":
            self.step4(event)
        return event

    def step1(self, event):
        if isinstance(event, mlrun.serving.server.MockEvent):
            data=event.body
        else:
            data=event
        calc = data['a'] * data['b']
        data['calc']=calc
        return event

    def step2(self, event):
        if isinstance(event, mlrun.serving.server.MockEvent):
            data=event.body
        else:
            data=event
        calc = data['calc'] + data['a'] + data['b']
        data['calc']=calc
        return event

    def step3(self, event):
        if isinstance(event, mlrun.serving.server.MockEvent):
            data=event.body
        else:
            data=event
        calc = data['calc'] + min(data['a'], data['b'])
        data['calc']=calc
        return event

    def step4(self, event):
        if isinstance(event, mlrun.serving.server.MockEvent):
            data=event.body
        else:
            data=event
        calc = data['calc'] + pow(data['a'], data['b'])
        data['calc']=calc
        return event


def step1(event):
    if isinstance(event, mlrun.serving.server.MockEvent):
        data = event.body
    else:
        data = event
    calc = data['a'] * data['b']
    data['calc'] = calc
    return event

def step2(event):
    if isinstance(event, mlrun.serving.server.MockEvent):
        data = event.body
    else:
        data = event
    calc = data['calc'] + data['a'] + data['b']
    data['calc'] = calc
    return event

def step3(event):
    if isinstance(event, mlrun.serving.server.MockEvent):
        data = event.body
    else:
        data = event
    calc = data['calc'] + min(data['a'], data['b'])
    data['calc'] = calc
    return event

def step4(event):
    if isinstance(event, mlrun.serving.server.MockEvent):
        data = event.body
    else:
        data = event
    calc = data['calc'] + pow(data['a'], data['b'])
    data['calc'] = calc
    return event