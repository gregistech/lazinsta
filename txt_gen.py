import openai

class TextGenerator:
	def __init__(self, organization, api_key, preset_manager, model = "gpt-3.5-turbo"):
		openai.organization = organization 
		openai.api_key = api_key 
		self.model = model
		self._preset_manager = preset_manager	
	def generate(self, instruction, n = 4):
		while True:
			try:
				return list(map(lambda choice: choice.message.content, openai.ChatCompletion.create(
						model=self.model,
						messages=[
							{ 
								"role": "system", 
								"content": self._preset_manager.get("identity") 
							},
							{ "role": "user", "content": instruction }
						],
						n=n
					).choices)
				)
			except openai.error.RateLimitError:
				print("Rate limit or overloaded servers! Retrying...")
