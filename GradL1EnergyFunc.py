import EnergyFunc
import Image

class GradL1EnergyFunc(EnergyFunc.EnergyFunc):
    def calcEnergy(self, img):
        (width, height) = img.size
        pix = img.load()
        energy = [[0 for j in range(height)] for i in range(width)]
        
        for i in range(width):
            for j in range(height):
                dx = abs(pix[i, j] - pix[i+1, j]) if i != (width-1) else 0
                dy = abs(pix[i, j] - pix[i, j+1]) if j != (height-1) else 0
                energy[i][j] = dx + dy
        return energy

def main():
    in_img = Image.open("input_gray.png")
    l1_energy = GradL1EnergyFunc()
    energy = l1_energy.calcEnergy(in_img)
    print energy[3][4]

if __name__ == '__main__':
    main()
