from PIL import Image, ImageOps, ImageDraw, ImageFont
import numpy as np

min_rate = 0.9
max_rate = 1.1

img_path = "Pictures/00Fullimage.png"  # img taken from camera
textList = ["BBQ Souce","Chicken","Big Nugget","Sausage","MeatBall",
            "Cheese","Nugget","Ham. Patties","Meat","Mushroom"]
mean_list = []

# Open File and read all lines
with open('mean_list.txt', 'r') as file:
    lines = file.readlines()
    # all lines on loop
    for line in lines:
        values = line.strip().split('/')
        # if empty line skip
        if not values:
            continue
        try:
            # make values integer and create a list
            rgb_values = [int(value) for value in values]
            # add this list to mean_list
            mean_list.append(rgb_values)
        except ValueError:
            # If line is not acceptable skip
            continue

def get_all_rgb(piece):
    image_RGB = []
    # open img
    image = piece
    # take img sizes
    width, height = image.size
    # Loop al pixels
    for y in range(int(height)):
        for x in range(int(width)):
            # took pixels rgb values
            rgb_value = image.getpixel((x, y))
            R = rgb_value[0]
            G = rgb_value[1]
            B = rgb_value[2]
            if (R == 0) or (G == 0) or (B == 0):
                pass
            elif (R/G >= min_rate and R/G <= max_rate) and (R/B >= min_rate and R/B <= max_rate) and (B/G >= min_rate and B/G <= max_rate):
                pass
            # return rgb values
            else:
                image_RGB.append([R, G, B])
    return image_RGB

# open img file
image = Image.open(img_path)
# img's width-height
width, height = image.size
# Pieces width-height
piece_width = width // 5
piece_height = height // 2

pieces = []
pieces_with_text = []  # pieces' red bordered and subtitled version

