class saImage:
    def __init__(self, hour, faceID, minute, name, month):
        self.hour   = int(hour,   base=10)
        self.faceID = int(faceID, base=10)
        self.minute = int(minute, base=10)
        self.name   = name
        self.month  = int(month,  base=10)
        
    def fileName(self):
        return "faceID_"+str(self.faceID) +\
                "_name_"+str(self.name) +   \
                "_month_"+str(self.month) + \
                "_hr_"+str(self.hour) +     \
                "_min_"+str(self.minute) +  \
                "_.png"
                
    def __repr__(self):
        return repr((' ID: {:2}'.format(self.faceID)+
                        ', min: {:2}'.format(self.minute)+
                        ', hr: {:2}'.format(self.hour)+
                        ', month: {:2}'.format(self.month)+
                        ', name: {:14}'.format(self.name)+
                        ', filename: {}'.format(self.fileName())
                    ))