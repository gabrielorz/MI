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
        return '({}, {}, {}, {})'.format(self.xmin, self.ymin, self.xmax, self.ymax)

    def fitting_window(self, asp) :
        aspwd = self.aspect_ratio()
        if aspwd > asp :
            new_height = self.width /asp
            margin = (new_height -self.height)/2
            ymin = self.ymin - margin
            ymax = ymin + new_height
            window= Box2D(self.xmin, ymin, self.xmax, ymax)
        else :
            new_width = self.height *asp
            margin = (new_width -self.width)/2
            xmin = self.xmin - margin
            xmax = xmin + new_width
            window= Box2D(xmin, self.ymin, xmax, self.ymax)
        return window

    
