from collections import OrderedDict
class Serializable(object):
    def de_serialize(self,str):
        pass

    def serialize(self):
        pass


class ValueHolder(Serializable):
    type=None
    value=None

    __valueHolderMap = OrderedDict()

    def __str__(self):
        return self.serialize()

    def __add__(self, other):
        if isinstance(other,str):
            return str(self) + other
        else:
            return str(self) + str(other)

    def __radd__(self, other):
        if isinstance(other,str):
            return other + str(self)
        else:
            return str(other)+str(self)


    @staticmethod
    def get_appropriate_value_holder(typeProvided):
        for typeInRegistry,valueHolderType in ValueHolder.__valueHolderMap.items():
            if issubclass(typeProvided,typeInRegistry):
                return valueHolderType

    @staticmethod
    def get_new_value_holder_for(data):
        valueholder=ValueHolder.get_appropriate_value_holder(type(data))()
        valueholder.value=data
        return valueholder

    @classmethod
    def register(cls,type):
        def real_decorator(scls):
            ValueHolder.__valueHolderMap[type] = scls
            return scls

        return real_decorator


@ValueHolder.register(int)
class IntegerHolder(ValueHolder):
    def __init__(self):
        self.value=None

    def de_serialize(self,str):
        self.value=int(str)

    def serialize(self):
        return str(self.value)

    def __add__(self, other):
        if isinstance(other,str):
            return str(self) + other
        elif isinstance(other,IntegerHolder):
            retHolder=IntegerHolder()
            retHolder.value=self.value+other.value
            return retHolder
        elif isinstance(other,int):
            retHolder = IntegerHolder()
            retHolder.value = self.value + other
            return retHolder
        else:
            return str(self) + str(other)

    def __radd__(self, other):
        if isinstance(other,str):
            return other + str(self)
        elif isinstance(other,IntegerHolder):
            retHolder=IntegerHolder()
            retHolder.value=self.value+other.value
            return retHolder
        elif isinstance(other,int):
            retHolder = IntegerHolder()
            retHolder.value = self.value + other
            return retHolder
        else:
            return str(other) + str(self)


@ValueHolder.register(str)
class StringHolder(ValueHolder):

    def __init__(self):
        self.value = None

    def de_serialize(self,string):
        self.value = string

    def serialize(self):
        return self.value

@ValueHolder.register(type(None))
class NoneHolder(ValueHolder):
    def __init__(self):
        self.value = None

    def de_serialize(self,string):
        self.value=None

    def serialize(self):
        return self.value

@ValueHolder.register(object)
class ObjectHolder(ValueHolder):
    def __init__(self):
        self.value = None

    def de_serialize(self,string):
        self.value=None

    def serialize(self):
        return self.value