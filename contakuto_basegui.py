import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import contakuto_stylesheet as style
from lang import *
import time
from PIL import Image

class QListWidgetX(QWidget):
    def __init__ (self, parent = None):
        super().__init__()
        self.itemID = None
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.textQVBoxLayout = QVBoxLayout()
        self.textUpQLabel    = QLabel()
        self.textUpQLabel.setObjectName("listItem_upLabel")
        self.textUpQLabel.setTextInteractionFlags
        self.textDownQLabel  = QLabel()
        self.textDownQLabel.setObjectName("listItem_downLabel")
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout  = QHBoxLayout()
        self.iconQLabel      = QLabel()
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)

    def setID(self, id):
        self.itemID = id

    def getID(self):
        return self.itemID

    def setTextUp(self, text):
        self.textUpQLabel.setText(text)

    def setTextUpStyleSheet(self, stylesheet):
        self.textUpQLabel.setStyleSheet(stylesheet)

    def setTextDown(self, text):
        self.textDownQLabel.setText(text)

    def setTextDownStyleSheet(self, stylesheet):
        self.textDownQLabel.setStyleSheet(stylesheet)

    def setIcon(self, image):
        self.iconQLabel.setPixmap(image)


class QMainWindowX(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        # Setting Translucent and Frameless Window
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.oldPos = self.pos()
        self.oldX = self.x()
        self.oldY = self.y()
        self.history = []
        self.back_history = []

        # Create screen resolution object
        #self.wx = App(False)
        #self.screenres = GetDisplaySize()

        # Setting Custom Background, Window Border and Shadow
        self.container = QWidget(self)
        self.container.setObjectName("container")
        self.container.setGeometry(QRect(
            20,
            20,
            self.width() - 40,
            self.height() - 40))
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(10)
        self.shadow.setOffset(0, 0)
        self.shadow.setColor(QColor(0, 0, 0, 180))
        self.container.setGraphicsEffect(self.shadow)

        # Setting Font Family and Font Size
        self.font = QFont("Helvetica Neue", 14)
        self.font.setStyleStrategy(QFont.PreferAntialias)
        self.setFont(QFont(self.font))

        # Custom Title Bar
        self.titlebar = QLabel(self.container)
        self.titlebar.setObjectName("titlebar")
        self.titlebar.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)
        self.titlebar.setGeometry(QRect(
            0, 0, self.container.width(), 40))

        # Exit Button
        self.exit_button = QPushButton(self.titlebar)
        self.exit_button.setObjectName("exit_button")
        self.exit_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.exit_button.setFixedSize(16, 16)
        self.exit_button.move(17, 12)
        self.exit_button.clicked.connect(self.closeWindow)

        # Minimize Button
        self.minimize_button = QPushButton(self.titlebar)
        self.minimize_button.setObjectName("minimize_button")
        self.minimize_button.setCursor(self.exit_button.cursor())
        self.minimize_button.setFixedSize(self.exit_button.width(), self.exit_button.height())
        self.minimize_button.move(
            self.exit_button.x() + self.exit_button.width() + 10, 
            self.exit_button.y())
        self.minimize_button.clicked.connect(self.showMinimized)

        # Fullscreen Button
        self.fullscreen_button = QPushButton(self.titlebar)
        self.fullscreen_button.setDisabled(True)
        self.fullscreen_button.setObjectName("fullscreen_button")
        self.fullscreen_button.setCursor(self.exit_button.cursor())
        self.fullscreen_button.setFixedSize(self.exit_button.width(), self.exit_button.height())
        self.fullscreen_button.move(
            self.minimize_button.x() + self.minimize_button.width() + 10, 
            self.minimize_button.y())
        
        # Back Button
        self.back_button = QPushButton(self.titlebar)
        self.back_button.setObjectName("back_button")
        self.back_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_button.setDisabled(True)
        self.back_button.setFixedSize(34, 24)
        self.back_button.move(
            self.fullscreen_button.x() + 40,
            (self.titlebar.height() - self.back_button.height()) / 2)
        self.back_button.clicked.connect(self.backScreen)

        # Forward Button
        self.forward_button = QPushButton(self.titlebar)
        self.forward_button.setObjectName("forward_button")
        self.forward_button.setCursor(self.back_button.cursor())
        self.forward_button.setDisabled(True)
        self.forward_button.setFixedSize(self.back_button.width(), self.back_button.height())
        self.forward_button.move(
            self.back_button.x() + self.back_button.width(), 
            self.back_button.y())
        self.forward_button.clicked.connect(self.forwardScreen)

        # Add Button
        self.add_button = QPushButton(self.titlebar)
        self.add_button.setObjectName("add_button")
        self.add_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.add_button.setGeometry(QRect(
            self.forward_button.x() + self.forward_button.width() + 10,
            self.back_button.y(),
            40, 
            self.back_button.height()))
        
        # Search Button
        self.search_button = QPushButton(self.titlebar)
        self.search_button.setObjectName("search_button")
        self.search_button.setCursor(self.add_button.cursor())
        self.search_button.setGeometry(QRect(
            self.add_button.x() + self.add_button.width(),
            self.add_button.y(),
            self.add_button.width(), 
            self.add_button.height()))

        # Search Textbox
        self.search = QLineEdit()
        self.search.setObjectName("searchbox")
        self.search.setFixedSize(200, self.titlebar.height() - 14)
        self.search.move(
            self.titlebar.width() - self.search.width() - 8,
            8)
        self.search.setMaxLength(50)
        self.search_icon = QLabel(self.search)
        self.search_icon.move(1, 1)
        self.search_icon_pixmap = QPixmap("./image/gui/search_icon.png")
        self.search_icon.setPixmap(self.search_icon_pixmap)
        self.search_icon.setFixedSize(self.search_icon_pixmap.size())

        # Search Textbox
        self.profile_button = QPushButton(self.titlebar)
        self.profile_button.setObjectName("searchbox")
        self.profile_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.profile_button.setFixedSize(200, self.add_button.height())
        self.profile_button.move(
            self.titlebar.width() - self.search.width() - 8,
            8)
        self.profile_button.clicked.connect(self.ProfilePopup)

        # Settings Button
        self.settings_button = QPushButton(self.titlebar)
        self.settings_button.setObjectName("settings_button")
        self.settings_button.setVisible(False)
        self.settings_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.settings_button.setFixedSize(self.add_button.width(), self.add_button.height())
        self.settings_button.move(
            self.profile_button.x() - 10 -self.settings_button.width(),
            self.add_button.y())

        # Contacts Button
        self.contacts_button = QPushButton(self.titlebar)
        self.contacts_button.setObjectName("contacts_button")
        self.contacts_button.setVisible(False)
        self.contacts_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.contacts_button.setFixedSize(self.settings_button.width(), self.settings_button.height())
        self.contacts_button.move(
            self.settings_button.x() - self.contacts_button.width(),
            self.settings_button.y())

        # Sidebar
        self.sidebar = QWidget(self.container)
        self.sidebar.setObjectName("sidebar")
        self.sidebar.move(1, self.titlebar.height())
        self.sidebar.setFixedSize(253, self.container.height() - self.titlebar.height() - 1)

        # Profile Popup
        self.profile_popup = QWidget(self.container)
        self.profile_popup.setObjectName("profile_popup")
        self.profile_popup.setVisible(False)
        self.profile_popup.setFixedSize(self.profile_button.width(), 215)
        self.profile_popup.move(
            self.profile_button.x(), 
            self.titlebar.height())
        self.pfshadow = QGraphicsDropShadowEffect()
        self.pfshadow.setBlurRadius(15) 
        self.pfshadow.setOffset(0)
        self.profile_popup.setGraphicsEffect(self.pfshadow)

        # Profile picture
        self.profile_picture = QLabel(self.profile_popup)
        self.profile_picture.setFixedSize(110, 110)
        self.profile_picture.move(
            (self.profile_popup.width() - self.profile_picture.width()) / 2,
            15)
        self.pfbtn_posX = (self.profile_popup.width() - 170) / 2

        # Profile fullname
        self.profile_fullname = QLabel(self.profile_popup)
        self.profile_fullname.setObjectName("profile_fullname")
        self.profile_fullname.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.profile_fullname.setFixedSize(
            self.profile_popup.width() - 30,
            20)
        self.profile_fullname.move(
            (self.profile_popup.width() - self.profile_fullname.width()) / 2,
            self.profile_picture.y() + self.profile_picture.height() + 5)

        # Profile username
        self.profile_username = QLabel(self.profile_popup)
        self.profile_username.setObjectName("profile_username")
        self.profile_username.setAlignment(self.profile_fullname.alignment())
        self.profile_username.setFixedSize(self.profile_fullname.width(), 20)
        self.profile_username.move(
            self.profile_fullname.x(),
            self.profile_fullname.y() + self.profile_fullname.height())


        # Edit profile button
        self.edit_profile_button = QPushButton(self.profile_popup)
        self.edit_profile_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.edit_profile_button.setFixedSize(80, 25)
        self.edit_profile_button.move(
            self.pfbtn_posX,
            self.profile_username.y() + self.profile_username.height() + 10)

        # SignOut button
        self.signout_button = QPushButton(self.profile_popup)
        self.signout_button.setCursor(self.edit_profile_button.cursor())
        self.signout_button.setFixedSize(
            self.edit_profile_button.width(),
            self.edit_profile_button.height())
        self.signout_button.move(
            self.edit_profile_button.x() + self.edit_profile_button.width() + 10,
            self.edit_profile_button.y())

        # Home Widget Main Label
        self.homelabel = QLabel

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        self.oldX = event.globalX()
        self.oldY = event.globalY()
        if not self.profile_popup.underMouse():
            self.profile_popup.setVisible(False)

    # Custom Window Moving Event
    def mouseMoveEvent(self, event):
        #time.sleep(0.02)  # sleep for 20ms
        delta = QPoint(event.globalPos() - self.oldPos)
        if self.titlebar.underMouse():
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
            self.oldX = event.globalX()
            self.oldY = event.globalY()

    def closeWindow(self):
        for i in range(10):
            i = i / 10
            self.setWindowOpacity(1 - i)
            self.move(self.x() + 5, self.y() + 3)
            self.setFixedSize(self.width() - 10, self.height() - 6)
            time.sleep(0.0005)
        sys.exit()

    def clearBackHistory(self):
        self.back_history = []
        self.forward_button.setDisabled(True)

    def backScreen(self):
        try:
            self.history[-1].close()
            self.history[-2].show()
        except IndexError:
            pass
        self.back_history.append(self.history[-1])
        del self.history[-1]
        if not len(self.history):
            self.back_button.setDisabled(True)
        else:
            self.back_button.setDisabled(False)
        if not len(self.back_history):
            self.forward_button.setDisabled(True)
        else:
            self.forward_button.setDisabled(False)

    def forwardScreen(self):
        try:
            self.back_history[-1].show()
            self.back_history[-1].raise_()
        except:
            pass
        if len(self.back_history):
            self.history.append(self.back_history[-1])
            del self.back_history[-1]
        if not len(self.back_history):
            self.forward_button.setDisabled(True)
        else:
            self.forward_button.setDisabled(False)
        if not len(self.history):
            self.back_button.setDisabled(True)
        else:
            self.back_button.setDisabled(False)

    def ProfilePopup(self):
        self.profile_popup.setVisible(False)
        self.profile_popup.raise_()
        self.titlebar.raise_()
        self.profile_popup.setVisible(True)
        self.profile_button.setFocus()

    def settingInterface(self, lang):
        self.resize(
            self.container.width() + 40,
            self.container.height() + 40)
        self.titlebar.setGeometry(QRect(
            0, 0, self.container.width(), 40))
        self.search.move(
            self.titlebar.width() - self.search.width() - 8,
            8)
        self.profile_button.move(
            self.titlebar.width() - self.search.width() - 8,
            8)
        self.settings_button.move(
            self.profile_button.x() - 10 -self.settings_button.width(),
            self.add_button.y())
        self.contacts_button.move(
            self.settings_button.x() - self.contacts_button.width(),
            self.settings_button.y())
        self.sidebar.setFixedSize(self.sidebar.width(), self.container.height() - self.titlebar.height() - 1)
        self.profile_popup.move(
            self.profile_button.x(), 
            self.titlebar.height())
        self.search.setPlaceholderText(lang["search"])
        self.edit_profile_button.setText(lang["edit"])
        self.signout_button.setText(lang["signout"])


