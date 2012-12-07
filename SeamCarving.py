import Image
import GradL1EnergyFunc

def main():
    sc = SeamCarving("input_gray.png")
    e1 = GradL1EnergyFunc.GradL1EnergyFunc()
    sc.loadImage()
    sc.setFunction(e1)
    sc.getEnergyImage()
    sc.in_img.show()

class SeamCarving(object):
    def __init__(self, file_name):
        self.file_name = file_name

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
        for i in range():

    def getEnergyVisualImage(energy_img):
        rgb_center = (255, 127, 0)
        res_img = Image.new("RGB", energy_img.size)
        res_pix = res_img.load()
        energy_pix = energy_img.load()
        (width, height) = res_img.size
        # TODO(qi0914@gmail.com): make this loop parallel
        for i in range(width):
            for j in range(height):
                rgb = []
                for k in range(3):
                    val = 511 - abs(rgb_center[k] - energy_pix[i, j]) * 4
                    #val = energy_pix[i, j]
                    if val < 0:
                        val = 0
                    elif val > 255:
                        val = 255
                    rgb.append(val)
                res_pix[i, j] = tuple(rgb)
        return res_img

    def createClone(self):
        clone = SeamCarving(self.file_name)
        return clone

if __name__ == '__main__':
    main()
