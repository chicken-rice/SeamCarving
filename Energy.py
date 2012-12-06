from zope.interface import Interface

class Energy(Interface):
    def calcEnergy(self, img):
    """return energy image"""