class QMessageBoxX(QDialog):
    def __init__(self, icon=None, boldtext="", text="", ok=True, oktext="OK", cancel=False, canceltext="Cancel", stylesheet=style.basegui):
        super().__init__()
        # Setting Translucent and Frameless Window
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet(stylesheet)
        self.oldPos = self.pos()
        self.oldX = self.x()
        self.oldY = self.y()
        # Create screen resolution object
        #self.wx = App(False)
        #self.screenres = GetDisplaySize()
        
        self.iconType = icon
        # Setting Custom Background, Window Border and Shadow
        self.container = QWidget(self)
        self.container.setObjectName("messagebox_container")
        self.container.move(20, 20)
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(10)
        self.shadow.setOffset(0, 0)
        self.shadow.setColor(QColor(0, 0, 0, 180))
        self.container.setGraphicsEffect(self.shadow)

        # Setting Font Family and Font Size
        self.font = QFont("Helvetica Neue", 14)
        self.font.setStyleStrategy(QFont.PreferAntialias)
        self.setFont(QFont(self.font))

        # Custom Title Bar
        self.titlebar = QLabel(self.container)
        self.titlebar.setObjectName("titlebar")
        self.titlebar.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)
        self.titlebar.move(0, 0)

        # Exit Button
        self.exit_button = QPushButton(self.titlebar)
        self.exit_button.setObjectName("exit_button")
        self.exit_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.exit_button.setFixedSize(14, 14)
        self.exit_button.move(12, 8)
        self.exit_button.clicked.connect(self.close)

        # Minimize Button
        self.minimize_button = QPushButton(self.titlebar)
        self.minimize_button.setObjectName("minimize_button")
        self.minimize_button.setCursor(self.exit_button.cursor())
        self.minimize_button.setDisabled(True)
        self.minimize_button.setFixedSize(self.exit_button.width(), self.exit_button.height())
        self.minimize_button.move(
            self.exit_button.x() + self.exit_button.width() + 10, 
            self.exit_button.y())
        self.minimize_button.clicked.connect(self.showMinimized)

        # Fullscreen Button
        self.fullscreen_button = QPushButton(self.titlebar)
        self.fullscreen_button.setDisabled(True)
        self.fullscreen_button.setObjectName("fullscreen_button")
        self.fullscreen_button.setCursor(self.exit_button.cursor())
        self.fullscreen_button.setFixedSize(self.exit_button.width(), self.exit_button.height())
        self.fullscreen_button.move(
            self.minimize_button.x() + self.minimize_button.width() + 10, 
            self.minimize_button.y())

        self.icon = QLabel(self.container)
        self.icon.move(30, self.titlebar.height() + 20)
        if self.iconType and self.iconType != "input":
            self.icon.setFixedSize(50, 50)
            if self.iconType == "warning":
                self.icon_pixmap = QPixmap("./image/gui/warning.png")
                self.icon_pixmap_scaled = self.icon_pixmap.scaled(
                    self.icon.width(), self.icon.height(),
                    aspectRatioMode=Qt.IgnoreAspectRatio, transformMode=Qt.SmoothTransformation)
                self.icon.setPixmap(self.icon_pixmap_scaled)
            elif self.iconType == "information":
                self.icon_pixmap = QPixmap("./image/gui/information.png")
                self.icon_pixmap_scaled = self.icon_pixmap.scaled(
                    self.icon.width(), self.icon.height(),
                    aspectRatioMode=Qt.IgnoreAspectRatio, transformMode=Qt.SmoothTransformation)
                self.icon.setPixmap(self.icon_pixmap_scaled)
            elif self.iconType == "question":
                self.icon_pixmap = QPixmap("./image/gui/question.png")
                self.icon_pixmap_scaled = self.icon_pixmap.scaled(
                    self.icon.width(), self.icon.height(),
                    aspectRatioMode=Qt.IgnoreAspectRatio, transformMode=Qt.SmoothTransformation)
                self.icon.setPixmap(self.icon_pixmap_scaled)
                self.sd = QGraphicsDropShadowEffect()
                self.sd.setBlurRadius(15)
                self.sd.setOffset(0)
                self.icon.setGraphicsEffect(self.sd)
        else:
            self.icon.setFixedSize(0, 0)

        self.boldtext = QLabel(self.container)
        self.boldtext.setObjectName("messagebox_boldtext")
        self.boldtext.setFixedHeight(25)
        self.boldtext.move(self.icon.x() + self.icon.width() + 20, self.icon.y())
        self.boldtext.setText(boldtext)

        self.text = QLabel(self.container)
        self.text.setMaximumWidth(1200)
        self.text.setWordWrap(False)
        self.text.move(self.boldtext.x(), self.boldtext.y() + self.boldtext.height())
        self.text.setText(text)
        self.text.adjustSize()

        self.textbox = QLineEdit(self.container)
        self.textbox.setObjectName("messagebox_textbox")
        if self.iconType == "input":
            self.textbox.setFixedSize(200, 25)
            self.textbox.setVisible(True)
        else:
            self.textbox.setVisible(False)
            self.textbox.setFixedSize(0, 0)
        self.textbox.move(
            self.boldtext.x(),
            self.text.y() + self.text.height() + 10)

        self.cancel = QPushButton(self.container)
        self.cancel.setCursor(QCursor(Qt.PointingHandCursor))
        self.cancel.setText(canceltext)
        self.cancel.clicked.connect(self.cancelButton)
        
        self.ok = QPushButton(self.container)
        self.ok.setObjectName("blue_button")
        self.ok.setCursor(self.cancel.cursor())
        self.ok.setVisible(ok)
        self.ok.setFixedSize(90, 20)
        self.ok.setText(oktext)
        self.ok.clicked.connect(self.okButton)
        
        self.container.setFixedWidth(max(
            self.boldtext.x() + self.boldtext.width() + self.icon.x(),
            self.text.x() + self.text.width() + self.icon.x(),
            self.textbox.x() + self.textbox.width() + self.icon.x()))
        self.titlebar.setFixedSize(self.container.width(), 30)
        if cancel:
            self.cancel.setFixedSize(90, 20)
            self.cancel.move(
                self.container.width() - self.cancel.width() - 30,
                self.textbox.y() + self.textbox.height() + 20)
        else:
            self.cancel.setFixedSize(0, 20)
            self.cancel.move(
                self.container.width() - self.cancel.width() - 20,
                self.textbox.y() + self.textbox.height() + 20)
        self.ok.move(
            self.cancel.x() - self.ok.width() - 5,
            self.cancel.y())
        self.container.setFixedHeight(self.ok.y() + self.ok.height() + 15)
        self.setFixedSize(self.container.width() + 40, self.container.height() + 40)

        self.effect = QGraphicsOpacityEffect(self)
        self.showAnimation = QPropertyAnimation(self.effect, b"opacity")
        self.showAnimation.setDuration(200)
        self.showAnimation.setStartValue(0)
        self.showAnimation.setEndValue(1)
        self.setGraphicsEffect(self.effect)
        self.showAnimation.start(QAbstractAnimation.DeleteWhenStopped)
        self.showAnimation.finished.connect(self.effect.deleteLater)

    def setupTextbox(self, placeholder="", text="", maxlength=None):
        self.textbox.setText(text)
        self.textbox.setPlaceholderText(placeholder)
        if maxlength:
            self.textbox.setMaxLength(maxlength)

    def getText(self):
        return self.textbox.text()

    def okButton(self):
        return self.done(1)

    def cancelButton(self):
        return self.done(0)


