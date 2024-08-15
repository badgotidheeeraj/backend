import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name='dy4gxhzyt',
    api_key='142481373268446',
    api_secret='052lDSUE74zyGCvLrHR44x1St9s',
)

response = cloudinary.uploader.upload('/home/me/Downloads/Blogger/backend/digital_market_images/Screenshot_from_2024-06-13_18-00-54.png')
print(response)
