class ConfigManager:
	def __init__(self, work_dir = "./conf"):
		self.work_dir = work_dir
	def get_conf(self, key):
		with open(f"{self.work_dir}/{key}.txt", "r") as f:
			return f.read().rstrip()
