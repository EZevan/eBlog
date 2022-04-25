# Reference PIL
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import string
import random


def random_color():
    """
    Generate random color
    """
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return color


def gen_captcha(char_size=16, char_num=4, point_num=50, line_num=5):
    """
    Generate random captcha
    """
    width, height = 100, 20
    char_pool = string.digits + string.ascii_letters

    # Instantiate an image object
    image = Image.new("RGB", (width, height), (255, 255, 255))

    # Instantiate a draw object with image above
    draw = ImageDraw.Draw(image)

    # Claim a font with specified font file and font size
    font = ImageFont.truetype(font="static/assets/font/JetBrainsMono.ttf", size=char_size)

    captcha = str()

    # Generate random captcha char iteratively
    for i in range(char_num):
        x = random.randint(i*(width/char_num)+char_size/2, (i+1)*(width/char_num)-char_size)
        y = random.randint(0, (height - char_size))
        char = random.choice(char_pool)
        captcha += char
        draw.text((x, y), char, fill=random_color(), font=font)

    # Generate random point within image
    for i in range(point_num):
        x, y = random.randint(0, width), random.randint(0, height)
        draw.point((x, y), fill=random_color())

    # Generate random line within image
    for i in range(line_num):
        x1, x2 = random.randint(0, width), random.randint(0, width)
        y1, y2 = random.randint(0, height), random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=random_color())

    # Create a byte memory handle
    fb = BytesIO()

    # Save the captcha picture into memory
    image.save(fb, "PNG")

    # Get the byte data of captcha picture
    data = fb.getvalue()

    return data, captcha


if __name__ == '__main__':
    gen_captcha()
