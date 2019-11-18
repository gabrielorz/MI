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

    def fitting_window(self, asp):
        """
        TO BE IMPLEMENTED
        Returns the smallest box that fits self but has the given aspect ratio
        """
        if self.aspect_ratio() != asp:
            new_asp = asp/self.aspect_ratio()
            xmin = self.xmin
            ymin = self.ymin
            xmax = self.xmax
            ymax = self.ymax
            if new_asp > 1:
                new_height = self.height
                new_width = asp*self.height
            else:
                new_width = self.width
                new_height = self.width/asp
            xmin = (xmax+xmin-new_width)/2
            ymin = (ymax+ymin-new_height)/2
            xmax = xmin + new_width
            ymax = ymin + new_height
        else:
            xmin = self.xmin
            ymin = self.ymin
            xmax = self.xmax
            ymax = self.ymax
        return Box2D(xmin, ymin, xmax, ymax)
