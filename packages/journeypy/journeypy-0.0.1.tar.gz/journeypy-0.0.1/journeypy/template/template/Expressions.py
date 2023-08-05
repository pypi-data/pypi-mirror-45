from journeypy.template.data.value.Values import ValueHolder,StringHolder
from journeypy.template.data.variable.Variables import MapVariable,ValueHolderVariable
class Expression(object):
    def fill(self,context):
        pass

    def get_required_variables(self,context):
        pass

class ConstantExpression(Expression):
    def __init__(self,value):
        self.value=value



    def fill(self,context):
        return ValueHolder.get_new_value_holder_for(self.value)

    def get_required_variables(self,context):
        mapVariable = MapVariable({})
        return mapVariable

class VariableExpression(Expression):
    def __init__(self,name):
        self.name=name

    def ofType(self,type):
        self.type=type
        return self

    def fill(self,context):
        data=context.get(self.name)
        return ValueHolder.get_new_value_holder_for(data)

    def get_required_variables(self,context):
        mapVariable = MapVariable({})

        if not self.name in context.currentContext:
            valueholderType=ValueHolder.get_appropriate_value_holder(self.type)
            valueholderVariable=ValueHolderVariable(valueholderType)
            mapVariable.map[self.name]=valueholderVariable

        return mapVariable

class FunctionExpression(Expression):
    def __init__(self,operation,expressions=[]):
        self.operation=operation
        self.expressions=expressions

    def with_argument(self,expression):
        self.expressions.append(expression)

    def fill(self,context):
        lstVH=[]
        for expression in self.expressions:
            lstVH.append(expression.fill(context))
        val=self.operation(*lstVH)
        if isinstance(val,ValueHolder):
            return val
        else:
            return ValueHolder.get_new_value_holder_for(val)

    def get_required_variables(self,context):
        mapVariable = MapVariable({})

        if not self.name in context.currentContext:
            valueholderType=ValueHolder.get_appropriate_value_holder()
            valueholderVariable=ValueHolderVariable(valueholderType)
            mapVariable.map[self.name]=valueholderVariable

        return mapVariable

