

from PyQt5.QtWidgets import *
import sys
import sqlite3

### Import telas sistema ###

from telas_py.login import Ui_Form_login
from telas_py.cadastro import Ui_form_cadastro
from telas_py.info import Ui_form_info
from telas_py.logado import Ui_form_logado



### Classe Tela Principal ###

class tela_login(QMainWindow):
    def __init__(self, *args, **argvs):
        super(tela_login, self).__init__(*args, **argvs)
        self.ui = Ui_Form_login()
        self.ui.setupUi(self)       

        ### Evento / Botões ###

        self.ui.bt_user.clicked.connect(self.ui.ln_login.setFocus)
        self.ui.bt_senha.clicked.connect(self.ui.ln_senha.setFocus)
        self.ui.bt_entrar.clicked.connect(self.botao_entrar)
        self.ui.bt_cadastrar.clicked.connect(self.botao_cadastro)
        self.ui.bt_info.clicked.connect(self.botao_info)


    ### Função Mensagem / Erro - Informar Login ###

    def login_preench(self):
        msg1 = QMessageBox()
        msg1.setIcon(QMessageBox.Information)
        msg1.setWindowTitle('Atenção')
        msg1.setText('Favor Informar o Login!')
        x = msg1.exec_()

    ### Função Mensagem / Erro - Informar Senha ###

    def senha_preench(self):
        msg1 = QMessageBox()
        msg1.setIcon(QMessageBox.Information)
        msg1.setWindowTitle('Atenção')
        msg1.setText('Favor Informar a senha!')
        x = msg1.exec_()

    ### Função - Mensagem / Erro - Dados Login Incorretos ###

    def mens_dados_incorretos(self):
        msg1 = QMessageBox()
        msg1.setIcon(QMessageBox.Critical)
        msg1.setWindowTitle('Atenção')
        msg1.setText('Os Dados do Login estão Incorretos!')
        x = msg1.exec_()


    ### Função / Botão Entrar ###

    def botao_entrar(self):    

        try:
            nome = self.ui.ln_login.text()
            senha = self.ui.ln_senha.text()

            if len(nome) == 0:
                self.login_preench()
                self.ui.ln_login.setFocus()

            elif len(senha) == 0:
                self.senha_preench()
                self.ui.ln_senha.setFocus()
            
            else:
                banco = sqlite3.connect('base_dados/dados.db')
                cursor = banco.cursor()
                cursor.execute('SELECT senha FROM user WHERE nome = \''+nome+"\'")
                senha_bd = cursor.fetchone()[0]
                banco.close()
                validacao = False
        except:
            print("Erro de login")
            validacao = True
        try:
            
            if not validacao:
                if senha == senha_bd:
                    self.tela_logado_sistema()
                else:
                    self.mens_dados_incorretos()
            else:
                self.mens_dados_incorretos()
        except:
            print("Erro de login")

    ### Função / Botão Cadastro ###

    def botao_cadastro(self):        
        self.tela = tela_cadastro() 
        self.tela.show()  
        tela_login.hide(self)
    
    ### Função / Botão Info ###

    def botao_info(self):        
        self.tela = tela_info() 
        self.tela.show()   
        tela_login.hide(self)

    ### Função / Tela Logado ###

    def tela_logado_sistema(self):        
        self.tela = tela_logado() 
        self.tela.show()   
        tela_login.hide(self)
 
         
###############################################################################

        
### Classe Tela Cadastro ######################################################

class tela_cadastro(QDialog):
    def __init__(self, *args, **argvs):
        super(tela_cadastro, self).__init__(*args, **argvs)
        self.ui = Ui_form_cadastro()
        self.ui.setupUi(self)

        ### Evento / Botões ###

        self.ui.bt_user.clicked.connect(self.ui.ln_login.setFocus)
        self.ui.bt_senha.clicked.connect(self.ui.ln_senha.setFocus)
        self.ui.bt_voltar.clicked.connect(self.botao_voltar)
        self.ui.bt_info.clicked.connect(self.botao_info)
        self.ui.bt_cadastrar.clicked.connect(self.botao_cadastrar)

    ### Função - Mensagem / Cadastro Realizado ###

    def mens_cad_realizado(self):
        msg1 = QMessageBox()
        msg1.setIcon(QMessageBox.Information)
        msg1.setWindowTitle('Informação')
        msg1.setText('Cadastro Realizado!')
        x = msg1.exec_()

    ### Função - Mensagem / Erro - Cadastro Não Realizado ###

    def mens_cad_error(self):
        msg1 = QMessageBox()
        msg1.setIcon(QMessageBox.Critical)
        msg1.setWindowTitle('Erro')
        msg1.setText('Cadastro não Realizado!')
        x = msg1.exec_()

    ### Função - Mensagem / Erro - Informar o Nome ###

    def mens_nome_error(self):
        msg1 = QMessageBox()
        msg1.setIcon(QMessageBox.Information)
        msg1.setWindowTitle('Atenção')
        msg1.setText('Favor Informar o Nome!')
        x = msg1.exec_()

    ### Função - Mensagem / Erro - Informar a Senha ###

    def mens_senha_error(self):
        msg1 = QMessageBox()
        msg1.setIcon(QMessageBox.Information)
        msg1.setWindowTitle('Atenção')
        msg1.setText('Favor Informar a Senha!')
        x = msg1.exec_()
    
    ### Função / Botão Cadastrar ###

    def botao_cadastrar(self):
        self.nome = self.ui.ln_login.text()
        self.senha = self.ui.ln_senha.text()

        if self.nome == "":
            self.mens_nome_error()
            self.ui.ln_login.setFocus()
        elif self.senha == "":
            self.mens_senha_error()
            self.ui.ln_senha.setFocus()
        else:
            
            try:
                banco = sqlite3.connect('base_dados/dados.db')
                cursor = banco.cursor()
                cursor.execute("INSERT INTO user (nome, senha) VALUES ('"+self.nome+"','"+self.senha+"')")
                banco.commit()
                banco.close()
                self.mens_cad_realizado()
                self.botao_voltar()

        
            except sqlite3.Error as erro:
                self.mens_cad_error()        

    ### Função / Botão Voltar ###

    def botao_voltar(self):
        self.tela = tela_login() 
        self.tela.show()    
        tela_cadastro.hide(self)

    ### Função / Botão Info ###

    def botao_info(self):        
        self.tela = tela_info() 
        self.tela.show()   
        tela_cadastro.hide(self)

        
###############################################################################


### Classe Tela Informações ###################################################

class tela_info(QDialog):
    def __init__(self, *args, **argvs):
        super(tela_info, self).__init__(*args, **argvs)
        self.ui = Ui_form_info()
        self.ui.setupUi(self)
        self.ui.bt_info.clicked.connect(self.botao_voltar) 

    ### Função / Botão Voltar ###

    def botao_voltar(self):
        self.tela = tela_login() 
        self.tela.show()    
        tela_info.hide(self)

###############################################################################


### Classe Tela Seja Bam Vindo ################################################

class tela_logado(QDialog):
    def __init__(self, *args, **argvs):
        super(tela_logado, self).__init__(*args, **argvs)
        self.ui = Ui_form_logado()
        self.ui.setupUi(self) 
        self.ui.bt_voltar_2.clicked.connect(self.botao_voltar)

    ### Função / Botão Voltar ###

    def botao_voltar(self):
        self.tela = tela_login() 
        self.tela.show()    
        tela_info.hide(self)    


###############################################################################


app = QApplication(sys.argv)
if (QDialog.Accepted == True):
    windows = tela_login()
    windows.show()

sys.exit(app.exec_())