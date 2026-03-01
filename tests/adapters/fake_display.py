from pico_w_explorer.ports import DisplayPort


class FakeDisplay(DisplayPort):
    def __init__(self) -> None:
        self.last_text: str | None = None
        self.texts: list[str] = []

    def show_text(self, text: str) -> None:
        self.last_text = text
        self.texts.append(text)
