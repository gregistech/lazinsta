import openai

class TextGenerator:
	def __init__(self, organization, api_key, model = "gpt-3.5-turbo"):
		openai.organization = organization 
		openai.api_key = api_key 
		self.model = model
	def generate(self, identity, instruction, n = 4):
		return list(map(lambda choice: choice.message.content, openai.ChatCompletion.create(
				model=self.model,
				messages=[
					{ "role": "system", "content": identity },
					{ "role": "user", "content": instruction }
				],
				n=n
			).choices)
		)
