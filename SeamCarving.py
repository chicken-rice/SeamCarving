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
    
def main2():
    sc = SeamCarving("parts/part4.png")
    sc.loadImage()
    sc2 = SeamCarving("parts/part5.png")
    sc2.loadImage()
    sc3 = sc2.createClone()
    sc3.file_name = "parts/part4_5.png"
    
    e1 = GradL1EnergyFunc.GradL1EnergyFunc()
    lapl = LaplEnergyFunc.LaplEnergyFunc()
    sc.setFunction(e1)
    sc2.setFunction(lapl)
    
    sc.getEnergyImage()
    sc2.getEnergyImage()
    sc3.energy_img = addEnergy(sc.energy_img, sc2.energy_img)
    
    sc.test2()
    sc2.test2()
    sc3.test2()
    
def main3():
    sc = SeamCarving("parts/part4_side.png")
    sc.loadImage()
    sc2 = SeamCarving("parts/part5_side.png")
    sc2.loadImage()
    sc.lowpassFilter()
    sc2.lowpassFilter()

    sc3 = sc2.createClone()
    #sc4 = sc3.createClone()
    sc3.file_name = "parts/part45_side.png"
    #sc4.file_name = "parts/distance.png"
    
    e1 = GradL1EnergyFunc.GradL1EnergyFunc()
    lapl = LaplEnergyFunc.LaplEnergyFunc()
    sc.setFunction(e1)
    sc2.setFunction(lapl)
    
    sc.getEnergyImage()
    sc2.getEnergyImage()
    
    sc.adjustRange()
    sc2.adjustRange()
    

    
    sc3.energy_img = addEnergy(sc.energy_img, sc2.energy_img)
    #sc4.energy_img = addDistanceEnergy(sc.in_img, sc2.in_img)
    
    print max([max(sc.energy_img[i]) for i in range(len(sc.energy_img))]),
    print min([min(sc.energy_img[i]) for i in range(len(sc.energy_img))])

    print max([max(sc2.energy_img[i]) for i in range(len(sc2.energy_img))]),
    print min([min(sc2.energy_img[i]) for i in range(len(sc2.energy_img))])

    print max([max(sc3.energy_img[i]) for i in range(len(sc3.energy_img))]),
    print min([min(sc3.energy_img[i]) for i in range(len(sc3.energy_img))])    
    
    #print max([max(sc4.energy_img[i]) for i in range(len(sc4.energy_img))]),
    #print min([min(sc4.energy_img[i]) for i in range(len(sc4.energy_img))])    
    sc.test2()
    sc2.test2()
    sc3.test2()
    #sc4.test2()
    
    
class SeamCarving(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.energy_img = []

    def test(self):
        self.adjustRange()
        self.getEnergyVisualImage()
        self.res_img.show()
        
    def test2(self):
        thres = [3, 7, 15, 31, 63, 127, 255]
        sc_list = []
        for i in range(len(thres)):
             temp_sc = self.createClone()
             sc_list.append(temp_sc)

        print len(sc_list)
        for i in range(len(sc_list)):
            sc_list[i].energy_img = threshold_img(sc_list[i].energy_img, thres[i])
            sc_list[i].adjustRange()
            sc_list[i].getEnergyVisualImage()
            f_name = "result_low/" + sc_list[i].file_name.split("/")[1].split(".p")[0] + "_ene" + str(thres[i]) + ".png"
            f2_name = "result_low/" + sc_list[i].file_name.split("/")[1].split(".p")[0] + "_res" + str(thres[i]) + ".png"
            #sc_list[i].res_img.show()
            
            sc_list[i].res_img.save(f_name,"png")
            
            path = sc_list[i].getPath()
            (width, height) = sc_list[i].res_img.size
            pix = sc_list[i].res_img.load()
            for i in range(height):
                pix[path[i], i] = (255, 0, 0)
            sc_list[i].res_img.save(f2_name,"png")

        #self.energy_img = threshold_img(self.energy_img, 255)
        #self.adjustRange()
        #self.getEnergyVisualImage()
        #f_name = "result_low/" + self.file_name.split("/")[1].split(".p")[0] + "_ene255.png"
        #self.res_img.show()
        #self.res_img.save(f_name,"png")
        
    def saveEVI(self):
        self.getEnergyImage()
        self.adjustRange()
        self.getEnergyVisualImage()
        f_name = "result/" + self.file_name.split("/")[1].split(".p")[0] + "_ene.png"
        self.res_img.save(f_name,"png")

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

    def lowpassFilter(self):
        temp_img = self.in_img.copy()
        orig_pix = self.in_img.load()
        temp_pix = temp_img.load()
        (width, height) = self.in_img.size
        for i in range(width):
            for j in range(height):
                count = 0
                sum = 0
                for i2 in range(i-1, i+2):
                    for j2 in range(j-1, j+2):
                        #print i, j, i2, j2
                        if (0 <= i2 < width and 0 <= j2 < height):
                            sum += temp_pix[i2, j2]
                            count += 1
                            
                orig_pix[i, j] = sum / count
    

    def createClone(self):
        clone = SeamCarving(self.file_name)
        clone.in_img = self.in_img.copy()
        if len(self.energy_img) != 0:
            width = len(self.energy_img)
            height = len(self.energy_img[0])
            clone.energy_img = [[self.energy_img[i][j] for j in range(height)] for i in range(width)]

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

def addDistanceEnergy(img1, img2):
    #width = len(img1)
    #height = len(img1[0])
    (width, height) = img1.size
    pix1 = img1.load()
    pix2 = img2.load()
    res_ene = [[0 for j in range(height)] for i in range(width)]
    for i in range(width):
        for j in range(height):
            if pix1[i, j] != 0 and pix2[i, j] != 0:
                res_ene[i][j] = abs(pix1[i, j] - pix2[i, j])
    return res_ene

def threshold_img(in_ene, max_val):
    width = len(in_ene)
    height = len(in_ene[0])
    res_ene = [[in_ene[i][j] for j in range(height)] for i in range(width)]
    for i in range(width):
        for j in range(height):
            if in_ene[i][j] > max_val:
                res_ene[i][j] = max_val
    return res_ene

if __name__ == '__main__':
    main3()
