from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
import textwrap

FONT_PATH = "barlow.ttf"
BLUR_RADIUS = 10
BRIGHTNESS = .25
ASPECT_RATIO = (1, 1)
def crop_center(image, aspect_ratio):
	width, height = image.size
	new_aspect_ratio = float(aspect_ratio[0]) / aspect_ratio[1]
	if float(width) / height > new_aspect_ratio:
		new_size = (int(height * new_aspect_ratio), height)
		left = (width - new_size[0]) / 2
		top = 0
	else:
		new_size = (width, int(width / new_aspect_ratio))
		left = 0
		top = (height - new_size[1]) / 2
	right = left + new_size[0]
	bottom = top + new_size[1]
	return image.crop((int(left), int(top), int(right), int(bottom)))
def write_brand(image):
	draw = ImageDraw.Draw(image)
	font = ImageFont.truetype(FONT_PATH, 64)

	bbox = (image.width / 2, image.height * .875)
	text = "IskolaHACK"

	draw.text(bbox, text, anchor="mm", font=font, fill=(217, 112, 74))
	return image
def write_text(image, text):
	draw = ImageDraw.Draw(image)
	font = ImageFont.truetype(FONT_PATH, 72)

	bbox = (image.width / 2, image.height / 2)	
	text = "\n".join(textwrap.wrap(text, 30))

	draw.text(bbox, text, anchor="mm", font=font, fill=(255, 255, 255))
	return image
def edit_image(image, text):
	cropped = crop_center(image, ASPECT_RATIO)
	blurred = cropped.filter(ImageFilter.GaussianBlur(radius=BLUR_RADIUS))
	faded = ImageEnhance.Brightness(blurred).enhance(BRIGHTNESS)
	written = write_text(faded, text)
	branded = write_brand(written)
	return branded


def get_conf(key):
	with open(f"{key}.txt", "r") as f:
		return f.read().rstrip()
import openai
openai.organization = get_conf("organization") 
openai.api_key = get_conf("api_key")
SYSTEM = get_conf("system")
USER = get_conf("user")
def generate_texts():
	return list(map(lambda choice: choice.message.content, openai.ChatCompletion.create(
			model="gpt-3.5-turbo",
			messages=[
				{ "role": "system", "content": SYSTEM },
				{ "role": "user", "content": USER }
			],
			n=4
		).choices)
	)
from urllib.request import urlopen
def generate_images(text):
	return list(map(lambda data: Image.open(urlopen(data.url)), openai.Image.create(prompt=text, n=4).data))

def print_instructions():
	print("Type your choice to save a text.")
	print("Type 'r' to rerun generation.")
	print("Type 'q' to return to the last screen.")
def print_texts(texts):
	print()
	print("-" * 20)
	for i, text in enumerate(texts):
		print(f"{i+1}: {text}")
	print("-" * 20)
	print()
class QuitNotice(Exception):
	pass
class RerunNotice(Exception):
	pass
def get_choice():
	while True:
		inp = input(f"{PREFIX} ")
		if inp == "q":
			raise QuitNotice
		elif inp == "r":
			raise RerunNotice
		try:
			choice = int(inp) - 1
			if choice < 0:
				raise IndexError("Negative indexes would roll over.")
			return choice
		except IndexError:
			print("Out of range choice!")
		except ValueError:
			print("Invalid choice!")

def save_text(text):
	with open("texts.txt", "a") as f:
		f.write(f"{text}\n")
def delete_text(text):
	with open("texts.txt", "r") as f:
		lines = f.readlines()
	lines.remove(text)
	with open("texts.txt", "w") as f:
		f.write("\n".join(lines))
def get_texts():
	with open("texts.txt", "r") as f:
		return f.readlines()

import uuid
def create_post(image):
	image.save(f"{uuid.uuid4()}.jpg")
	image.show()

def edit_texts():
	run_gen = True
	while run_gen:
		print("Generating texts...")
		texts = generate_texts()
		while True:
			print_texts(texts)
			print_instructions()
			try:	
				text = texts[get_choice()]
				texts.remove(text)
				save_text(text)
				print("Text saved!")
			except QuitNotice:
				run_gen = False
				break
			except RerunNotice:
				break
def choose_text():
	texts = get_texts()
	texts.reverse()
	print_texts(texts)
	print("Choose the used text.")
	while True:
		try:
			text = texts[get_choice()]
			delete_text(text)
			return text
		except QuitNotice:
			raise QuitNotice
		except RerunNotice:
			continue

def choose_image(text):
	run_gen = True
	while run_gen:
		print("Generating images...")
		images = generate_images(text)
		for i, image in enumerate(images):
			image.show()
			input(f"Showing image {i+1}... (Press ENTER to continue)")
		print("Type your choice to use an image.")
		print("Type 'r' to rerun generation.")
		print("Type 'q' to return to the last screen.")
		while True:
			try:
				return images[get_choice()]
			except QuitNotice:
				run_gen = False
				break
			except RerunNotice:
				break
	raise QuitNotice
	

PREFIX = "(lazinsta)"

while True:
	print("Type '0' to edit texts.")
	print("Type '1' to generate posts.")
	print("Type 'q' to exit.")
	inp = input(f"{PREFIX} ")
	if inp == "0":
		edit_texts()
	elif inp == "1":
		try:
			text = choose_text()
			image = choose_image(text)
			final = edit_image(image, text)
			create_post(final)
		except QuitNotice:
			break
	elif inp == "q":
		break
	else:
		print("Unknown command!")
print("Goodbye!")
