from journeypy.template.Template import Template
from journeypy.core.data.variable.Variables import MapVariable


class Text(Template):
    blocks=[]
    def process(self, context,io):
        mapVariable=self.get_required_variables(context,io)
        context.pour(mapVariable.read(io))
        return self.fill(context)

    def get_required_variables_blind(self, context):
        mapVariable=MapVariable({})
        return mapVariable

    def fillReturnValue(self, context):
        finalStr=''
        for block in self.blocks:
            finalStr+=block.fill(context)
        return finalStr

    def get_required_variables(self, context, io):
        mapVariable = MapVariable({})
        for block in self.blocks:
            mapVariable.map.update(block.get_required_variables(context).map)

        return mapVariable


class Block(object):
    def fill(self,context):
        pass

    def get_required_variables(self,context):
        pass

    def get_required_variables(self,context,io):
        return self.getRequiredVariables(self,context)

class StaticStringBlock(Block):
    value=None

    def __init__(self,value):
        self.value=value

    def fill(self,context):
        return self.value

    def get_required_variables(self,context):
        return MapVariable({})

class ExpressionBlock(Block):
    def __init__(self,expression):
        self.expression=expression

    def fill(self,context):
        return self.expression.fill(context).serialize()

    def get_required_variables(self,context):
        return self.expression.get_required_variables(context)

