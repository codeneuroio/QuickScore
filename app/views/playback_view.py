from PyQt5.QtWidgets import QGridLayout, QPushButton, QWidget


class PlaybackView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Components
        self.next_button = QPushButton("Next")
        self.prev_button = QPushButton("Prev")
        self.replay_button = QPushButton("Play")
        self.discard_button = QPushButton("Discard Event")
        self.flag_button = QPushButton("Flag Event")
        self.buttons = [
            self.next_button,
            self.prev_button,
            self.replay_button,
            self.discard_button,
            self.discard_button,
            self.flag_button,
        ]

        # Layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.prev_button, 0, 0, 1, 3)
        self.layout.addWidget(self.replay_button, 0, 3, 1, 3)
        self.layout.addWidget(self.next_button, 0, 6, 1, 3)
        self.layout.addWidget(self.discard_button, 1, 6, 1, 3)
        self.layout.addWidget(self.flag_button, 1, 0, 1, 3)

        # Initialize
        self.disable_buttons()
        self.discard_button.setCheckable(True)
        self.flag_button.setCheckable(True)

    def enable_buttons(self):
        [button.setEnabled(True) for button in self.buttons]

    def disable_buttons(self):
        [button.setEnabled(False) for button in self.buttons]
