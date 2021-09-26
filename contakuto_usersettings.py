import os
from types import prepare_class
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from contakuto_basegui import *
import contakuto_stylesheet as style
import contakuto_main as main
from PIL import Image

class UserSettingsUI(QWidget):
    def __init__(self, lang, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setObjectName("usersettings_box")
        self.setFixedSize(
            self.parent().parent().container.width() - self.parent().parent().sidebar.width() - 2,
            self.parent().parent().container.height() - self.parent().parent().titlebar.height() - 1)
        self.move(
            self.parent().parent().sidebar.width() + 1,
            self.parent().parent().titlebar.height())

        # Settings list
        self.settings_list_widget = QListWidget(self)
        self.settings_list_widget.setObjectName("settings_list")
        self.settings_list_widget.setFixedSize(
            270,
            self.height())
        self.settings_list_widget.move(0, 0)
        self.settings_list_items = [
            [lang["profile_picture"], lang["profile_picture_setting"], "profile_picture.png"],
            [lang["fullname"], lang["fullname_setting"], "fullname.png"],
            [lang["password"], lang["password_setting"], "password.png"],
            [lang["pin"], lang["pin_setting"], "pin.png"],
            [lang["language"], lang["language_setting"], "language.png"],
            [lang["theme"], lang["theme_setting"], "theme.png"]
        ]
        for item in self.settings_list_items:
            itemWidget = QListWidgetX()
            itemPicture = QPixmap("./image/gui/{0}".format(item[2]))
            itemPicture_scaled = itemPicture.scaled(
                40, 40,
                aspectRatioMode=Qt.IgnoreAspectRatio, transformMode=Qt.SmoothTransformation)
            itemWidget.setIcon(itemPicture_scaled)
            itemWidget.setTextUp(item[0])
            itemWidget.setTextDown(item[1])
            listItem = QListWidgetItem(item[0])
            listItem.setSizeHint(itemWidget.sizeHint())
            self.settings_list_widget.addItem(listItem)
            self.settings_list_widget.setItemWidget(listItem, itemWidget)
        self.settings_list_widget.itemClicked.connect(self.showSettingsWidget)

        # Profile Picture Widget
        self.profile_picture_box = QWidget(self)
        self.profile_picture_box.setObjectName("settings_subwidget")
        self.profile_picture_box.setVisible(False)
        self.profile_picture_box.setFixedSize(
            self.width() - self.settings_list_widget.width(),
            self.height())
        self.profile_picture_box.move(
            self.settings_list_widget.width(),
            0)
        # Profile picture label
        self.profile_picture_description = QLabel(self.profile_picture_box)
        self.profile_picture_description.setObjectName("settings_description")
        self.profile_picture_description.move(30, 30)
        self.profile_picture_description.setFixedWidth(
            self.profile_picture_box.width() - self.profile_picture_description.x()*2)
        self.profile_picture_description.setText(lang["profile_picture_description"])
        self.profile_picture_description.setWordWrap(True)
        self.profile_picture_description.adjustSize()
        # Profile picture container
        self.profile_picture_container = QWidget(self.profile_picture_box)
        self.profile_picture_container.setObjectName("field_container")
        self.profile_picture_container.setFixedWidth(self.profile_picture_description.width())
        self.profile_picture_container.move(
            self.profile_picture_description.x(),
            self.profile_picture_description.y() + self.profile_picture_description.height() + 10)
        # Profile pcture
        self.profile_picture = QLabel(self.profile_picture_container)
        self.profile_picture.setObjectName("profile_picture")
        self.profile_picture.move(
            50, 
            10)
        self.profile_picture.setFixedSize(114, 114)
        if not user.getData("picture"):
            self.old_path = "./image/default_avatar.png"
        else:
            self.old_path = "./data/{0}/profile_pictures/{1}".format(
                user.getData("username"),
                user.getData("picture"))
        self.picture_path = self.old_path
        self.newImage = None
        self.picture = QPixmap(self.old_path)
        self.picture_scaled = self.picture.scaled(
            self.profile_picture.width() - 4, self.profile_picture.height() - 4,
            aspectRatioMode=Qt.IgnoreAspectRatio, transformMode=Qt.SmoothTransformation)
        self.profile_picture.setPixmap(self.picture_scaled)
        self.pfpic_shadow = QGraphicsDropShadowEffect()
        self.pfpic_shadow.setBlurRadius(15)
        self.pfpic_shadow.setOffset(0, 0)
        self.profile_picture.setGraphicsEffect(self.pfpic_shadow)
        # Profile picture edit button--
        self.profile_picture_edit = QPushButton(self.profile_picture_container)
        self.profile_picture_edit.setCursor(QCursor(Qt.PointingHandCursor))
        self.profile_picture_edit.setFixedSize(100, 25)
        self.profile_picture_edit.move(
            self.profile_picture.x() + self.profile_picture.width() + 30,
            self.profile_picture.y())
        self.profile_picture_edit.setText(lang["edit"])
        self.profile_picture_edit.clicked.connect(self.getProfilePicture)
        # Profile picture remove button
        self.profile_picture_remove = QPushButton(self.profile_picture_container)
        self.profile_picture_remove.setCursor(self.profile_picture_edit.cursor())
        self.profile_picture_remove.setFixedSize(self.profile_picture_edit.size())
        self.profile_picture_remove.move(
            self.profile_picture_edit.x(),
            self.profile_picture_edit.y() + self.profile_picture_edit.height() + 5)
        self.profile_picture_remove.setText(lang["remove"])
        self.profile_picture_remove.clicked.connect(self.removeProfilePicture)
        self.profile_picture_container.adjustSize()
        # Profile picture save button
        self.profile_picture_save = QPushButton(self.profile_picture_box)
        self.profile_picture_save.setObjectName("save_button")
        self.profile_picture_save.setCursor(self.profile_picture_edit.cursor())
        self.profile_picture_save.setFixedSize(self.profile_picture_edit.size())
        self.profile_picture_save.move(
            self.profile_picture_container.x() + self.profile_picture_container.width() - self.profile_picture_save.width() - 20,
            self.profile_picture_container.y() + self.profile_picture_container.height() + 10)
        self.profile_picture_save.setText(lang["save"])
        self.profile_picture_save.clicked.connect(self.saveProfilePicture)
        
        # Fullname Widget
        self.fullname_box = QWidget(self)
        self.fullname_box.setObjectName(self.profile_picture_box.objectName())
        self.fullname_box.setVisible(False)
        self.fullname_box.setFixedSize(self.profile_picture_box.size())
        self.fullname_box.move(self.profile_picture_box.pos())
        # Fullname description
        self.fullname_description = QLabel(self.fullname_box)
        self.fullname_description.setObjectName(self.profile_picture_description.objectName())
        self.fullname_description.setFixedWidth(self.profile_picture_description.width())
        self.fullname_description.move(self.profile_picture_description.pos())
        self.fullname_description.setText(lang["fullname_description"])
        self.fullname_description.setWordWrap(True)
        self.fullname_description.adjustSize()
        # Fullname container box
        self.fullname_container = QWidget(self.fullname_box)
        self.fullname_container.setObjectName(self.profile_picture_container.objectName())
        self.fullname_container.setFixedWidth(self.fullname_description.width())
        self.fullname_container.move(
            self.fullname_description.x(),
            self.fullname_description.y() + self.fullname_description.height() + 10)
        # Username label
        self.username_label = QLabel(self.fullname_container)
        self.username_label.setObjectName("field_label")
        self.username_label.setFixedSize(100, 25)
        self.username_label.move(40, 10)
        self.username_label.setText(lang["username"])
        # Username
        self.username = QLabel(self.fullname_container)
        self.username.setObjectName("username")
        self.username.setFixedSize(200, 25)
        self.username.move(
            self.username_label.x() + self.username_label.width() + 10,
            self.username_label.y())
        self.username.setText("@" + user.getData("username"))
        # Fullname label
        self.fullname_label = QLabel(self.fullname_container)
        self.fullname_label.setObjectName(self.username_label.objectName())
        self.fullname_label.setGeometry(QRect(
            self.username_label.x(),
            self.username_label.y() + self.username_label.height() + 10,
            self.username_label.width(),
            self.username_label.height()))
        self.fullname_label.setText(lang["fullname"])
        # Fullname
        self.fullname = QLineEdit(self.fullname_container)
        self.fullname.setGeometry(QRect(
            self.username.x(), self.fullname_label.y(),
            self.username.width(), self.username.height()))
        self.fullname.setPlaceholderText(lang["fullname"])
        self.fullname.setMaxLength(22)
        self.fullname.setText(user.getData("fullname"))
        self.fullname.textChanged.connect(self.checkFullname)
        self.fullname_container.adjustSize()
        # Fullname save button
        self.fullname_save = QPushButton(self.fullname_box)
        self.fullname_save.setObjectName("save_button")
        self.fullname_save.setCursor(self.profile_picture_save.cursor())
        self.fullname_save.setText(lang["save"])
        self.fullname_save.setFixedSize(self.profile_picture_save.size())
        self.fullname_save.move(
            self.fullname_container.x() + self.fullname_container.width() - self.fullname_save.width() - 20,
            self.fullname_container.y() + self.fullname_container.height() + 10)
        self.fullname_save.clicked.connect(self.saveFullname)

        # Password Widget
        self.password_box = QWidget(self)
        self.password_box.setObjectName(self.profile_picture_box.objectName())
        self.password_box.setVisible(False)
        self.password_box.setFixedSize(self.profile_picture_box.size())
        self.password_box.move(self.profile_picture_box.pos())
        # Password description
        self.password_description = QLabel(self.password_box)
        self.password_description.setObjectName(self.fullname_description.objectName())
        self.password_description.setWordWrap(True)
        self.password_description.setFixedWidth(self.fullname_description.width())
        self.password_description.move(self.fullname_description.pos())
        self.password_description.setText(lang["password_description"])
        self.password_description.adjustSize()
        # Password Container
        self.password_container = QWidget(self.password_box)
        self.password_container.setObjectName(self.fullname_container.objectName())
        self.password_container.setFixedWidth(self.password_description.width())
        self.password_container.move(
            self.password_description.x(),
            self.password_description.y() + self.password_description.height() + 10)
        # Current password label
        self.current_password_label = QLabel(self.password_container)
        self.current_password_label.setObjectName("field_label")
        self.current_password_label.setFixedSize(150, 25)
        self.current_password_label.move(20, 10)
        self.current_password_label.setText(lang["current_password"])
        # Current password textbox
        self.current_password = QLineEdit(self.password_container)
        self.current_password.setPlaceholderText(lang["current_password"])
        self.current_password.setEchoMode(QLineEdit.Password)
        self.current_password.setValidator(QRegExpValidator(QRegExp("^[a-zA-Z0-9_]{6,14}$")))
        self.current_password.setFixedSize(180, 25)
        self.current_password.move(
            self.current_password_label.x() + self.current_password_label.width(),
            self.current_password_label.y())
        self.current_password.textChanged.connect(self.checkPassword)
        # New password label
        self.new_password_label = QLabel(self.password_container)
        self.new_password_label.setObjectName(self.current_password_label.objectName())
        self.new_password_label.setFixedSize(self.current_password_label.size())
        self.new_password_label.move(
            self.current_password_label.x(),
            self.current_password_label.y() + self.current_password_label.height() + 10)
        self.new_password_label.setText(lang["new_password"])
        # New password textbox
        self.new_password = QLineEdit(self.password_container)
        self.new_password.setPlaceholderText(lang["new_password"])
        self.new_password.setEchoMode(QLineEdit.Password)
        self.new_password.setValidator(QRegExpValidator(QRegExp("^[a-zA-Z0-9_]{6,14}$")))
        self.new_password.setFixedSize(self.current_password.size())
        self.new_password.move(
            self.current_password.x(),
            self.new_password_label.y())
        self.new_password.textChanged.connect(self.checkPassword)
        # Confirm password label
        self.confirm_password_label = QLabel(self.password_container)
        self.confirm_password_label.setObjectName(self.current_password_label.objectName())
        self.confirm_password_label.setFixedSize(self.current_password_label.size())
        self.confirm_password_label.move(
            self.current_password_label.x(),
            self.new_password_label.y() + self.new_password_label.height() + 10)
        self.confirm_password_label.setText(lang["confirm_password"])
        # Confirm password textbox
        self.confirm_password = QLineEdit(self.password_container)
        self.confirm_password.setPlaceholderText(lang["confirm_password"])
        self.confirm_password.setEchoMode(QLineEdit.Password)
        self.confirm_password.setValidator(QRegExpValidator(QRegExp("^[a-zA-Z0-9_]{6,14}$")))
        self.confirm_password.setFixedSize(self.current_password.size())
        self.confirm_password.move(
            self.current_password.x(),
            self.confirm_password_label.y())
        self.confirm_password.textChanged.connect(self.checkPassword)
        self.password_container.adjustSize()
        # Password save button
        self.password_save = QPushButton(self.password_box)
        self.password_save.setObjectName("save_button")
        self.password_save.setCursor(self.profile_picture_save.cursor())
        self.password_save.setText(lang["save"])
        self.password_save.setDisabled(True)
        self.password_save.setFixedSize(self.profile_picture_save.size())
        self.password_save.move(
            self.password_container.x() + self.password_container.width() - self.password_save.width() - 20,
            self.password_container.y() + self.password_container.height() + 10)
        self.password_save.clicked.connect(self.savePassword)

        # PIN widget
        self.pin_box = QWidget(self)
        self.pin_box.setObjectName(self.profile_picture_box.objectName())
        self.pin_box.setVisible(False)
        self.pin_box.setFixedSize(self.profile_picture_box.size())
        self.pin_box.move(self.profile_picture_box.pos())
        # PIN description
        self.pin_description = QLabel(self.pin_box)
        self.pin_description.setObjectName(self.fullname_description.objectName())
        self.pin_description.setWordWrap(True)
        self.pin_description.setFixedWidth(self.fullname_description.width())
        self.pin_description.move(self.fullname_description.pos())
        self.pin_description.setText(lang["pin_description"])
        self.pin_description.adjustSize()
        # PIN container
        self.pin_container = QWidget(self.pin_box)
        self.pin_container.setObjectName(self.fullname_container.objectName())
        self.pin_container.setFixedWidth(self.pin_description.width())
        self.pin_container.move(
            self.pin_description.x(),
            self.pin_description.y() + self.pin_description.height() + 10)
        # Current PIN label
        self.current_pin_label = QLabel(self.pin_container)
        self.current_pin_label.setObjectName("field_label")
        self.current_pin_label.setFixedSize(150, 25)
        self.current_pin_label.move(20, 10)
        self.current_pin_label.setText(lang["current_pin"])
        # Current PIN
        self.current_pin = QLineEdit(self.pin_container)
        self.current_pin.setPlaceholderText(lang["current_pin"])
        self.current_pin.setEchoMode(QLineEdit.Password)
        self.current_pin.setValidator(QRegExpValidator(QRegExp("^[0-9]{4,4}$")))
        self.current_pin.setFixedSize(180, 25)
        self.current_pin.move(
            self.current_pin_label.x() + self.current_pin_label.width(),
            self.current_pin_label.y())
        self.current_pin.textChanged.connect(self.checkPIN)
        # New PIN Label
        self.new_pin_label = QLabel(self.pin_container)
        self.new_pin_label.setObjectName("field_label")
        self.new_pin_label.setFixedSize(self.current_pin_label.size())
        self.new_pin_label.move(
            self.current_pin_label.x(),
            self.current_pin_label.y() + self.current_pin_label.height() + 10)
        self.new_pin_label.setText(lang["new_pin"])
        # New PIN
        self.new_pin = QLineEdit(self.pin_container)
        self.new_pin.setPlaceholderText(lang["new_pin"])
        self.new_pin.setEchoMode(QLineEdit.Password)
        self.new_pin.setValidator(self.current_pin.validator())
        self.new_pin.setFixedSize(self.current_pin.size())
        self.new_pin.move(
            self.current_pin.x(),
            self.new_pin_label.y())
        self.new_pin.textChanged.connect(self.checkPIN)
        # Confirm PIN label
        self.confirm_pin_label = QLabel(self.pin_container)
        self.confirm_pin_label.setObjectName("field_label")
        self.confirm_pin_label.setFixedSize(self.current_pin_label.size())
        self.confirm_pin_label.move(
            self.current_pin_label.x(),
            self.new_pin_label.y() + self.new_pin_label.height() + 10)
        self.confirm_pin_label.setText(lang["confirm_pin"])
        # Confirm PIN
        self.confirm_pin = QLineEdit(self.pin_container)
        self.confirm_pin.setPlaceholderText(lang["confirm_pin"])
        self.confirm_pin.setEchoMode(QLineEdit.Password)
        self.confirm_pin.setValidator(self.current_pin.validator())
        self.confirm_pin.setFixedSize(self.current_pin.size())
        self.confirm_pin.move(
            self.current_pin.x(),
            self.confirm_pin_label.y())
        self.confirm_pin.textChanged.connect(self.checkPIN)
        self.pin_container.adjustSize()
        # PIN save button
        self.pin_save = QPushButton(self.pin_box)
        self.pin_save.setObjectName("save_button")
        self.pin_save.setCursor(self.profile_picture_save.cursor())
        self.pin_save.setText(lang["save"])
        self.pin_save.setDisabled(True)
        self.pin_save.setFixedSize(self.profile_picture_save.size())
        self.pin_save.move(
            self.pin_container.x() + self.pin_container.width() - self.pin_save.width() - 20,
            self.pin_container.y() + self.pin_container.height() + 10)
        self.pin_save.clicked.connect(self.savePIN)

        # Language box
        self.language_box = QWidget(self)
        self.language_box.setObjectName(self.profile_picture_box.objectName())
        self.language_box.setVisible(False)
        self.language_box.setFixedSize(self.profile_picture_box.size())
        self.language_box.move(self.profile_picture_box.pos())
        # Language description
        self.language_description = QLabel(self.language_box)
        self.language_description.setObjectName(self.fullname_description.objectName())
        self.language_description.setWordWrap(True)
        self.language_description.setFixedWidth(self.fullname_description.width())
        self.language_description.move(self.fullname_description.pos())
        self.language_description.setText(lang["language_description"])
        self.language_description.adjustSize()
        # Language container
        self.language_container = QWidget(self.language_box)
        self.language_container.setObjectName(self.fullname_container.objectName())
        self.language_container.setFixedWidth(self.language_description.width())
        self.language_container.move(
            self.language_description.x(),
            self.language_description.y() + self.language_description.height() + 10)
        # Language options
        self.language_options = QWidget(self.language_container)
        self.language_options.setObjectName("language_options")
        self.language_options.setFixedSize(300, 30)
        self.language_options.move(
            (self.language_container.width() - self.language_options.width()) / 2,
            30)
        
        # Language item - English
        self.language_english = QPushButton(self.language_options)
        self.language_english.setObjectName("language_item")
        self.language_english.setCursor(QCursor(Qt.PointingHandCursor))
        self.language_english.setFixedSize(
            self.language_options.width() / 3,
            self.language_options.height())
        self.language_english.setText(lang["language_english"])
        self.language_english.clicked.connect(lambda: self.setLanguageAnimation("english"))
        # Language item - Vietnamese
        self.language_vietnamese = QPushButton(self.language_options)
        self.language_vietnamese.setObjectName(self.language_english.objectName())
        self.language_vietnamese.setCursor(self.language_english.cursor())
        self.language_vietnamese.setFixedSize(self.language_english.size())
        self.language_vietnamese.move(
            self.language_english.x() + self.language_english.width(),
            self.language_english.y())
        self.language_vietnamese.setText(lang["language_vietnamese"])
        self.language_vietnamese.clicked.connect(lambda: self.setLanguageAnimation("vietnamese"))
        # Language item - Japanese
        self.language_japanese = QPushButton(self.language_options)
        self.language_japanese.setObjectName(self.language_english.objectName())
        self.language_japanese.setCursor(self.language_english.cursor())
        self.language_japanese.setFixedSize(self.language_english.size())
        self.language_japanese.move(
            self.language_vietnamese.x() + self.language_vietnamese.width(),
            self.language_vietnamese.y())
        self.language_japanese.setText(lang["language_japanese"])
        self.language_japanese.clicked.connect(lambda: self.setLanguageAnimation("japanese"))
        # Language selection
        self.language_selection = QPushButton(self.language_container)
        self.language_selection.setObjectName("language_selection")
        self.language_selection.setCursor(QCursor(Qt.PointingHandCursor))
        self.language_selection.setFixedSize(
            self.language_english.width(),
            self.language_english.height())
        if user.getData("language") == "english":
            self.language_selected = "english"
            self.language_selection.setText(lang["language_english"])
            self.language_selection.move(
                self.language_options.x() + self.language_english.x(),
                self.language_options.y())
        elif user.getData("language") == "vietnamese":
            self.language_selected = "vietnamese"
            self.language_selection.setText(lang["language_vietnamese"])
            self.language_selection.move(
                self.language_options.x() + self.language_vietnamese.x(),
                self.language_options.y())
        elif user.getData("language") == "japanese":
            self.language_selected = "japanese"
            self.language_selection.setText(lang["language_japanese"])
            self.language_selection.move(
                self.language_options.x() + self.language_japanese.x(),
                self.language_options.y())
        self.lngstn_shadow = QGraphicsDropShadowEffect()
        self.lngstn_shadow.setBlurRadius(15)
        self.lngstn_shadow.setOffset(1)
        self.language_selection.setGraphicsEffect(self.lngstn_shadow)
        self.language_container.adjustSize()
        # Language save button
        self.language_save = QPushButton(self.language_box)
        self.language_save.setObjectName(self.profile_picture_save.objectName())
        self.language_save.setCursor(self.profile_picture_save.cursor())
        self.language_save.setText(lang["save"])
        self.language_save.setFixedSize(self.profile_picture_save.size())
        self.language_save.move(
            self.language_container.x() + self.language_container.width() - self.language_save.width() - 20,
            self.language_container.y() + self.language_container.height() + 10)
        self.language_save.clicked.connect(self.saveLanguage)
        
        # Theme box
        self.theme_box = QWidget(self)
        self.theme_box.setObjectName(self.profile_picture_box.objectName())
        self.theme_box.setVisible(False)
        self.theme_box.setFixedSize(self.profile_picture_box.size())
        self.theme_box.move(self.profile_picture_box.pos())
        # Theme description
        self.theme_description = QLabel(self.theme_box)
        self.theme_description.setObjectName(self.fullname_description.objectName())
        self.theme_description.setWordWrap(True)
        self.theme_description.setFixedWidth(self.fullname_description.width())
        self.theme_description.move(self.fullname_description.pos())
        self.theme_description.setText(lang["theme_description"])
        self.theme_description.adjustSize()
        # Theme container
        self.theme_container = QWidget(self.theme_box)
        self.theme_container.setObjectName(self.fullname_container.objectName())
        self.theme_container.setFixedWidth(self.theme_description.width())
        self.theme_container.move(
            self.theme_description.x(),
            self.theme_description.y() + self.theme_description.height() + 10)
        # Light theme button
        self.theme_light_button = QPushButton(self.theme_container)
        self.theme_light_button.setObjectName("theme_button")
        self.theme_light_button.setFixedSize(104, 65)
        self.theme_light_button.move(
            (self.theme_container.width() - self.theme_light_button.width()*2 - 40) / 2,
            20)
        self.theme_light_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.tlb_shadow = QGraphicsDropShadowEffect()
        self.tlb_shadow.setBlurRadius(15)
        self.tlb_shadow.setOffset(0)
        self.theme_light_button.setGraphicsEffect(self.tlb_shadow)
        self.theme_light_button.clicked.connect(lambda: self.setTheme("light"))
        # Light them image
        self.theme_light_image = QLabel(self.theme_light_button)
        self.theme_light_image.setObjectName("theme_icon")
        self.theme_light_image.setFixedSize(self.theme_light_button.size())
        self.theme_light_pixmap = QPixmap("./image/gui/light_theme.png")
        self.theme_light_pixmap_scaled = self.theme_light_pixmap.scaled(
            self.theme_light_image.width(),
            self.theme_light_image.height(),
            transformMode=Qt.SmoothTransformation)
        rounded = QPixmap(self.theme_light_pixmap_scaled)
        rounded.fill(QColor("transparent"))
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(self.theme_light_pixmap_scaled))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(
            self.theme_light_pixmap_scaled.rect(),
            5, 5)
        painter.end()
        self.theme_light_image.setPixmap(rounded)
        del rounded
        del painter
        # Light theme label
        self.theme_light_label = QLabel(self.theme_container)
        self.theme_light_label.setObjectName("theme_label")
        self.theme_light_label.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        self.theme_light_label.setFixedSize(
            self.theme_light_button.width(),
            20)
        self.theme_light_label.move(
            self.theme_light_button.x(),
            self.theme_light_button.y() + self.theme_light_button.height() + 10)
        self.theme_light_label.setText(lang["theme_light"])     
        # Dark theme button
        self.theme_dark_button = QPushButton(self.theme_container)
        self.theme_dark_button.setFixedSize(self.theme_light_button.size())
        self.theme_dark_button.move(
            self.theme_light_button.x() + self.theme_light_button.width() + 40,
            self.theme_light_button.y())
        self.theme_dark_button.setCursor(self.theme_light_button.cursor())
        self.tdb_shadow = QGraphicsDropShadowEffect()
        self.tdb_shadow.setBlurRadius(self.tlb_shadow.blurRadius())
        self.tdb_shadow.setOffset(self.tlb_shadow.offset())
        self.theme_dark_button.setGraphicsEffect(self.tdb_shadow)
        self.theme_dark_button.clicked.connect(lambda: self.setTheme("dark"))
        # Dark theme image
        self.theme_dark_image = QLabel(self.theme_dark_button)
        self.theme_dark_image.setObjectName(self.theme_light_image.objectName())
        self.theme_dark_image.setFixedSize(
            self.theme_dark_button.width(),
            self.theme_dark_button.height())
        self.theme_dark_pixmap = QPixmap("./image/gui/dark_theme.png")
        self.theme_dark_pixmap_scaled = self.theme_dark_pixmap.scaled(
            self.theme_dark_image.width(),
            self.theme_dark_image.height(),
            transformMode=Qt.SmoothTransformation)
        rounded = QPixmap(self.theme_dark_pixmap_scaled)
        rounded.fill(QColor("transparent"))
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(self.theme_dark_pixmap_scaled))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(
            self.theme_dark_pixmap_scaled.rect(),
            5, 5)
        painter.end()
        self.theme_dark_image.setPixmap(rounded)
        del rounded
        del painter
        # Dark theme label
        self.theme_dark_label = QLabel(self.theme_container)
        self.theme_dark_label.setObjectName(self.theme_light_label.objectName())
        self.theme_dark_label.setAlignment(self.theme_light_label.alignment())
        self.theme_dark_label.setFixedSize(self.theme_light_label.size())
        self.theme_dark_label.move(
            self.theme_dark_button.x(),
            self.theme_light_label.y())
        self.theme_dark_label.setText(lang["theme_dark"])
        # Theme selection border
        self.theme_selection = QPushButton(self.theme_container)
        self.theme_selection.setCursor(QCursor(Qt.PointingHandCursor))
        self.theme_selection.setObjectName("theme_selection")
        self.ts_shadow = QGraphicsDropShadowEffect()
        self.ts_shadow.setBlurRadius(20)
        self.ts_shadow.setOffset(0)
        self.ts_shadow.setColor(QColor(0, 0, 0))
        self.theme_selection.setGraphicsEffect(self.ts_shadow)
        self.theme_selection.setFixedSize(
            self.theme_light_button.width() + 4,
            self.theme_light_button.height() + 4)
        if user.getData("theme") == "light":
            self.theme_selection.move(
                self.theme_light_button.x() - 2,
                self.theme_light_button.y() - 2)
        else:
            self.theme_selection.move(
                self.theme_dark_button.x() - 2,
                self.theme_dark_button.y() - 2)
        self.theme_selecting = user.getData("theme")
        self.theme_container.adjustSize()
        # Theme save button
        self.theme_save = QPushButton(self.theme_box)
        self.theme_save.setObjectName("save_button")
        self.theme_save.setFixedSize(self.profile_picture_save.size())
        self.theme_save.move(
            self.theme_container.x() + self.theme_container.width() - self.theme_save.width() - 20,
            self.theme_container.y() + self.theme_container.height() + 10)
        self.theme_save.setText(lang["save"])
        self.theme_save.setCursor(self.profile_picture_save.cursor())
        self.theme_save.clicked.connect(self.saveTheme)

    def getProfilePicture(self):
        # Open file dialog to get new picture
        self.imageType = "JPEG Files (*.jpg *jpeg);;PNG (*.png)"
        self.imageName, self.imageType = QFileDialog.getOpenFileName(self, "Open", "",  self.imageType)
        if self.imageName != "":
            # Open crop image dialog
            self.CropImageDialog = CropImageDialog(
                image_path=self.imageName,
                button_text=lang["crop"],
                theme=self.parent().parent().styleSheet())
            if self.CropImageDialog.exec():
                # Set new picture as pixmap to GUI
                self.picture_path = self.imageName
                self.picture = self.CropImageDialog.getImagePixmap()
                self.picture_scaled = self.picture.scaled(
                    self.profile_picture.width() - 4, self.profile_picture.height() - 4,
                    aspectRatioMode=Qt.IgnoreAspectRatio, transformMode=Qt.SmoothTransformation)
                self.profile_picture.setPixmap(self.picture_scaled)
                self.newImage = self.CropImageDialog.getImage()
                # Write new image name to data file
                user.setData("picture", "profile_picture.jpg")
        else:
            pass

    def removeProfilePicture(self):
        # Set default avatar
        self.picture_path = None
        self.picture = QPixmap("./image/default_avatar.png")
        self.profile_picture.setPixmap(self.picture)
        # Clear user profile picture data
        user.setData("picture", None)

    def saveProfilePicture(self):
        if self.picture_path != self.old_path and self.picture_path != None:
            # Set picture name
            self.picturefolder_path = "./data/{0}/profile_pictures/".format(user.getData("username"))
            self.pictureName = "profile_picture.jpg"
            # Save new picture
            self.newImage_path = self.picturefolder_path + self.pictureName
        try:
            user.saveData()
            message = QMessageBoxX(
                icon="information",
                boldtext=lang["saved_successfully"],
                text=lang["saved_successfully_description"],
                stylesheet=self.parent().parent().styleSheet())
            message.exec()
            if self.picture_path != None:
                # Get photo and resize
                self.newImage.save(self.newImage_path)
                self.parent().parent().pfpic = QPixmap(self.newImage_path)
                self.parent().parent().pfpic_scaled = self.parent().parent().pfpic.scaled(
                    self.parent().parent().profile_picture.width(),
                    self.parent().parent().profile_picture.height(),
                    aspectRatioMode=Qt.IgnoreAspectRatio,
                    transformMode=Qt.SmoothTransformation)
            else:
                self.parent().parent().pfpic_scaled = QPixmap("./image/default_avatar.png")
            rounded = QPixmap(self.parent().parent().pfpic_scaled.size())
            rounded.fill(QColor("transparent"))
            # Create rounded picture
            painter = QPainter(rounded)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(QBrush(self.parent().parent().pfpic_scaled))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(
                self.parent().parent().pfpic_scaled.rect(),
                self.parent().parent().profile_picture.width() / 2,
                self.parent().parent().profile_picture.height() / 2)
            self.parent().parent().profile_picture.setPixmap(rounded)
            painter.end()
            del painter
            del rounded
            self.settings_list_widget.setCurrentItem(None)
            self.profile_picture_box.setVisible(False)
        except PermissionError:
            message = QMessageBoxX(
                icon="warning",
                boldtext=lang["permission_denied"],
                text=lang["permission_denied_description"],
                stylesheet=self.parent().parent().styleSheet())
            message.exec()

    def checkFullname(self):
        if len(self.fullname.text()):
            self.fullname_save.setDisabled(False)
        else:
            self.fullname_save.setDisabled(True)

    def saveFullname(self):
        user.setData("fullname", self.fullname.text())
        try:
            user.saveData()
            self.parent().parent().profile_button.setText(self.fullname.text())
            self.parent().parent().profile_fullname.setText(self.fullname.text())
            message = QMessageBoxX(
                icon="information",
                boldtext=lang["saved_successfully"],
                text=lang["saved_successfully_description"],
                stylesheet=self.parent().parent().styleSheet())
            message.exec()
            self.settings_list_widget.setCurrentItem(None)
            self.fullname_box.setVisible(False)
        except PermissionError:
            message = QMessageBoxX(
                icon="warning",
                boldtext=lang["permission_denied"],
                text=lang["permission_denied_description"],
                stylesheet=self.parent().parent().styleSheet())
            message.exec()

    def checkPassword(self):
        # Password validating condition
        self.curpw_val = len(self.current_password.text()) >= 6
        self.newpw_val = len(self.new_password.text()) >= 6
        self.cfmpw_val = len(self.confirm_password.text()) >= 6
        if self.curpw_val and self.newpw_val and self.cfmpw_val:
            self.password_save.setDisabled(False)
        else:
            self.password_save.setDisabled(True)

    def savePassword(self):
        if self.current_password.text() != user.getData("password"):
            message = QMessageBoxX(
                icon="warning",
                boldtext=lang["wrong_current_password"],
                text=lang["wrong_current_password_description"],
                stylesheet=self.parent().parent().styleSheet())
            message.exec()
        elif self.confirm_password.text() != self.new_password.text():
            message = QMessageBoxX(
                icon="warning",
                boldtext=lang["wrong_confirm_password"],
                text=lang["wrong_confirm_password_description"],
                stylesheet=self.parent().parent().styleSheet())
            message.exec()
        else:
            try:
                user.setData("password", self.confirm_password.text())
                user.saveData()
                message = QMessageBoxX(
                    icon="information",
                    boldtext=lang["saved_successfully"],
                    text=lang["saved_successfully_description"],
                    stylesheet=self.parent().parent().styleSheet())
                message.exec()
                self.settings_list_widget.setCurrentItem(None)
                self.current_password.clear()
                self.new_password.clear()
                self.confirm_password.clear()
                self.password_box.setVisible(False)
            except PermissionError:
                message = QMessageBoxX(
                    icon="warning",
                    boldtext=lang["permission_denied"],
                    text=lang["permission_denied_description"],
                    stylesheet=self.parent().parent().styleSheet())
                message.exec()

    def checkPIN(self):
        # PIN validating conditions
        self.curpin_val = len(self.current_pin.text()) >= 4
        self.newpin_val = len(self.new_pin.text()) >= 4
        self.cfpin_val = len(self.confirm_pin.text()) >= 4
        if self.curpin_val and self.newpin_val and self.cfpin_val:
            self.pin_save.setDisabled(False)
        else:
            self.pin_save.setDisabled(True)
    
    def savePIN(self):
        if self.current_pin.text() != user.getData("pin"):
            message = QMessageBoxX(
                icon="warning",
                boldtext=lang["wrong_current_pin"],
                text=lang["wrong_current_pin_description"],
                stylesheet=self.parent().parent().styleSheet())
            message.exec()
        elif self.confirm_pin.text() != self.new_pin.text():
            message = QMessageBoxX(
                icon="warning",
                boldtext=lang["wrong_confirm_pin"],
                text=lang["wrong_confirm_pin_description"],
                stylesheet=self.parent().parent().styleSheet())
            message.exec()
        else:
            try:
                user.setData("pin", self.confirm_pin.text())
                user.saveData()
                message = QMessageBoxX(
                    icon="information",
                    boldtext=lang["saved_successfully"],
                    text=lang["saved_successfully_description"],
                    stylesheet=self.parent().parent().styleSheet())
                message.exec()
                self.settings_list_widget.setCurrentItem(None)
                self.current_pin.clear()
                self.new_pin.clear()
                self.confirm_pin.clear()
                self.pin_box.setVisible(False)
            except PermissionError:
                message = QMessageBoxX(
                    icon="warning",
                    boldtext=lang["permission_denied"],
                    text=lang["permission_denied_description"],
                    stylesheet=self.parent().parent().styleSheet())
                message.exec()

    def setLanguageAnimation(self, language):
        self.language_options.setDisabled(True)
        self.lang_animation = QPropertyAnimation(self.language_selection, b"pos")
        self.lang_animation.setDuration(200)
        self.lang_animation.setEasingCurve(QEasingCurve.OutCirc)
        self.current_pos = self.language_selection.pos()
        self.lang_animation.setStartValue(self.current_pos)
        if language == "english":
            self.language_selection.setText(lang["language_english"])
            self.lang_animation.setEndValue(QPoint(
                self.language_options.x() + self.language_english.x(),
                self.language_options.y() + self.language_english.y()))
            self.lang_animation.start()
            self.lang_animation.finished.connect(lambda: self.setLanguagePosition("english"))
        elif language == "vietnamese":
            self.language_selection.setText(lang["language_vietnamese"])
            self.lang_animation.setEndValue(QPoint(
                self.language_options.x() + self.language_vietnamese.x(),
                self.language_options.y() + self.language_vietnamese.y()))
            self.lang_animation.start()
            self.lang_animation.finished.connect(lambda: self.setLanguagePosition("vietnamese"))
        elif language == "japanese":
            self.language_selection.setText(lang["language_japanese"])
            self.lang_animation.setEndValue(QPoint(
                self.language_options.x() + self.language_japanese.x(),
                self.language_options.y() + self.language_japanese.y()))
            self.lang_animation.start()
            self.lang_animation.finished.connect(lambda: self.setLanguagePosition("japanese"))

    def setLanguagePosition(self, language):
        self.language_options.setDisabled(False)
        self.language_selected = language
        if language == "english":
            self.language_selection.move(
                self.language_options.x() + self.language_english.x(),
                self.language_options.y() + self.language_english.y())
        elif language == "vietnamese":
            self.language_selection.move(
                self.language_options.x() + self.language_vietnamese.x(),
                self.language_options.y() + self.language_vietnamese.y())
        elif language == "japanese":
            self.language_selection.move(
                self.language_options.x() + self.language_japanese.x(),
                self.language_options.y() + self.language_japanese.y())

    def saveLanguage(self):
        user.setData("language", self.language_selected)
        try:
            user.saveData()
            message = QMessageBoxX(
                icon="information",
                boldtext=lang["reboot_require"],
                text=lang["reboot_require_description"],
                ok=True,
                cancel=True,
                stylesheet=self.parent().parent().styleSheet())
            if message.exec():
                self.parent().parent().close()
                main.user = user
                main.mainui = main.MainUI(user.getData("language"))
                main.mainui.show()
            else:
                message = QMessageBoxX(
                    icon="information",
                    boldtext=lang["saved_successfully"],
                    text=lang["saved_successfully_description"],
                    stylesheet=self.parent().parent().styleSheet())
                message.exec()
        except PermissionError:
            message = QMessageBoxX(
                icon="warning",
                boldtext=lang["permission_denied"],
                text=lang["permission_denied_description"],
                stylesheet=self.parent().parent().styleSheet())
            message.exec()


    def setTheme(self, theme):
        if theme == "light":
            self.parent().parent().setStyleSheet(style.basegui)
            self.theme_selection.move(
                self.theme_light_button.x() - 2,
                self.theme_light_button.y() - 2)
            self.theme_selecting = "light"
        else:
            self.parent().parent().setStyleSheet(style.basegui_darktheme)
            self.theme_selection.move(
                self.theme_dark_button.x() - 2,
                self.theme_dark_button.y() - 2)
            self.theme_selecting = "dark"

    def saveTheme(self):
        user.setData("theme", self.theme_selecting)
        try:
            user.saveData()
            message = QMessageBoxX(
                icon="information",
                boldtext=lang["saved_successfully"],
                text=lang["saved_successfully_description"],
                stylesheet=self.parent().parent().styleSheet())
            message.exec()
            self.settings_list_widget.setCurrentItem(None)
            self.theme_box.setVisible(False)
        except PermissionError:
            message = QMessageBoxX(
                icon="warning",
                boldtext=lang["permission_denied"],
                text=lang["permission_denied_description"],
                stylesheet=self.parent().parent().styleSheet())
            message.exec()



    def showSettingsWidget(self):
        currentIndex = self.settings_list_widget.currentRow()
        widgetList = [
            self.profile_picture_box,
            self.fullname_box,
            self.password_box,
            self.pin_box,
            self.language_box,
            self.theme_box]
        try:
            for widget in widgetList:
                widget.setVisible(False)
            widgetList[currentIndex].setVisible(True)
        except:
            pass








        