class QDialogX(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        # Setting Translucent and Frameless Window
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.oldPos = self.pos()
        self.oldX = self.x()
        self.oldY = self.y()

        # Setting Custom Background, Window Border and Shadow
        self.container = QWidget(self)
        self.container.setObjectName("container")
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(10)
        self.shadow.setOffset(0, 0)
        self.shadow.setColor(QColor(0, 0, 0, 180))
        self.container.setGraphicsEffect(self.shadow)

        # Custom Title Bar
        self.titlebar = QLabel(self.container)
        self.titlebar.setObjectName("titlebar")
        self.titlebar.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)
        self.titlebar.setFixedSize(self.container.width(), 30)
        self.titlebar.move(0, 0)

        # Exit Button
        self.exit_button = QPushButton(self.titlebar)
        self.exit_button.setObjectName("exit_button")
        self.exit_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.exit_button.setFixedSize(14, 14)
        self.exit_button.move(12, 8)
        self.exit_button.clicked.connect(self.close)

        # Minimize Button
        self.minimize_button = QPushButton(self.titlebar)
        self.minimize_button.setObjectName("minimize_button")
        self.minimize_button.setCursor(self.exit_button.cursor())
        self.minimize_button.setDisabled(True)
        self.minimize_button.setFixedSize(self.exit_button.width(), self.exit_button.height())
        self.minimize_button.move(
            self.exit_button.x() + self.exit_button.width() + 10, 
            self.exit_button.y())
        self.minimize_button.clicked.connect(self.showMinimized)

        # Fullscreen Button
        self.fullscreen_button = QPushButton(self.titlebar)
        self.fullscreen_button.setDisabled(True)
        self.fullscreen_button.setObjectName("fullscreen_button")
        self.fullscreen_button.setCursor(self.exit_button.cursor())
        self.fullscreen_button.setFixedSize(self.exit_button.width(), self.exit_button.height())
        self.fullscreen_button.move(
            self.minimize_button.x() + self.minimize_button.width() + 10, 
            self.minimize_button.y())

    # Mouse Press Event
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        self.oldX = event.globalX()
        self.oldY = event.globalY()

    # Custom Window Moving Event
    def mouseMoveEvent(self, event):
        #time.sleep(0.02)  # sleep for 20ms
        delta = QPoint (event.globalPos() - self.oldPos)
        if (self.oldX >= self.x() + self.container.x() + self.titlebar.x()
            and self.oldX <= self.x() + self.container.x() + self.titlebar.x() + self.titlebar.width()
            and self.oldY >= self.y() + self.container.y() + self.titlebar.y()
            and self.oldY <= self.y() + self.container.y() + self.titlebar.y() + self.titlebar.height()):
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
            self.oldX = event.globalX()
            self.oldY = event.globalY()


