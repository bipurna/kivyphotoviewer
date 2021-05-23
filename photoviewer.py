import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
import os
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from PIL import Image, ImageEnhance
from PIL.ExifTags import TAGS
import codecs
from kivy.core.window import Window
from kivy.metrics import dp

title = "Photos"

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class PhotoViewWidget(BoxLayout):
    global title
    loadfile = ObjectProperty(None)
    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        try:
            imagename = str(filename[0])
            self.ids.imageView.source = imagename
            image = Image.open(imagename)
            self.ids.name.text=imagename
            exifdata = image.getexif()
            image_data = {}
            for tag_id in exifdata:
                # get the tag name, instead of human unreadable tag id
                tag = TAGS.get(tag_id, tag_id)
                data = exifdata.get(tag_id)

                # decode bytes 
                if isinstance(data, bytes):
                    data = data.decode('utf-8', 'ignore')
                
                image_data[f"{tag:20}".strip()] = data
                new_l = Label(text=f"{tag:20}".strip()+f": {data}".strip(),font_size=dp(10))
                self.ids.details.add_widget(new_l)
        except Exception as e:
            self.ids.details.clear_widgets()
            self.ids.name.text= ""
        self.dismiss_popup()

class PhotoViewApp(App):
    def build(self):
        self.title = title
        return PhotoViewWidget()


if __name__ == '__main__':
    papp = PhotoViewApp()
    papp.icon="images/share.png"
    Window.minimum_height = 500
    Window.minimum_width = 600
    papp.run()