printCount = 0
for i in range(10):
    printCount+=1
    x = (i % 5) * piece_width
    y = (i // 5) * piece_height
    piece = image.crop((x, y, x + piece_width, y + piece_height))
    current_data=get_all_rgb(piece)
    data_diff_list = []
    for data_ in current_data:
        data_diffRGB_list = []
        for j in range(10):
            data_diff_RGB = []
            data = mean_list[j]
            for k in range(3):
                data_diff = abs(data[k] - data_[k])
                data_diff_RGB.append(data_diff)
            data_diffRGB_list.append(data_diff_RGB)
        data_diff_list.append(data_diffRGB_list)

    R_val0, R_val1, R_val2, R_val3, R_val4, R_val5, R_val6, R_val7, R_val8, R_val9 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    G_val0, G_val1, G_val2, G_val3, G_val4, G_val5, G_val6, G_val7, G_val8, G_val9 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    B_val0, B_val1, B_val2, B_val3, B_val4, B_val5, B_val6, B_val7, B_val8, B_val9 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    for x in data_diff_list: #len 2k
        count = 0
        for y in x: #len 10
            if count == 0:
                R_val0 += y[0]
                G_val0 += y[1]
                B_val0 += y[2]
            if count == 1:
                R_val1 += y[0]
                G_val1 += y[1]
                B_val1 += y[2]
            if count == 2:
                R_val2 += y[0]
                G_val2 += y[1]
                B_val2 += y[2]
            if count == 3:
                R_val3 += y[0]
                G_val3 += y[1]
                B_val3 += y[2]
            if count == 4:
                R_val4 += y[0]
                G_val4 += y[1]
                B_val4 += y[2]
            if count == 5:
                R_val5 += y[0]
                G_val5 += y[1]
                B_val5 += y[2]
            if count == 6:
                R_val6 += y[0]
                G_val6 += y[1]
                B_val6 += y[2]
            if count == 7:
                R_val7 += y[0]
                G_val7 += y[1]
                B_val7 += y[2]
            if count == 8:
                R_val8 += y[0]
                G_val8 += y[1]
                B_val8 += y[2]
            if count == 9:
                R_val9 += y[0]
                G_val9 += y[1]
                B_val9 += y[2]
            count += 1

    q = len(data_diff_list)

    R0, R1, R2, R3, R4 = int(R_val0 / q), int(R_val1 / q), int(R_val2 / q), int(R_val3 / q), int(R_val4 / q)
    R5, R6, R7, R8, R9 = int(R_val5 / q), int(R_val6 / q), int(R_val7 / q), int(R_val8 / q), int(R_val9 / q)

    G0, G1, G2, G3, G4 = int(G_val0 / q), int(G_val1 / q), int(G_val2 / q), int(G_val3 / q), int(G_val4 / q)
    G5, G6, G7, G8, G9 = int(G_val5 / q), int(G_val6 / q), int(G_val7 / q), int(G_val8 / q), int(G_val9 / q)

    B0, B1, B2, B3, B4 = int(B_val0 / q), int(B_val1 / q), int(B_val2 / q), int(B_val3 / q), int(B_val4 / q)
    B5, B6, B7, B8, B9 = int(B_val5 / q), int(B_val6 / q), int(B_val7 / q), int(B_val8 / q), int(B_val9 / q)

    last_list = [R0+G0+B0,R1+G1+B1,R2+G2+B2,R3+G3+B3,R4+G4+B4,R5+G5+B5,R6+G6+B6,R7+G7+B7,R8+G8+B8,R9+G9+B9]

    print("___",printCount, "__:")
    #print([R0,G0,B0],[R1,G1,B1],[R2,G2,B2],[R3,G3,B3],[R4,G4,B4],[R5,G5,B5],[R6,G6,B6],[R7,G7,B7],[R8,G8,B8],[R9,G9,B9])
    print(last_list,"\n")
    min = 999
    index = 10
    for p in range(10):
        if min > last_list[p]:
            min = last_list[p]
            index = p

    text = textList[index]
    # text color green
    text_color = (0, 255, 0)
    # text font / font-size
    font = ImageFont.truetype("arial.ttf", 9)
    # copy red bordered pice
    piece_with_text = piece.copy()
    # create ImageDraw for drawing on picture
    draw = ImageDraw.Draw(piece_with_text)

    # Calculate the text coordinates
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (piece_with_text.width - text_width) // 2  # center text horizontal
    text_y = piece_with_text.height - text_height - 10  # text on bottom

    # draw text
    draw.text((text_x, text_y), text, font=font, fill=text_color)
    # Add red Border to img
    piece_with_text = ImageOps.expand(piece_with_text, border=1, fill='red')

    #add pieces to list
    pieces.append(piece)
    pieces_with_text.append(piece_with_text)

# spread up-down pieces
top_pieces = pieces[:5]
bottom_pieces = pieces[5:]
top_pieces_with_text = pieces_with_text[:5]
bottom_pieces_with_text = pieces_with_text[5:]

# connect top pieces
top_combined = np.concatenate(top_pieces, axis=1)
top_image = Image.fromarray(top_combined)
top_combined_with_text = np.concatenate(top_pieces_with_text, axis=1)
top_image_with_text = Image.fromarray(top_combined_with_text)

# connect bottom pieces
bottom_combined = np.concatenate(bottom_pieces, axis=1)
bottom_image = Image.fromarray(bottom_combined)
bottom_combined_with_text = np.concatenate(bottom_pieces_with_text, axis=1)
bottom_image_with_text = Image.fromarray(bottom_combined_with_text)

# connect top-bottom pieces
combined_image = np.concatenate([top_combined, bottom_combined], axis=0)
output_image = Image.fromarray(combined_image)

# red border and green text added pieces connected
combined_image_with_text = np.concatenate([top_combined_with_text, bottom_combined_with_text], axis=0)
output_image_with_text = Image.fromarray(combined_image_with_text)

# make output picture x3 larger
output_image_resized = output_image.resize((output_image.width * 3, output_image.height * 3))

# x3 larger output with red border and green text
output_image_with_text_resized = output_image_with_text.resize((output_image_with_text.width * 3, output_image_with_text.height * 3))
output_image_with_text_resized.show()

input("")
