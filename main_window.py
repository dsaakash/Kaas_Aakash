from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QListWidget, QCheckBox, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import Qt
from excel_manager import ExcelManager

class MainWindow(QMainWindow):
    def __init__(self, excel_manager):
        super().__init__()
        self.excel_manager = excel_manager
        self.init_ui()

    def init_ui(self):
        # Create main layout
        main_layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # ... existing UI setup code ...

        # Add Dashboard dropdown
        self.dashboard_dropdown = QComboBox()
        self.dashboard_dropdown.addItem("Dashboard")
        self.dashboard_dropdown.currentIndexChanged.connect(self.show_dashboard)

        # Create dashboard widget
        self.dashboard_widget = QWidget()
        self.dashboard_layout = QVBoxLayout()
        self.dashboard_widget.setLayout(self.dashboard_layout)
        self.dashboard_widget.hide()

        # Add dashboard widget to main layout
        main_layout.addWidget(self.dashboard_dropdown)
        main_layout.addWidget(self.dashboard_widget)

        # ... rest of the UI setup code ...

    def show_dashboard(self):
        if self.dashboard_dropdown.currentText() == "Dashboard":
            self.update_dashboard()
            self.dashboard_widget.show()
        else:
            self.dashboard_widget.hide()

    def update_dashboard(self):
        # Clear existing items
        for i in reversed(range(self.dashboard_layout.count())): 
            self.dashboard_layout.itemAt(i).widget().setParent(None)

        dashboard_data = self.excel_manager.get_dashboard_data()

        for section, title in [("today", "Today's Payments"), ("past_due", "Past Due Payments"), ("upcoming", "Upcoming Week's Payments")]:
            section_widget = QWidget()
            section_layout = QVBoxLayout()
            section_widget.setLayout(section_layout)

            section_label = QLabel(title)
            section_label.setStyleSheet("font-weight: bold; font-size: 14px;")
            section_layout.addWidget(section_label)

            for item in dashboard_data[section]:
                checkbox = QCheckBox(f"{item['Description']} - {item['Amount']}")
                checkbox.setStyleSheet("margin-left: 20px;")
                section_layout.addWidget(checkbox)

            self.dashboard_layout.addWidget(section_widget)

        process_button = QPushButton("Process Selected Transactions")
        process_button.clicked.connect(self.process_selected_transactions)
        self.dashboard_layout.addWidget(process_button)

    def process_selected_transactions(self):
        selected_rows = []
        for i in range(self.dashboard_layout.count() - 1):  # Exclude the button
            section_widget = self.dashboard_layout.itemAt(i).widget()
            section_layout = section_widget.layout()
            for j in range(1, section_layout.count()):  # Start from 1 to skip the label
                checkbox = section_layout.itemAt(j).widget()
                if checkbox.isChecked():
                    # Find the corresponding row in the Freedom(Future) sheet
                    description, amount = checkbox.text().split(" - ")
                    future_sheet = self.excel_manager.get_sheet_data('Freedom(Future)')
                    row_index = future_sheet[(future_sheet['Description'] == description) & (future_sheet['Amount'] == float(amount))].index[0]
                    selected_rows.append(row_index)

        if selected_rows:
            self.excel_manager.process_transactions(selected_rows)
            self.update_dashboard()
        else:
            QMessageBox.warning(self, "No Selection", "Please select at least one transaction to process.")

    # ... rest of the class methods ...