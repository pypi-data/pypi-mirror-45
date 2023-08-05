from journeypy.template.template.text.Templates import *
from journeypy.template.template.Expressions import *
def text(*argv):
    textObj=Text()
    textObj.blocks=argv
    return textObj;

def string(str):
    return StaticStringBlock(str)

def strExp(expression):
    return ExpressionBlock(expression)

def var(name):
    return VariableExpression(name)

def fun(operation,*expressions):
    return FunctionExpression(operation,expressions)