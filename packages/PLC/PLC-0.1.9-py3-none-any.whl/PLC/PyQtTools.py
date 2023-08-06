from PyQt5 import QtWidgets
import os
def FileDialog(self, filetypes):
    options = QtWidgets.QFileDialog.Options()
    options |= QtWidgets.QFileDialog.DontUseNativeDialog
    fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                        filetypes, options=options)
    if fileName:
        return fileName
def FileExistEffect(self, Object, LoadBtn = None):
    if os.path.isfile(Object.text()):
        Object.setStyleSheet("")
        if LoadBtn is not None: LoadBtn.setEnabled(True)
    else:
        if LoadBtn is not None: LoadBtn.setEnabled(False)
        Object.setStyleSheet("background-color:red;")