import EnergyFunc
import Image

class LaplEnergyFunc(EnergyFunc.EnergyFunc):
    def calcEnergy(self, img):
        (width, height) = img.size
        pix = img.load()
        energy = [[pix[i, j] for j in range(height)] for i in range(width)]
        
        for i in range(2, width-1):
            for j in range(2, height-1):
                fil_val = 0
                for fil_i in range(-1, 2):
                    for fil_j in range(-1, 2):
                        fil_val -= pix[i+fil_i, j+fil_j]
                fil_val += 9 * pix[i, j]
                energy[i][j] = abs(fil_val)
        return energy

def main():
    in_img = Image.open("input_gray.png")
    energy_func = LaplEnergyFunc()
    energy = energy_func.calcEnergy(in_img)
    print energy[3][4]

if __name__ == '__main__':
    main()
