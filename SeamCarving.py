import Image
import GradL1EnergyFunc
import LaplEnergyFunc

def main():
    sc = SeamCarving("input_gray.png")
    sc.loadImage()
    sc2 = sc.createClone()
    sc3 = sc.createClone()
    e1 = GradL1EnergyFunc.GradL1EnergyFunc()
    lapl = LaplEnergyFunc.LaplEnergyFunc()
    sc.setFunction(e1)
    sc2.setFunction(lapl)

    sc.getEnergyImage()
    sc2.getEnergyImage()
    #sc3.energy_img = sc.energy_img
    sc3.energy_img = addEnergy(sc.energy_img, sc2.energy_img)
    #print addEnergy(sc.energy_img, sc2.energy_img)

    

    print max([max(sc.energy_img[i]) for i in range(len(sc.energy_img))]),
    print min([min(sc.energy_img[i]) for i in range(len(sc.energy_img))])

    print max([max(sc2.energy_img[i]) for i in range(len(sc2.energy_img))]),
    print min([min(sc2.energy_img[i]) for i in range(len(sc2.energy_img))])

    print max([max(sc3.energy_img[i]) for i in range(len(sc3.energy_img))]),
    print min([min(sc3.energy_img[i]) for i in range(len(sc3.energy_img))])
    sc.test()
    sc2.test()
    sc3.test()

class SeamCarving(object):
    def __init__(self, file_name):
        self.file_name = file_name

    def test(self):
        self.adjustRange()
        self.getEnergyVisualImage()
        self.res_img.show()

    def displayEVI(self):
        self.getEnergyImage()
        self.adjustRange()
        self.getEnergyVisualImage()
        self.res_img.show()

    def displayPathOnEVI(self):
        self.getEnergyImage()
        path = self.getPath()
        self.adjustRange()
        self.getEnergyVisualImage()
        
        (width, height) = self.res_img.size
        pix = self.res_img.load()
        for i in range(height):
            pix[path[i], i] = (255, 0, 0)
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
        ene_table = [[self.energy_img[i][j] for j in range(height)] for i in range(width)]
        for i in range(height-2, 0, -1):
            for j in range(width):
                min_val = ene_table[j][i+1]
                for k in [j-1, j+1]:
                    if 0 <= k < width and min_val > ene_table[k][i+1]:
                        min_val = ene_table[k][i+1]
                ene_table[j][i] += min_val

        path = []
        min_ind = 0
        for i in range(width):
           if ene_table[min_ind][0] > ene_table[i][0]:
               min_ind = i
        path.append(i)

        for i in range(1, height):
            min_inde = path[i-1]
            for j in [path[i-1]-1, path[i-1]+1]:
                if 0 <= j < width and ene_table[min_inde][i] > ene_table[j][i]:
                    min_inde = j
            path.append(min_inde)
        return path

    def createClone(self):
        clone = SeamCarving(self.file_name)
        clone.in_img = self.in_img.copy()
        return clone

def addEnergy(ene1, ene2):
    width = len(ene1)
    height = len(ene1[0])
    res_ene = [[0 for j in range(height)] for i in range(width)]
    for i in range(width):
        for j in range(height):
            if ene1[i][j] != 0 and ene2[i][j] != 0:
                res_ene[i][j] = ene1[i][j] + ene2[i][j]
    return res_ene


if __name__ == '__main__':
    main()
