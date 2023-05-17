from conf_manager import ConfigManager
from img_editor import ImageEditor 
from img_gen import ImageGenerator 
from txt_gen import TextGenerator
from txt_storage import TextStorage
from tui import TUI
from preset_manager import PresetManager
from post_publisher import PostPublisher

conf_manager = ConfigManager()
preset_manager = PresetManager()

img_gen = ImageGenerator(conf_manager.get_conf("organization"), conf_manager.get_conf("api_key"))
img_editor = ImageEditor(conf_manager.get_conf("font_path"), conf_manager.get_conf("branding"))

txt_storage = TextStorage()
txt_gen = TextGenerator(
	conf_manager.get_conf("organization"), 
	conf_manager.get_conf("api_key"), 
	preset_manager
)

post_publisher = PostPublisher()

PREFIX = "(lazinsta)"
tui = TUI(
	PREFIX, 
	txt_storage, 
	txt_gen, 
	img_gen, 
	img_editor, 
	preset_manager, 
	post_publisher
)
tui.start()
