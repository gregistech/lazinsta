import uuid
from PIL import Image
from dataclasses import dataclass

@dataclass
class Post:
	image: Image
	caption: str
	tags: list[str]

class PostPublisher:	
	def __init__(self, work_dir = "./posts"):
		self._work_dir = work_dir
	def publish(self, post):
		print(post.caption)
		for tag in post.tags:
			print(f"#{tag} ", end="")
		print()
		post.image.save(f"{self._work_dir}/{uuid.uuid4()}.jpg")
