import Energy

class GradL1Energy(object):
    implements(Energy)

    def calcEnergy(self, img):
        (width, height) = img.size
        
