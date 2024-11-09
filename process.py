import os
from PIL import Image, ImageDraw 
import numpy as np

A4 = (1600, 1130)
per_page = 4
align_w = 300

def load_alfabet(folder, new_width):
    images = {}
    for fname in os.listdir(folder):
        char = os.path.splitext(fname)[0]
        ffnm = os.path.join(folder, fname)
        im = Image.open(ffnm)    
        new_height = new_width * im.height // im.width
        im = im.resize((new_width, new_height), Image.LANCZOS)
        images[char.lower()] = im
    return images

def get_concat_v(imgs):
    a = np.full((A4[0], A4[1], 3), 255, dtype=np.uint8)
    dst = Image.fromarray(a, 'RGB')
    for i in range(len(imgs)):
        word_len = len(imgs[i][0])
        chars_image = np.full((A4[0]//per_page - 1, A4[1], 3), 255, dtype=np.uint8)
        horiz_img = Image.fromarray(chars_image, 'RGB')
        horiz_img.paste(imgs[i][1], (50, 0))
        start = A4[0] // per_page
        width = (A4[1]-430)//word_len
        alfabet = load_alfabet("litere", width - 20)
        height = align_w//2
        img_draw = ImageDraw.Draw(horiz_img)
        for j in range(word_len):            
            shape = [(start + j * width, 10), (start + j*width + width - 20, height)]
            img_draw.rectangle(shape, fill="#FFFFFF", outline='black')
        for j in range(word_len):
            horiz_img.paste(alfabet[imgs[i][0][j]], (start + j*width, 20 + height))
        dst.paste(horiz_img, (0, (A4[0]//per_page)*i))
    return dst

def resize_images(path):
    img_resized = []
    images = os.listdir(path)
    names = [(os.path.splitext(fname)[0], fname) for fname in images]
    for img in names:
        ffnm = os.path.join(path, img[1])
        im = Image.open(ffnm)    
        new_width = align_w
        new_height = new_width * im.height // im.width
        im = im.resize((new_width, new_height), Image.LANCZOS)
        img_resized += [(img[0], im)]
    return img_resized

def main():
    img_resized = resize_images("poze")
    k = 1
    for i in range(len(img_resized) // per_page):
        filtered_names = [img_resized[i*per_page+j][0].replace('\u0103', 'a').replace('\u0219', 's').replace('\u021b', 't').replace('\u00e2', 'a') for j in range(per_page)]
        print(f"Construiesc foaia de lucru: {k:03}.png din [{",".join(filtered_names)}]")
        imgs = [(img_resized[i*per_page+j][0], img_resized[i*per_page+j][1]) for j in range(per_page)]
        page = get_concat_v(imgs)
        page.save(f"{k:03}.png")
        k += 1

if __name__ == "__main__":
    main()
   