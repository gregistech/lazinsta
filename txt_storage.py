class TextStorage:
	def __init__(self, work_dir = "./"):
		self.work_dir = work_dir

	def save(self, text):
		with open(f"{self.work_dir}/texts.txt", "a") as f:
			f.write(f"{text}\n")
	def delete(self, text):
		with open(f"{self.work_dir}/texts.txt", "r") as f:
			lines = f.readlines()
		lines.remove(text)
		with open(f"{self.work_dir}/texts.txt", "w") as f:
			f.write("".join(lines))
	def get(self):
		with open(f"{self.work_dir}/texts.txt", "r") as f:
			return f.readlines()
