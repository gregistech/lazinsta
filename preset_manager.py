class PresetManager:
	def get(self, key):
		if key == "identity":
			return """You are a professional hungarian copywriter who specialises in Instagram posts. You know exactly how to capture the attention of hungarian students."""
		elif key == "instruction":
			return """Write a short hungarian sentence (to be used on an Instagram photo) that will appeal to hungarian teenagers (such as high school and university students) about the hungarian education system, at max one sentence. The goal is the get people to follow my account, and keep engagement rates high. Can be a criticism, or a way to improve the system. Don't get bogged down on creativity and individual freedoms. Some examples for formatting:

\"Az oktatásunkban az érettségi egyet jelent a kreativitás és az egyéni gondolkodás megfojtásával.\"
\"Az oktatásban vannak hiányosságok, de az én személyes fejlődésemnek nem állhatnak útjában.\"
\"Kritikusnak lenni az oktatással kapcsolatban nem jelenti azt, hogy nem tiszteljük azokat az embereket, akik értünk dolgoznak minden nap.\"
		"""
		elif key == "instruction_hashtag":
			return """Write 30 hashtags to be used under an Instagram photo that will appeal to hungarian teenagers (such as high school and university students) about the hungarian education system. The text on the picture says: {text}. Do not number them. Put them on one line, like how I'll be pasting it into Instagram. Some examples for formatting:

#oktatas #magyar #fesztival #teszt #iskola #hello
			"""
