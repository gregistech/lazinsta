from img_editor import ImageEditor 
from img_gen import ImageGenerator 

def edit_image(img_editor, image, text):
	cropped = img_editor.crop_center(image)
	blurred = img_editor.blur(cropped)
	faded = img_editor.fade(blurred)
	written = img_editor.write_text(faded, text)
	branded = img_editor.write_brand(written)
	return branded
def choose_image(text):
	run_gen = True
	while run_gen:
		print("Generating images...")
		images = img_gen.generate(text)
		for i, image in enumerate(images):
			image.show()
			input(f"Showing image {i+1}... (Press ENTER to continue)")
		print("Type your choice to use an image.")
		print("Type 'r' to rerun generation.")
		print("Type 'q' to return to the last screen.")
		while True:
			try:
				return images[get_choice(len(images))]
			except QuitNotice:
				run_gen = False
				break
			except RerunNotice:
				break
	raise QuitNotice


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

USER_HASHTAG = get_conf("user_hashtag")
def generate_hashtags(text):
	return list(map(lambda choice: choice.message.content, openai.ChatCompletion.create(
			model="gpt-3.5-turbo",
			messages=[
				{ "role": "system", "content": SYSTEM },
				{ "role": "user", "content": USER_HASHTAG.replace("{text}", text) }
			],
			n=4
		).choices)
	)


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
def get_choice(length):
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
			elif choice >= length:
				raise IndexError("Out of range choice!")
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
				text = texts[get_choice(len(texts))]
				texts.remove(text)
				save_text(text)
				print("Text saved!")
			except QuitNotice:
				run_gen = False
				break
			except RerunNotice:
				break
import editor
def choose_text():
	texts = get_texts()
	texts.reverse()
	print_texts(texts)
	print("Choose the used text.")
	while True:
		try:
			text = texts[get_choice(len(texts))]
			delete_text(text)
			text = editor.edit(contents=text.encode("UTF-8")).decode("UTF-8")
			return text
		except QuitNotice:
			raise QuitNotice
		except RerunNotice:
			continue

def choose_hashtags(text):
	run_gen = True
	while run_gen:
		print("Generating hashtags...")
		hashtags = generate_hashtags(text)
		print_texts(hashtags)
		print("Type your choice to use a hashtag batch.")
		print("Type 'r' to rerun generation.")
		print("Type 'q' to return to the last screen.")
		while True:
			try:
				return hashtags[get_choice(len(hashtags))]
			except QuitNotice:
				run_gen = False
				break
			except RerunNotice:
				break
	raise QuitNotice


img_gen = ImageGenerator(get_conf("organization"), get_conf("api_key"))

FONT_PATH = "barlow.ttf"
BRANDING = "IskolaHACK"
img_editor = ImageEditor(FONT_PATH, BRANDING)

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
			hashtags = choose_hashtags(text)
			image = choose_image(text)
			final = edit_image(img_editor, image, text)
			print(f"Your hashtags: {hashtags}")
			create_post(final)
		except QuitNotice:
			break
	elif inp == "q":
		break
	else:
		print("Unknown command!")
print("Goodbye!")
