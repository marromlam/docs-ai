import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QFileDialog,
)
from docs_gpt import DocSearch


class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create widgets
        self.file_button = QPushButton("Select document", self)
        self.file_button.clicked.connect(self.show_file_dialog)

        self.input_label = QLabel("Question:", self)
        self.input_text = QLineEdit(self)

        # New button added to the right of the input box
        self.additional_button = QPushButton("Search", self)
        self.additional_button.clicked.connect(self.on_additional_button_click)

        self.output_label = QLabel("Answer:", self)
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.file_button)

        # Horizontal layout for input box and additional button
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_text)
        input_layout.addWidget(self.additional_button)
        layout.addLayout(input_layout)

        layout.addWidget(self.output_label)
        layout.addWidget(self.output_text)

        # Set the layout for the main window
        self.setLayout(layout)

        self.ai = None

        # Set up the main window
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("docs-ai")
        self.show()

    def show_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            "All Files (*);;Text Files (*.txt)",
            options=options,
        )

        if file_name:
            self.input_text.clear()
            self.output_text.clear()
            self.ai = DocSearch(file_name)

    def on_additional_button_click(self):
        # Add your custom functionality when the additional button is clicked
        self.output_text.clear()
        if self.ai:
            print("Additional Button Clicked!")
            query = self.input_text.text()
            # append the query to the output text
            self.output_text.append(query)
            self.ai.ask_question(
                query,
                lambda x: self.output_text.append(x),
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleApp()
    sys.exit(app.exec_())
