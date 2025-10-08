from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

width, height = 900, 1600
# background_color = "white"
background_color = (235, 242, 255)
title_color = (20, 10, 10)
subtitle_color = "grey"
body_color = (15, 10, 10)
header_color = (0, 0, 0)

font_title = ImageFont.truetype(f"{base_dir}/fonts/Montserrat-Bold.ttf", 70)
font_subtitle = ImageFont.truetype(f"{base_dir}/fonts/OpenSans-SemiBold.ttf", 35)
font_body = ImageFont.truetype(f"{base_dir}/fonts/OpenSans-SemiBold.ttf", 30)
font_header = ImageFont.truetype(f"{base_dir}/fonts/OpenSans-SemiBold.ttf", 30)


def write_line_element(element_text, x_box, y_line, draw):
    element_width = draw.textlength(element_text, font=font_body)
    x_element = x_box + (160 - element_width) / 2
    draw.text((x_element, y_line), element_text, fill=body_color, font=font_body)


def choose_weather(precipitation, cloud, hour, sunrise, sunset):
    if precipitation == 0:
        if cloud < 33:
            if sunrise < hour < sunset:
                weather = "sun"
            else:
                weather = "moon"
        elif cloud < 67:
            if sunrise < hour < sunset:
                weather = "cloudy_sun"
            else:
                weather = "cloudy_moon"
        else:
            weather = "cloudy"
    elif precipitation < 4:
        weather = "light_rain"
    else:
        weather = "heavy_rain"
    return weather


def assemble_image(hourly_df, daily_df, city_name):
    # Create blank white image
    img = Image.new("RGB", (width, height), color=background_color)

    # Draw text
    draw = ImageDraw.Draw(img)

    # Measure text size to centre it
    bbox_title = draw.textbbox((0, 0), city_name, font=font_title)
    x_title = (width - (bbox_title[2] - bbox_title[0])) / 2
    y_title = 70  # top margin
    draw.text((x_title, y_title), city_name, fill=title_color, font=font_title)

    # Current date (formatted like "Tuesday 7 October")
    today = datetime.now().strftime("%A %d %B")
    bbox_subtitle = draw.textbbox((0, 0), today, font=font_subtitle)
    x_subtitle = (width - (bbox_subtitle[2] - bbox_subtitle[0])) / 2
    y_subtitle = y_title + bbox_title[3] - bbox_title[1] + 30  # 30px spacing below title
    draw.text((x_subtitle, y_subtitle), today, fill=subtitle_color, font=font_subtitle)

    draw.text((95, 220), "Hour", fill=header_color, font=font_header)
    draw.text((233, 220), "Weather", fill=header_color, font=font_header)
    draw.text((412, 220), "Temperature", fill=header_color, font=font_header)
    draw.text((625, 220), "Rain probability", fill=header_color, font=font_header)

    sunrise_ts = daily_df["sunrise"][0]
    sunset_ts = daily_df["sunset"][0]

    sunrise = datetime.fromtimestamp(sunrise_ts).hour + datetime.fromtimestamp(sunrise_ts).minute / 60
    sunset = datetime.fromtimestamp(sunset_ts).hour + datetime.fromtimestamp(sunset_ts).minute / 60

    for i, row in hourly_df.iterrows():
        temperature = row["temperature_2m"]
        precipitation = row["precipitation"]
        cloud = row["cloud_cover"]
        pp = row["precipitation_probability"]
        hour = int(row["date"].hour)

        y_line = 290 + i * 74

        hour_text = str(hour)
        write_line_element(hour_text, 50, y_line, draw)

        weather = choose_weather(precipitation, cloud, hour, sunrise, sunset)
        icon_path = f"{base_dir}/icons/{weather}.png"
        icon = Image.open(icon_path).convert("RGBA")
        icon_size = 60
        icon.thumbnail((icon_size, icon_size))
        x_icon = 208 + (160 - icon_size) // 2
        img.paste(icon, (x_icon, y_line - 11), icon)

        temperature_text = f"{round(temperature)}°C"
        write_line_element(temperature_text, 428, y_line, draw)

        pp_text = f"{round(pp)}%"
        write_line_element(pp_text, 650, y_line, draw)

    # Save
    img.save(f"images/{city_name}.jpg")
