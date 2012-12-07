import Image
import GradL1EnergyFunc
import LaplEnergyFunc

def main():
    sc = SeamCarving("input_gray.png")
    sc.loadImage()
    sc2 = sc.createClone()
    e1 = GradL1EnergyFunc.GradL1EnergyFunc()
    lapl = LaplEnergyFunc.LaplEnergyFunc()
    sc.setFunction(e1)
    sc2.setFunction(lapl)

    sc.displayEVI()
    sc2.displayEVI()

class SeamCarving(object):
    def __init__(self, file_name):
        self.file_name = file_name

    def displayEVI(self):
        self.getEnergyImage()
        self.adjustRange()
        self.getEnergyVisualImage()
        self.res_img.show()

    def loadImage(self):
        self.in_img = Image.open(self.file_name)

    def setFunction(self, energy_func):
        self.func = energy_func

    def getEnergyImage(self):
        self.energy_img = self.func.calcEnergy(self.in_img)

    def adjustRange(self):
        max_val = max([max(self.energy_img[i]) for i in range(len(self.energy_img))])
        min_val = min([min(self.energy_img[i]) for i in range(len(self.energy_img))])
        range_val = max_val - min_val
        for i in range(len(self.energy_img)):
            for j in range(len(self.energy_img[0])):
                self.energy_img[i][j] = int((self.energy_img[i][j] - min_val) * 255 / range_val)

    def getEnergyVisualImage(self):
        width = len(self.energy_img)
        height = len(self.energy_img[0])
        rgb_center = (255, 127, 0)
        self.res_img = Image.new("RGB", (width, height))
        res_pix = self.res_img.load()

        # TODO(qi0914@gmail.com): make this loop parallel
        for i in range(width):
            for j in range(height):
                rgb = []
                for k in range(3):
                    val = 511 - abs(rgb_center[k] - self.energy_img[i][j]) * 4
                    if val < 0:
                        val = 0
                    elif val > 255:
                        val = 255
                    rgb.append(val)
                res_pix[i, j] = tuple(rgb)

    def getPath(self):
        width = len(self.energy_img)
        height = len(self.energy_img[0])
        

    def createClone(self):
        clone = SeamCarving(self.file_name)
        clone.in_img = self.in_img.copy()
        return clone

if __name__ == '__main__':
    main()
