import datetime
import math

import mlrun


class TS703Pipeline:

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
        elif self.name=="step5":
            self.step5(event)
        elif self.name=="step6":
            self.step6(event)
        elif self.name=="step7":
            self.step7(event)
        elif self.name=="step8":
            self.step8(event)
        elif self.name=="step9":
            self.step9(event)
        elif self.name=="step10":
            self.step10(event)
        return event

    def step1(self, event):
        if isinstance(event, mlrun.serving.server.MockEvent):
            data=event.body
        else:
            data=event
        data['calc'] = data['a'] * data['b']
        return event

    def step2(self, event):
        if isinstance(event, mlrun.serving.server.MockEvent):
            data=event.body
        else:
            data=event
        data['calc'] = data['calc'] + data['a'] + data['b']
        return event

    def step3(self, event):
        if isinstance(event, mlrun.serving.server.MockEvent):
            data=event.body
        else:
            data=event
        data['calc'] = data['calc'] + min(data['a'], data['b'])
        return event

    def step4(self, event):
        if isinstance(event, mlrun.serving.server.MockEvent):
            data=event.body
        else:
            data=event
        data['calc'] = data['calc'] + pow(data['a'], data['b'])
        return event

    def step5(self, event):
        if isinstance(event, mlrun.serving.server.MockEvent):
            data=event.body
        else:
            data=event
        data['calc'] = data['calc'] - (data['b'] * data['b'])
        return event

    def step6(self, event):
        if isinstance(event, mlrun.serving.server.MockEvent):
            data=event.body
        else:
            data=event
        data['calc'] = data['calc'] * 0.95
        return event

    def step7(self, event):
        if isinstance(event, mlrun.serving.server.MockEvent):
            data=event.body
        else:
            data=event
        data['calc'] = data['calc'] * 2
        return event

    def step8(self, event):
        if isinstance(event, mlrun.serving.server.MockEvent):
            data = event.body
        else:
            data = event
        data['calc'] = data['calc'] + 101
        return event

    def step9(self, event):
        if isinstance(event, mlrun.serving.server.MockEvent):
            data = event.body
        else:
            data = event
        data['calc'] = data['calc'] - 42
        return event

    def step10(self, event):
        if isinstance(event, mlrun.serving.server.MockEvent):
            data = event.body
        else:
            data = event
        data['calc'] = math.sin(data['calc'])
        return event

    def step11(self, event):
        if isinstance(event, mlrun.serving.server.MockEvent):
            data = event.body
        else:
            data = event
        if data['calc'] % 2:
            data['calc'] = data['calc'] - 1
        return event


def step1(event):
    if isinstance(event, mlrun.serving.server.MockEvent):
        data = event.body
    else:
        data = event
    data['calc'] = data['a'] * data['b']
    return event

def step2(event):
    if isinstance(event, mlrun.serving.server.MockEvent):
        data = event.body
    else:
        data = event
    data['calc'] = data['calc'] + data['a'] + data['b']
    return event

def step3(event):
    if isinstance(event, mlrun.serving.server.MockEvent):
        data = event.body
    else:
        data = event
    data['calc'] = data['calc'] + min(data['a'], data['b'])
    return event

def step4(event):
    if isinstance(event, mlrun.serving.server.MockEvent):
        data = event.body
    else:
        data = event
    data['calc'] = data['calc'] + pow(data['a'], data['b'])
    return event

def step5(event):
    if isinstance(event, mlrun.serving.server.MockEvent):
        data=event.body
    else:
        data=event
    data['calc'] = data['calc'] - (data['b'] * data['b'])
    return event

def step6(event):
    if isinstance(event, mlrun.serving.server.MockEvent):
        data=event.body
    else:
        data=event
    data['calc'] = data['calc'] * 0.95
    return event

def step7(event):
    if isinstance(event, mlrun.serving.server.MockEvent):
        data=event.body
    else:
        data=event
    data['calc'] = data['calc'] * 2
    return event

def step8(event):
    if isinstance(event, mlrun.serving.server.MockEvent):
        data=event.body
    else:
        data=event
    data['calc'] = data['calc'] + 101
    return event

def step9(event):
    if isinstance(event, mlrun.serving.server.MockEvent):
        data = event.body
    else:
        data = event
    data['calc'] = data['calc'] - 42
    return event

def step10(event):
    if isinstance(event, mlrun.serving.server.MockEvent):
        data = event.body
    else:
        data = event
    data['calc'] = math.sin(data['calc'])
    return event

def step11(event):
    if isinstance(event, mlrun.serving.server.MockEvent):
        data = event.body
    else:
        data = event
    if data['calc'] % 2:
        data['calc'] = data['calc'] - 1
    return event
