# import pdfreader
from kivy.app import App
from kivy.uix.button import Button


class Clippy(App):
    def build(self):
        return Button(text="Welcome to Clippy!")


def main():
    Clippy().run()


if __name__:
    main()
