from journeypy.core.data.value.Values import ValueHolder
from journeypy.core.data.variable.Variables import MapVariable
class Template(object):
    def process(self, context,io):
        mapVariable=self.get_required_variables_blind(context)
        context.pour(mapVariable.read(io))
        return self.fill(context)

    def get_required_variables_blind(self,context):
        return MapVariable({})

    def fillReturnValue(self,context):
        pass

    def fill(self,context):
        return ValueHolder.get_new_value_holder_for(self.fillReturnValue(context))

    def get_required_variables(self,context,io):
        if io==None:
            return self.get_required_variables_blind(self,context)
        return MapVariable({})

