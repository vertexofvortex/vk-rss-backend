from io import BytesIO
from typing import Union
from PIL import Image, ImageFont, ImageDraw, ImageColor
from .textwrapper import TextWrapper
from os.path import dirname, join


def generate_image(
    title: str,
    description: str,
    source: str,
    image_bytes: Union[BytesIO, None],
    logo_bytes: BytesIO,
) -> BytesIO:
    CANVAS_WIDTH = 1500
    CANVAS_HEIGHT = 1500
    SOURCE_SIZE = 33
    TITLE_SIZE = 68
    DESCRIPTION_SIZE = 45

    canvas = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT))

    if image_bytes:
        image = Image.open(image_bytes)
    else:
        image = Image.open(join(dirname(__file__), "default_bg.jpg"))

    image_aspect_ratio = image.width / image.height
    image_resized = image.resize(
        (CANVAS_WIDTH, int(CANVAS_WIDTH / image_aspect_ratio)),
    )

    logo = Image.open(logo_bytes)
    logo_aspect_ratio = logo.width / logo.height
    logo_resized = logo.resize((50, int(50 / logo_aspect_ratio)))

    logo_constant = Image.open(join(dirname(__file__), "logo.png"))

    font_source = ImageFont.truetype(
        join(dirname(__file__), "fonts", "GraphikLCG-Medium.ttf"), size=SOURCE_SIZE
    )

    font_title = ImageFont.truetype(
        join(dirname(__file__), "fonts", "GraphikLCG-Bold.ttf"), size=TITLE_SIZE
    )

    font_description = ImageFont.truetype(
        join(dirname(__file__), "fonts", "Lora-Regular.ttf"), size=DESCRIPTION_SIZE
    )

    title_wrapper = TextWrapper(title, font_title, CANVAS_WIDTH - 100)
    description_wrapper = TextWrapper(description, font_description, CANVAS_WIDTH - 100)

    wrapped_title = title_wrapper.wrapped_text()["text"]
    wrapped_title_len = title_wrapper.wrapped_text()["length"]
    wrapped_description = description_wrapper.wrapped_text()["text"]

    draw = ImageDraw.Draw(canvas)

    canvas.paste(image_resized, (0, 0))

    draw.rounded_rectangle(
        (0, canvas.height / 2, canvas.width, canvas.height + 50),
        radius=50,
        fill="white",
    )

    canvas.paste(logo_resized, (50, int(canvas.height / 2 + 50)))

    draw.text(
        (
            50 + logo_resized.width + 20,
            int((CANVAS_HEIGHT / 2 + 50) + logo_resized.height / 2 - SOURCE_SIZE / 2),
        ),
        text=source.upper(),
        font=font_source,
        fill=ImageColor.getrgb("#3134fd"),
    )

    draw.text(
        (50, int(canvas.height / 2 + 50 + logo_resized.height + 50)),
        text=wrapped_title,
        font=font_title,
        fill="black",
    )

    draw.text(
        (
            50,
            int(
                canvas.height / 2
                + 50
                + logo_resized.height
                + 50
                + wrapped_title_len * TITLE_SIZE
                + 50
            ),
        ),
        text=wrapped_description,
        font=font_description,
        fill="black",
    )

    canvas.paste(
        logo_constant, (canvas.width - logo_constant.width, 0), mask=logo_constant
    )

    # FIXME: debug
    # canvas.save("test.png", format="png")
    canvas_bytearray = BytesIO()
    canvas.save(canvas_bytearray, format="png")

    return canvas_bytearray
