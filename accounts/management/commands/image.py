from PIL import Image, UnidentifiedImageError
from io import BytesIO
from django.core.files.base import ContentFile


def compress_image(image, max_size=(600, 600), quality=80):
    try:
        img = Image.open(image)
    except UnidentifiedImageError:
        return None  # ❗ НЕ изображение

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    img.thumbnail(max_size)

    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=quality, optimize=True)

    return ContentFile(buffer.getvalue())
