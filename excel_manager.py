import pandas as pd
from datetime import datetime, timedelta
import os

class ExcelManager:
    def __init__(self, config):
        self.config = config
        self.excel_file = None
        self.sheets = {}
        self.valid_categories = ['Salaries', 'Maintenance', 'Income', 'EMI', 'Hand Loans', 'Chit Box']
        self.load_excel(config.get('excel_file', ''))

    def load_excel(self, file_path):
        if file_path and os.path.exists(file_path):
            try:
                self.excel_file = pd.ExcelFile(file_path)
                self.sheets = {sheet: pd.read_excel(self.excel_file, sheet) for sheet in self.excel_file.sheet_names}
                print(f"Loaded Excel file: {file_path}")
                print(f"Available sheets: {self.get_sheet_names()}")
            except Exception as e:
                print(f"Error loading Excel file: {e}")
        else:
            print(f"Excel file not found: {file_path}")
        
        # Ensure 'Freedom(Future)' and 'Transactions(Past)' sheets exist
        if 'Freedom(Future)' not in self.sheets:
            self.sheets['Freedom(Future)'] = pd.DataFrame()
        if 'Transactions(Past)' not in self.sheets:
            self.sheets['Transactions(Past)'] = pd.DataFrame()

    def get_sheet_names(self):
        return list(self.sheets.keys()) if self.excel_file else []

    def get_sheet_data(self, sheet_name):
        return self.sheets.get(sheet_name)

    def process_transactions(self, selected_rows):
        future_sheet = self.sheets['Freedom(Future)']
        past_sheet = self.sheets['Transactions(Past)']
        accounts_sheet = self.sheets['Accounts(Present)']

        for index in selected_rows:
            row = future_sheet.iloc[index]
            category = row['Category']

            if category not in self.valid_categories:
                raise ValueError(f"Invalid category: {category}. Must be one of {self.valid_categories}")

            new_row = {
                'TrNo': past_sheet['TrNo'].max() + 1 if not past_sheet.empty else 1,
                'Date': datetime.now().strftime('%Y-%m-%d'),
                'Description': row['Description'],
                'Amount': row['Amount'],
                'PaymentMode': row['PaymentMode'],
                'AccID': row['AccID'],
                'Department': row['Department'],
                'Comments': row['Comments'],
                'Category': category,
                'DeductedReceivedThrough': row['DeductedReceivedThrough'],
                'ExpectedPaymentDate': row['Date']
            }
            past_sheet = pd.concat([past_sheet, pd.DataFrame([new_row])], ignore_index=True)

            # Add entry to the respective category sheet
            category_sheet_name = f"{self.valid_categories.index(category) + 1}_{category}"
            if category_sheet_name in self.sheets:
                category_sheet = self.sheets[category_sheet_name]
                category_sheet = pd.concat([category_sheet, pd.DataFrame([new_row])], ignore_index=True)
                self.sheets[category_sheet_name] = category_sheet
            else:
                print(f"Warning: Sheet '{category_sheet_name}' not found. Creating new sheet.")
                self.sheets[category_sheet_name] = pd.DataFrame([new_row])

            # Update CurrentBalance in Accounts(Present) sheet
            acc_id = row['AccID']
            amount = row['Amount']
            acc_row = accounts_sheet[accounts_sheet['AccID'] == acc_id]
            if not acc_row.empty:
                current_balance = acc_row['CurrentBalance'].values[0]
                new_balance = current_balance + amount
                accounts_sheet.loc[accounts_sheet['AccID'] == acc_id, 'CurrentBalance'] = new_balance
            else:
                print(f"Warning: AccID {acc_id} not found in Accounts(Present) sheet.")

        future_sheet = future_sheet.drop(selected_rows).reset_index(drop=True)

        self.sheets['Freedom(Future)'] = future_sheet
        self.sheets['Transactions(Past)'] = past_sheet
        self.sheets['Accounts(Present)'] = accounts_sheet

        # Save changes to Excel file
        with pd.ExcelWriter(self.config['excel_file'], engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            for sheet_name, sheet_data in self.sheets.items():
                if not sheet_data.empty:
                    sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)
                else:
                    print(f"Warning: Sheet '{sheet_name}' is empty and will not be saved.")

        print("Transactions processed successfully")
        self.refresh_all_sheets()

    def refresh_all_sheets(self):
        self.load_excel(self.config['excel_file'])

    def add_transaction(self, new_transaction):
        # Add to Transactions(Past) sheet
        past_sheet = self.sheets['Transactions(Past)']
        past_sheet = past_sheet.append(new_transaction, ignore_index=True)

        # Add to respective category sheet
        category = new_transaction['Category']
        if category not in self.valid_categories:
            raise ValueError(f"Invalid category: {category}. Must be one of {self.valid_categories}")

        category_sheet_name = f"{self.valid_categories.index(category) + 1}_{category}"
        if category_sheet_name in self.sheets:
            category_sheet = self.sheets[category_sheet_name]
            category_sheet = category_sheet.append(new_transaction, ignore_index=True)
            self.sheets[category_sheet_name] = category_sheet
        else:
            print(f"Warning: Sheet '{category_sheet_name}' not found. Creating new sheet.")
            self.sheets[category_sheet_name] = pd.DataFrame([new_transaction])

        # Update CurrentBalance in Accounts(Present) sheet
        acc_id = new_transaction['AccID']
        amount = new_transaction['Amount']
        accounts_sheet = self.sheets['Accounts(Present)']
        acc_row = accounts_sheet[accounts_sheet['AccID'] == acc_id]
        if not acc_row.empty:
            current_balance = acc_row['CurrentBalance'].values[0]
            new_balance = current_balance + amount
            accounts_sheet.loc[accounts_sheet['AccID'] == acc_id, 'CurrentBalance'] = new_balance
        else:
            print(f"Warning: AccID {acc_id} not found in Accounts(Present) sheet.")

        self.sheets['Transactions(Past)'] = past_sheet
        self.sheets['Accounts(Present)'] = accounts_sheet

        # Save changes to Excel file
        with pd.ExcelWriter(self.config['excel_file'], engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            for sheet_name, sheet_data in self.sheets.items():
                sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)

        print("Transaction added successfully")
        self.refresh_all_sheets()

    def get_dashboard_data(self):
        future_sheet = self.sheets['Freedom(Future)']
        today = datetime.now().date()
        one_week_later = today + timedelta(days=7)

        today_payments = []
        past_due_payments = []
        upcoming_payments = []

        for _, row in future_sheet.iterrows():
            payment_date = pd.to_datetime(row['Date']).date()
            if payment_date == today:
                today_payments.append(row)
            elif payment_date < today:
                past_due_payments.append(row)
            elif today < payment_date <= one_week_later:
                upcoming_payments.append(row)

        return {
            "today": today_payments,
            "past_due": past_due_payments,
            "upcoming": upcoming_payments
        }

    def get_total_expense(self):
        accounts_sheet = self.get_sheet_data('Accounts(Present)')
        return accounts_sheet['CurrentBalance'].sum()

    def add_future_transaction(self, new_transaction):
        future_sheet = self.sheets['Freedom(Future)']
        future_sheet = future_sheet.append(new_transaction, ignore_index=True)
        self.sheets['Freedom(Future)'] = future_sheet

        # Save changes to Excel file
        with pd.ExcelWriter(self.config['excel_file'], engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            future_sheet.to_excel(writer, sheet_name='Freedom(Future)', index=False)

        print("Future transaction added successfully")
        self.refresh_all_sheets()

    def update_cell(self, sheet_name, row, column, value):
        if sheet_name in self.sheets:
            self.sheets[sheet_name].iloc[row, column] = value
            self.save_changes()
        else:
            raise ValueError(f"Sheet '{sheet_name}' not found")

    def save_changes(self):
        with pd.ExcelWriter(self.config['excel_file'], engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            for sheet_name, sheet_data in self.sheets.items():
                sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)
        self.refresh_all_sheets()