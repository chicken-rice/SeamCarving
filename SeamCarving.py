import Image

def getEnergyVisualImage(energy_img):
    #(min, max) = energy_img.getextrema()
    #range = max - min + 1
    rgb_center = (255, 127, 0)

    res_img = Image.new("RGB", energy_img.size)
    res_pix = res_img.load()
    energy_pix = energy_img.load()

    (width, height) = res_img.size
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

if __name__ == "__main__":
    in_img = Image.open("input_gray.png")
    in_img.show()
    in_pix = in_img.load()

    res = getEnergyVisualImage(in_img)
    res.show()
    res.save("res.png2", "png")

    
