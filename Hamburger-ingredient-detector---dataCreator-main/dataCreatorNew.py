from PIL import Image, ImageOps
import numpy as np

with open("mean_list.txt", "w") as dosya:
    dosya.write("")

min_rate = 0.9
max_rate = 1.1
img_path_list = ["Pictures/00Fullimage.png","Pictures/1.png","Pictures/2.png","Pictures/3.png","Pictures/4.png"]

#data creator
def get_all_rgb(piece):
    image_RGB = []
    # open img
    image = piece

    # take img size
    width, height = image.size

    # loop all pixels
    for y in range(int(height)):
        for x in range(int(width)):
            # take pixels RGB
            rgb_value = image.getpixel((x, y))
            R = rgb_value[0]
            G = rgb_value[1]
            B = rgb_value[2]
            if (R == 0)  or (G == 0) or (B == 0):
                pass
            elif (R/G >= min_rate and R/G <= max_rate) and (R/B >= min_rate and R/B <= max_rate) and (B/G >= min_rate and B/G <= max_rate):
                pass
            else:
                image_RGB.append([R,G,B])

    return image_RGB

the_list = []
for img_path in img_path_list:
    # open img file
    image = Image.open(img_path)

    # img width height
    width, height = image.size

    # Parçaların width height
    piece_width = width // 5
    piece_height = height // 2

    # spread pieces
    pieces = []
    for i in range(10):
        x = (i % 5) * piece_width
        y = (i // 5) * piece_height
        piece = image.crop((x, y, x + piece_width, y + piece_height))


        # Take all RGB values
        img_values = get_all_rgb(piece)
        R_list = []
        G_list = []
        B_list = []

        for a in img_values:
            R_list.append(a[0])
            G_list.append(a[1])
            B_list.append(a[2])

        R_mean = int(np.mean(R_list))
        G_mean = int(np.mean(G_list))
        B_mean = int(np.mean(B_list))
        the_list.append([R_mean,G_mean,B_mean])


r0,r1,r2,r3,r4,r5,r6,r7,r8,r9 = 0,0,0,0,0,0,0,0,0,0
g0,g1,g2,g3,g4,g5,g6,g7,g8,g9 = 0,0,0,0,0,0,0,0,0,0
b0,b1,b2,b3,b4,b5,b6,b7,b8,b9 = 0,0,0,0,0,0,0,0,0,0


for i in range(len(the_list)):
    print(the_list[i])
    if i%10 == 0:
        r0+=the_list[i][0]
        g0+=the_list[i][1]
        b0+=the_list[i][2]
    if i%10 == 1:
        r1+=the_list[i][0]
        g1+=the_list[i][1]
        b1+=the_list[i][2]
    if i%10 == 2:
        r2+=the_list[i][0]
        g2+=the_list[i][1]
        b2+=the_list[i][2]
    if i%10 == 3:
        r3+=the_list[i][0]
        g3+=the_list[i][1]
        b3+=the_list[i][2]
    if i%10 == 4:
        r4+=the_list[i][0]
        g4+=the_list[i][1]
        b4+=the_list[i][2]
    if i%10 == 5:
        r5+=the_list[i][0]
        g5+=the_list[i][1]
        b5+=the_list[i][2]
    if i%10 == 6:
        r6+=the_list[i][0]
        g6+=the_list[i][1]
        b6+=the_list[i][2]
    if i%10 == 7:
        r7+=the_list[i][0]
        g7+=the_list[i][1]
        b7+=the_list[i][2]
    if i%10 == 8:
        r8+=the_list[i][0]
        g8+=the_list[i][1]
        b8+=the_list[i][2]
    if i%10 == 9:
        r9+=the_list[i][0]
        g9+=the_list[i][1]
        b9+=the_list[i][2]
length_img_list = len(img_path_list)
r0 = r0/length_img_list
r1 = r1/length_img_list
r2 = r2/length_img_list
r3 = r3/length_img_list
r4 = r4/length_img_list
r5 = r5/length_img_list
r6 = r6/length_img_list
r7 = r7/length_img_list
r8 = r8/length_img_list
r9 = r9/length_img_list

g0 = g0/length_img_list
g1 = g1/length_img_list
g2 = g2/length_img_list
g3 = g3/length_img_list
g4 = g4/length_img_list
g5 = g5/length_img_list
g6 = g6/length_img_list
g7 = g7/length_img_list
g8 = g8/length_img_list
g9 = g9/length_img_list

b0 = b0/length_img_list
b1 = b1/length_img_list
b2 = b2/length_img_list
b3 = b3/length_img_list
b4 = b4/length_img_list
b5 = b5/length_img_list
b6 = b6/length_img_list
b7 = b7/length_img_list
b8 = b8/length_img_list
b9 = b9/length_img_list

new_list_rgb = [[r0,g0,b0],[r1,g1,b1],[r2,g2,b2],[r3,g3,b3],[r4,g4,b4],[r5,g5,b5],[r6,g6,b6],[r7,g7,b7],[r8,g8,b8],[r9,g9,b9]]
for i in new_list_rgb:
    with open("mean_list.txt", "a") as dosya:
        dosya.write(f"{int(i[0])}/")
        dosya.write(f"{int(i[1])}/")
        dosya.write(f"{int(i[2])}\n")
