import sys
from PyQt6 import QtCore,QtWidgets
from PyQt6.QtWidgets import QWidget, QApplication , QLabel
from PyQt6.QtGui import QIcon,QPixmap
from PyQt6.QtCore import QTimer
from bs4 import BeautifulSoup
import requests

url = "https://borsa.doviz.com/hisseler"
response = requests.get(url)

html_content = response.content
soup = BeautifulSoup(html_content, "html.parser")

def hisse_degeri(aranan_sirket):
    try:
        aranan_sirket = aranan_sirket.upper().replace("İ", "I").replace("Ö", "O").replace("Ü", "U").replace("Ğ", "G").replace("Ç", "C").replace("Ş", "S")

        
        tr_element = soup.find("tr", {"data-name": lambda x: x and aranan_sirket in x.split(' - ')[0].upper()})

        
        if tr_element:
            text_bold_elements = tr_element.find_all("td", {"class": "text-bold"})
            color_down_element = tr_element.find("td", {"class": "color-down"})
            
            
            other_td_elements = tr_element.find_all("td", {"class": None})

            
            degerler_2 = [
                text_bold_elements[0].text.strip() if text_bold_elements and len(text_bold_elements) > 0 else None,
                other_td_elements[1].text.strip() if other_td_elements and len(other_td_elements) > 1 else None,
                other_td_elements[2].text.strip() if other_td_elements and len(other_td_elements) > 2 else None,
                other_td_elements[3].text.strip() if other_td_elements and len(other_td_elements) > 3 else None,
                text_bold_elements[1].text.strip() if text_bold_elements and len(text_bold_elements) > 1 else None
            ]
            
            return degerler_2
    except Exception as e:
        print(f"Hata: {e}")
        return None

class Ui_Form(QWidget):
    def __init__(self):
        
        super().__init__()

        self.setupUi(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        icon_path = "Your_Path/borsa_istanbul_logo_dikey.png" # Görsel yolu - Image Path
        icon = QIcon(icon_path)
        self.setWindowIcon(icon)
        self.setStyleSheet("background-color: #FF6666;")    
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(711, 438)
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(parent=Form)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(100, 40, 231, 101))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.radio_yazisi = QLabel("BIST Kodu : ")
        self.verticalLayout_6.addWidget(self.radio_yazisi)
        self.bist_Gir_2 = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget_5)
        self.bist_Gir_2.setObjectName("bist_Gir_2")
        self.verticalLayout_6.addWidget(self.bist_Gir_2)
        self.verticalLayout_5.addLayout(self.verticalLayout_6)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_5)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_3.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_5)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_3.addWidget(self.pushButton_4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.textEdit = QtWidgets.QTextEdit(parent=Form)
        self.textEdit.setGeometry(QtCore.QRect(100, 150, 231, 191))
        self.textEdit.setObjectName("textEdit")
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(parent=Form)
        self.dateTimeEdit.setGeometry(QtCore.QRect(360, 40, 251, 22))
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.dateTimeEdit.setDisplayFormat("yyyy-MM-dd hh:mm:ss")
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Borsa"))
        self.pushButton_3.setText(_translate("Form", "Temizle"))
        self.pushButton_4.setText(_translate("Form", "Ara"))
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.pushButton_3.clicked.connect(self.delete)
        self.pushButton_4.clicked.connect(self.ara)

        self.show()

    def delete(self):
        self.textEdit.clear()
    def ara(self):
        girilen_bist = self.bist_Gir_2.text()
        deger = hisse_degeri(girilen_bist)
        self.textEdit.setText(f"{girilen_bist.upper()} hisse değerleri :\nSon : {deger[0]}\nEn yüksek : {deger[1]}\nEn düşük : {deger[2]}\nHacim : {deger[3]}\nDeğişim (yüzdelik) : {deger[4]}")

    def update_time(self):
        current_time = QtCore.QDateTime.currentDateTime()
        self.dateTimeEdit.setDateTime(current_time)
