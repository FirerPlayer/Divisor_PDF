from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout


from tkinter import filedialog, Tk
from divider import split_pdf, get_pdf_number_pages

from kivy.config import Config

# Config.set("graphics", "minimum_width", 600)
# Config.set("graphics", "minimum_height", 300)
Config.set("graphics", "width", 600)
Config.set("graphics", "height", 300)
Config.set("graphics", "resizable", 0)

Config.write()


def pop_ok(title, text_content):
    pop = Popup()
    pop.title = title
    pop.content = Label(text=text_content)
    b = Button(text="Ok", on_press=pop.dismiss)
    b.size_hint_y = 0.4
    b.x, b.y = 250, 65
    fl = FloatLayout()
    fl.add_widget(b)
    pop.content.add_widget(fl)
    pop.size_hint = 0.5, 0.5
    pop.open()


class ZipCheck(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.c = CheckBox()
        self.add_widget(self.c)
        rl = RelativeLayout()
        rl.add_widget(Label(text="Compress Zip", color="white", y=20))
        self.add_widget(rl)

    def get_status(self):
        return self.c.active


class PagesInput(AnchorLayout):
    def __init__(self, text, inital_value=1, **kwargs):
        super().__init__(**kwargs)
        self.i = TextInput()
        self.i.text = f"{inital_value}"
        self.i.multiline = False
        self.i.size_hint_max_y = 30
        self.i.size_hint_max_x = 40
        self.add_widget(self.i)
        rl = RelativeLayout()
        rl.add_widget(Label(text=text, color="white", y=25))
        self.add_widget(rl)

    def get_text(self):
        return self.i.text

    def set_text(self, txt):
        self.i.text = txt


class SplitButton(Button):
    def __init__(self, call, **kwargs):
        super().__init__(**kwargs)
        self.text = "Split PDF"
        self.font_size = 18
        self.background_color = "#7030d1"
        self.call: dict = call
        # self.size_hint = 0.5, 0.4

    def set_call(self, call):
        self.call = call

    def on_press(self):
        try:
            split_pdf(
                file_path=self.call["file_path"].get_text(),
                out_path=self.call["out_path"].get_text(),
                is_zip=self.call["is_zip"].get_status(),
                start=int(self.call["start_in"].get_text()),
                end=int(self.call["end_in"].get_text()),
            )
            pop_ok("Sucesso", "Partes extraidas com sucesso !")
        except IndexError:
            pop_ok("Erro", "Paginas inválidas")
        except FileNotFoundError:
            pop_ok("Erro", "Arquivo ou diretório inválido")


class FileInput(AnchorLayout):
    def __init__(self, hint_text="", **kwargs):
        super().__init__(**kwargs)
        self.i = TextInput()
        self.i.multiline = False
        self.i.hint_text = hint_text
        self.i.size_hint_max_y = 35
        self.i.size_hint_max_x = 600
        self.padding = 50, 0, -50, 0
        self.add_widget(self.i)

    def get_text(self):
        return self.i.text

    def set_text(self, txt):
        self.i.text = txt


class BrowseButton(AnchorLayout):
    def __init__(
        self, text, file_input, is_folder=False, end_input: PagesInput = None, **kwargs
    ):
        super().__init__(**kwargs)
        b = Button()
        b.text = text
        b.on_press = self._press
        b.size_hint_max_y = 40
        b.size_hint_max_x = 150
        self.add_widget(b)
        self.file_input: FileInput = file_input
        self.end_input = end_input
        self.is_folder = is_folder

    def _press(self):
        root = Tk()
        root.withdraw()
        filetypes = (("PDF files", "*.pdf"),)
        if self.is_folder:
            folder_name = filedialog.askdirectory(
                title="Open a directory", initialdir="."
            )
            self.file_input.set_text(folder_name)
        else:
            file_name = filedialog.askopenfilename(
                title="Open a file", initialdir=".", filetypes=filetypes
            )
            self.file_input.set_text(file_name)
            if self.end_input:
                self.end_input.set_text(f"{get_pdf_number_pages(file_name)}")


class Home(BoxLayout):
    def __init__(self, **kwargs):
        super(Home, self).__init__(**kwargs)
        self.orientation = "vertical"
        file_input = FileInput(hint_text="Arquivo PDF")
        out_input = FileInput(hint_text="Salvar em...")
        zip_check = ZipCheck()
        start_in = PagesInput(text="Inicio")
        end_in = PagesInput(text="Fim", inital_value=1)
        box = BoxLayout(orientation="horizontal")
        box.add_widget(file_input)
        box.add_widget(BrowseButton("Escolher PDF", file_input, False, end_in))
        box1 = BoxLayout(orientation="horizontal")
        box1.add_widget(out_input)
        box1.add_widget(BrowseButton("Escolher Pasta", out_input, True))
        box2 = BoxLayout(orientation="horizontal")
        box2.add_widget(zip_check)
        box2.add_widget(start_in)
        box2.add_widget(end_in)
        l = Label(
            text="DIVISOR DE PDF\n Separe cada página do seu PDF em arquivos únicos"
        )
        l.halign = "center"
        self.add_widget(l)
        self.add_widget(box)
        self.add_widget(box1)
        self.add_widget(box2)
        self.add_widget(
            SplitButton(
                {
                    "file_path": file_input,
                    "out_path": out_input,
                    "is_zip": zip_check,
                    "start_in": start_in,
                    "end_in": end_in,
                }
            )
        )


class PDFParts(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "PDF Parts"
        self.icon = "icon.png"

    def build(self):
        return Home()


if __name__ == "__main__":
    PDFParts().run()
