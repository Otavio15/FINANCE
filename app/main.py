from PyQt5 import QtCore, QtGui, QtWidgets
from style import Ui_MainWindow
from assets import Relatorio

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        def gerarRelatorio():
            self.progressBar.setValue(self.progressBar.value() + 2)
            self.lcdNumber.display(self.progressBar.value() + 2)
            flag_imprimir_tabela = self.checkBox_1.isChecked()
            self.progressBar.setValue(self.progressBar.value() + 2)
            self.lcdNumber.display(self.progressBar.value() + 2)
            flag_imprimir_grafico = self.checkBox_2.isChecked()
            self.progressBar.setValue(self.progressBar.value() + 2)
            self.lcdNumber.display(self.progressBar.value() + 2)
            flag_imprimir_grafico_normalizado = self.checkBox_3.isChecked()
            self.progressBar.setValue(self.progressBar.value() + 2)
            self.lcdNumber.display(self.progressBar.value() + 2)
            flag_imprimir_grafico_volatividade = self.checkBox_4.isChecked()
            self.progressBar.setValue(self.progressBar.value() + 2)
            self.lcdNumber.display(self.progressBar.value() + 2)
            flag_imprimir_retorno_volatividade = self.checkBox_6.isChecked()
            self.progressBar.setValue(self.progressBar.value() + 2)
            self.lcdNumber.display(self.progressBar.value() + 2)
            flag_imprimir_melhores_ativos = self.checkBox_7.isChecked()
            self.progressBar.setValue(self.progressBar.value() + 2)
            self.lcdNumber.display(self.progressBar.value() + 2)
            texto = self.texto.toPlainText()
            self.progressBar.setValue(self.progressBar.value() + 2)
            self.lcdNumber.display(self.progressBar.value() + 2)
            data_inicio = self.dataInicio.text()
            self.progressBar.setValue(self.progressBar.value() + 2)
            self.lcdNumber.display(self.progressBar.value() + 2)
            data_inicio = data_inicio[6:] + '-' + data_inicio[3:5] + '-' +data_inicio[0:2]
            self.progressBar.setValue(self.progressBar.value() + 2)
            self.lcdNumber.display(self.progressBar.value() + 2)
            data_fim = self.dataFim.text()
            self.progressBar.setValue(self.progressBar.value() + 2)
            self.lcdNumber.display(self.progressBar.value() + 2)
            data_fim = data_fim[6:] + '-' + data_fim[3:5] + '-' +data_fim[0:2]
            self.progressBar.setValue(self.progressBar.value() + 2)
            self.lcdNumber.display(self.progressBar.value() + 2)
            rel = Relatorio()
            self.progressBar.setValue(self.progressBar.value() + 2)
            self.lcdNumber.display(self.progressBar.value() + 2)
            acoes = rel.organizarTiker(texto)
            self.progressBar.setValue(self.progressBar.value() + 2)
            self.lcdNumber.display(self.progressBar.value() + 2)
            try:
                rel.gerar_relatorio(flag_imprimir_tabela,flag_imprimir_grafico,flag_imprimir_grafico_normalizado,flag_imprimir_grafico_volatividade,flag_imprimir_retorno_volatividade,flag_imprimir_melhores_ativos, data_inicio, data_fim, acoes)
                self.progressBar.setValue(self.progressBar.value() + 86)
                self.lcdNumber.display(self.progressBar.value() + 86)
            except:
                self.progressBar.setValue(0)
                self.lcdNumber.display(0)

            self.progressBar.setValue(0)
            self.lcdNumber.display(0)

        self.gerarRelatorio.clicked.connect(gerarRelatorio)
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())