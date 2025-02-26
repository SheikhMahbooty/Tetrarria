class Colors:
    gray = (127, 127, 127)
    cyan = (15, 155, 215)
    yellow = (227, 155, 4)
    purple = (175, 41, 138)
    green = (92, 178, 5)
    red = (219, 52, 28)
    blue = (33, 65, 198)
    orange = (227, 91, 2)
    darker_blue = (44, 44, 127)
    white = (255, 255, 255)
    light_blue = (0, 153, 153)
    
    @classmethod
    def get_cell_colors(cls):
        return [cls.gray, cls.cyan, cls.yellow, cls.purple,
                cls.green, cls.red, cls.blue, cls.orange]        