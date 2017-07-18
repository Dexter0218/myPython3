from PIL import Image
import pytesseract
im =Image.open('captcha.jpg')
text = pytesseract.image_to_string(im,lang = 'chi_sim')
print(text)