import io
import sys
import qrcode
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox, QFileDialog, \
    QDialog
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os
from sys import platform

'''Demo'''


class qrcodeGUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setFixedSize(600, 400)
        self.setWindowTitle('二维码生成器')
        self.grid = QGridLayout()
        # 定义组件
        # 	--Label
        self.content_label = QLabel('HA01-RED-M:')
        self.path_label = QLabel('')
        # self.color_size_label = QLabel('颜色-尺码：')
        # self.size_label = QLabel('尺寸:')
        # self.version_label = QLabel('版本:')
        # self.margin_label = QLabel('边距:')
        # self.rendering_label = QLabel('效果:')
        self.show_label = QLabel()
        # 		使得图片可缩放
        self.show_label.setScaledContents(True)
        # 		显示时的最大尺寸
        self.show_label.setMaximumSize(200, 200)
        # 	--输入框
        self.content_edit = QLineEdit()
        self.content_edit.setText('')

        self.path_edit = QLineEdit()
        self.path_edit.setText('')

        # 颜色尺码输入框
        self.color_content_edit = QLineEdit()
        self.color_content_edit.setText('')
        # 	--按钮
        self.generate_button = QPushButton('生成二维码')
        self.save_button = QPushButton('保存二维码')
        self.path_button = QPushButton('设置路径')
        # 	--下拉框
        # self.version_combobox = QComboBox()
        # for i in range(1, 41):
        # 	self.version_combobox.addItem('%s' % str(i))
        self.size_combobox = QComboBox()
        for i in range(1, 2):
            self.size_combobox.addItem('%s * %s' % (str(i * 100), str(i * 100)))
        # 	--微调框
        self.margin_spinbox = QSpinBox()
        # 布局
        # 	数字依次对应行, 列, 行数和列数
        # self.grid.addWidget(self.color_size_label, 1, 5, 1, 1)
        # self.grid.addWidget(self.color_content_edit, 1, 6, 1, 3)

        # self.grid.addWidget(self.version_label, 1, 5, 1, 1)
        # self.grid.addWidget(self.version_combobox, 1, 6, 1, 1)
        self.grid.addWidget(self.content_label, 0, 1, 1, 1)
        self.grid.addWidget(self.content_edit, 0, 2, 1, 8)

        # self.grid.addWidget(self.path_label, 1, 1, 1, 1)
        self.grid.addWidget(self.path_label,  1, 3, 1, 8)
        self.grid.addWidget(self.path_button,1,1,1,2)

        # self.grid.addWidget(self.size_label, 1, 1, 1, 1)
        # self.grid.addWidget(self.size_combobox, 1, 2, 1, 1)
        # self.grid.addWidget(self.margin_label, 3, 5, 1, 1)
        # self.grid.addWidget(self.margin_spinbox, 3, 6, 1, 1)
        # self.grid.addWidget(self.generate_button, 2, 1, 1, 2)
        self.grid.addWidget(self.save_button, 2, 1, 1, 2)

        # self.grid.addWidget(self.rendering_label, 3, 1, 1, 1)
        self.grid.addWidget(self.show_label, 3, 1, 5, 5)



        self.setLayout(self.grid)
        self.generate_button.clicked.connect(self.genQrcode)
        self.save_button.clicked.connect(self.saveQrcode)
        self.path_button.clicked.connect(self.getQrcodeSavePath)
        # self.margin_spinbox.valueChanged.connect(self.genQrcode)
        # self.genQrcode()

    '''生成二维码'''

    def genQrcode(self):
        content = self.content_edit.text()
        if content == '':
            self.show_ERROR_message()
            exit()
        # content2 = self.color_content_edit.text()
        # try:
        #     margin = int(self.margin_spinbox.text())
        # except:
        #     margin = 0
        margin = 0
        size = int(self.size_combobox.currentText().split('*')[0])
        qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_L,
                           box_size=size // 29,
                           border=margin)
        qr.add_data(content)
        self.qr_img = qr.make_image()

        fp = io.BytesIO()
        self.qr_img.save(fp, 'BMP')
        qimg = QtGui.QImage()
        qimg.loadFromData(fp.getvalue(), 'BMP')
        qimg_pixmap = QtGui.QPixmap.fromImage(qimg)
        self.show_label.setPixmap(qimg_pixmap)

    '''保存二维码'''

    def saveQrcode(self):
        self.genQrcode()
        qrCodeDirFlag = self.path_label.text()
        if qrCodeDirFlag == '':
            if platform == "linux" or platform == "linux2":
                # linux
                desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
                image_font = ImageFont.truetype("Keyboard.ttf", 22)
            elif platform == "darwin":
                # OS X
                desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
                image_font = ImageFont.truetype("Keyboard.ttf", 22)
            elif platform == "win32":
                # Windows...
                desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
                image_font = ImageFont.truetype("arial.ttf", 22)
            # self.show_ERROR_message()
            # self.getQrcodeSavePath()
        # qrCodeDir = self.path_label.text()
        qrCodeDir = desktop_path
        background = Image.new('RGBA', (170, 130), (255, 255, 255, 255))
        draw = ImageDraw.Draw(background)
        # chalk = ImageFont.truetype("Keyboard.ttf", 22)
        # image_font = ImageFont.load_default()
        spu, color, size = self.content_edit.text().upper().split('-')
        draw.text((15, 70), spu, (0, 0, 0), font=image_font)
        draw.text((15, 95), color + '-' + size, (0, 0, 0), font=image_font)
        qr = self.qr_img
        background.paste(qr, (20, 5))
        rotate_backgroud = background.rotate(-90, expand=True)
        # rotate_backgroud.save(self.content_edit.text().upper() + '-' + self.color_content_edit.text().upper() +'.png')

        # filename = QFileDialog.getSaveFileName(self, '保存',
        #                                        './' + self.content_edit.text().upper() + '-' + self.color_content_edit.text().upper() + '.png',
        #                                        # '所有文件(*)')
        filename = qrCodeDir + '/' + self.content_edit.text().upper() + '.png'
        rotate_backgroud.save(filename)
        
        try:
            os.startfile(filename, "print")
        except Exception as e:
            raise

        if os.path.exists(filename):
            # self.show_SUCCESS_message()
            print("success")
        else:
            self.show_ERROR_message()

        # if filename[0] != '':
        #     rotate_backgroud.save(filename[0])
        #     QDialog().show()
            # self.addTextOnQrcode()
    def getQrcodeSavePath(self):
        filename = QFileDialog.getExistingDirectory()
        self.path_label.setText(filename)
        return filename

    def addTextOnQrcode(self):
        background = Image.new('RGBA', (170, 130), (255, 255, 255, 255))
        draw = ImageDraw.Draw(background)
        chalk = ImageFont.truetype("arial.ttf", 22)
        draw.text((15, 70), self.content_edit.text().upper(), (0, 0, 0), font=chalk)
        draw.text((15, 95), self.color_content_edit.text().upper(), (0, 0, 0), font=chalk)
        qr = self.qr_img
        background.paste(qr, (20, 5))
        rotate_backgroud = background.rotate(-90, expand=True)
        rotate_backgroud.save(self.content_edit.text().upper() + '-' + self.color_content_edit.text().upper() + '.png')

    def show_ERROR_message(self):
        QtWidgets.QMessageBox.critical(self, "错误", "请设置路径和输入sku")
    def show_SUCCESS_message(self):
        QtWidgets.QMessageBox.information(self, "成功", "保存成功")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = qrcodeGUI()
    gui.show()
    sys.exit(app.exec_())
