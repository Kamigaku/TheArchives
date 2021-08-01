import urllib.request
import random
import os
from PIL import Image, ImageFont, ImageDraw, ImageColor

# front_card_template = ["..\\..\\ressources\\front_1.png", "..\\..\\ressources\\front_2.png",
#                        "..\\..\\ressources\\front_3.png", "..\\..\\ressources\\front_4.png",
#                        "..\\..\\ressources\\front_5.png", "..\\..\\ressources\\front_6.png",
#                        "..\\..\\ressources\\front_7.png", "..\\..\\ressources\\front_8.png",
#                        "..\\..\\ressources\\front_9.png", "..\\..\\ressources\\front_10.png",
#                        "..\\..\\ressources\\front_11.png", "..\\..\\ressources\\front_12.png"]
#
# back_card_template = ["..\\..\\ressources\\back_1.png", "..\\..\\ressources\\back_2.png",
#                       "..\\..\\ressources\\back_3.png", "..\\..\\ressources\\back_4.png",
#                       "..\\..\\ressources\\back_5.png", "..\\..\\ressources\\back_6.png",
#                       "..\\..\\ressources\\back_7.png", "..\\..\\ressources\\back_8.png",
#                       "..\\..\\ressources\\back_9.png", "..\\..\\ressources\\back_10.png",
#                       "..\\..\\ressources\\back_11.png", "..\\..\\ressources\\back_12.png"]

rarities_label = ["E", "D", "C", "B", "A", "S", "SS"]


front_card_template = ["ressources" + os.sep + "front_1.png", "ressources" + os.sep + "front_2.png",
                       "ressources" + os.sep + "front_3.png", "ressources" + os.sep + "front_4.png",
                       "ressources" + os.sep + "front_5.png", "ressources" + os.sep + "front_6.png",
                       "ressources" + os.sep + "front_7.png", "ressources" + os.sep + "front_8.png",
                       "ressources" + os.sep + "front_9.png", "ressources" + os.sep + "front_10.png",
                       "ressources" + os.sep + "front_11.png", "ressources" + os.sep + "front_12.png"]

back_card_template = ["ressources" + os.sep + "back_1.png", "ressources" + os.sep + "back_2.png",
                      "ressources" + os.sep + "back_3.png", "ressources" + os.sep + "back_4.png",
                      "ressources" + os.sep + "back_5.png", "ressources" + os.sep + "back_6.png",
                      "ressources" + os.sep + "back_7.png", "ressources" + os.sep + "back_8.png",
                      "ressources" + os.sep + "back_9.png", "ressources" + os.sep + "back_10.png",
                      "ressources" + os.sep + "back_11.png", "ressources" + os.sep + "back_12.png"]

data_title = dict(size_x=400, size_y=30, x=224, y=361)
data_picture = dict(size_x=448, size_y=303, x=0, y=0)
data_description = dict(size_x=390, size_y=140, x=34, y=404)
data_affiliation = dict(size_x=100, size_y=25, x=224, y=616)
data_footer = dict(size_x=440, size_y=20, x=30, y=650)
data_rarity = dict(size_x=30, size_y=30, x=42, y=590)


def wrap_text(text, width, font):
    text_lines = []
    text_line = []
    text = text.replace('\n', ' [br] ')
    words = text.split()
    font_size = font.getsize(text)

    for word in words:
        if word == '[br]':
            text_lines.append(' '.join(text_line))
            text_line = []
            continue
        text_line.append(word)
        w, h = font.getsize(' '.join(text_line))
        if w > width:
            text_line.pop()
            text_lines.append(' '.join(text_line))
            text_line = [word]

    if len(text_line) > 0:
        text_lines.append(' '.join(text_line))

    return text_lines


def resize_font_size(font: ImageFont, max_width: int, max_height, text: str,
                     img_draw: ImageDraw, default_font_size: int, should_wrap: bool = False):
    name_w, name_h = img_draw.textsize(text, font=font)
    initial_text = text
    while name_w > max_width:
        default_font_size -= 1
        font = ImageFont.truetype("ressources" + os.sep + "fonts" + os.sep + "tahoma.ttf", default_font_size)
        if should_wrap:
            text = wrap_text(initial_text, max_width, font)
            text = "\n".join(text)
        name_w, name_h = img_draw.textsize(text, font=font)
    while name_h > max_height:
        default_font_size -= 1
        font = ImageFont.truetype("ressources" + os.sep + "fonts" + os.sep + "tahoma.ttf", default_font_size)
        if should_wrap:
            text = wrap_text(initial_text, max_width, font)
            text = "\n".join(text)
        name_w, name_h = img_draw.textsize(text, font=font)
    return font, name_w, name_h


