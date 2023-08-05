class Context(object):
    currentContext={}
    def __init__(self):
        self.currentContext={}
        self.ref=self.currentContext

    def get(self,key):
        return self.currentContext[key]

    def pour(self,map):
        Context.pour_to(self.ref,map)
        Context.pour_to(self.currentContext,map)

    @staticmethod
    def pour_to_map(mapTarget,mapSource):
        for key in mapSource:
            if key in mapTarget:
                Context.pour_to(mapTarget[key],mapSource[key])
            else:
                mapTarget[key]=mapSource[key]

    @staticmethod
    def pour_to_list(listTarget,listSource):
        if len(listTarget)>len(listSource):
            for i in range(len(listSource)):
                Context.pour_to(listTarget[i],listSource[i])
        else:
            for i in range(len(listTarget)):
                Context.pour_to(listTarget[i],listSource[i])

            for i in range(len(listTarget),len(listSource)):
                listTarget.append(listSource[i])

    @staticmethod
    def pour_to(target,source):
        if isinstance(target,dict) and isinstance(source,dict):
            Context.pour_to_map(target,source)
        elif isinstance(target,list) and isinstance(source,list):
            Context.pour_to_list(target,source)