class CropImageResizePoint(QWidget):
    def __init__(self, position, parent=None):
        super().__init__()
        self.setFixedSize(5, 5)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setObjectName("crop_image_resize_point")
        self.position = position
        self.setParent(parent)
        self.oldPos = self.parent().pos()
        self.oldX = self.parent().x()
        self.oldY = self.parent().y()

        if self.position == "top" or self.position == "bottom":
            self.setCursor(QCursor(Qt.SizeVerCursor))
        else:
            self.setCursor(QCursor(Qt.SizeHorCursor))

    def mousePressEvent(self, event):
        self.firstX = event.globalX()
        self.firstY = event.globalY()
        self.oldPos = event.globalPos()
        self.oldX = event.globalX()
        self.oldY = event.globalY()

    def mouseMoveEvent(self, event):
        deltaX = event.globalX() - self.oldX
        deltaY = event.globalY() - self.oldY
        if self.position == "top":
            if (self.parent().y() > 0 
                and self.parent().parent().width() > self.parent().x() + self.parent().width()
                and self.parent().width() >= 20
                and self.parent().height() >= 20
                ) or deltaY > 0:
                    self.parent().move(self.parent().x(), self.parent().y() + deltaY)
                    self.parent().resize(self.parent().width() - deltaY, self.parent().height() - deltaY)

        elif self.position == "bottom":
            if (self.parent().y() + self.parent().height() < self.parent().parent().height()
                and self.parent().parent().width() > self.parent().x() + self.parent().width()
                and self.parent().width() >= 20
                and self.parent().height() >= 20
                ) or deltaY < 0:
                    self.parent().resize(
                        self.parent().width() + deltaY,
                        self.parent().height() + deltaY)

        elif self.position == "left":
            if (self.parent().x() > 0 
                and self.parent().y() > 0 
                and self.parent().width() >= 20 
                and self.parent().height() >= 20 
                and self.parent().parent().height() > self.parent().y() + self.parent().height()
                ) or deltaX > 0:
                    self.parent().move(self.parent().x() + deltaX, self.parent().y() + deltaX)
                    self.parent().resize(self.parent().width() - deltaX, self.parent().height() - deltaX)

        elif self.position == "right":
            if (self.parent().x() + self.parent().width() < self.parent().parent().width()
                and self.parent().y() + self.parent().height() < self.parent().parent().height()
                and self.parent().width() >= 20
                and self.parent().height() >= 20
                ) or deltaY < 0:
                    self.parent().resize(self.parent().width() + deltaX, self.parent().height() + deltaX)


        self.oldX = event.globalX()
        self.oldY = event.globalY()