def create_card(seed, title: str, image_url: str, description: str, rarity: int, affiliation=None):
    random.seed(seed)

    card_index = random.randrange(0, len(front_card_template))
    img_front = Image.open(front_card_template[card_index])
    img_back = Image.open(back_card_template[card_index])
    img_draw = ImageDraw.Draw(img_front)

    # Fonts
    size_title_font = 35
    tahoma_fonts = ImageFont.truetype("ressources" + os.sep + "fonts" + os.sep + "tahoma.ttf", size_title_font)

    # Title
    title_font = ImageFont.truetype("ressources" + os.sep + "fonts" + os.sep + "tahoma.ttf", 35)
    title_font, font_width, font_height = resize_font_size(title_font, data_title["size_x"],
                                                           data_title["size_y"], title, img_draw, 35)
    img_draw.text((data_title["x"] - (font_width / 2), data_title["y"] - (font_height / 2)), title, font=title_font)

    # Affiliation
    affiliation_font = ImageFont.truetype("ressources" + os.sep + "fonts" + os.sep + "tahoma.ttf", 12)
    affiliation_font, font_width, font_height = resize_font_size(affiliation_font, data_affiliation["size_x"],
                                                                 data_affiliation["size_y"], affiliation, img_draw, 35)
    img_draw.text((data_affiliation["x"] - (font_width / 2), data_affiliation["y"] - (font_height / 2)),
                  affiliation, font=affiliation_font)

    # Description
    description_font = ImageFont.truetype("ressources" + os.sep + "fonts" + os.sep + "tahoma.ttf", 20)
    description_font, font_width, font_height = resize_font_size(description_font, data_description["size_x"],
                                                                 data_description["size_y"], description, img_draw,
                                                                 14, True)
    wrapped_text = wrap_text(description, data_description["size_x"], description_font)
    wrapped_text = "\n".join(wrapped_text)
    img_draw.multiline_text((data_description["x"], data_description["y"]),
                            wrapped_text, font=description_font)

    # Rarity
    rarity_font = ImageFont.truetype("ressources" + os.sep + "fonts" + os.sep + "tahoma.ttf", 24)
    rarity_font, font_width, font_height = resize_font_size(rarity_font, data_rarity["size_x"],
                                                            data_rarity["size_y"], rarities_label[rarity], img_draw, 24)
    img_draw.text((data_rarity["x"] - (font_width / 2), data_rarity["y"] - (font_height / 2)), rarities_label[rarity],
                  font=rarity_font)

    # Picture
    urllib.request.urlretrieve(image_url, "temp.png")
    img_character = Image.open("temp.png")

    ratio_img = data_picture["size_x"] / data_picture["size_y"]
    ratio_picture = img_character.width / img_character.height
    if ratio_picture < ratio_img:
        img_character = img_character.resize((data_picture["size_x"],
                                              int(data_picture["size_x"] * img_character.height / img_character.width)))
    else:
        img_character = img_character.resize((int(data_picture["size_y"] * img_character.width / img_character.height),
                                              data_picture["size_y"]))

    img_mask = Image.new("L", img_character.size, 0)
    draw = ImageDraw.Draw(img_mask)
    draw.rectangle((data_picture["x"], data_picture["y"],
                   data_picture["size_x"] + data_picture["x"], data_picture["size_y"] + data_picture["y"]),
                   fill=255)

    img_front.paste(img_character, (data_picture["x"], data_picture["y"]), img_mask)
    os.remove("temp.png")
    return img_front, img_back


def gather_pictures_in_one(pictures, offset_x: int, offset_y: int, space_x: int, space_y: int):
    total_height = 0
    total_width = 0
    for picture in pictures:
        total_width += picture.width + space_x
        if picture.height > total_height:
            total_height = picture.height
    total_height + space_y
    global_picture = Image.new("RGBA", (total_width + offset_x, total_height + offset_y), ImageColor.getrgb("#000000"))

    current_offset_x = int(offset_x / 2)
    current_offset_y = int(offset_y / 2)

    for picture in pictures:
        global_picture.paste(picture, (current_offset_x, current_offset_y))
        current_offset_x += picture.width + space_x
    return global_picture


if __name__ == "__main__":
    img_front, img_back = create_card(105, "Elsa", "https://static.wikia.nocookie.net/villains/images/9/97/Xenomorphs.jpg/revision/latest/scale-to-width-down/1000?cb=20181223215802",
                "'Elsa the Snow Queen' is the deuteragonist of Walt Disney Animation Studios's 2013 "
                "animated feature film Frozen and the protagonist of its 2019 Frozen II. Born with the power of ice "
                "and snow, Elsa is the firstborn daughter of King Agnarr and Queen Iduna, the older sister of Anna, "
                "and the former queen of Arendelle. Throughout most of her young life, Elsa feared that her powers were"
                "monstrous. Therefore, she isolated herself from the world as a means of protecting her family and "
                "kingdom. Elsa's anxieties would eventually trigger a curse that plunged Arendelle into an eternal "
                "winter. Through Anna's love, however, Elsa was able to control her powers and live peacefully amongst "
                "her people with a newfound self-confidence.", 1, "Disney Princess\nMonster")
    img_front.save("front.png")
    img_back.save("back.png")
