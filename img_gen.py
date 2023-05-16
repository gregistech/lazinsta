import openai
from PIL import Image
from urllib.request import urlopen

class ImageGenerator:
	def __init__(self, organization, api_key):
		openai.organization = organization 
		openai.api_key = api_key 
	def generate(self, text):
		return list(map(lambda data: Image.open(urlopen(data.url)), openai.Image.create(prompt=text, n=4).data))
