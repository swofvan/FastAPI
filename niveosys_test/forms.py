ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png"]

MAX_IMAGE_SIZE = 2 * 1024 * 1024

 
async def check_image(file):

    extension = file.filename.split(".")[-1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        return False
    
    image_data = await file.read()

    if len(image_data) > MAX_IMAGE_SIZE:
        return False
    
    file.file.seek(0)

    return True