class CropImageRect(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setParent(parent)
        self.resize(
            min(self.parent().width(), self.parent().height()) / 3 * 2,
            min(self.parent().width(), self.parent().height()) / 3 * 2)
        self.move(
            (self.parent().width() - self.width()) / 2,
            (self.parent().height() - self.height()) / 2)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setObjectName("crop_image_rect")
        self.setCursor(QCursor(Qt.OpenHandCursor))
        self.oldPos = self.pos()
        self.oldX = self.x()
        self.oldY = self.y()
        
        # Top point
        self.top_point = CropImageResizePoint("top", parent=self)
        self.top_point.move(
            (self.width() - self.top_point.width()) / 2,
            0)

        # Bottom point
        self.bottom_point = CropImageResizePoint("bottom", parent=self)
        self.bottom_point.move(
            (self.width() - self.bottom_point.width()) / 2,
            self.height() - self.bottom_point.height())

        # Left point
        self.left_point = CropImageResizePoint("left", parent=self)
        self.left_point.move(
            0,
            (self.height() - self.left_point.height()) / 2)

        # Right point
        self.right_point = CropImageResizePoint("right", parent=self)
        self.right_point.move(
            self.width() - self.right_point.width(),
            (self.height() - self.right_point.height()) / 2)

    def mousePressEvent(self, event):
        self.setCursor(QCursor(Qt.ClosedHandCursor))
        self.oldPos = event.globalPos()
        self.oldX = event.globalX()
        self.oldY = event.globalY()

    def mouseReleaseEvent(self, event):
        self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.firstPos = event.globalPos()
        self.oldPos = event.globalPos()
        self.oldX = event.globalX()
        self.oldY = event.globalY()

    def resizeEvent(self, event):
        # Limit resizing, max size and min size
        if self.width() < 20 or self.height() < 20:
            self.resize(20, 20)
        elif self.x() + self.width() > self.parent().width():
            self.resize(
                self.parent().width() - self.x(),
                self.parent().width() - self.x())
        elif self.y() + self.height() > self.parent().height():
            self.resize(
                self.parent().height() - self.y(),
                self.parent().height() - self.y())
        elif self.x() < 0 or self.y() < 0:
            self.resize(self.width(), self.height())
            self.move(self.x(), self.y())
        # Move resizing point
        self.top_point.move(
            (self.width() - self.top_point.width()) / 2,
            0)
        self.bottom_point.move(
            self.top_point.x(),
            self.height() - self.bottom_point.height())
        self.left_point.move(
            0,
            (self.height() - self.left_point.height()) / 2)
        self.right_point.move(
            self.width() - self.right_point.width(),
            (self.height() - self.right_point.height()) / 2)

    def moveEvent(self, event):
        if self.x() < 0:
            self.move(0, self.y())
        elif self.x() > self.parent().width() - self.width():
            self.move(self.parent().width() - self.width(), self.y())
        elif self.y() < 0:
            self.move(self.x(), 0)
        elif self.y() > self.parent().height() - self.height():
            self.move(self.x(), self.parent().height() - self.height())


class CropImageDialog(QDialogX):
    def __init__(self, image_path, button_text, theme, parent=None):
        super().__init__()
        self.setStyleSheet(theme)
        self.titlebar.setFixedWidth(self.container.width())
        self.adjustSize()
        self.image_path = image_path

        self.image_container = QWidget(self.container)
        self.image_container.setObjectName("image_crop_box")
        self.image_container.move(20, self.titlebar.height() + 20)
        self.image_container_shadow = QGraphicsDropShadowEffect()
        self.image_container_shadow.setBlurRadius(15)
        self.image_container_shadow.setOffset(0)
        self.image_container.setGraphicsEffect(self.image_container_shadow)
        
        self.image_widget = QLabel(self.image_container)
        self.image_widget.move(5, 5)
        self.image = Image.open(self.image_path)
        self.image_pixmap = QPixmap(self.image_path)
        self.maxsize = 370
        if max(self.image_pixmap.width(), self.image_pixmap.height()) > self.maxsize:
            self.resize_ratio = self.maxsize / max(self.image_pixmap.width(), self.image_pixmap.height())
            self.image_pixmap_scaled = self.image_pixmap.scaled(
                self.image_pixmap.width() * self.resize_ratio,
                self.image_pixmap.height() * self.resize_ratio,
                transformMode=Qt.SmoothTransformation)
            self.image_widget.setPixmap(self.image_pixmap_scaled)
            self.image_widget.setFixedSize(
                self.image_pixmap_scaled.width(),
                self.image_pixmap_scaled.height())
        else:
            self.resize_ratio = 1
            self.image_widget.setPixmap(self.image_pixmap)
            self.image_widget.setFixedSize(
                self.image_pixmap.width(),
                self.image_pixmap.height())
        self.image_container.setFixedSize(
            self.image_widget.width() + 10,
            self.image_widget.height() + 10)

        self.cropwidget = CropImageRect(self.image_widget)
        
        self.button = QPushButton(self.container)
        self.button.setObjectName("blue_button")
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setFixedSize(120, 30)
        self.button.move(
            self.image_container.x() + (self.image_container.width() - self.button.width()) / 2,
            self.image_container.y() + self.image_container.height() + 20)
        self.button.setText(button_text)
        self.button.clicked.connect(self.cropImage)

        self.container.move(20, 20)
        self.container.setFixedSize(
            self.image_container.x()*2 + self.image_container.width(),
            self.button.y() + self.button.height() + 20)
        self.titlebar.setFixedWidth(self.container.width())
        self.resize(self.container.width() + 40, self.container.height() + 40)

        self.cropped_image_pixmap = None
        self.cropped_image = None


    def closeEvent(self, event):
        self.done(0)
        event.accept()

    def cropImage(self):
        self.cropped_image = self.image.crop((
            self.cropwidget.x() / self.resize_ratio,
            self.cropwidget.y() / self.resize_ratio,
            (self.cropwidget.x() + self.cropwidget.width()) / self.resize_ratio,
            (self.cropwidget.y() + self.cropwidget.height()) / self.resize_ratio))
        if self.cropped_image.size > (512, 512):
            self.cropped_image = self.cropped_image.resize((512, 512))
        self.cropped_image.save("temp-cropped.png")
        self.cropped_image_pixmap = QPixmap("temp-cropped.png")
        os.remove("temp-cropped.png")
        self.done(1)

    def getImagePixmap(self):
        return self.cropped_image_pixmap

    def getImage(self):
        return self.cropped_image

    
