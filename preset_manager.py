import os

class PresetManager:
	def __init__(self, work_dir = "./preset"):
		self._work_dir = work_dir
		self._preset = self.get_presets()[0]

	def get_presets(self):
		return list(
			map(
				lambda details: details[0].split("/")[-1],
				os.walk(self._work_dir)
			)
		)[1:]
	def set(self, preset):
		self._preset = preset
	def get(self, key):
		with open(f"{self._work_dir}/{self._preset}/{key}.txt") as f:
			return f.read().rstrip()
