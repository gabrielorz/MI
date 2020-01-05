"""
A class containing a list of objects

"""
class ObjectList:
    def __init__(self) :
        self.__objects = []

    def __getitem__(self, i) :
        return self.__objects[i]

    def __setitem__(self, i, obj):
        self.__objects[i] = obj

    def __len__(self):
        return len(self.__objects)

    def __str__(self):
        return "List of {:} objects".format(len(self))
    
    def append(self, object):
        object2 = self.get_object(object.name)
        if object2 != None:
            object.name = self.next_available_name(object.name)
        self.__objects.append(object)
    
    def get_object(self, name):
        for object in self:
            if object.name == name:
                return object
        return None

    def next_available_name(self, name):
        n = 0
        for object in self:
            if object.name.startswith(name+'_'):
                naux = int(object.name[object.name.find('_')+1:])
                if naux > n:
                    n = naux
        return name+'_'+str(n+1)

class ImageList(ObjectList):
    def render(self, ax):
        try:
            i = 0
            j = 0
            for idx in range(len(self)):
                self[idx].render(ax[i][j])
                j = j +1
                if j == ax.shape[1]:
                    i = i +1
                    j = 0
            if i < ax.shape[0] :
                while j < ax.shape[1]:
                    ax[i][j].axis('off')
                    j = j+1
        except:
            self[idx].render(ax)
            
