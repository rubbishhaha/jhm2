import matplotlib.image as img
import numpy as np

#input value
image = img.imread("test_image.webp")
h,w = image.shape[:2]
pix_w,pix_h = int(input("width:")),int(input("height:"))

#find gray scaled photo
balanced_image = np.zeros([h-h%pix_h,w-w%pix_w,1])
for i in range(h-h%pix_h):
    for u in range(w-w%pix_w):
        balanced_image[i][u] = (int(image[i][u][0]) + int(image[i][u][1]) + int(image[i][u][2]))/3

#scale image
nw = int((w-w%pix_w)/pix_w)
nh = int((h-h%pix_h)/pix_h)
scaled_image = np.zeros([nh,nw,1])
for i in range(nh):
    for u in range(nw):
        mean_pix = 0
        for pih in range(pix_h):
            mean_w = 0
            for piw in range(pix_w):
                mean_w += int(balanced_image[pix_h*i+pih][pix_w*u+piw])
               # print([i,u,piw,pih])
            mean_pix += mean_w/pix_w
        scaled_image[i][u] = mean_pix/pix_h

#print image
for i in range(nh):
    for u in range(nw):
        if scaled_image[i][u] >= 200:
            print("%",end="")
        elif scaled_image[i][u] >= 150:
            print("@",end="")
        elif scaled_image[i][u] >= 100:
            print("a",end="")
        elif scaled_image[i][u] >= 50:
            print("+",end="")
        elif scaled_image[i][u] >= 15:
            print("·",end="")
        else:
            print(" ",end="")
    print("")

                

            
        

