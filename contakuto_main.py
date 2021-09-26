import sys
import os
import openpyxl as xl
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import contakuto_stylesheet as style
import contakuto_login as login
import contakuto_edit_create_contact
import contakuto_usersettings
from contakuto_basegui import *
from data_class import *
from lang import *

class MainUI(QMainWindowX):
    def __init__(self, parent=None):
        super().__init__(self)
        self.langvalue = user.getData("language")
        self.lang = lang[self.langvalue]
        self.theme = user.getData("theme")
        self.setWindowTitle(self.lang["contakuto"])
        if self.theme == "light":
            self.setStyleSheet(style.basegui)
        else:
            self.setStyleSheet(style.basegui_darktheme)
            self.shadow.setBlurRadius(20)
            self.shadow.setOffset(0, 5)
            self.pfshadow.setColor(QColor(0, 0, 0))
        self.container.setFixedSize(960, 620)
        self.titlebar.setText(self.lang["contakuto"])
        super().settingInterface(lang=self.lang)
        self.datafile_row = 6
        self.main_directory = os.path.dirname(__file__)

        # Titlebar Button
        self.add_button.clicked.connect(self.CreateContact)
        self.search_button.clicked.connect(self.showSearchBox)
        self.profile_button.setText(user.getData("fullname"))
        self.contacts_button.clicked.connect(self.showContactBox)
        self.edit_profile_button.clicked.connect(self.userSettingsWidget)
        self.signout_button.clicked.connect(self.signOut)

        # Searchbox
        self.searchbox = QLineEdit(self.sidebar)
        self.searchbox.setObjectName("searchbox")
        self.searchbox.setPlaceholderText(self.lang["search"])
        self.searchbox.setFixedSize(self.sidebar.width() - 1, 0)
        self.searchbox.move(0, 0)
        self.searchbox_shadow = QGraphicsDropShadowEffect()
        self.searchbox_shadow.setBlurRadius(15)
        self.searchbox_shadow.setOffset(0, 1)
        self.searchbox.setGraphicsEffect(self.searchbox_shadow)
        self.searchbox.textChanged.connect(self.searchContacts)

        self.search_clear = QPushButton(self.searchbox)
        self.search_clear.setObjectName("search_clear")
        self.search_clear.setCursor(QCursor(Qt.PointingHandCursor))
        self.search_clear.setVisible(False)
        self.search_clear.setFixedSize(14, 14)
        self.search_clear.move(
            self.searchbox.width() - self.search_clear.width() - 5,
            (30 - self.search_clear.height()) / 2)
        self.search_clear.clicked.connect(self.searchClear)

        # Profile picture
        if user.getData("picture") != None and user.getData("picture") != "":
            self.pfpic = QPixmap("./data/{0}/profile_pictures/{1}".format(
                user.getData("username"), 
                user.getData("picture")))
            self.pfpic_scaled = self.pfpic.scaled(
                self.profile_picture.width(), 
                self.profile_picture.height(), 
                aspectRatioMode=Qt.IgnoreAspectRatio, 
                transformMode=Qt.SmoothTransformation)
        else:
            self.pfpic = QPixmap("./image/default_avatar.png")
            self.pfpic_scaled = self.pfpic.scaled(
                self.profile_picture.width(), 
                self.profile_picture.height(), 
                aspectRatioMode=Qt.IgnoreAspectRatio, 
                transformMode=Qt.SmoothTransformation)
        rounded = QPixmap(self.pfpic_scaled.size())
        rounded.fill(QColor("transparent"))
        # Create rounded picture
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(self.pfpic_scaled))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(
            self.pfpic_scaled.rect(),
            self.profile_picture.width() / 2,
            self.profile_picture.height() / 2)
        self.profile_picture.setPixmap(rounded)
        painter.end()
        del painter
        del rounded

        # Profile name
        self.profile_fullname.setText(user.getData("fullname"))
        self.profile_username.setText("@" + user.getData("username"))

        # Contact list
        self.contact_list = QListWidget(self.sidebar)
        self.contact_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.contact_list.setGeometry(QRect(0, 0, self.sidebar.width() - 3, self.sidebar.height()))
        user.setupContactList(self.contact_list)
        self.contact_list.itemClicked.connect(self.showContactContent)

        # Introduction widget
        self.intro_widget = QLabel(self.container)
        self.intro_widget.setObjectName("intro_widget")
        self.intro_widget.setAlignment(Qt.AlignCenter)
        self.intro_widget.setFixedSize(
            self.container.width() - self.sidebar.width() - 2,
            200)
        self.intro_widget.move(
            self.sidebar.width(),
            (self.container.height() - self.titlebar.height() - self.intro_widget.height()) / 2)
        self.intro_widget.setText("""
            <span style="font-size: 40px; line-height: 60px; font-weight: bold">CONTAKUTO</span><br/>
            <span style="font-size: 30px; line-height: 40px;">The Contact App</span><br/>
            <span style="font-size: 20px; line-height: 28px;">Version 1.0</span><br/>
            <p style="font-size: 15px; line-height: 25px;">A lilte gift for ya, mommy!</p>
        """)

        # Contact content scroll widget
        self.contact_box_scroll = QScrollArea(self.container)
        self.contact_box_scroll.setObjectName("contact_box_scroll")
        self.contact_box_scroll.setVisible(False)
        self.contact_box_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.contact_box_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.contact_box_scroll.setFixedSize(
            self.container.width() - self.sidebar.width() - 2,
            self.container.height() - self.titlebar.height() - 1)
        self.contact_box_scroll.move(self.sidebar.width() + 1, self.titlebar.height())
        self.contact_box_scroll.setAutoFillBackground(False)
        # Contact box
        self.contact_box = QWidget()
        self.contact_box.setObjectName("contact_box")
        self.contact_box.setFixedWidth(self.container.width() - self.sidebar.width() - 2)
        self.contact_box.setMinimumHeight(self.container.height() - self.titlebar.height() - 2)
        self.contact_box_scroll.setWidget(self.contact_box)

        # Contact Name Box
        self.contact_name_box = QWidget(self.contact_box)
        self.contact_name_box.setObjectName("contact_name_box")
        self.contact_name_box.setGeometry(QRect(
            40,
            20,
            self.contact_box.width() - 80,
            150))
        self.contact_name_box.setVisible(False)

        # Contact profile picture
        self.contact_profile_picture = QLabel(self.contact_name_box)
        self.contact_profile_picture.setFixedSize(99, 99)
        self.contact_profile_picture.move(25, 25)
        self.contact_picture = QPixmap("{0}/data/{1}/profile_pictures/danquynh.jpg".format(
            self.main_directory, 
            user.getData("username")))
        self.contact_picture_scaled = self.contact_picture.scaled(
            self.contact_profile_picture.width(), 
            self.contact_profile_picture.height(), 
            aspectRatioMode=Qt.IgnoreAspectRatio, 
            transformMode=Qt.SmoothTransformation)
        self.contact_profile_picture.setPixmap(self.contact_picture_scaled)
        # Contact Fullname
        self.contact_fullname = QLabel(self.contact_name_box)
        self.contact_fullname.setObjectName("contact_fullname")
        self.contact_fullname.setGeometry(QRect(
            self.contact_profile_picture.x() + self.contact_profile_picture.width() + 30, 
            self.contact_profile_picture.y() + 7,
            250, 
            25))
        self.contact_fullname.setAlignment(Qt.AlignLeft)
        self.contact_fullname.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.contact_fullname.setCursor(QCursor(Qt.PointingHandCursor))
        # Contact Nickname
        self.contact_nickname = QLabel(self.contact_name_box)
        self.contact_nickname.setObjectName("contact_nickname")
        self.contact_nickname.setCursor(self.contact_fullname.cursor())
        self.contact_nickname.setGeometry(QRect(
            self.contact_fullname.x(), 
            self.contact_fullname.y() + self.contact_fullname.height(), 
            self.contact_fullname.width(), 
            20))
        self.contact_nickname.setAlignment(self.contact_fullname.alignment())
        # Contact Company
        self.contact_company = QLabel(self.contact_name_box)
        self.contact_company.setGeometry(QRect(
            self.contact_fullname.x(), 
            self.contact_nickname.y() + self.contact_nickname.height(), 
            self.contact_fullname.width(), 
            20))
        self.contact_company.setCursor(self.contact_fullname.cursor())
        self.contact_company.setAlignment(self.contact_fullname.alignment())
        # Contact Job Title
        self.contact_jobtitle = QLabel(self.contact_name_box)
        self.contact_jobtitle.setGeometry(QRect(
            self.contact_fullname.x(), 
            self.contact_company.y() + self.contact_company.height(), 
            self.contact_fullname.width(), 
            20))
        self.contact_jobtitle.setCursor(self.contact_fullname.cursor())
        self.contact_jobtitle.setAlignment(self.contact_fullname.alignment())
        # Phone Button
        self.contact_phone_button = QPushButton(self.contact_name_box)
        self.contact_phone_button.setObjectName("contact_phone_button")
        self.contact_phone_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.contact_phone_button.setFixedSize(30, 30)
        self.contact_phone_button.move(
            self.contact_fullname.x() + self.contact_fullname.width() + 15,
            self.contact_fullname.y())
        self.contact_phone_button.clicked.connect(self.unavailabeFeature)
        # Message Button
        self.contact_message_button = QPushButton(self.contact_name_box)
        self.contact_message_button.setObjectName("contact_message_button")
        self.contact_message_button.setCursor(self.contact_phone_button.cursor())
        self.contact_message_button.setFixedSize(
            self.contact_phone_button.width(),
            self.contact_phone_button.height())
        self.contact_message_button.move(
            self.contact_phone_button.x() + self.contact_phone_button.width() + 5,
            self.contact_phone_button.y())
        self.contact_message_button.clicked.connect(self.unavailabeFeature)
        # Facetime Button
        self.contact_facetime_button = QPushButton(self.contact_name_box)
        self.contact_facetime_button.setObjectName("contact_facetime_button")
        self.contact_facetime_button.setCursor(self.contact_phone_button.cursor())
        self.contact_facetime_button.setFixedSize(
            self.contact_phone_button.width(),
            self.contact_phone_button.height())
        self.contact_facetime_button.move(
            self.contact_message_button.x() + self.contact_message_button.width() + 5,
            self.contact_phone_button.y())
        self.contact_facetime_button.clicked.connect(self.unavailabeFeature)
        # Email Button
        self.contact_email_button = QPushButton(self.contact_name_box)
        self.contact_email_button.setObjectName("contact_email_button")
        self.contact_email_button.setCursor(self.contact_phone_button.cursor())
        self.contact_email_button.setFixedSize(
            self.contact_phone_button.width(),
            self.contact_phone_button.height())
        self.contact_email_button.move(
            self.contact_facetime_button.x() + self.contact_facetime_button.width() + 5,
            self.contact_phone_button.y())
        # Facebook Button
        self.contact_facebook_button = QPushButton(self.contact_name_box)
        self.contact_facebook_button.setObjectName("contact_facebook_button")
        self.contact_facebook_button.setCursor(self.contact_phone_button.cursor())
        self.contact_facebook_button.setFixedSize(
            self.contact_phone_button.width(),
            self.contact_phone_button.height())
        self.contact_facebook_button.move(
            self.contact_phone_button.x(),
            self.contact_phone_button.y() + self.contact_phone_button.height() + 5)
        # Twitter Button
        self.contact_twitter_button = QPushButton(self.contact_name_box)
        self.contact_twitter_button.setObjectName("contact_twitter_button")
        self.contact_twitter_button.setCursor(self.contact_phone_button.cursor())
        self.contact_twitter_button.setFixedSize(
            self.contact_phone_button.width(),
            self.contact_phone_button.height())
        self.contact_twitter_button.move(
            self.contact_facebook_button.x() + self.contact_facebook_button.width() + 5,
            self.contact_facebook_button.y())
        # Instagram Button
        self.contact_instagram_button = QPushButton(self.contact_name_box)
        self.contact_instagram_button.setObjectName("contact_instagram_button")
        self.contact_instagram_button.setCursor(self.contact_phone_button.cursor())
        self.contact_instagram_button.setFixedSize(
            self.contact_phone_button.width(),
            self.contact_phone_button.height())
        self.contact_instagram_button.move(
            self.contact_twitter_button.x() + self.contact_twitter_button.width() + 5,
            self.contact_twitter_button.y())
        # Map Button
        self.contact_map_button = QPushButton(self.contact_name_box)
        self.contact_map_button.setObjectName("contact_map_button")
        self.contact_map_button.setCursor(self.contact_phone_button.cursor())
        self.contact_map_button.setFixedSize(
            self.contact_phone_button.width(),
            self.contact_phone_button.height())
        self.contact_map_button.move(
            self.contact_instagram_button.x() + self.contact_instagram_button.width() + 5,
            self.contact_instagram_button.y())
        # Edit Contact
        self.contact_edit = QPushButton(self.contact_name_box)
        self.contact_edit.setObjectName("contact_edit_button")
        self.contact_edit.setFixedSize(70, 20)
        self.contact_edit.move(
            self.contact_phone_button.x(), 
            self.contact_facebook_button.y() + self.contact_facebook_button.height() + 10)
        self.contact_edit.setText(self.lang["edit"])
        self.contact_edit.setCursor(QCursor(Qt.PointingHandCursor))
        self.contact_edit.clicked.connect(self.EditContact)
        # Remove Contact
        self.contact_remove = QPushButton(self.contact_name_box)
        self.contact_remove.setObjectName("contact_remove_button")
        self.contact_remove.setGeometry(QRect(
            self.contact_edit.x() + self.contact_edit.width() + 5, 
            self.contact_edit.y(), 
            self.contact_edit.width(), 
            self.contact_edit.height()))
        self.contact_remove.setText(self.lang["remove"])
        self.contact_remove.setCursor(QCursor(Qt.PointingHandCursor))
        self.contact_remove.clicked.connect(self.removeContact)

        # Contact Phone Box
        self.contact_phone_box = QWidget(self.contact_box)
        self.contact_phone_box.setObjectName("contact_phone_box")
        self.contact_phone_box.setVisible(False)
        self.contact_phone_box.setFixedWidth(self.contact_name_box.width() / 2 - 10)
        self.contact_phone_box.move(
            self.contact_name_box.x(), 
            self.contact_name_box.y() + self.contact_name_box.height() + 15)
        # Contact Phone 1 Label
        self.contact_phonenumber1_label = QLabel(self.contact_phone_box)
        self.contact_phonenumber1_label.setGeometry(QRect(15, 10, 70, 20))
        self.contact_phonenumber1_label.setObjectName("label")
        self.contact_phonenumber1_label.setCursor(QCursor(Qt.PointingHandCursor))
        # Contact Phone 2 Label
        self.contact_phonenumber2_label = QLabel(self.contact_phone_box)
        self.contact_phonenumber2_label.setObjectName(self.contact_phonenumber1_label.objectName())
        self.contact_phonenumber2_label.setStyleSheet(self.contact_phonenumber1_label.styleSheet())
        self.contact_phonenumber2_label.setCursor(self.contact_phonenumber1_label.cursor())
        self.contact_phonenumber2_label.setGeometry(QRect(
            self.contact_phonenumber1_label.x(), 
            self.contact_phonenumber1_label.y() + self.contact_phonenumber1_label.height() + 5, 
            self.contact_phonenumber1_label.width(), 
            self.contact_phonenumber1_label.height()))
        # Contact Phone 3 Label
        self.contact_phonenumber3_label = QLabel(self.contact_phone_box)
        self.contact_phonenumber3_label.setStyleSheet(self.contact_phonenumber1_label.styleSheet())
        self.contact_phonenumber3_label.setObjectName(self.contact_phonenumber1_label.objectName())
        self.contact_phonenumber3_label.setCursor(self.contact_phonenumber1_label.cursor())
        self.contact_phonenumber3_label.setGeometry(QRect(
            self.contact_phonenumber1_label.x(), 
            self.contact_phonenumber2_label.y() + self.contact_phonenumber2_label.height() + 5, 
            self.contact_phonenumber1_label.width(), 
            self.contact_phonenumber1_label.height()))
        # Contact Phone 4 Label
        self.contact_phonenumber4_label = QLabel(self.contact_phone_box)
        self.contact_phonenumber4_label.setStyleSheet(self.contact_phonenumber1_label.styleSheet())
        self.contact_phonenumber4_label.setObjectName(self.contact_phonenumber1_label.objectName())
        self.contact_phonenumber4_label.setCursor(self.contact_phonenumber1_label.cursor())
        self.contact_phonenumber4_label.setGeometry(QRect(
            self.contact_phonenumber1_label.x(), 
            self.contact_phonenumber3_label.y() + self.contact_phonenumber3_label.height() + 5, 
            self.contact_phonenumber1_label.width(), 
            self.contact_phonenumber1_label.height()))
        # Contact Phone 1 Number
        self.contact_phonenumber1 = QLabel(self.contact_phone_box)
        self.contact_phonenumber1.setFixedSize(170, 20)
        self.contact_phonenumber1.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.contact_phonenumber1.setCursor(QCursor(Qt.IBeamCursor))
        self.contact_phonenumber1.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.contact_phonenumber1.move(
            self.contact_phonenumber1_label.x() + self.contact_phonenumber1_label.width() + 30, 
            self.contact_phonenumber1_label.y())
        # Contact Phone 2 Number
        self.contact_phonenumber2 = QLabel(self.contact_phone_box)
        self.contact_phonenumber2.setAlignment(self.contact_phonenumber1.alignment())
        self.contact_phonenumber2.setCursor(self.contact_phonenumber1.cursor())
        self.contact_phonenumber2.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.contact_phonenumber2.setGeometry(QRect(
            self.contact_phonenumber1.x(), 
            self.contact_phonenumber2_label.y(), 
            self.contact_phonenumber1.width(), 
            self.contact_phonenumber1.height()))
        # Contact Phone 3 Number
        self.contact_phonenumber3 = QLabel(self.contact_phone_box)
        self.contact_phonenumber3.setAlignment(self.contact_phonenumber1.alignment())
        self.contact_phonenumber3.setCursor(self.contact_phonenumber1.cursor())
        self.contact_phonenumber3.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.contact_phonenumber3.setGeometry(QRect(
            self.contact_phonenumber1.x(), 
            self.contact_phonenumber3_label.y(), 
            self.contact_phonenumber1.width(), 
            self.contact_phonenumber1.height()))
        # Contact Phone 4 Number
        self.contact_phonenumber4 = QLabel(self.contact_phone_box)
        self.contact_phonenumber4.setAlignment(self.contact_phonenumber1.alignment())
        self.contact_phonenumber4.setCursor(self.contact_phonenumber1.cursor())
        self.contact_phonenumber4.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.contact_phonenumber4.setGeometry(QRect(
            self.contact_phonenumber1.x(), 
            self.contact_phonenumber4_label.y(), 
            self.contact_phonenumber1.width(), 
            self.contact_phonenumber1.height()))

        self.contact_phone_box.adjustSize()


        # Contact Email Box
        self.contact_email_box = QWidget(self.contact_box)
        self.contact_email_box.setObjectName("contact_email_box")
        self.contact_email_box.move(
            self.contact_name_box.x(), 
            self.contact_phone_box.y() + self.contact_phone_box.height() + 10)
        self.contact_email_box.setFixedWidth(self.contact_phone_box.width())
        self.contact_email_box.setVisible(False)
        # Contact Email 1 Label
        self.contact_email1_label = QLabel(self.contact_email_box)
        self.contact_email1_label.setObjectName("label")
        self.contact_email1_label.setGeometry(15, 10, 70, 20)
        self.contact_email1_label.setCursor(QCursor(Qt.PointingHandCursor))
        # Contact Email 2 Label
        self.contact_email2_label = QLabel(self.contact_email_box)
        self.contact_email2_label.setObjectName(self.contact_email1_label.objectName())
        self.contact_email2_label.setCursor(self.contact_email1_label.cursor())
        self.contact_email2_label.setGeometry(QRect(
            self.contact_email1_label.x(), 
            self.contact_email1_label.y() + self.contact_email1_label.height() + 5,
            self.contact_phonenumber1_label.width(), 
            self.contact_phonenumber1_label.height()))
        # Contact Email 1
        self.contact_email1 = QLabel(self.contact_email_box)
        self.contact_email1.setFixedSize(170, 20)
        self.contact_email1.setAlignment(self.contact_phonenumber1.alignment())
        self.contact_email1.setCursor(QCursor(Qt.IBeamCursor))
        self.contact_email1.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.contact_email1.move(
            self.contact_email1_label.x() + self.contact_email1_label.width() + 30, 
            self.contact_email1_label.y())
        # Contact Email 2
        self.contact_email2 = QLabel(self.contact_email_box)
        self.contact_email2.setAlignment(self.contact_email1.alignment())
        self.contact_email2.setCursor(self.contact_email1.cursor())
        self.contact_email2.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.contact_email2.setGeometry(QRect(
            self.contact_email1.x(), 
            self.contact_email2_label.y(), 
            self.contact_email1.width(), 
            self.contact_email1.height()))

        self.contact_email_box.adjustSize()

        # Contact SNS
        self.contact_sns_box = QWidget(self.contact_box)
        self.contact_sns_box.setObjectName("contact_sns_box")
        self.contact_sns_box.move(
            self.contact_name_box.x(),
            self.contact_email_box.y() + self.contact_email_box.height() + 10)
        self.contact_sns_box.setFixedWidth(self.contact_email_box.width())
        self.contact_sns_box.setVisible(False)
        # Contact SNS 1 Label
        self.contact_sns1_label = QLabel(self.contact_sns_box)
        self.contact_sns1_label.setObjectName("label")
        self.contact_sns1_label.setGeometry(QRect(15, 10, 70, 20))
        self.contact_sns1_label.setCursor(QCursor(Qt.PointingHandCursor))
        # Contact SNS 2 Label
        self.contact_sns2_label = QLabel(self.contact_sns_box)
        self.contact_sns2_label.setObjectName(self.contact_sns1_label.objectName())
        self.contact_sns2_label.setCursor(self.contact_sns1_label.cursor())
        self.contact_sns2_label.setGeometry(QRect(
            self.contact_sns1_label.x(), 
            self.contact_sns1_label.y() + self.contact_sns1_label.height() + 5,
            self.contact_sns1_label.width(), 
            self.contact_sns1_label.height()))
        # Contact SNS 3 Label
        self.contact_sns3_label = QLabel(self.contact_sns_box)
        self.contact_sns3_label.setObjectName(self.contact_sns1_label.objectName())
        self.contact_sns3_label.setCursor(self.contact_sns1_label.cursor())
        self.contact_sns3_label.setGeometry(QRect(
            self.contact_sns1_label.x(), 
            self.contact_sns2_label.y() + self.contact_sns2_label.height() + 5, 
            self.contact_sns1_label.width(),
            self.contact_sns1_label.height()))
        # Contact SNS 1
        self.contact_sns1 = QLabel(self.contact_sns_box)
        self.contact_sns1.setFixedSize(170, 20)
        self.contact_sns1.setAlignment(self.contact_phonenumber1.alignment())
        self.contact_sns1.setCursor(QCursor(Qt.IBeamCursor))
        self.contact_sns1.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.contact_sns1.move(
            self.contact_sns1_label.x() + self.contact_sns1_label.width() + 30,
            self.contact_sns1_label.y())
        # Contact SNS 2
        self.contact_sns2 = QLabel(self.contact_sns_box)
        self.contact_sns2.setAlignment(self.contact_sns1.alignment())
        self.contact_sns2.setCursor(self.contact_sns1.cursor())
        self.contact_sns2.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.contact_sns2.setGeometry(QRect(
            self.contact_sns1.x(), 
            self.contact_sns2_label.y(), 
            self.contact_sns1.width(), 
            self.contact_sns1.height()))
        # Contact SNS 3
        self.contact_sns3 = QLabel(self.contact_sns_box)
        self.contact_sns3.setAlignment(self.contact_sns1.alignment())
        self.contact_sns3.setCursor(self.contact_sns1.cursor())
        self.contact_sns3.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.contact_sns3.setGeometry(QRect(
            self.contact_sns1.x(), 
            self.contact_sns3_label.y(),
            self.contact_sns1.width(), 
            self.contact_sns1.height()))
        
        self.contact_sns_box.adjustSize()
        

        # Contact Adress
        self.contact_address_box = QWidget(self.contact_box)
        self.contact_address_box.setObjectName("contact_address_box")
        self.contact_address_box.move(
            self.contact_phone_box.x() + self.contact_phone_box.width() + 20,
            self.contact_phone_box.y())
        self.contact_address_box.setFixedWidth(self.contact_phone_box.width() + 1)
        self.contact_address_box.setVisible(False)
        # Contact Address 1 Label
        self.contact_address1_label = QLabel(self.contact_address_box)
        self.contact_address1_label.setObjectName("label")
        self.contact_address1_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.contact_address1_label.setGeometry(15, 10, 70, 20)
        self.contact_address1_label.setCursor(QCursor(Qt.PointingHandCursor))
        # Contact Address 1
        self.contact_address1 = QLabel(self.contact_address_box)
        self.contact_address1.setFixedWidth(170)
        self.contact_address1.setMaximumHeight(60)
        self.contact_address1.setAlignment(Qt.AlignLeft)
        self.contact_address1.setCursor(QCursor(Qt.IBeamCursor))
        self.contact_address1.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.contact_address1.setWordWrap(True)
        self.contact_address1.adjustSize()
        self.contact_address1.move(
            self.contact_address1_label.x() + self.contact_address1_label.width()  + 30, 
            self.contact_address1_label.y() + 2)
        # Contact Address 2 Label
        self.contact_address2_label = QLabel(self.contact_address_box)
        self.contact_address2_label.setObjectName(self.contact_address1_label.objectName())
        self.contact_address2_label.setAlignment(self.contact_address1_label.alignment())
        self.contact_address2_label.setCursor(self.contact_address1_label.cursor())
        self.contact_address2_label.setGeometry(QRect(
            self.contact_address1_label.x(), 
            self.contact_address1.y() + self.contact_address1.height() + 10, 
            self.contact_address1_label.width(), 
            self.contact_address1_label.height()))
        # Contact Address 2
        self.contact_address2 = QLabel(self.contact_address_box)
        self.contact_address2.setFixedWidth(self.contact_address1.width())
        self.contact_address2.setMaximumHeight(60)
        self.contact_address2.setAlignment(self.contact_address1.alignment())
        self.contact_address2.setCursor(self.contact_address1.cursor())
        self.contact_address2.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.contact_address2.setWordWrap(True)
        self.contact_address2.move(
            self.contact_address1.x(), 
            self.contact_address1.y() + self.contact_address1.height() + 10)

        # Contact Birthday Box
        self.contact_birthday_box = QWidget(self.contact_box)
        self.contact_birthday_box.setObjectName("contact_birthday_box")
        self.contact_birthday_box.setFixedWidth(self.contact_address_box.width())
        self.contact_birthday_box.move(
            self.contact_address_box.x(), 
            self.contact_address_box.y() + self.contact_address_box.height() + 20)
        self.contact_birthday_box.setVisible(False)
        # Contact Birthday Label
        self.contact_birthday_label = QLabel(self.contact_birthday_box)
        self.contact_birthday_label.setObjectName("label")
        self.contact_birthday_label.setCursor(QCursor(Qt.PointingHandCursor))
        self.contact_birthday_label.setGeometry(QRect(15, 10, 70, 20))
        self.contact_birthday_label.setText(self.lang["birthday"])
        # Contact Birthday
        self.contact_birthday = QLabel(self.contact_birthday_box)
        self.contact_birthday.setFixedSize(170, 20)
        self.contact_birthday.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.contact_birthday.setCursor(QCursor(Qt.IBeamCursor))
        self.contact_birthday.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.contact_birthday.move(
            self.contact_birthday_label.x() + self.contact_birthday_label.width() + 30, 
            self.contact_birthday_label.y() + 2)
        # Contact ID Card Label
        self.contact_idcard_label = QLabel(self.contact_birthday_box)
        self.contact_idcard_label.setObjectName(self.contact_birthday_label.objectName())
        self.contact_idcard_label.setCursor(self.contact_birthday_label.cursor())
        self.contact_idcard_label.setFixedSize(self.contact_birthday_label.size())
        self.contact_idcard_label.move(
            self.contact_birthday_label.x(),
            self.contact_birthday_label.y() + self.contact_birthday_label.height())
        # Contact ID Card
        self.contact_idcard = QLabel(self.contact_birthday_box)
        self.contact_idcard.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.contact_idcard.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.contact_idcard.setCursor(self.contact_birthday.cursor())
        self.contact_idcard.setFixedWidth(self.contact_birthday.width())
        self.contact_idcard.move(
            self.contact_idcard_label.x() + self.contact_idcard_label.width() + 30,
            self.contact_idcard_label.y())
        # Contact Bank Label
        self.contact_bank_label = QLabel(self.contact_birthday_box)
        self.contact_bank_label.setObjectName(self.contact_birthday_label.objectName())
        self.contact_bank_label.setCursor(self.contact_birthday_label.cursor())
        self.contact_bank_label.setFixedSize(
            self.contact_birthday_label.width() + 20,
            self.contact_birthday_label.height())
        self.contact_bank_label.move(
            self.contact_birthday_label.x(),
            self.contact_birthday_label.y() + self.contact_birthday_label.height() + 5)
        # Contact Bank Account
        self.contact_bank = QLabel(self.contact_birthday_box)
        self.contact_bank.setAlignment(self.contact_idcard.alignment())
        self.contact_bank.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.contact_bank.setWordWrap(True)
        self.contact_bank.setCursor(self.contact_birthday.cursor())
        self.contact_bank.setFixedWidth(self.contact_birthday.width())
        self.contact_bank.move(
            self.contact_birthday.x(),
            self.contact_bank_label.y())

        # Contact Note Box
        self.contact_note_box = QWidget(self.contact_box)
        self.contact_note_box.setObjectName(self.contact_phone_box.objectName())
        self.contact_note_box.setFixedWidth(self.contact_address_box.width())
        self.contact_note_box.move(
            self.contact_address_box.x(),
            self.contact_birthday_box.y() + self.contact_birthday_box.height() + 10)
        # Contact note label
        self.contact_note_label = QLabel(self.contact_note_box)
        self.contact_note_label.setObjectName(self.contact_phonenumber1_label.objectName())
        self.contact_note_label.setAlignment(Qt.AlignTop)
        self.contact_note_label.setCursor(self.contact_phonenumber1_label.cursor())
        self.contact_note_label.setGeometry(self.contact_phonenumber1_label.geometry())
        self.contact_note_label.setText(self.lang["note"])
        # Contact note
        self.contact_note = QLabel(self.contact_note_box)
        self.contact_note.setFixedWidth(self.contact_address1.width())
        self.contact_note.setCursor(QCursor(Qt.IBeamCursor))
        self.contact_note.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.contact_note.setWordWrap(True)
        self.contact_note.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.contact_note.move(
            self.contact_address1.x(),
            self.contact_note_label.y())
        

    def showContactContent(self):
        if not len(self.history) or self.history[-1] != self.contact_box_scroll:
            self.history.append(self.contact_box_scroll)
        self.contact_box_scroll.show()
        self.contact_box_scroll.raise_()
        if not len(self.history):
            self.back_button.setDisabled(True)
        else:
            self.back_button.setDisabled(False)
        self.clearBackHistory()
        # Contact content widget
        itemID = self.contact_list.itemWidget(self.contact_list.currentItem()).getID()
        self.datafile_row = user.getContactRowByID(itemID)
        
        # Contact Name Box
        self.contact_name_box.setVisible(True)
        if user.getContactData(self.datafile_row, "picture"):
            self.contact_picture = QPixmap("{0}/data/{1}/profile_pictures/{2}".format(
                self.main_directory,
                user.getData("username"),
                user.getContactData(self.datafile_row, "picture")))
        else:
            self.contact_picture = QPixmap("./image/default_avatar.png")
        self.contact_picture_scaled = self.contact_picture.scaled(
            self.contact_profile_picture.width(), 
            self.contact_profile_picture.height(), 
            aspectRatioMode=Qt.IgnoreAspectRatio, 
            transformMode=Qt.SmoothTransformation)
        rounded = QPixmap(self.contact_picture_scaled.size())
        rounded.fill(QColor("transparent"))
        # Create rounded picture
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(self.contact_picture_scaled))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(
            self.contact_picture_scaled.rect(),
            self.contact_profile_picture.width() / 2,
            self.contact_profile_picture.height() / 2)
        self.contact_profile_picture.setPixmap(rounded)
        painter.end()
        del painter
        del rounded

        self.name_datalist = (
            user.getContactData(self.datafile_row, "fullname"),
            user.getContactData(self.datafile_row, "nickname"),
            user.getContactData(self.datafile_row, "company"),
            user.getContactData(self.datafile_row, "jobtitle"))
        if self.name_datalist.count(None) == 4 or self.name_datalist.count("") == 4:
            self.contact_name_box.setVisible(False)
        else:
            self.contact_name_box.setVisible(True)
            self.contact_fullname.setText(user.getContactData(self.datafile_row, "fullname"))
            self.contact_nickname.setText(user.getContactData(self.datafile_row, "nickname"))
            self.contact_company.setText(user.getContactData(self.datafile_row, "company"))
            self.contact_jobtitle.setText(user.getContactData(self.datafile_row, "jobtitle"))
        del self.name_datalist


        def setLabelText(label, text):
            try:
                label.setText(self.lang[text])
            except KeyError:
                label.setText(text)
        # Phone Number Box
        self.phone_datalist = (
            user.getContactData(self.datafile_row, "phone1"),
            user.getContactData(self.datafile_row, "phone2"),
            user.getContactData(self.datafile_row, "phone3"),
            user.getContactData(self.datafile_row, "phone4"))
        if self.phone_datalist.count(None) + self.phone_datalist.count("") == 4:
            self.contact_phone_button.setDisabled(True)
            self.contact_message_button.setDisabled(True)
            self.contact_facetime_button.setDisabled(True)
            self.contact_phone_box.setVisible(False)
            self.contact_phone_box.setFixedHeight(0)
            self.contact_phone_box.move(
                self.contact_phone_box.x(),
                self.contact_name_box.y() + self.contact_name_box.height())
        else:
            self.contact_phone_button.setDisabled(False)
            self.contact_message_button.setDisabled(False)
            self.contact_facetime_button.setDisabled(False)
            self.contact_phone_box.setVisible(True)
            self.contact_phone_box.setFixedHeight(
                (4 - (self.phone_datalist.count(None) + self.phone_datalist.count(""))) * 25 + 15)
            self.contact_phone_box.move(
                self.contact_phone_box.x(),
                self.contact_name_box.y() + self.contact_name_box.height() + 20)
            self.contact_phonenumber1.setText(user.getContactData(self.datafile_row, "phone1"))
            self.contact_phonenumber2.setText(user.getContactData(self.datafile_row, "phone2"))
            self.contact_phonenumber3.setText(user.getContactData(self.datafile_row, "phone3"))
            self.contact_phonenumber4.setText(user.getContactData(self.datafile_row, "phone4"))
            setLabelText(self.contact_phonenumber1_label, user.getContactData(self.datafile_row, "phone1_label"))
            setLabelText(self.contact_phonenumber2_label, user.getContactData(self.datafile_row, "phone2_label"))
            setLabelText(self.contact_phonenumber3_label, user.getContactData(self.datafile_row, "phone3_label"))
            setLabelText(self.contact_phonenumber4_label, user.getContactData(self.datafile_row, "phone4_label"))
        del self.phone_datalist
        
        # Email
        self.email_datalist = (
            user.getContactData(self.datafile_row, "email1"),
            user.getContactData(self.datafile_row, "email2"))
        if self.email_datalist.count(None) + self.email_datalist.count("") == 2:
            self.contact_email_button.setDisabled(True)
            self.contact_email_box.setVisible(False)
            self.contact_email_box.setFixedHeight(0)
            self.contact_email_box.move(
                self.contact_email_box.x(),
                self.contact_phone_box.y() + self.contact_phone_box.height())
        else:
            self.contact_email_button.setDisabled(False)
            self.contact_email_box.setVisible(True)
            self.contact_email_box.setFixedHeight(
                (2 - (self.email_datalist.count(None) + self.email_datalist.count("")))* 25 + 15)
            self.contact_email_box.move(
                self.contact_email_box.x(),
                self.contact_phone_box.y() + self.contact_phone_box.height() + 20)
            self.contact_email1.setText(user.getContactData(self.datafile_row, "email1"))
            self.contact_email2.setText(user.getContactData(self.datafile_row, "email2"))
            setLabelText(self.contact_email1_label, user.getContactData(self.datafile_row, "email1_label"))
            setLabelText(self.contact_email2_label, user.getContactData(self.datafile_row, "email2_label"))
        del self.email_datalist

        # SNS
        self.sns_datalist = (
            user.getContactData(self.datafile_row, "sns1"),
            user.getContactData(self.datafile_row, "sns2"),
            user.getContactData(self.datafile_row, "sns3"))
        self.sns_label_datalist = (
            user.getContactData(self.datafile_row, "sns1_label"),
            user.getContactData(self.datafile_row, "sns2_label"),
            user.getContactData(self.datafile_row, "sns3_label"))
        def disabledSNSButton(label, button):
            if label in self.sns_label_datalist:
                button.setDisabled(False)
            else:
                button.setDisabled(True)
        disabledSNSButton("Facebook", self.contact_facebook_button)
        disabledSNSButton("Twitter", self.contact_twitter_button)
        disabledSNSButton("Instagram", self.contact_instagram_button)
        if self.sns_datalist.count(None) + self.sns_datalist.count("") == 3:
            self.contact_sns_box.setVisible(False)
            self.contact_sns_box.setFixedHeight(0)
            self.contact_sns_box.move(
                self.contact_sns_box.x(),
                self.contact_email_box.y() + self.contact_email_box.height())
        else:
            self.contact_sns_box.setVisible(True)
            self.contact_sns_box.setFixedHeight(
                (3 - (self.sns_datalist.count(None) + self.sns_datalist.count("")))*25 + 15)
            self.contact_sns_box.move(
                self.contact_sns_box.x(),
                self.contact_email_box.y() + self.contact_email_box.height() + 20)
            self.contact_sns1.setText(user.getContactData(self.datafile_row, "sns1"))
            self.contact_sns2.setText(user.getContactData(self.datafile_row, "sns2"))
            self.contact_sns3.setText(user.getContactData(self.datafile_row, "sns3"))
            setLabelText(self.contact_sns1_label, user.getContactData(self.datafile_row, "sns1_label"))
            setLabelText(self.contact_sns2_label, user.getContactData(self.datafile_row, "sns2_label"))
            setLabelText(self.contact_sns3_label, user.getContactData(self.datafile_row, "sns3_label"))
        del self.sns_datalist

        # Address
        self.address_datalist = (
            user.getContactData(self.datafile_row, "address1"),
            user.getContactData(self.datafile_row, "address2"))
        if self.address_datalist.count(None) + self.address_datalist.count("") == 2:
            self.contact_map_button.setDisabled(True)
            self.contact_address_box.setVisible(False)
            self.contact_address_box.resize(self.contact_address_box.width(), 0)
            self.contact_address_box.move(
                self.contact_address_box.x(),
                self.contact_name_box.y() + self.contact_name_box.height())
        else:
            self.contact_map_button.setDisabled(False)
            self.contact_address_box.setVisible(True)
            self.contact_address_box.move(
                self.contact_address_box.x(),
                self.contact_name_box.y() + self.contact_name_box.height() + 20)
            # Address 1
            setLabelText(self.contact_address1_label, user.getContactData(self.datafile_row, "address1_label"))
            self.contact_address1.setText(user.getContactData(self.datafile_row, "address1"))
            self.contact_address1.adjustSize()
            # Address 2
            if not user.getContactData(self.datafile_row, "address2"):
                self.contact_address2_label.resize(self.contact_address2_label.width(), 0)
                self.contact_address2_label.move(
                    self.contact_address2_label.x(),
                    self.contact_address1_label.y() + self.contact_address1_label.height())
                self.contact_address2.resize(self.contact_address2.width(), 0)
                self.contact_address2.move(
                    self.contact_address2.x(),
                    self.contact_address1.y() + self.contact_address1.height() + 10)
            else:
                setLabelText(self.contact_address2_label, user.getContactData(self.datafile_row, "address2_label"))
                self.contact_address2_label.move(
                    self.contact_address2_label.x(), 
                    self.contact_address1.y() + self.contact_address1.height() + 10)
                self.contact_address2_label.resize(self.contact_address2_label.width(), 25)
                self.contact_address2.setText(user.getContactData(self.datafile_row, "address2"))
                self.contact_address2.move(self.contact_address2.x(), self.contact_address2_label.y())
                self.contact_address2.adjustSize()
            self.contact_address_box.adjustSize()
            self.contact_address_box.resize(
                self.contact_address_box.width(),
                self.contact_address_box.height() + 10)
            self.contact_address_box.adjustSize()
            self.contact_address_box.resize(
                self.contact_address_box.width(),
                self.contact_address_box.height() - 5)
        del self.address_datalist

        # Birthday
        if (not user.getContactData(self.datafile_row, "year")
            and not user.getContactData(self.datafile_row, "idcard")
            and not user.getContactData(self.datafile_row, "bank")):
            self.contact_birthday_box.setVisible(False)
            self.contact_birthday_box.resize(
                self.contact_birthday_box.width(),
                0)
            self.contact_birthday_box.move(
                self.contact_birthday_box.x(),
                self.contact_address_box.y() + self.contact_address_box.height())
        else:
            self.contact_birthday_box.setVisible(True)
            self.contact_birthday_box.move(
               self.contact_birthday_box.x(),
                self.contact_address_box.y() + self.contact_address_box.height() + 20)
            self.birthday_item = (
                str(user.getContactData(self.datafile_row, "year")),
                " ",
                self.lang["month"][int(user.getContactData(self.datafile_row, "month"))],
                " ",
                str(user.getContactData(self.datafile_row, "day"))
            )
            self.contact_birthday.setText(self.lang["date"].format(
                str(user.getContactData(self.datafile_row, "year")),
                self.lang["month"][int(user.getContactData(self.datafile_row, "month"))],
                str(user.getContactData(self.datafile_row, "day"))))

            # ID Card
            if not user.getContactData(self.datafile_row, "idcard"):
                self.contact_idcard_label.resize(
                    self.contact_idcard_label.width(),
                    0)
                self.contact_idcard_label.move(
                    self.contact_birthday_label.x(),
                    self.contact_birthday_label.y())
                self.contact_idcard_label.clear()
                self.contact_idcard.resize(
                    self.contact_idcard.width(),
                    0)
                self.contact_idcard.move(
                    self.contact_idcard.x(),
                    self.contact_birthday.y())
                self.contact_idcard.clear()
            else:
                self.contact_idcard_label.resize(
                    self.contact_idcard_label.width(),
                    20)
                self.contact_idcard_label.move(
                    self.contact_birthday_label.x(),
                    self.contact_birthday_label.y() + self.contact_birthday_label.height() + 5)
                setLabelText(self.contact_idcard_label, user.getContactData(self.datafile_row, "idcard_label"))
                self.contact_idcard.resize(
                    self.contact_idcard.width(),
                    20)
                self.contact_idcard.move(
                    self.contact_idcard.x(),
                    self.contact_idcard_label.y())
                setLabelText(self.contact_idcard, user.getContactData(self.datafile_row, "idcard"))

            # Bank
            if not user.getContactData(self.datafile_row, "bank"):
                self.contact_bank_label.resize(self.contact_bank_label.width(), 0)
                self.contact_bank_label.move(self.contact_idcard_label.pos())
                self.contact_bank_label.clear()
                self.contact_bank_label.setVisible(False)
                self.contact_bank.resize(self.contact_bank.width(), 0)
                self.contact_bank.move(self.contact_idcard.pos())
                self.contact_bank.clear()
                self.contact_bank.setVisible(False)
            else:
                self.contact_bank_label.resize(self.contact_bank_label.width(), 20)
                self.contact_bank_label.setVisible(True)
                self.contact_bank_label.move(
                    self.contact_bank_label.x(),
                    self.contact_idcard_label.y() + self.contact_idcard_label.height() + 5)
                setLabelText(self.contact_bank_label, user.getContactData(self.datafile_row, "bank_label"))
                self.contact_bank.move(self.contact_bank.x(), self.contact_bank_label.y() + 2)
                self.contact_bank.setVisible(True)
                if user.getContactData(self.datafile_row, "bank_branch"):
                    bank_branch = "\n" + str(user.getContactData(self.datafile_row, "bank_branch"))
                else:
                    bank_branch = ""
                self.contact_bank.setText(str(user.getContactData(self.datafile_row, "bank")) + bank_branch)
                self.contact_bank.adjustSize()
            self.contact_birthday_box.adjustSize()

        # Note
        if not user.getContactData(self.datafile_row, "note"):
            self.contact_note_box.setVisible(False)
        else:
            self.contact_note_box.setVisible(True)
            self.contact_note_box.move(
                self.contact_birthday_box.x(),
                self.contact_birthday_box.y() + self.contact_birthday_box.height() + 10)
            self.contact_note.setText(user.getContactData(self.datafile_row, "note"))
            self.contact_note.adjustSize()

            self.contact_note_box.adjustSize()
            

        # Adjust contact box size
        self.contact_box.adjustSize()

    def CreateContact(self):
        contakuto_edit_create_contact.user = user
        contakuto_edit_create_contact.lang = self.lang
        self.create_contact_scroll = QScrollArea(self.container)
        self.create_contact_scroll.setObjectName("create_contact_box_scroll")
        self.create_contact_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.create_contact_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.create_contact_scroll.setFixedSize(
            self.container.width() - self.sidebar.width() - 2,
            self.container.height() - self.titlebar.height() - 1)
        self.create_contact_scroll.move(
            self.sidebar.width() + 1,
            self.titlebar.height() + 1)
        self.create_contact = contakuto_edit_create_contact.ContactModifyingUI(
            scroll_widget=self.create_contact_scroll,
            mode=0,
            row=user.getEmptyRow())
        self.create_contact.showUpContent()
        self.create_contact_scroll.setWidget(self.create_contact)
        self.create_contact_scroll.show()
        self.create_contact_scroll.raise_()
        self.history.append(self.create_contact_scroll)
        self.clearBackHistory()
        if not len(self.history):
            self.back_button.setDisabled(True)
        else:
            self.back_button.setDisabled(False)

    def EditContact(self):
        contakuto_edit_create_contact.user = user
        contakuto_edit_create_contact.lang = self.lang
        self.edit_contact_scroll = QScrollArea(self.container)
        self.edit_contact_scroll.setObjectName("edit_contact_box_scroll")
        self.edit_contact_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.edit_contact_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.edit_contact_scroll.setFixedSize(self.contact_box_scroll.size())
        self.edit_contact_scroll.move(
            self.sidebar.width() + 1,
            self.titlebar.height() + 1)
        self.edit_contact = contakuto_edit_create_contact.ContactModifyingUI(
            scroll_widget=self.edit_contact_scroll,
            mode=1,
            row=self.datafile_row)
        self.edit_contact.showUpContent()
        self.edit_contact_scroll.setWidget(self.edit_contact)
        self.edit_contact_scroll.show()
        self.history.append(self.edit_contact_scroll)
        self.clearBackHistory()
        if not len(self.history):
            self.back_button.setDisabled(True)
        else:
            self.back_button.setDisabled(False)

    def removeContact(self):
        message = QMessageBoxX(
            icon="warning",
            boldtext="Contact removing confirmation",
            text="Are you sure to remove this contact?",
            ok=True,
            cancel=True,
            stylesheet=self.styleSheet())
        if message.exec() == 1:
            user.removeContactData(self.datafile_row)
            try:
                user.saveData()
                self.contact_list.clear()
                user.setupContactList(self.contact_list)
                self.history[-1].close()
                del self.history[-1]
            except PermissionError:
                message = QMessageBoxX(
                    icon = "warning",
                    boldtext = self.lang["permission_denied"],
                    text = self.lang["permission_denied_description"],
                    stylesheet=self.styleSheet())
                message.exec()
    def unavailabeFeature(self):
        message = QMessageBoxX(
            icon="warning",
            boldtext=self.lang["unavailable_feature"],
            text=self.lang["unavailable_feature_description"],
            stylesheet=self.styleSheet())
        message.exec()

    def showSearchBox(self):
        if self.searchbox.height() == 0:
            self.searchbox.setVisible(True)
            self.searchbox.setFixedHeight(30)
            self.searchbox.setFocus()
            self.contact_list.move(
                self.contact_list.x(),
                self.searchbox.y() + self.searchbox.height() + 10)
        else:
            self.searchbox.setVisible(False)
            self.searchbox.setFixedHeight(0)
            self.contact_list.move(
                self.contact_list.x(),
                0)
    
    def showContactBox(self):
        try:
            self.contact_box_scroll.raise_()
        except:
            pass
        if not len(self.history):
            self.back_button.setDisabled(True)
        else:
            self.back_button.setDisabled(False)
        self.clearBackHistory()

    def searchClear(self):
        self.searchbox.clear()
        self.searchbox.setFocus()

    def searchContacts(self):
        if self.searchbox.text():
            self.search_clear.setVisible(True)
            self.contact_list.clear()
            user.searchContactData(self.contact_list, self.searchbox.text())
        else:
            self.search_clear.setVisible(False)
            self.contact_list.clear()
            user.setupContactList(self.contact_list)

    def userSettingsWidget(self):
        contakuto_usersettings.lang = self.lang
        contakuto_usersettings.user = user
        self.usersettings = contakuto_usersettings.UserSettingsUI(self.lang, self.container)
        self.usersettings.show()
        self.history.append(self.usersettings)
        self.clearBackHistory()
        if not len(self.history):
            self.back_button.setDisabled(True)
        else:
            self.back_button.setDisabled(False)

    def signOut(self):
        self.message = QMessageBoxX(
            icon = "question",
            boldtext = "Close app confirmation",
            text = "Are you sure to close program?",
            ok = True,
            cancel = True,
            stylesheet=self.styleSheet())
        if self.message.exec() == 1:
            self.close()
            self.loginui = login.LoginUI()
            self.loginui.show()
        else:
            pass


def main():
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont("./image/fonts/SanFranciscoDisplay-Regular.otf")
    QFontDatabase.addApplicationFont("./image/fonts/SanFranciscoDisplay-Bold.otf")
    QFontDatabase.addApplicationFont("./image/fonts/SanFranciscoDisplay-Medium.otf")
    QFontDatabase.addApplicationFont("./image/fonts/SanFranciscoDisplay-Thin.otf")
    loginui = login.LoginUI()
    loginui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()


