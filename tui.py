import editor
import uuid
from post_publisher import Post

class QuitNotice(Exception):
	pass
class RerunNotice(Exception):
	pass

class TUI:
	def __init__(self, 
		prefix, 
		txt_storage, 
		txt_gen, 
		img_gen, 
		img_editor, 
		preset_manager,
		post_publisher
	):
		self._prefix = prefix
		self._txt_storage = txt_storage
		self._txt_gen = txt_gen
		self._img_gen = img_gen
		self._img_editor = img_editor
		self._preset_manager = preset_manager
		self._post_publisher = post_publisher

	def start(self):
		while True:
			try:
				print("Type '0' to choose a preset.")
				print("Type '1' to edit texts.")
				print("Type '2' to generate posts.")
				print("Type 'q' to exit.")
				choice = self._get_choice(2)
				if choice == 0:
					preset = self._choose_preset()
					self._preset_manager.set(preset)
				elif choice == 1:
					self._edit_texts()
				elif choice == 2:
					try:
						text = self._choose_text()
						tags = self._choose_tags(text)
						image = self._choose_image(text)
						final = self._edit_image(image, text)						
						post = Post(
							image = final, 
							caption = text, 
							tags = tags
						)
						self._post_publisher.publish(post)
					except QuitNotice:
						print("Returning to main menu.")
				else:
					print("Unknown command!")
			except KeyboardInterrupt:
				break
			except QuitNotice:
				break
			except RerunNotice:
				pass
		print("Goodbye!")
	def _print_instructions(self):
		print("Type your choice to save a text.")
		print("Type 'r' to rerun generation.")
		print("Type 'q' to return to the last screen.")
	def _print_texts(self, texts):
		print()
		print("-" * 20)
		for i, text in enumerate(texts):
			print(f"{i+1}: {text}")
		print("-" * 20)
		print()
	def _get_choice(self, length):
		while True:
			try:
				inp = input(f"{self._prefix} ")
				if inp[0] == "q":
					raise QuitNotice
				elif inp[0] == "r":
					raise RerunNotice
				elif int(inp) <= length:
					return int(inp)
				else:
					print("Out of range choice!")
			except QuitNotice:
				raise QuitNotice
			except RerunNotice:
				raise RerunNotice
			except:
				print("Unknown error!")

	def _edit_image(self, image, text):
		cropped = self._img_editor.crop_center(image)
		blurred = self._img_editor.blur(cropped)
		faded = self._img_editor.fade(blurred)
		written = self._img_editor.write_text(faded, text)
		branded = self._img_editor.write_brand(written)
		return branded
	def _choose_image(self, text):
		run_gen = True
		while run_gen:
			print("Generating images...")
			images = self._img_gen.generate(text)
			for i, image in enumerate(images):
				image.show()
				input(f"Showing image {i+1}... (Press ENTER to continue)")
			print("Type your choice to use an image.")
			print("Type 'r' to rerun generation.")
			print("Type 'q' to return to the last screen.")
			while True:
				try:
					return images[self._get_choice(len(images)) - 1]
				except QuitNotice:
					run_gen = False
					break
				except RerunNotice:
					break
		raise QuitNotice

	def _edit_texts(self):
		run_gen = True
		while run_gen:
			topic = input("Make the prompt more specific (if the preset allows): ")
			print("Generating texts...")
			texts = self._txt_gen.generate(
				self._preset_manager.get("instruction").replace(
					"{topic}", 
					topic
				)
			)
			while True:
				self._print_texts(texts)
				self._print_instructions()
				try:	
					text = texts[self._get_choice(len(texts)) - 1]
					texts.remove(text)
					self._txt_storage.save(text)
					print("Text saved!")
				except QuitNotice:
					run_gen = False
					break
				except RerunNotice:
					break
	def _choose_preset(self):
		presets = self._preset_manager.get_presets()
		self._print_texts(presets)
		print("Choose the your new preset.")
		while True:
			try:
				return presets[self._get_choice(len(presets)) - 1]
			except QuitNotice:
				raise QuitNotice
			except RerunNotice:
				continue
	def _choose_text(self):
		texts = self._txt_storage.get()
		texts.reverse()
		self._print_texts(texts)
		print(f"{len(texts) + 1}: [use custom text]")
		print("Choose the used text.")
		while True:
			try:
				choice = self._get_choice(len(texts) + 1)
				if choice < len(texts):
					text = texts[choice - 1]
					self._txt_storage.delete(text)
				else:
					text = ""
				return editor.edit(contents=text.encode("UTF-8")).decode("UTF-8")
			except QuitNotice:
				raise QuitNotice
			except RerunNotice:
				continue
	def _choose_tags(self, text):
		run_gen = True
		while run_gen:
			print("Generating tags...")
			batches = list(
				map(
					lambda batch: batch.split(" "), 
					self._txt_gen.generate(
						self._preset_manager.get("instruction_tags").replace(
							"{text}", text
						)
					)
				)
			)
			self._print_texts(batches)
			print("Type your choice to use a tag batch.")
			print("Type 'r' to rerun generation.")
			print("Type 'q' to return to the last screen.")
			while True:
				try:
					return batches[self._get_choice(len(batches)) - 1]
				except QuitNotice:
					run_gen = False
					break
				except RerunNotice:
					break
		raise QuitNotice
