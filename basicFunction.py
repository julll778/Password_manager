from PyQt6.QtWidgets import QDialog, QTreeWidgetItem
from manageData import *
from utils import *
from gui import *

class PasswordManager(Ui_PasswordManager, QDialog):
    def __init__(self):
        super(PasswordManager, self).__init__()
        self.setupUi(self)

        self.signin_pushButton1.clicked.connect(self.signin_page)
        self.create_pushButton1.clicked.connect(self.creat_page)

        self.back_pushButton2.clicked.connect(self.back_page)
        self.back_pushButton3.clicked.connect(self.back_page)
        creating_tables()

    def set_up(self):
        username = self.username_input2.text().strip()
        password = self.password_input2.text().strip()
        confirm_password = self.confirm_pass_input2.text().strip()

        exist = username_exists(username)

        if exist:
            self.message_label2.setText('username already exist')
        elif username == "":
            self.message_label2.setText("Enter a username")
        else:
            complexity = check_password(password)
            if complexity:
                if password == confirm_password:
                    hashed_password = hash_password(password)
                    set_up_account(username, hashed_password)
                    self.clear_set_up()
                    self.message_label2.setText('account created successfully!')
                else:
                    self.message_label2.setText('passwords do not match')
            else:
                self.message_label2.setText('password must include uppercase, lowercase, numbers and a special character ')

    def signin_page(self):
        self.pages.setCurrentIndex(2)
        self.login_pushButton3.clicked.connect(lambda: self.sign_in())
        self.clear_log_in()

    def sign_in(self):
        username = self.username_input3.text().strip()
        password = self.password_input3.text().strip()

        if username == "":
            self.message_label3.setText("Enter a username")
        else:
            exist = username_exists(username)
            if exist:
                hashed = retrieve_password(username)
                correct = check_password_hash(password, hashed)  #comparing hashes to check if password is correct
                if correct:
                    key = derive_key(password)
                    id_num = get_user_id(username)
                    self.credentials(id_num, key)
                else:
                    self.message_label3.setText("Password is incorrect")
            else:
                self.message_label3.setText("Username is incorrect")

    def credentials(self, id_num, key):
        self.pages.setCurrentIndex(3)
        self.message_label_acc2.clear()
        self.message_label_acc1.clear()

        self.back_pushButton_acc1.clicked.connect(lambda: self.edit_add_pages.setCurrentIndex(1))
        self.back_pushButton_acc2.clicked.connect(self.back_page, id_num, key)

        self.site_input_acc2.clear()
        self.username_input2.clear()
        self.password_input2.clear()

        self.display_credentials(id_num)

        self.site_account_tree4.itemClicked.connect(lambda item, column: self.manage_account(item, column, id_num, key))
        self.generate_pushButton_acc2.clicked.connect(self.filling_password_credentials)
        self.add_pushButton_acc2.clicked.connect(lambda: self.adding_credentials(id_num, key))

    def manage_account(self, item, column, id_num, key):

        if column == 1:
            self.message_label_acc1.clear()
            self.site_input_acc1.clear()
            self.username_input_acc1.clear()
            self.password_input_acc1.clear()

            self.edit_add_pages.setCurrentIndex(0)

            try:
                username = item.text(column)
                site = item.parent().text(0)
                password = get_password(id_num, username, site, key)
                self.password_input_acc1.insert(password)
                self.site_input_acc1.insert(site)
                self.username_input_acc1.insert(username)

                self.pushButton_7.clicked.disconnect()
                self.delete_pushButton_acc1.clicked.disconnect()
            except:
                pass  # Ignore if no connection exists yet

            self.pushButton_7.clicked.connect(lambda: self.editing_credentials(username, site, id_num, key))
            self.delete_pushButton_acc1.clicked.connect(lambda : self.deleting_credentials(username, site, id_num))

    def editing_credentials(self, username, site, id_num, key):
        new_site = self.site_input_acc1.text().strip()
        new_username = self.username_input_acc1.text().strip()
        new_password = self.password_input_acc1.text().strip()

        creds_dict = {site_list[0]: site_list[1:] for site_list in retrieve_credentials(id_num)}

        exists = new_site in creds_dict and new_username in creds_dict[new_site]


        if new_site == "":
            self.message_label_acc1.setText("Provide a site name")
        elif new_username == "":
            self.message_label_acc1.setText("Provide a username")
        elif exists:
            self.message_label_acc1.setText("username exists")
        else:
            complex = check_password(new_password)
            if complex:
                update_credential(id_num, username, site, new_site, new_username, new_password, key)
                self.message_label_acc1.setText("Edited successfully!")
                self.display_credentials(id_num)
            else:
                self.message_label_acc1.setText("Password is not complex")

    def deleting_credentials(self, username, site, id_num):

        deleted_credential(id_num, username, site)
        self.display_credentials(id_num)
        self.message_label_acc1.setText("Account deleted successfully")

    def adding_credentials(self,id_num, key):

        site = self.site_input_acc2.text().strip()
        username = self.username_input_acc2.text().strip()
        password = self.password_input_acc2.text().strip()

        creds_dict = {site_list[0]: site_list[1:] for site_list in retrieve_credentials(id_num)}

        exists = site in creds_dict and username in creds_dict[site]

        if site == "":
            self.message_label_acc2.setText("Provide a site name")
        elif username == "":
            self.message_label_acc2.setText("Provide a username")
        elif exists:
            self.message_label_acc2.setText("username exists")
        else:
            complex = check_password(password)
            if complex:
                insert_credential(id_num, site, username, password, key)
                self.message_label_acc2.setText("Added successfully!")
                self.display_credentials(id_num)
            else:
                self.message_label_acc2.setText("Password is not complex")

    def display_credentials(self, id_num):
        self.site_account_tree4.clear()
        creds = retrieve_credentials(id_num)
        self.site_account_tree4.clear()

        for site_list in creds:
            site_item = QTreeWidgetItem(self.site_account_tree4)
            site_item.setText(0, site_list[0])

            for username in site_list[1:]:
                user_item = QTreeWidgetItem(site_item)
                user_item.setText(1, username)

    def clear_set_up(self):
        self.username_input2.clear()
        self.password_input2.clear()
        self.confirm_pass_input2.clear()
        self.message_label2.clear()

    def clear_log_in(self):
        self.username_input3.clear()
        self.password_input3.clear()
        self.message_label3.clear()

    def creat_page(self):
        self.pages.setCurrentIndex(1)
        self.clear_set_up()
        self.generate_pushButton2.clicked.connect(lambda: self.filling_password_signup())
        self.creat_pushButton2.clicked.connect(lambda:self.set_up())

    def filling_password_signup(self):
        self.password_input2.clear()
        self.confirm_pass_input2.clear()
        self.password_input2.insert(generate_password())

    def filling_password_credentials(self):
        self.password_input_acc2.clear()
        self.password_input_acc2.insert(generate_password())

    def back_page(self):
        self.pages.setCurrentIndex(0)
        self.clear_set_up()
        self.clear_log_in()

