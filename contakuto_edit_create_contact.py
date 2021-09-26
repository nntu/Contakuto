from data_class import *
import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from contakuto_basegui import *
import datetime


# Edit Profile Window
class ContactModifyingUI(QWidget):
    def __init__(self, parent=None, scroll_widget=None, mode=0, row=6):
        super(ContactModifyingUI, self).__init__(parent)
        self.setObjectName("contact_edit_create")
        self.setAttribute(Qt.WA_StyledBackground)
        self.setFixedWidth(scroll_widget.width())
        self.setMinimumHeight(scroll_widget.height())
        self.setStyleSheet(scroll_widget.parent().parent().styleSheet())
        self.main_directory = os.path.dirname(__file__)
        self.picturefolder_path = "./data/{0}/profile_pictures/".format(user.getData("username"))
        self.defaultPicture_path = "./image/default_avatar.png"
        self.old_path = None
        self.newImage = None

        # Control creating mode or editing mode
        self.mode = mode
        self.row = row

        # Control exit function
        self.save = 0

        # Control width attributes of all boxes
        self.main_width = self.width() - 20

        # Profile Picture Box
        self.profile_picture_box = QGroupBox(self)
        self.profile_picture_box.setObjectName("edit_profile_picture_box")
        self.profile_picture_box.setGeometry(QRect(15, 10, 144, 144))
        # Profile Picture
        self.profile_picture = QLabel(self.profile_picture_box)
        self.profile_picture.setObjectName("edit_profile_picture")
        self.profile_picture.setGeometry(15, 15, 114, 114)
        # Edit Picture Label
        self.edit_picture_label = QLabel(self.profile_picture_box)
        self.edit_picture_label.resize(self.profile_picture.width(), 20)
        self.edit_picture_label.move(
            self.profile_picture.x() + (self.profile_picture.width() - self.edit_picture_label.width()) / 2, 
            self.profile_picture.y() + (self.profile_picture.height() - self.edit_picture_label.height()))
        self.edit_picture_label.setObjectName("edit_picture_label")
        self.edit_picture_label.setAlignment(Qt.AlignCenter)
        self.edit_picture_label.setText(lang["edit"])
        # Edit Profile Picture Button
        self.edit_picture_button = QPushButton(self.profile_picture_box)
        self.edit_picture_button.setObjectName("edit_profile_picture_button")
        self.edit_picture_button.setAttribute(Qt.WA_StyledBackground)
        self.edit_picture_button.setGeometry(QRect(
            self.profile_picture.x() - 3, 
            self.profile_picture.y() - 3, 
            self.profile_picture.width() + 6, 
            self.profile_picture.height() + 6))
        self.edit_picture_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.edit_picture_button.clicked.connect(self.getImage)


        # Name Box
        self.name_box = QGroupBox(self)
        self.name_box.setGeometry(QRect(
            self.profile_picture_box.x() + self.profile_picture_box.width() + 10, 
            self.profile_picture_box.y(), 
            320, 
            self.profile_picture_box.height()))
        # Full Name Label
        self.fullname_label = QLabel(self.name_box)
        self.fullname_label.setGeometry(QRect(20, 15, 80, 25))
        self.fullname_label.setText(lang["fullname"])
        # Nickname Label
        self.nickname_label = QLabel(self.name_box)
        self.nickname_label.setGeometry(QRect(
            self.fullname_label.x(), 
            self.fullname_label.y() + self.fullname_label.height() + 5, 
            self.fullname_label.width(), 
            self.fullname_label.height()))
        self.nickname_label.setText(lang["nickname"])
        # Company Label
        self.company_label = QLabel(self.name_box)
        self.company_label.setGeometry(QRect(
            self.fullname_label.x(), 
            self.nickname_label.y() + self.nickname_label.height() + 5, 
            self.fullname_label.width(), 
            self.fullname_label.height()))
        self.company_label.setText(lang["company"])
        # Job Title Label
        self.jobtitle_label = QLabel(self.name_box)
        self.jobtitle_label.setGeometry(QRect(
            self.fullname_label.x(), 
            self.company_label.y() + self.company_label.height() + 5, 
            self.fullname_label.width(), 
            self.fullname_label.height()))
        self.jobtitle_label.setText(lang["jobtitle"])
        # Full Name
        self.fullname = QLineEdit(self.name_box)
        self.fullname.setGeometry(QRect(
            self.fullname_label.x() + self.fullname_label.width() + 20, 
            self.fullname_label.y(), 
            170, 
            25))
        self.fullname.setPlaceholderText(lang["fullname"])
        # Nickname
        self.nickname = QLineEdit(self.name_box)
        self.nickname.setGeometry(QRect(
            self.fullname.x(), 
            self.fullname.y() + self.fullname.height() + 5, 
            self.fullname.width(), 
            self.fullname.height()))
        self.nickname.setPlaceholderText(lang["nickname"])
        # Company
        self.company = QLineEdit(self.name_box)
        self.company.setGeometry(QRect(
            self.fullname.x(), 
            self.nickname.y() + self.nickname.height() + 5, 
            self.fullname.width(), 
            self.fullname.height()))
        self.company.setPlaceholderText(lang["company"])
        # Job Title
        self.jobtitle = QLineEdit(self.name_box)
        self.jobtitle.setGeometry(QRect(
            self.fullname.x(), 
            self.company.y() + self.company.height() + 5, 
            self.fullname.width(), 
            self.fullname.height()))
        self.jobtitle.setPlaceholderText(lang["jobtitle"])

        # Save Box
        self.save_box = QGroupBox(self)
        self.save_box.move(
            self.name_box.x() + self.name_box.width() + 10, 
            self.profile_picture_box.y())
        self.save_box.setFixedSize(
            self.main_width - self.save_box.x(), 
            self.profile_picture_box.height())
        # Save Button
        self.save_button = QPushButton(self.save_box)
        self.save_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.save_button.setObjectName("blue_button")
        self.save_button.resize(110, 30)
        self.save_button.move(
            (self.save_box.width() - self.save_button.width()) / 2, 
            self.save_box.height() / 2 - self.save_button.height() - 5)
        self.save_button.setText(lang["save"])
        # Cancel Button
        self.cancel_button = QPushButton(self.save_box)
        self.cancel_button.setCursor(self.save_button.cursor())
        self.cancel_button.setGeometry(QRect(
            self.save_button.x(), 
            self.save_button.y() + self.save_button.height() + 5, 
            self.save_button.width(), 
            self.save_button.height()))
        self.cancel_button.setText(lang["cancel"])
        self.cancel_button.clicked.connect(self.close)


        # Phone Box
        self.phone_box = QGroupBox(self)
        self.phone_box.setGeometry(QRect(
            self.profile_picture_box.x(), 
            self.profile_picture_box.y() + self.profile_picture_box.height() + 10, 
            self.main_width / 2 - 10, 
            145))
        self.phonenumber_labelKey = ["home", "work", "school", "fax", "custom"]
        self.phonenumber_labelItems = []
        for key in self.phonenumber_labelKey:
            self.phonenumber_labelItems.append(lang[key])

        # Phone 1 Add Button
        self.phonenumber1_addbutton = QPushButton(self.phone_box)
        self.phonenumber1_addbutton.resize(150, 25)
        self.phonenumber1_addbutton.move(
            (self.phone_box.width() - self.phonenumber1_addbutton.width()) / 2, 
            15)
        self.phonenumber1_addbutton.setText(lang["add_phone_number"])
        self.phonenumber1_addbutton.setCursor(QCursor(Qt.PointingHandCursor))
        self.phonenumber1_addbutton.clicked.connect(
            lambda: self.addPhone(
                self.phonenumber1_label, 
                self.phonenumber1_addbutton, 
                self.phonenumber1_deletebutton, 
                self.phonenumber1_textbox))
        # Phone 1 Delete Button
        self.phonenumber1_deletebutton = QPushButton(self.phone_box)
        self.phonenumber1_deletebutton.setGeometry(QRect(30, 15, 40, 25))
        self.phonenumber1_deletebutton.setStyleSheet("color: red;")
        self.phonenumber1_deletebutton.setText(lang["delete"])
        self.phonenumber1_deletebutton.setCursor(self.phonenumber1_addbutton.cursor())
        self.phonenumber1_deletebutton.clicked.connect(
            lambda: self.deletePhone(
                self.phonenumber1_label, 
                self.phonenumber1_addbutton, 
                self.phonenumber1_deletebutton, 
                self.phonenumber1_textbox, 
                0))
        # Phone 1 Label
        self.phonenumber1_label = QComboBox(self.phone_box)
        self.phonenumber1_previouslabel = QLabel()
        self.phonenumber1_label.addItems(self.phonenumber_labelItems)
        self.phonenumber1_label.setGeometry(QRect(
            self.phonenumber1_deletebutton.x() + self.phonenumber1_deletebutton.width() + 10, 
            self.phonenumber1_deletebutton.y(), 
            80, 
            self.phonenumber1_deletebutton.height()))
        self.phonenumber1_label.setCursor(self.phonenumber1_deletebutton.cursor())
        self.phonenumber1_label.currentIndexChanged.connect(
            lambda: self.addCustomLabel(
                self.phonenumber1_label, 
                self.phonenumber1_previouslabel))
        # Phone 1 Textbox
        self.phonenumber1_textbox = QLineEdit(self.phone_box)
        self.phonenumber1_textbox.setGeometry(QRect(
            self.phonenumber1_label.x() + self.phonenumber1_label.width() + 10, 
            self.phonenumber1_deletebutton.y(), 
            130, 
            self.phonenumber1_deletebutton.height()))
        self.phonenumber1_textbox.setPlaceholderText("0123 456 789")
        self.phonenumber1_textbox.setValidator(QRegExpValidator(QRegExp("^[0-9+- ]{3,15}$")))
        self.phonenumber1_textbox.setMaxLength(15)

        # Phone 2 Add Button
        self.phonenumber2_addbutton = QPushButton(self.phone_box)
        self.phonenumber2_addbutton.setGeometry(QRect(
            self.phonenumber1_addbutton.x(), 
            self.phonenumber1_addbutton.y() + self.phonenumber1_addbutton.height() + 5, 
            self.phonenumber1_addbutton.width(), 
            self.phonenumber1_addbutton.height()))
        self.phonenumber2_addbutton.setText(self.phonenumber1_addbutton.text())
        self.phonenumber2_addbutton.setCursor(QCursor(Qt.PointingHandCursor))
        self.phonenumber2_addbutton.clicked.connect(
            lambda: self.addPhone(
                self.phonenumber2_label, 
                self.phonenumber2_addbutton, 
                self.phonenumber2_deletebutton, 
                self.phonenumber2_textbox))
        # Phone 2 Delete Button
        self.phonenumber2_deletebutton = QPushButton(self.phone_box)
        self.phonenumber2_deletebutton.setGeometry(QRect(
            self.phonenumber1_deletebutton.x(), 
            self.phonenumber2_addbutton.y(), 
            self.phonenumber1_deletebutton.width(), 
            self.phonenumber1_deletebutton.height()))
        self.phonenumber2_deletebutton.setStyleSheet(self.phonenumber1_deletebutton.styleSheet())
        self.phonenumber2_deletebutton.setText(self.phonenumber1_deletebutton.text())
        self.phonenumber2_deletebutton.setCursor(QCursor(Qt.PointingHandCursor))
        self.phonenumber2_deletebutton.clicked.connect(
            lambda: self.deletePhone(
                self.phonenumber2_label, 
                self.phonenumber2_addbutton, 
                self.phonenumber2_deletebutton, 
                self.phonenumber2_textbox, 1))
        # Phone 2 Label
        self.phonenumber2_label = QComboBox(self.phone_box)
        self.phonenumber2_previouslabel = QLabel()
        self.phonenumber2_label.addItems(self.phonenumber_labelItems)
        self.phonenumber2_label.setGeometry(QRect(
            self.phonenumber1_label.x(), 
            self.phonenumber2_addbutton.y(), 
            self.phonenumber1_label.width(), 
            self.phonenumber1_label.height()))
        self.phonenumber2_label.setCursor(QCursor(Qt.PointingHandCursor))
        self.phonenumber2_label.currentIndexChanged.connect(
            lambda: self.addCustomLabel(
                self.phonenumber2_label, 
                self.phonenumber2_previouslabel))
        # Phone 2 Textbox
        self.phonenumber2_textbox = QLineEdit(self.phone_box)
        self.phonenumber2_textbox.setGeometry(QRect(
            self.phonenumber1_textbox.x(), 
            self.phonenumber2_addbutton.y(), 
            self.phonenumber1_textbox.width(), 
            self.phonenumber1_textbox.height()))
        self.phonenumber2_textbox.setPlaceholderText(self.phonenumber1_textbox.placeholderText())
        self.phonenumber2_textbox.setValidator(self.phonenumber1_textbox.validator())
        self.phonenumber2_textbox.setMaxLength(self.phonenumber1_textbox.maxLength())

        # Phone 3 Add Button
        self.phonenumber3_addbutton = QPushButton(self.phone_box)
        self.phonenumber3_addbutton.setGeometry(QRect(
            self.phonenumber1_addbutton.x(), 
            self.phonenumber2_addbutton.y() + self.phonenumber2_addbutton.height() + 5, 
            self.phonenumber1_addbutton.width(), 
            self.phonenumber1_addbutton.height()))
        self.phonenumber3_addbutton.setText(self.phonenumber1_addbutton.text())
        self.phonenumber3_addbutton.setCursor(QCursor(Qt.PointingHandCursor))
        self.phonenumber3_addbutton.clicked.connect(
            lambda: self.addPhone(
                self.phonenumber3_label, 
                self.phonenumber3_addbutton, 
                self.phonenumber3_deletebutton, 
                self.phonenumber3_textbox))
        # Phone 3 Delete Button
        self.phonenumber3_deletebutton = QPushButton(self.phone_box)
        self.phonenumber3_deletebutton.setGeometry(QRect(
            self.phonenumber1_deletebutton.x(), 
            self.phonenumber3_addbutton.y(), 
            self.phonenumber1_deletebutton.width(), 
            self.phonenumber1_deletebutton.height()))
        self.phonenumber3_deletebutton.setStyleSheet(self.phonenumber1_deletebutton.styleSheet())
        self.phonenumber3_deletebutton.setText(self.phonenumber1_deletebutton.text())
        self.phonenumber3_deletebutton.setCursor(QCursor(Qt.PointingHandCursor))
        self.phonenumber3_deletebutton.clicked.connect(
            lambda: self.deletePhone(
                self.phonenumber3_label, 
                self.phonenumber3_addbutton, 
                self.phonenumber3_deletebutton, 
                self.phonenumber3_textbox, 
                2))
        # Phone 3 Label
        self.phonenumber3_label = QComboBox(self.phone_box)
        self.phonenumber3_previouslabel = QLabel()
        self.phonenumber3_label.addItems(self.phonenumber_labelItems)
        self.phonenumber3_label.setGeometry(QRect(
            self.phonenumber1_label.x(), 
            self.phonenumber3_addbutton.y(), 
            self.phonenumber1_label.width(), 
            self.phonenumber1_label.height()))
        self.phonenumber3_label.setCursor(QCursor(Qt.PointingHandCursor))
        self.phonenumber3_label.currentIndexChanged.connect(
            lambda: self.addCustomLabel(
                self.phonenumber3_label, 
                self.phonenumber3_previouslabel))
        # Phone 3 Textbox
        self.phonenumber3_textbox = QLineEdit(self.phone_box)
        self.phonenumber3_textbox.setGeometry(QRect(
            self.phonenumber1_textbox.x(), 
            self.phonenumber3_addbutton.y(), 
            self.phonenumber1_textbox.width(), 
            self.phonenumber1_textbox.height()))
        self.phonenumber3_textbox.setPlaceholderText(self.phonenumber1_textbox.placeholderText())
        self.phonenumber3_textbox.setValidator(self.phonenumber1_textbox.validator())
        self.phonenumber3_textbox.setMaxLength(self.phonenumber1_textbox.maxLength())
        # Phone 4 Add Button
        self.phonenumber4_addbutton = QPushButton(self.phone_box)
        self.phonenumber4_addbutton.setGeometry(QRect(
            self.phonenumber1_addbutton.x(), 
            self.phonenumber3_addbutton.y() + self.phonenumber3_addbutton.height() + 5, 
            self.phonenumber1_addbutton.width(), 
            self.phonenumber1_addbutton.height()))
        self.phonenumber4_addbutton.setText(self.phonenumber1_addbutton.text())
        self.phonenumber4_addbutton.setCursor(self.phonenumber1_addbutton.cursor())
        self.phonenumber4_addbutton.clicked.connect(
            lambda: self.addPhone(
                self.phonenumber4_label, 
                self.phonenumber4_addbutton, 
                self.phonenumber4_deletebutton, 
                self.phonenumber4_textbox))
        # Phone 4 Delete Button
        self.phonenumber4_deletebutton = QPushButton(self.phone_box)
        self.phonenumber4_deletebutton.setGeometry(QRect(
            self.phonenumber1_deletebutton.x(), 
            self.phonenumber4_addbutton.y(), 
            self.phonenumber1_deletebutton.width(), 
            self.phonenumber1_deletebutton.height()))
        self.phonenumber4_deletebutton.setStyleSheet(self.phonenumber1_deletebutton.styleSheet())
        self.phonenumber4_deletebutton.setText(self.phonenumber1_deletebutton.text())
        self.phonenumber4_deletebutton.setCursor(QCursor(Qt.PointingHandCursor))
        self.phonenumber4_deletebutton.clicked.connect(
            lambda: self.deletePhone(
                self.phonenumber4_label, 
                self.phonenumber4_addbutton, 
                self.phonenumber4_deletebutton, 
                self.phonenumber4_textbox, 3))
        # Phone 4 Label
        self.phonenumber4_label = QComboBox(self.phone_box)
        self.phonenumber4_previouslabel = QLabel()
        self.phonenumber4_label.addItems(self.phonenumber_labelItems)
        self.phonenumber4_label.setGeometry(QRect(
            self.phonenumber1_label.x(), 
            self.phonenumber4_addbutton.y(), 
            self.phonenumber1_label.width(), 
            self.phonenumber1_label.height()))
        self.phonenumber4_label.setCursor(QCursor(Qt.PointingHandCursor))
        self.phonenumber4_label.currentIndexChanged.connect(
            lambda: self.addCustomLabel(
                self.phonenumber4_label, 
                self.phonenumber4_previouslabel))
        # Phone 4 Textbox
        self.phonenumber4_textbox = QLineEdit(self.phone_box)
        self.phonenumber4_textbox.setGeometry(QRect(
            self.phonenumber1_textbox.x(), 
            self.phonenumber4_addbutton.y(), 
            self.phonenumber1_textbox.width(), 
            self.phonenumber1_textbox.height()))
        self.phonenumber4_textbox.setPlaceholderText(self.phonenumber1_textbox.placeholderText())
        self.phonenumber4_textbox.setValidator(self.phonenumber1_textbox.validator())
        self.phonenumber4_textbox.setMaxLength(self.phonenumber1_textbox.maxLength())

        # Email Box
        self.email_box = QGroupBox(self)
        self.email_box.setGeometry(QRect(
            self.phone_box.x(), 
            self.phone_box.y() + self.phone_box.height() + 10, 
            self.phone_box.width(), 
            85))
        self.email_labelKey = ["home", "work", "school", "custom"]
        self.email_labelItems = []
        for key in self.email_labelKey:
            self.email_labelItems.append(lang[key])

        # Email 1 Add Button
        self.email1_addbutton = QPushButton(self.email_box)
        self.email1_addbutton.resize(150, 25)
        self.email1_addbutton.move(
            (self.email_box.width() - self.email1_addbutton.width()) / 2, 
            15)
        self.email1_addbutton.setText(lang["add_email"])
        self.email1_addbutton.setCursor(QCursor(Qt.PointingHandCursor))
        self.email1_addbutton.clicked.connect(
            lambda: self.addEmail(
                self.email1_addbutton, 
                self.email1_deletebutton, 
                self.email1_label, 
                self.email1_textbox))
        # Email 1 Delete Button
        self.email1_deletebutton = QPushButton(self.email_box)
        self.email1_deletebutton.setGeometry(QRect(10, 15, 40, 25))
        self.email1_deletebutton.setStyleSheet("color: red;")
        self.email1_deletebutton.setText(lang["delete"])
        self.email1_deletebutton.setCursor(QCursor(Qt.PointingHandCursor))
        self.email1_deletebutton.clicked.connect(
            lambda: self.deleteEmail(
                self.email1_addbutton, 
                self.email1_deletebutton, 
                self.email1_label, 
                self.email1_textbox, 
                0))
        # Email 1 Label
        self.email1_label = QComboBox(self.email_box)
        self.email1_previouslabel = QLabel()
        self.email1_label.addItems(self.email_labelItems)
        self.email1_label.setGeometry(QRect(
            self.email1_deletebutton.x() + self.email1_deletebutton.width() + 10, 
            self.email1_addbutton.y(), 
            80, 
            self.email1_addbutton.height()))
        self.email1_label.setCursor(QCursor(Qt.PointingHandCursor))
        self.email1_label.currentIndexChanged.connect(
            lambda: self.addCustomLabel(
                self.email1_label, 
                self.email1_previouslabel))
        # Email 1 Textbox
        self.email1_textbox = QLineEdit(self.email_box)
        self.email1_textbox.move(
            self.email1_label.x() + self.email1_label.width() + 10, 
            self.email1_addbutton.y())
        self.email1_textbox.setFixedSize(
            self.email_box.width() - self.email1_deletebutton.x() - self.email1_textbox.x(), 
            self.email1_addbutton.height())
        self.email1_textbox.setPlaceholderText("qwerty123@abc.com")
        self.email1_textbox.setMaxLength(30)

        # Email 2 Add Button
        self.email2_addbutton = QPushButton(self.email_box)
        self.email2_addbutton.setGeometry(QRect(
            self.email1_addbutton.x(), 
            self.email1_addbutton.y() + self.email1_addbutton.height() + 5, 
            self.email1_addbutton.width(), 
            self.email1_addbutton.height()))
        self.email2_addbutton.setText(self.email1_addbutton.text())
        self.email2_addbutton.setCursor(self.email1_addbutton.cursor())
        self.email2_addbutton.clicked.connect(
            lambda: self.addEmail(
                self.email2_addbutton, 
                self.email2_deletebutton, 
                self.email2_label, 
                self.email2_textbox))
        # Email 2 Delete Button
        self.email2_deletebutton = QPushButton(self.email_box)
        self.email2_deletebutton.setGeometry(QRect(
            self.email1_deletebutton.x(), 
            self.email2_addbutton.y(), 
            self.email1_deletebutton.width(), 
            self.email1_addbutton.height()))
        self.email2_deletebutton.setStyleSheet(self.email1_deletebutton.styleSheet())
        self.email2_deletebutton.setText(self.email1_deletebutton.text())
        self.email2_deletebutton.setCursor(self.email1_deletebutton.cursor())
        self.email2_deletebutton.clicked.connect(
            lambda: self.deleteEmail(
                self.email2_addbutton, 
                self.email2_deletebutton, 
                self.email2_label, 
                self.email2_textbox, 1))
        # Email 2 Label
        self.email2_label = QComboBox(self.email_box)
        self.email2_previouslabel = QLabel()
        self.email2_label.addItems(self.email_labelItems)
        self.email2_label.setGeometry(QRect(
            self.email1_label.x(), 
            self.email2_addbutton.y(), 
            self.email1_label.width(), 
            self.email1_label.height()))
        self.email2_label.setCursor(self.email1_label.cursor())
        self.email2_label.currentIndexChanged.connect(
            lambda: self.addCustomLabel(
                self.email2_label, 
                self.email2_previouslabel))
        # Email 2 Textbox
        self.email2_textbox = QLineEdit(self.email_box)
        self.email2_textbox.setGeometry(QRect(
            self.email1_textbox.x(), 
            self.email2_addbutton.y(), 
            self.email1_textbox.width(), 
            self.email1_textbox.height()))
        self.email2_textbox.setPlaceholderText(self.email1_textbox.placeholderText())
        self.email2_textbox.setValidator(self.email1_textbox.validator())
        self.email2_textbox.setMaxLength(self.email1_textbox.maxLength())
        self.email2_textbox.setVisible(False)

        # SNS Box
        self.sns_box = QGroupBox(self)
        self.sns_box.setGeometry(QRect(
            self.phone_box.x(), 
            self.email_box.y() + self.email_box.height() + 10, 
            self.phone_box.width(), 
            115))
        self.sns_labelKey = ["facebook", "instagram", "twitter", "line", "tiktok", "custom"]
        self.sns_labelItems = []
        for key in self.sns_labelKey:
            self.sns_labelItems.append(lang[key])
        # SNS 1 Add Button
        self.sns1_addbutton = QPushButton(self.sns_box)
        self.sns1_addbutton.resize(150, 25)
        self.sns1_addbutton.move(
            (self.sns_box.width() - self.sns1_addbutton.width()) / 2, 
            15)
        self.sns1_addbutton.setText(lang["add_sns_account"])
        self.sns1_addbutton.setCursor(QCursor(Qt.PointingHandCursor))
        self.sns1_addbutton.clicked.connect(
            lambda: self.addEmail(
                self.sns1_addbutton, 
                self.sns1_deletebutton, 
                self.sns1_label, 
                self.sns1_textbox))
        # SNS 1 Delete Button
        self.sns1_deletebutton = QPushButton(self.sns_box)
        self.sns1_deletebutton.setGeometry(QRect(10, 15, 40, 25))
        self.sns1_deletebutton.setStyleSheet("color: red;")
        self.sns1_deletebutton.setText(lang["delete"])
        self.sns1_deletebutton.setCursor(QCursor(Qt.PointingHandCursor))
        self.sns1_deletebutton.clicked.connect(
            lambda: self.deleteEmail(
                self.sns1_addbutton, 
                self.sns1_deletebutton, 
                self.sns1_label, 
                self.sns1_textbox, 0))
        # SNS 1 Label
        self.sns1_label = QComboBox(self.sns_box)
        self.sns1_previouslabel = QLabel()
        self.sns1_label.addItems(self.sns_labelItems)
        self.sns1_label.setGeometry(QRect(
            self.sns1_deletebutton.x() + self.sns1_deletebutton.width() + 10, 
            self.sns1_addbutton.y(), 
            80, 
            self.sns1_addbutton.height()))
        self.sns1_label.setCursor(QCursor(Qt.PointingHandCursor))
        self.sns1_label.currentIndexChanged.connect(
            lambda: self.addCustomLabel(
                self.sns1_label, 
                self.sns1_previouslabel))
        # SNS 1 Textbox
        self.sns1_textbox = QLineEdit(self.sns_box)
        self.sns1_textbox.setGeometry(QRect(
            self.sns1_label.x() + self.sns1_label.width() + 10, 
            self.sns1_addbutton.y(), 
            self.email1_textbox.width(), 
            self.sns1_addbutton.height()))
        self.sns1_textbox.setPlaceholderText("Frank Lampard")
        self.sns1_textbox.setMaxLength(30)

        # SNS 2 Add Button
        self.sns2_addbutton = QPushButton(self.sns_box)
        self.sns2_addbutton.setGeometry(QRect(
            self.sns1_addbutton.x(), 
            self.sns1_addbutton.y() + self.sns1_addbutton.height() + 5, 
            self.sns1_addbutton.width(), 
            self.email1_addbutton.height()))
        self.sns2_addbutton.setText(self.sns1_addbutton.text())
        self.sns2_addbutton.setCursor(self.sns1_addbutton.cursor())
        self.sns2_addbutton.clicked.connect(
            lambda: self.addEmail(
                self.sns2_addbutton, 
                self.sns2_deletebutton, 
                self.sns2_label, 
                self.sns2_textbox))
        # SNS 2 Delete Button
        self.sns2_deletebutton = QPushButton(self.sns_box)
        self.sns2_deletebutton.setGeometry(QRect(
            self.sns1_deletebutton.x(), 
            self.sns2_addbutton.y(), 
            self.sns1_deletebutton.width(), 
            self.sns1_deletebutton.height()))
        self.sns2_deletebutton.setStyleSheet(self.sns1_deletebutton.styleSheet())
        self.sns2_deletebutton.setText(self.sns1_deletebutton.text())
        self.sns2_deletebutton.setCursor(self.sns1_deletebutton.cursor())
        self.sns2_deletebutton.clicked.connect(
            lambda: self.deleteEmail(
                self.sns2_addbutton, 
                self.sns2_deletebutton, 
                self.sns2_label, 
                self.sns2_textbox, 
                1))
        # SNS 2 Label
        self.sns2_label = QComboBox(self.sns_box)
        self.sns2_previouslabel = QLabel()
        self.sns2_label.addItems(self.sns_labelItems)
        self.sns2_label.setGeometry(QRect(
            self.sns1_label.x(), 
            self.sns2_addbutton.y(), 
            self.sns1_label.width(), 
            self.sns1_label.height()))
        self.sns2_label.setCursor(self.email1_label.cursor())
        self.sns2_label.currentIndexChanged.connect(
            lambda: self.addCustomLabel(
                self.sns2_label, 
                self.sns2_previouslabel))
        # SNS 2 Textbox
        self.sns2_textbox = QLineEdit(self.sns_box)
        self.sns2_textbox.setGeometry(QRect(
            self.sns1_textbox.x(), 
            self.sns2_addbutton.y(), 
            self.sns1_textbox.width(), 
            self.sns1_textbox.height()))
        self.sns2_textbox.setPlaceholderText("Didier Drogba")
        self.sns2_textbox.setMaxLength(self.sns1_textbox.maxLength())

        # SNS 3 Add Button
        self.sns3_addbutton = QPushButton(self.sns_box)
        self.sns3_addbutton.setGeometry(QRect(
            self.sns1_addbutton.x(), 
            self.sns2_addbutton.y() + self.sns2_addbutton.height() + 5, 
            self.sns1_addbutton.width(), 
            self.sns1_addbutton.height()))
        self.sns3_addbutton.setText(self.sns1_addbutton.text())
        self.sns3_addbutton.setCursor(self.sns1_addbutton.cursor())
        self.sns3_addbutton.clicked.connect(
            lambda: self.addEmail(
                self.sns3_addbutton, 
                self.sns3_deletebutton, 
                self.sns3_label, 
                self.sns3_textbox))
        # SNS 3 Delete Button
        self.sns3_deletebutton = QPushButton(self.sns_box)
        self.sns3_deletebutton.setGeometry(QRect(
            self.sns1_deletebutton.x(), 
            self.sns3_addbutton.y(), 
            self.sns1_deletebutton.width(), 
            self.sns1_deletebutton.height()))
        self.sns3_deletebutton.setStyleSheet(self.sns1_deletebutton.styleSheet())
        self.sns3_deletebutton.setText(self.sns1_deletebutton.text())
        self.sns3_deletebutton.setCursor(self.sns1_deletebutton.cursor())
        self.sns3_deletebutton.clicked.connect(
            lambda: self.deleteEmail(
                self.sns3_addbutton, 
                self.sns3_deletebutton, 
                self.sns3_label, 
                self.sns3_textbox, 
                2))
        # SNS 3 Label
        self.sns3_label = QComboBox(self.sns_box)
        self.sns3_previouslabel = QLabel()
        self.sns3_label.addItems(self.sns_labelItems)
        self.sns3_label.setGeometry(QRect(
            self.sns1_label.x(), 
            self.sns3_addbutton.y(), 
            self.sns1_label.width(), 
            self.sns1_label.height()))
        self.sns3_label.setCursor(self.sns1_label.cursor())
        self.sns3_label.setVisible(False)
        self.sns3_label.currentIndexChanged.connect(
            lambda: self.addCustomLabel(
                self.sns3_label, 
                self.sns3_previouslabel))
        # SNS 3 Textbox
        self.sns3_textbox = QLineEdit(self.sns_box)
        self.sns3_textbox.setGeometry(QRect(
            self.sns1_textbox.x(), 
            self.sns3_addbutton.y(), 
            self.sns1_textbox.width(), 
            self.sns1_textbox.height()))
        self.sns3_textbox.setPlaceholderText("Didier Drogba")
        self.sns3_textbox.setMaxLength(self.sns1_textbox.maxLength())

        # Address Box
        self.address_box = QGroupBox(self)
        self.address_box.resize(self.main_width - self.phone_box.width() - 20, 182)
        self.address_box_posX = self.phone_box.x() + self.phone_box.width() + 10
        self.address_box.move(self.address_box_posX, self.phone_box.y())
        self.address_labelKey = ["home", "work", "school", "custom"]
        self.address_labelItems = []
        for key in self.address_labelKey:
            self.address_labelItems.append(lang[key])
        # Address 1 Add Button
        self.address1_addbutton = QPushButton(self.address_box)
        self.address1_addbutton.resize(150, 25)
        self.address1_addbutton.move(
            (self.address_box.width() - self.address1_addbutton.width()) / 2, 
            15)
        self.address1_addbutton.setText(lang["add_address"])
        self.address1_addbutton.setCursor(QCursor(Qt.PointingHandCursor))
        self.address1_addbutton.clicked.connect(
            lambda: self.addAddress(
                addbutton = self.address1_addbutton,
                deletebutton = self.address1_deletebutton,
                label = self.address1_label,
                textbox = self.address1_textbox,
                addbutton2 = self.address2_addbutton,
                deletebutton2 = self.address2_deletebutton,
                label2 = self.address2_label,
                textbox2 = self.address2_textbox))
        # Address 1 Delete Button
        self.address1_deletebutton = QPushButton(self.address_box)
        self.address1_deletebutton.setGeometry(QRect(10, 15, 40, 25))
        self.address1_deletebutton.setStyleSheet("color: red;")
        self.address1_deletebutton.setText(lang["delete"])
        self.address1_deletebutton.setCursor(QCursor(Qt.PointingHandCursor))
        self.address1_deletebutton.clicked.connect(
            lambda: self.deleteAddress(
                addbutton = self.address1_addbutton,
                deletebutton = self.address1_deletebutton,
                label = self.address1_label,
                textbox = self.address1_textbox,
                default_index = 0,
                addbutton2 = self.address2_addbutton,
                deletebutton2 = self.address2_deletebutton,
                label2 = self.address2_label,
                textbox2 = self.address2_textbox))
        # Address 1 Label
        self.address1_label = QComboBox(self.address_box)
        self.address1_previouslabel = QLabel()
        self.address1_label.addItems(self.address_labelItems)
        self.address1_label.setGeometry(QRect(
            self.address1_deletebutton.x() + self.address1_deletebutton.width() + 10, 
            self.address1_deletebutton.y(), 
            80, 
            self.address1_addbutton.height()))
        self.address1_label.setCursor(QCursor(Qt.PointingHandCursor))
        self.address1_label.currentIndexChanged.connect(
            lambda: self.addCustomLabel(
                self.address1_label, 
                self.address1_previouslabel))
        # Address 1 Textbox
        self.address1_textbox = QTextEdit(self.address_box)
        self.address1_textbox.setGeometry(QRect(
            self.address1_label.x() + self.address1_label.width() + 10, 
            self.address1_deletebutton.y(), 
            170, 
            25))
        self.address1_textbox.setPlaceholderText("Street, City, State, Country")
        self.address1_textbox.setAcceptRichText(False)
        self.address1_textbox.textChanged.connect(
            lambda: self.limitAddressLength(self.address1_textbox, 70))

        # Address 2 Add Button
        self.address2_addbutton = QPushButton(self.address_box)
        self.address2_addbutton.setGeometry(QRect(
            self.address1_addbutton.x(), 
            self.address1_textbox.y() + self.address1_textbox.height() + 5, 
            self.address1_addbutton.width(), 
            self.address1_addbutton.height()))
        self.address2_addbutton.setText(self.address1_addbutton.text())
        self.address2_addbutton.setCursor(self.address1_addbutton.cursor())
        self.address2_addbutton.clicked.connect(
            lambda: self.addAddress(
                addbutton = self.address2_addbutton,
                deletebutton = self.address2_deletebutton,
                label = self.address2_label,
                textbox = self.address2_textbox))
        # Address 2 Delete Button
        self.address2_deletebutton = QPushButton(self.address_box)
        self.address2_deletebutton.setGeometry(QRect(
            self.address1_deletebutton.x(), 
            self.address2_addbutton.y(), 
            self.address1_deletebutton.width(), 
            self.address1_deletebutton.height()))
        self.address2_deletebutton.setStyleSheet(self.address1_deletebutton.styleSheet())
        self.address2_deletebutton.setText(self.address1_deletebutton.text())
        self.address2_deletebutton.setCursor(self.address1_deletebutton.cursor())
        self.address2_deletebutton.clicked.connect(
            lambda: self.deleteAddress(
                addbutton = self.address2_addbutton,
                deletebutton = self.address2_deletebutton,
                label = self.address2_label,
                textbox = self.address2_textbox,
                default_index = 1))
        # Address 2 Label
        self.address2_label = QComboBox(self.address_box)
        self.address2_previouslabel = QLabel()
        self.address2_label.addItems(self.address_labelItems)
        self.address2_label.setGeometry(QRect(
            self.address1_label.x(),
            self.address2_addbutton.y(), 
            self.address1_label.width(), 
            self.address1_label.height()))
        self.address2_label.setCursor(self.address1_label.cursor())
        self.address2_label.currentIndexChanged.connect(
            lambda: self.addCustomLabel(
                self.address2_label, 
                self.address2_previouslabel))
        # Address 2 Textbox
        self.address2_textbox = QTextEdit(self.address_box)
        self.address2_textbox.setGeometry(QRect(
            self.address1_textbox.x(), 
            self.address2_addbutton.y(), 
            self.address1_textbox.width(), 
            self.address1_textbox.height()))
        self.address2_textbox.setPlaceholderText(self.address1_textbox.placeholderText())
        self.address2_textbox.setAcceptRichText(False)
        self.address2_textbox.textChanged.connect(
            lambda: self.limitAddressLength(self.address2_textbox, 70))

        # Birthday Box
        self.birthday_box = QGroupBox(self)
        self.birthday_box.setFixedWidth(self.address_box.width())
        self.birthday_box.setStyleSheet("combobox-popup: 0;")
        self.time_now = datetime.datetime.now()
        # Birthday Add Button
        self.birthday_addbutton = QPushButton(self.birthday_box)
        self.birthday_addbutton.setCursor(self.phonenumber1_addbutton.cursor())
        self.birthday_addbutton.resize(150, 25)
        self.birthday_addbutton.move(
            (self.birthday_box.width() - self.birthday_addbutton.width()) / 2, 
            15)
        self.birthday_addbutton.setText(lang["add_birthday"])
        self.birthday_addbutton.clicked.connect(self.addBirthday)
        # Birthday Delete Button
        self.birthday_deletebutton = QPushButton(self.birthday_box)
        self.birthday_deletebutton.setCursor(self.phonenumber1_deletebutton.cursor())
        self.birthday_deletebutton.setGeometry(QRect(10, 15, 40, 25))
        self.birthday_deletebutton.setStyleSheet("color: red;")
        self.birthday_deletebutton.setText(lang["delete"])
        self.birthday_deletebutton.clicked.connect(self.deleteBirthday)
        # Birthday Year
        self.birthday_year = QComboBox(self.birthday_box)
        self.birthday_year_labelItems = []
        for i in range(1940, self.time_now.year):
            self.birthday_year_labelItems.append(str(i))
        self.birthday_year_labelItems.reverse()
        self.birthday_year.addItem(lang["year"])
        self.birthday_year.addItems(self.birthday_year_labelItems)
        self.birthday_year.setMaxVisibleItems(15)
        self.birthday_year.setGeometry(QRect(
            self.birthday_deletebutton.x() + self.birthday_deletebutton.width() + 10, 
            self.birthday_deletebutton.y(), 
            80, 
            25))
        self.birthday_year.setCursor(QCursor(Qt.PointingHandCursor))
        self.birthday_year.currentIndexChanged.connect(self.isSelectedYear)
        self.birthday_year.currentIndexChanged.connect(self.setVisibleDay)
        # Birthday Month
        self.birthday_month = QComboBox(self.birthday_box)
        self.birthday_month_labelItems = []
        for i in range(1, 14):
            self.birthday_month_labelItems.append(lang["month"][i-1])
        self.birthday_month.addItems(self.birthday_month_labelItems)
        self.birthday_month.setMaxVisibleItems(15)
        self.birthday_month.setGeometry(QRect(
            self.birthday_year.x() + self.birthday_year.width() + 10, 
            self.birthday_year.y(), 
            90, 
            self.birthday_year.height()))
        self.birthday_month.setCursor(self.birthday_year.cursor())
        self.birthday_month.activated.connect(self.setVisibleDay)
        # Birthday Day
        self.birthday_day = QComboBox(self.birthday_box)
        self.birthday_day_labelItems = []
        for i in range(1, 32):
            self.birthday_day_labelItems.append(str(i))
        self.birthday_day.addItem(lang["day"])
        self.birthday_day.addItems(self.birthday_day_labelItems)
        self.birthday_day.setMaxVisibleItems(15)
        self.birthday_day.move(
            self.birthday_month.x() + self.birthday_month.width() + 10, 
            self.birthday_year.y())
        self.birthday_day.setFixedSize(
            self.birthday_box.width() - self.birthday_deletebutton.x() - self.birthday_day.x(), 
            self.birthday_year.height())
        self.birthday_day.setCursor(self.birthday_year.cursor())
        # ID Card add button
        self.idcard_addbutton = QPushButton(self.birthday_box)
        self.idcard_addbutton.setText(lang["add_idcard"])
        self.idcard_addbutton.setCursor(self.phonenumber1_addbutton.cursor())
        self.idcard_addbutton.resize(self.phonenumber1_addbutton.size())
        self.idcard_addbutton.move(
            self.birthday_addbutton.x(),
            self.birthday_addbutton.y() + self.birthday_addbutton.height() + 5)
        self.idcard_addbutton.clicked.connect(lambda: self.addPhone(
            self.idcard_label,
            self.idcard_addbutton,
            self.idcard_deletebutton,
            self.idcard_textbox))
        # ID card delete button
        self.idcard_deletebutton = QPushButton(self.birthday_box)
        self.idcard_deletebutton.setStyleSheet(self.birthday_deletebutton.styleSheet())
        self.idcard_deletebutton.setText(self.phonenumber1_deletebutton.text())
        self.idcard_deletebutton.setCursor(self.phonenumber1_deletebutton.cursor())
        self.idcard_deletebutton.resize(self.phonenumber1_deletebutton.size())
        self.idcard_deletebutton.move(
            self.birthday_deletebutton.x(),
            self.idcard_addbutton.y())
        self.idcard_deletebutton.clicked.connect(lambda: self.deletePhone(
            self.idcard_label,
            self.idcard_addbutton,
            self.idcard_deletebutton,
            self.idcard_textbox,
            0))
        # ID card label
        self.idcard_label = QComboBox(self.birthday_box)
        self.idcard_labelKey = ["idcard", "license", "passport", "custom"]
        self.idcard_labelList = []
        for key in self.idcard_labelKey:
            self.idcard_labelList.append(lang[key])
        self.idcard_previouslabel = QLabel()
        self.idcard_label.addItems(self.idcard_labelList)
        self.idcard_label.setCursor(self.phonenumber1_label.cursor())
        self.idcard_label.resize(80, self.idcard_deletebutton.height())
        self.idcard_label.move(
            self.idcard_deletebutton.x() + self.idcard_deletebutton.width() + 10,
            self.idcard_deletebutton.y())
        self.idcard_label.activated.connect(lambda: self.addCustomLabel(
            self.idcard_label,
            self.idcard_previouslabel))
        # ID card textbox
        self.idcard_textbox = QLineEdit(self.birthday_box)
        self.idcard_textbox.setMaxLength(20)
        self.idcard_textbox.setPlaceholderText(lang["idcard_number"])
        self.idcard_textbox.setValidator(QRegExpValidator(QRegExp("^[a-zA-Z0-9]{1,20}$")))
        self.idcard_textbox.move(
            self.idcard_label.x() + self.idcard_label.width() + 10,
            self.idcard_deletebutton.y())
        self.idcard_textbox.setFixedSize(
            self.birthday_day.x() + self.birthday_day.width() - self.idcard_textbox.x(),
            25)
        # Bank Add Button
        self.bank_addbutton = QPushButton(self.birthday_box)
        self.bank_addbutton.setText(lang["add_bank"])
        self.bank_addbutton.setCursor(self.idcard_addbutton.cursor())
        self.bank_addbutton.setFixedSize(self.idcard_addbutton.size())
        self.bank_addbutton.move(
            self.idcard_addbutton.x(),
            self.idcard_addbutton.y() + self.idcard_addbutton.height() + 5)
        self.bank_addbutton.clicked.connect(lambda: self.add_deleteBank("add"))
        # Bank Delete button
        self.bank_deletebutton = QPushButton(self.birthday_box)
        self.bank_deletebutton.setCursor(self.phonenumber1_deletebutton.cursor())
        self.bank_deletebutton.setStyleSheet(self.phonenumber1_deletebutton.styleSheet())
        self.bank_deletebutton.setText(self.phonenumber1_deletebutton.text())
        self.bank_deletebutton.setFixedSize(self.phonenumber1_deletebutton.size())
        self.bank_deletebutton.move(
            self.idcard_deletebutton.x(),
            self.bank_addbutton.y())
        self.bank_deletebutton.clicked.connect(lambda: self.add_deleteBank("delete"))
        # Bank Label
        self.bank_label = QComboBox(self.birthday_box)
        self.bank_labelKey = ["vietcombank", "sacombank", "techcombank", "vietinbank", "bidv", "agribank", "mbbank", "vpbank", "acb", "shb", "yucho", "smbc", "ufj", "minato", "custom"]
        self.bank_labelList = []
        for key in self.bank_labelKey:
            self.bank_labelList.append(lang[key])
        self.bank_previouslabel = QLabel()
        self.bank_label.addItems(self.bank_labelList)
        self.bank_label.setCursor(QCursor(Qt.PointingHandCursor))
        self.bank_label.setFixedSize(
            self.idcard_label.width() + 15,
            self.idcard_label.height())
        self.bank_label.move(
            self.idcard_label.x(),
            self.bank_deletebutton.y())
        # Bank account textbox
        self.bank_account_textbox = QLineEdit(self.birthday_box)
        self.bank_account_textbox.setPlaceholderText(lang["bank_account"])
        self.bank_account_textbox.setValidator(QRegExpValidator(QRegExp("^[0-9]{1,20}$")))
        self.bank_account_textbox.move(
            self.bank_label.x() + self.bank_label.width() + 10,
            self.bank_deletebutton.y())
        self.bank_account_textbox.setFixedSize(
            self.birthday_box.width() - self.bank_deletebutton.x() - self.bank_account_textbox.x(),
            self.phonenumber1_textbox.height())
        # Bank branch textbox
        self.bank_branch_textbox = QTextEdit(self.birthday_box)
        self.bank_branch_textbox.move(
            self.bank_account_textbox.x(),
            self.bank_account_textbox.y() + self.bank_account_textbox.height() + 5)
        self.bank_branch_textbox.setFixedSize(
            self.bank_account_textbox.width(),
            45)
        self.bank_branch_textbox.setPlaceholderText(lang["bank_branch"])
        self.bank_branch_textbox.setAcceptRichText(False)
        self.birthday_box.adjustSize()

        # Note box
        self.note_box = QGroupBox(self)
        self.note_box.setFixedWidth(self.address_box.width())
        self.note_box.move(
            self.address_box.x(),
            self.birthday_box.y() + self.birthday_box.height() + 10)
        self.note_box.setStyleSheet("combobox-popup: 0;")
        # Note textbox
        self.note_textbox = QTextEdit(self.note_box)
        self.note_textbox.setAcceptRichText(False)
        self.note_textbox.setPlaceholderText(lang["note"])
        self.note_textbox.move(10, 10)
        self.note_textbox.setFixedWidth(self.note_box.width() - self.note_textbox.x()*2)
        self.note_textbox.setMinimumHeight(80)
        self.note_textbox.resize(self.note_textbox.width(), 80)
        self.note_textbox.textChanged.connect(lambda: self.limitNoteLength(400))
        self.note_box.adjustSize()


    # Get image from file browser
    def getImage(self):
        self.imageType = "JPEG Files (*.jpg *jpeg);;PNG (*.png)"
        self.imageName, self.imageType = QFileDialog.getOpenFileName(self, "Open", "",  self.imageType)
        if self.imageName != "":
            # Show crop image dialog
            self.crop_image_dialog = CropImageDialog(
                image_path=self.imageName,
                button_text=lang["crop"],
                theme=self.styleSheet())
            if self.crop_image_dialog.exec():
                # Set new photo as pixmap to GUI
                self.picture_path = self.imageName
                self.profile_picture_pixmap = self.crop_image_dialog.getImagePixmap()
                self.profile_picture_pixmap_scaled = self.profile_picture_pixmap.scaled(
                    110, 110,
                    aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
                self.profile_picture.setPixmap(self.profile_picture_pixmap_scaled)
                self.newImage = self.crop_image_dialog.getImage()
                self.path = self.picture_path
        else:
            pass
    # Add phone number
    def addPhone(self, label, addbutton, deletebutton, textbox):
        label.setVisible(True)
        addbutton.setVisible(False)
        deletebutton.setVisible(True)
        textbox.setVisible(True)

    # Delete phone number
    def deletePhone(self, label, addbutton, deletebutton, textbox, default_index):
        label.setVisible(False)
        label.setCurrentIndex(default_index)
        addbutton.setVisible(True)
        deletebutton.setVisible(False)
        textbox.setVisible(False)
        textbox.setText("")

    # Add Custom Phone Label
    def addCustomLabel(self, label, previous_label):
        if label.currentText() == lang["custom"]:
            # Dialog Window
            self.customLabel = QMessageBoxX(
                icon="input",
                boldtext=lang["custom_label"],
                text=lang["custom_label_question"],
                ok=True,
                cancel=True,
                stylesheet=self.styleSheet())
            self.customLabel.setupTextbox(
                placeholder=lang["label_name"],
                maxlength=12)
            if self.customLabel.exec():
                label.addItem(self.customLabel.getText())
                label.setCurrentText(self.customLabel.getText())
            else:
                label.setCurrentIndex(int(previous_label.objectName()))
        previous_label.setObjectName(str(label.currentIndex()))

    # Add Email
    def addEmail(self, addbutton, deletebutton,label, textbox):
        label.setVisible(True)
        addbutton.setVisible(False)
        deletebutton.setVisible(True)
        textbox.setVisible(True)

    # Delete Email
    def deleteEmail(self, addbutton, deletebutton, label, textbox, default_index):
        label.setVisible(False)
        label.setCurrentIndex(default_index)
        addbutton.setVisible(True)
        deletebutton.setVisible(False)
        textbox.setVisible(False)
        textbox.setText("")

    def addAddress(self, addbutton, deletebutton, label, textbox, addbutton2=None, deletebutton2=None, label2=None, textbox2=None):
        label.setVisible(True)
        addbutton.setVisible(False)
        deletebutton.setVisible(True)
        textbox.setVisible(True)
        textbox.setFixedHeight(75)
        try:
            addbutton2.move(addbutton2.x(), textbox.y() + textbox.height() + 5)
            deletebutton2.move(deletebutton2.x(), textbox.y() + textbox.height() + 5)
            label2.move(label2.x(), addbutton2.y())
            textbox2.move(textbox2.x(), addbutton2.y())
        except:
            pass
        self.address_box.adjustSize()
        self.birthday_box.move(
            self.birthday_box.x(),
            self.address_box.y() + self.address_box.height() + 10)
        self.note_box.move(
            self.note_box.x(),
            self.birthday_box.y() + self.birthday_box.height() + 10)
        self.adjustSize()

    # Delete Email
    def deleteAddress(self, addbutton, deletebutton, label, textbox, default_index, addbutton2=None, deletebutton2=None, label2=None, textbox2=None):
        label.setVisible(False)
        label.setCurrentIndex(default_index)
        addbutton.setVisible(True)
        deletebutton.setVisible(False)
        textbox.setText("")
        textbox.setVisible(False)
        textbox.setFixedHeight(25)
        try:
            addbutton2.move(addbutton2.x(), textbox.y() + textbox.height() + 5)
            deletebutton2.move(deletebutton2.x(), textbox.y() + textbox.height() + 5)
            label2.move(label2.x(), addbutton2.y())
            textbox2.move(textbox2.x(), addbutton2.y())
        except:
            pass
        self.address_box.adjustSize()
        self.birthday_box.move(
            self.birthday_box.x(),
            self.address_box.y() + self.address_box.height() + 10)
        self.note_box.move(
            self.note_box.x(),
            self.birthday_box.y() + self.birthday_box.height() + 10)
        self.adjustSize()

    def limitAddressLength(self, addresstext, limit):
        limit = 70
        if len(addresstext.toPlainText()) > limit:
            text = addresstext.toPlainText()
            text = text[:limit]
            addresstext.setText(text)
            cursor = addresstext.textCursor()
            cursor.setPosition(limit)
            addresstext.setTextCursor(cursor)

    def limitNoteLength(self, length):
        if len(self.note_textbox.toPlainText()) > length:
            text = self.note_textbox.toPlainText()
            text = text[:length]
            self.note_textbox.setText(text)
            cursor = self.note_textbox.textCursor()
            cursor.setPosition(length)
            self.note_textbox.setTextCursor(cursor)



    def addBirthday(self):
        self.birthday_addbutton.setVisible(False)
        self.birthday_deletebutton.setVisible(True)
        self.birthday_year.setVisible(True)
        self.birthday_month.setVisible(True)
        self.birthday_day.setVisible(True)

    def deleteBirthday(self):
        self.birthday_addbutton.setVisible(True)
        self.birthday_deletebutton.setVisible(False)
        self.birthday_year.setVisible(False)
        self.birthday_year.setCurrentIndex(0)
        self.birthday_month.setVisible(False)
        self.birthday_month.setEnabled(False)
        self.birthday_month.setCurrentIndex(0)
        self.birthday_day.setVisible(False)
        self.birthday_day.setEnabled(False)
        self.birthday_day.setCurrentIndex(0)

    def isSelectedYear(self):
        year = self.birthday_year.currentIndex()
        if not year:
            self.birthday_month.setDisabled(True)
        else:
            self.birthday_month.setDisabled(False)

    def setVisibleDay(self):
        year = self.birthday_year.currentText()
        month = self.birthday_month.currentIndex()
        # Check if month has been selected
        if self.birthday_month.currentIndex() == 0:
            self.birthday_day.setDisabled(True)
        else:
            self.birthday_day.setDisabled(False)
            self.birthday_day.clear()
            self.birthday_day.addItem(lang["day"])
            self.birthday_day_labelItems.clear()
            # Change day list item depend on selected month
            # Check selected month and leap year
            if self.birthday_month.currentIndex() == 2:
                for i in range(1, 29):
                    self.birthday_day.addItem(str(i))
                if int(year) % 4 == 0:
                    self.birthday_day.addItem("29")
            else:
                for i in range(1, 31):
                    self.birthday_day.addItem(str(i))
                month31 = [1, 3, 5, 7, 8, 10, 12]
                if month in month31:
                    self.birthday_day.addItem("31")

    def add_deleteBank(self, mode):
        if mode == "add":
            self.bank_addbutton.setVisible(False)
            self.bank_deletebutton.setVisible(True)
            self.bank_label.setVisible(True)
            self.bank_account_textbox.setVisible(True)
            self.bank_branch_textbox.setVisible(True)
            self.bank_branch_textbox.move(
                self.bank_account_textbox.x(),
                self.bank_account_textbox.y() + self.bank_account_textbox.height() + 5)
            self.bank_branch_textbox.setFixedSize(
                self.bank_account_textbox.width(),
                45)
        else:
            self.bank_addbutton.setVisible(True)
            self.bank_deletebutton.setVisible(False)
            self.bank_label.setVisible(False)
            self.bank_account_textbox.setVisible(False)
            self.bank_branch_textbox.setVisible(False)
        self.birthday_box.adjustSize()
        self.note_box.move(
            self.note_box.x(),
            self.birthday_box.y() + self.birthday_box.height() + 10)
        self.adjustSize()
        
    
    def showUpContent(self):
        self.datafile_row = self.row
        # Check if profile picture is set, if not, set default picture
        if self.mode == 0 or user.getContactData(self.datafile_row, "picture") == None:
            self.profile_picture_pixmap_scaled = QPixmap(self.defaultPicture_path)
            self.path = self.defaultPicture_path
        else:
            self.picture_path = "./data/{0}/profile_pictures/{1}".format(
                user.getData("username"), 
                user.getContactData(self.datafile_row, "picture"))
            self.old_path = self.picture_path
            self.profile_picture_pixmap = QPixmap(self.picture_path)
            self.profile_picture_pixmap_scaled = self.profile_picture_pixmap.scaled(
                110, 110,
                transformMode=Qt.SmoothTransformation)
            self.path = self.picture_path
        self.profile_picture.setPixmap(self.profile_picture_pixmap_scaled)
        self.fullname.setText(user.getContactData(self.datafile_row, "fullname"))
        self.nickname.setText(user.getContactData(self.datafile_row, "nickname"))
        self.company.setText(user.getContactData(self.datafile_row, "company"))
        self.jobtitle.setText(user.getContactData(self.datafile_row, "jobtitle"))
        if self.mode == 0:
            self.save_button.clicked.connect(lambda: self.saveContactData())
        elif self.mode == 1:
            self.save_button.clicked.connect(lambda: self.saveContactData())
        # Showing Field Which Has Label Content Function
        def fieldContent(addbutton, deletebutton, label, textbox, default_index, previous_label, label_data, data, textbox_additional_height = 25):
            if self.mode == 0 or data == None or data == "":
                addbutton.setVisible(True)
                deletebutton.setVisible(False)
                label.setVisible(False)
                textbox.setVisible(False)
                label.setCurrentIndex(default_index)
            else:
                addbutton.setVisible(False)
                deletebutton.setVisible(True)
                label.setVisible(True)
                textbox.setVisible(True)
                textbox.setFixedHeight(textbox_additional_height)
                if not label_data:
                    label.setCurrentIndex(default_index)
                else:
                    # Check if label's language text exists
                    try:
                        labeltext = lang[label_data]
                        label.setCurrentText(labeltext)
                    # If label's language text not exist, add this label as custom label
                    except KeyError:
                        labeltext = label_data
                        label.addItem(labeltext)
                        label.setCurrentText(labeltext)
                textbox.setText(str(data))
            previous_label.setObjectName(str(label.currentIndex()))
        fieldContent(
            addbutton = self.phonenumber1_addbutton,
            deletebutton = self.phonenumber1_deletebutton,
            label = self.phonenumber1_label,
            textbox = self.phonenumber1_textbox,
            default_index = 0,
            previous_label = self.phonenumber1_previouslabel,
            label_data = user.getContactData(self.datafile_row, "phone1_label"),
            data = user.getContactData(self.datafile_row, "phone1"))
        fieldContent(
            addbutton = self.phonenumber2_addbutton,
            deletebutton = self.phonenumber2_deletebutton,
            label = self.phonenumber2_label,
            textbox = self.phonenumber2_textbox,
            default_index = 1,
            previous_label = self.phonenumber2_previouslabel,
            label_data = user.getContactData(self.datafile_row, "phone2_label"),
            data = user.getContactData(self.datafile_row, "phone2"))
        fieldContent(
            addbutton = self.phonenumber3_addbutton,
            deletebutton = self.phonenumber3_deletebutton,
            label = self.phonenumber3_label,
            textbox = self.phonenumber3_textbox,
            default_index = 2,
            previous_label = self.phonenumber3_previouslabel,
            label_data = user.getContactData(self.datafile_row, "phone3_label"),
            data = user.getContactData(self.datafile_row, "phone3"))
        fieldContent(
            addbutton = self.phonenumber4_addbutton,
            deletebutton = self.phonenumber4_deletebutton,
            label = self.phonenumber4_label,
            textbox = self.phonenumber4_textbox,
            default_index = 3,
            previous_label = self.phonenumber4_previouslabel,
            label_data = user.getContactData(self.datafile_row, "phone4_label"),
            data = user.getContactData(self.datafile_row, "phone4"))
        fieldContent(
            addbutton = self.email1_addbutton,
            deletebutton = self.email1_deletebutton,
            label = self.email1_label,
            textbox = self.email1_textbox,
            default_index = 0,
            previous_label = self.email1_previouslabel,
            label_data = user.getContactData(self.datafile_row, "email1_label"),
            data = user.getContactData(self.datafile_row, "email1"))
        fieldContent(
            addbutton = self.email2_addbutton,
            deletebutton = self.email2_deletebutton,
            label = self.email2_label,
            textbox = self.email2_textbox,
            default_index = 1,
            previous_label = self.email2_previouslabel,
            label_data = user.getContactData(self.datafile_row, "email2_label"),
            data = user.getContactData(self.datafile_row, "email2"))
        fieldContent(
            addbutton = self.sns1_addbutton,
            deletebutton = self.sns1_deletebutton,
            label = self.sns1_label,
            textbox = self.sns1_textbox,
            default_index = 0,
            previous_label = self.sns1_previouslabel,
            label_data = user.getContactData(self.datafile_row, "sns1_label"),
            data = user.getContactData(self.datafile_row, "sns1"))
        fieldContent(
            addbutton = self.sns2_addbutton,
            deletebutton = self.sns2_deletebutton,
            label = self.sns2_label,
            textbox = self.sns2_textbox,
            default_index = 1,
            previous_label = self.sns2_previouslabel,
            label_data = user.getContactData(self.datafile_row, "sns2_label"),
            data = user.getContactData(self.datafile_row, "sns2"))
        fieldContent(
            addbutton = self.sns3_addbutton,
            deletebutton = self.sns3_deletebutton,
            label = self.sns3_label,
            textbox = self.sns3_textbox,
            default_index = 0,
            previous_label = self.sns3_previouslabel,
            label_data = user.getContactData(self.datafile_row, "sns3_label"),
            data = user.getContactData(self.datafile_row, "sns3"))
        fieldContent(
            addbutton = self.address1_addbutton,
            deletebutton = self.address1_deletebutton,
            label = self.address1_label,
            textbox = self.address1_textbox,
            default_index = 0,
            previous_label = self.address1_previouslabel,
            label_data = user.getContactData(self.datafile_row, "address1_label"),
            data = user.getContactData(self.datafile_row, "address1"),
            textbox_additional_height = 55)
        fieldContent(
            addbutton = self.address2_addbutton,
            deletebutton = self.address2_deletebutton,
            label = self.address2_label,
            textbox = self.address2_textbox,
            default_index = 1,
            previous_label = self.address2_previouslabel,
            label_data = user.getContactData(self.datafile_row, "address2_label"),
            data = user.getContactData(self.datafile_row, "address2"),
            textbox_additional_height = 55)
        # Update Address 2 fields' positions
        self.address2_addbutton.move(
            self.address1_addbutton.x(), 
            self.address1_textbox.y() + self.address1_textbox.height() + 5)
        self.address2_deletebutton.move(
            self.address1_deletebutton.x(),
            self.address2_addbutton.y())
        self.address2_label.move(
            self.address1_label.x(),
            self.address2_addbutton.y())
        self.address2_textbox.move(
            self.address1_textbox.x(),
            self.address2_addbutton.y())
        self.address_box.adjustSize()
        # Birthday box
        # Birthday
        if self.mode == 0 or user.getContactData(self.datafile_row, "year") == None:
                self.birthday_addbutton.setVisible(True)
                self.birthday_deletebutton.setVisible(False)
                self.birthday_year.setVisible(False)
                self.birthday_month.setVisible(False)
                self.birthday_day.setVisible(False)
                self.birthday_year.setCurrentIndex(0)
                self.birthday_month.setCurrentIndex(0)
                self.birthday_day.setCurrentIndex(0)
                self.birthday_month.setDisabled(True)
                self.birthday_day.setDisabled(True)
        else:
            self.birthday_addbutton.setVisible(False)
            self.birthday_deletebutton.setVisible(True)
            self.birthday_year.setVisible(True)
            self.birthday_month.setVisible(True)
            self.birthday_day.setVisible(True)
            self.birthday_year.setCurrentText(str(user.getContactData(self.datafile_row, "year")))
            if self.mode == 0 or user.getContactData(self.datafile_row, "month") == None:
                self.birthday_month.setCurrentIndex(0)
                self.birthday_day.setDisabled(True)
            else:
                self.birthday_month.setCurrentIndex(int(user.getContactData(self.datafile_row, "month")))
                self.birthday_day.setDisabled(False)
                if self.mode == 0 or user.getContactData(self.datafile_row, "day") == None:
                    self.birthday_day.setCurrentIndex(0)
                else:
                    self.birthday_day.setCurrentIndex(int(user.getContactData(self.datafile_row, "day")))
        # ID Card
        fieldContent(
            addbutton = self.idcard_addbutton,
            deletebutton = self.idcard_deletebutton,
            label = self.idcard_label,
            textbox = self.idcard_textbox,
            default_index = 0,
            previous_label = self.idcard_previouslabel,
            label_data = user.getContactData(self.datafile_row, "idcard_label"),
            data = user.getContactData(self.datafile_row, "idcard"))
        self.birthday_box.move(
            self.address_box.x(), 
            self.address_box.y() + self.address_box.height() + 10)
        # Bank
        if not self.mode or (not user.getContactData(self.datafile_row, "bank") and not user.getContactData(self.datafile_row, "bank_branch")):
            self.bank_addbutton.setVisible(True)
            self.bank_deletebutton.setVisible(False)
            self.bank_label.setVisible(False)
            self.bank_label.setCurrentIndex(0)
            self.bank_account_textbox.setVisible(False)
            self.bank_account_textbox.clear()
            self.bank_branch_textbox.setVisible(False)
            self.bank_branch_textbox.clear()
            self.bank_branch_textbox.move(self.bank_account_textbox.pos())
            self.bank_branch_textbox.setFixedSize(self.bank_account_textbox.size())
        else:
            self.bank_addbutton.setVisible(False)
            self.bank_deletebutton.setVisible(True)
            self.bank_label.setVisible(True)
            self.bank_label.setCurrentIndex(0)
            self.bank_account_textbox.setVisible(True)
            self.bank_branch_textbox.setVisible(True)
            self.bank_branch_textbox.move(
                self.bank_account_textbox.x(),
                self.bank_account_textbox.y() + self.bank_account_textbox.height() + 5)
            self.bank_branch_textbox.setFixedSize(
                self.bank_account_textbox.width(),
                45)
            if not user.getContactData(self.datafile_row, "bank_label"):
                self.bank_label.setCurrentText(0)
            else:
                try:
                    labeltext = lang[user.getContactData(self.datafile_row, "bank_label")]
                    self.bank_label.setCurrentText(labeltext)
                except KeyError:
                    labeltext = user.getContactData(self.datafile_row, "bank_label")
                    self.bank_label.addItem(labeltext)
                    self.bank_label.setCurrentText(labeltext)
            self.bank_account_textbox.setText(str(user.getContactData(self.datafile_row, "bank")))
            self.bank_branch_textbox.setText(str(user.getContactData(self.datafile_row, "bank_branch")))
        self.bank_previouslabel.setObjectName(str(self.bank_label.currentIndex()))
        self.birthday_box.adjustSize()

        # Note box
        self.note_textbox.setText(user.getContactData(self.datafile_row, "note"))
        self.note_box.move(
            self.address_box.x(),
            self.birthday_box.y() + self.birthday_box.height() + 10)
        self.adjustSize()

    def saveContactData(self):
        # Check contact fullname field. If field is empty, request to check again
        if not self.fullname.text() or self.fullname.text() == "":
            self.message = QMessageBoxX(
                icon = "warning",
                boldtext = "Invalidated full name",
                text = "Your full namme is empty! Please fill in a validated full name",
                stylesheet=self.styleSheet())
            self.message.exec()
        else:
            user.setContactData(self.row, "fullname", self.fullname.text())
            # If in creating mode, create new ID
            # Only save ID in creating mode
            if self.mode == 0:
                # Get ID from previous row, if this is the first row, ID = 1
                if self.row == 6:
                    self.id = 1
                else:
                    self.id = int(user.getContactData(self.row - 2, "id")) + 1
                user.setContactData(self.row, "id", self.id)
                
            # Check if picture has been set, if picture has not been set, write "None" value.
            if self.path == self.defaultPicture_path:
                user.setContactData(self.row, "picture", None)
            # Check if picture has been changed, if picture has been changed, copy and write new picture name.
            elif self.path != self.old_path:
                # Get photo
                self.newImage = self.crop_image_dialog.getImage()
                # Set picture name by contact ID
                self.pictureName = str(user.getContactData(self.row, "id")) + ".jpg"
                # Save new picture under random name
                self.newImage_path = self.picturefolder_path + self.pictureName
                self.newImage.save(self.newImage_path)
                # Write new image name to data file
                user.setContactData(self.row, "picture", os.path.basename(self.newImage_path))

            # Check if textbox is null before saving label data
            def checkTextbox(data_field, label, textvalue, labelkey, custom_index):
                if not textvalue:
                    user.setContactData(self.row, data_field, None)
                elif label.currentIndex() < custom_index:
                    user.setContactData(self.row, data_field, labelkey[label.currentIndex()])
                else:
                    user.setContactData(self.row, data_field, label.currentText())
            # Name
            user.setContactData(self.row, "nickname", self.nickname.text())
            user.setContactData(self.row, "company", self.company.text())
            user.setContactData(self.row, "jobtitle", self.jobtitle.text())
            # Phone
            user.setContactData(self.row, "phone1", self.phonenumber1_textbox.text())
            user.setContactData(self.row, "phone2", self.phonenumber2_textbox.text())
            user.setContactData(self.row, "phone3", self.phonenumber3_textbox.text())
            user.setContactData(self.row, "phone4", self.phonenumber4_textbox.text())
            checkTextbox("phone1_label", self.phonenumber1_label, self.phonenumber1_textbox.text(), self.phonenumber_labelKey, 4)
            checkTextbox("phone2_label", self.phonenumber2_label, self.phonenumber2_textbox.text(), self.phonenumber_labelKey, 4)
            checkTextbox("phone3_label", self.phonenumber3_label, self.phonenumber3_textbox.text(), self.phonenumber_labelKey, 4)
            checkTextbox("phone4_label", self.phonenumber4_label, self.phonenumber4_textbox.text(), self.phonenumber_labelKey, 4)
            # Email
            user.setContactData(self.row, "email1", self.email1_textbox.text())
            user.setContactData(self.row, "email2", self.email2_textbox.text())
            checkTextbox("email1_label", self.email1_label, self.email1_textbox.text(), self.email_labelKey, 3)
            checkTextbox("email2_label", self.email2_label, self.email2_textbox.text(), self.email_labelKey, 3)
            # SNS
            user.setContactData(self.row, "sns1", self.sns1_textbox.text())
            user.setContactData(self.row, "sns2", self.sns2_textbox.text())
            user.setContactData(self.row, "sns3", self.sns3_textbox.text())
            checkTextbox("sns1_label", self.sns1_label, self.sns1_textbox.text(), self.sns_labelKey, 5)
            checkTextbox("sns2_label", self.sns2_label, self.sns2_textbox.text(), self.sns_labelKey, 5)
            checkTextbox("sns3_label", self.sns3_label, self.sns3_textbox.text(), self.sns_labelKey, 5)

            # Address
            user.setContactData(self.row, "address1", self.address1_textbox.toPlainText())
            user.setContactData(self.row, "address2", self.address2_textbox.toPlainText())
            checkTextbox("address1_label", self.address1_label, self.address1_textbox.toPlainText(), self.address_labelKey, 3)
            checkTextbox("address2_label", self.address2_label, self.address2_textbox.toPlainText(), self.address_labelKey, 3)

            # Check birthday
            # Year
            if self.birthday_year.currentIndex() != 0:
                user.setContactData(self.row, "year", self.birthday_year.currentText())
            else:
                user.setContactData(self.row, "year", None)
            # Month
            if self.birthday_month.currentIndex() != 0:
                user.setContactData(self.row, "month", self.birthday_month.currentIndex())
            else:
                user.setContactData(self.row, "month", None)
            # Day
            if self.birthday_day.currentIndex() != 0:
                user.setContactData(self.row, "day", self.birthday_day.currentIndex())
            else:
                user.setContactData(self.row, "day", None)
            # ID Card
            user.setContactData(self.row, "idcard", self.idcard_textbox.text())
            checkTextbox("idcard_label", self.idcard_label, self.idcard_textbox.text(), self.idcard_labelKey, 3)
            # Bank
            user.setContactData(self.row, "bank", self.bank_account_textbox.text())
            user.setContactData(self.row, "bank_branch", self.bank_branch_textbox.toPlainText().replace("\n", ""))
            checkTextbox("bank_label", self.bank_label, self.bank_account_textbox.text(), self.bank_labelKey, 13)
            # Note
            user.setContactData(self.row, "note", self.note_textbox.toPlainText())
            # Write all data to the data file
            try:
                user.saveData()
                self.save = 1
                self.close()
            except PermissionError:
                self.message = QMessageBoxX(
                    icon = "warning",
                    boldtext=lang["permission_denied"],
                    text=lang["permission_denied_description"],
                    stylesheet=self.styleSheet())
                self.message.exec()

    def closeEvent(self, event):
        def afterClose():
            # Get contact list current item if any item in the list is selected
            if self.parent().parent().parent().parent().contact_list.currentItem() != None:
                currentItem = self.parent().parent().parent().parent().contact_list.currentRow()
            # Clear current list and setup new list
            self.parent().parent().parent().parent().contact_list.clear()
            user.setupContactList(self.parent().parent().parent().parent().contact_list)
            # If there is any item in the list which is selected before clearing, show that item
            try:
                self.parent().parent().parent().parent().contact_list.setCurrentRow(currentItem)
                self.parent().parent().parent().parent().showContactContent()
            except UnboundLocalError:
                pass
            try:
                self.parent().parent().parent().parent().history[-2].show()
                self.parent().parent().parent().parent().history[-2].raise_()
                del self.parent().parent().parent().parent().history[-1]
            except:
                pass
            if not len(self.parent().parent().parent().parent().history):
                self.parent().parent().parent().parent().back_button.setDisabled(True)
            else:
                self.parent().parent().parent().parent().back_button.setDisabled(False)
            self.parent().parent().close()
        # Warning when switch to another widget (not clicking the save button)
        if self.save == 0:
            # Show warning when fullname textbox is not empty
            if self.fullname.text():
                # Show warning message
                warning = QMessageBoxX(
                    icon="warning",
                    boldtext=lang["warning"],
                    text=lang["close_without_saving"],
                    ok=True,
                    cancel=True,
                    stylesheet=self.styleSheet())
                if not warning.exec():
                    event.ignore()
                else:
                    event.accept()
                    afterClose()
            # If fullname box is empty, close without warning message
            else:
                event.accept()
                afterClose()
        # Notification after save contact to file
        else:
            information = QMessageBoxX(
                icon = "information",
                boldtext = lang["saved_successfully"],
                text = lang["saved_successfully_description"],
                stylesheet=self.styleSheet())
            information.exec()
            self.parent().parent().close()
        # Update contact box content (in case old content before changing is still being showed)
        if self.mode != 0:
            self.parent().parent().parent().parent().showContactContent()
        # Update contact list on the sidebar
        user.setupContactList(self.parent().parent().parent().parent().contact_list) 
        