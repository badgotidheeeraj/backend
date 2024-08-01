from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

result = upload("path_to_your_test_image.jpg")
url, options = cloudinary_url(result['public_id'])
print(url)
