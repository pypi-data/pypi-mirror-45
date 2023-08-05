import sys
from journeypy.core.data.value.Values import ValueHolder,StringHolder
class Reader(object):
    def read(self,type):
        pass

    def get_writer(self):
        pass

    def set_writer(self,writer):
        pass

    def start_reading(self):
        pass

    def done_reading(self):
        pass

    def is_reading(self):
        pass

class Writer(object):
    # def __int__(self):
    #     pass

    def write_data(self,obj):
        pass

    def write_string(self,str):
        pass

    def get_reader(self):
        pass

    def set_reader(self,reader):
        pass

    def start_writing(self):
        pass

    def done_writing(self):
        pass

    def is_writing(self):
        pass

class IO(object):
    def __init__(self, writer=Writer(), reader=Reader()):
        self.writer = writer
        self.reader = reader
        self.writer.set_reader(self.reader)
        self.reader.set_writer(self.writer)

# def hello():
    # print("hello")

class ConsoleWriter(Writer):
    # out = sys.stdout

    # def __int__(self):
    #     # self.out = sys.stdout
    #     # hello()

    def write_data(self,obj):
        if(isinstance(obj,ValueHolder)):
            sys.stdout.write(obj.serialize())

    def write_string(self,string):
        sys.stdout.write(string)

    def get_reader(self):
        return self.reader

    def set_reader(self,reader):
        self.reader=reader

    def start_writing(self):
        pass

    def done_writing(self):
        pass

    def is_writing(self):
        return False


class ConsoleReader(Reader):
    sin=sys.stdin;
    def read(self,type):
        obj=type()
        obj.de_serialize(self.sin.readline())
        return obj

    def get_writer(self):
        return  self.writer

    def set_writer(self,writer):
        self.writer=writer

    def start_reading(self):
        pass

    def done_reading(self):
        pass

    def is_reading(self):
        return False;


class ConsoleIO(IO):
    def __int__(self, writer=ConsoleWriter(), reader=ConsoleReader()):
        super(ConsoleIO,self).__init__(writer,reader)

class MockOut(object):
    def __init__(self,strHolder):
        self.strHolder=strHolder

    def write(self,str):
        self.strHolder.value+=str

class MockIn(object):
    str=''
    def __init__(self,str):
        self.str=str
    def readline(self):
        return self.str

class MockIO(IO):
   def __init__(self,input='',output=None):
       if output==None:
           output=StringHolder()
           output.value=""
       min=MockIn(input)
       mout=MockOut(output)
       writer=ConsoleWriter()
       writer.out=mout
       reader=ConsoleReader()
       reader.sin=min
       super(MockIO, self).__init__(writer,reader)

def mock_consoleio(input=''):
    min = MockIn(input)
    writer = ConsoleWriter()
    reader = ConsoleReader()
    reader.sin = min
    return ConsoleIO(writer,reader)
