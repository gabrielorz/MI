class Box2D:
    def __init__(self, xmin, ymin, xmax, ymax) :
         self.xmin = xmin
         self.ymin = ymin
         self.xmax = xmax
         self.ymax = ymax

    @property
    def width(self):
        return self.xmax-self.xmin
    
    @property
    def height(self):
        return self.ymax-self.ymin
    
    def aspect_ratio(self) :
        return self.width/self.height

            
    def __str__(self):
        return '({:2.2f}, {:2.2f}, {:2.2f}, {:2.2f})'.format(self.xmin, self.ymin, self.xmax, self.ymax)

    def fitting_window(self, asp) :
        """
        TO BE IMPLEMENTED
        Returns the smallest box that fits self but has the given aspect ratio
        """
        pass

    
