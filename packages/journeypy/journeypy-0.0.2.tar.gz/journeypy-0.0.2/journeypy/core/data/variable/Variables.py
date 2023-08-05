class Readable(object):
    def read(self,io):
        pass


class ValueHolderVariable(Readable):
    valueHolderClass=None

    def __init__(self,valueHolderClass):
        self.valueHolderClass=valueHolderClass

    def read(self,io):
        io.writer.write_string(" of type String\n")
        return io.reader.read(self.valueHolderClass).value


class MapVariable(Readable):
    map = {}

    def __init__(self,map):
        self.map=map

    def read(self,io):
        dataMap={}
        for key in self.map:
            io.writer.write_string("Please provide value for " + key)
            dataMap[key]=self.map[key].read(io)

        return dataMap;
