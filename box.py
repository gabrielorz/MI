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
            if new_asp <= 1:
                xmin = self.xmin
                xmax = self.xmax
                new_height = self.height * new_asp - self.height
                ymin = self.ymin-abs(new_height/2)
                ymax = self.ymax+abs(new_height/2)
            else:
                ymin = self.ymin
                ymax = self.ymax
                new_width = self.width * new_asp - self.width
                xmin = self.xmin-abs(new_width/2)
                xmax = self.xmax+abs(new_width/2)
        else:
            xmin = self.xmin
            ymin = self.ymin
            xmax = self.xmax
            ymax = self.ymax
        return Box2D(xmin, ymin, xmax, ymax)
