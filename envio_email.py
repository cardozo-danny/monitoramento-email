import os
import smtplib
import imghdr  
from email.message import EmailMessage
import time


class Emailer:
    def __init__(self, email_origem, senha_email):
        self.email_origem = email_origem
        self.senha_email = senha_email

    def definir_conteudo(self, topico, e_mail_remetente, lista_contatos, conteudo_email):
        self.msg = EmailMessage()
        self.msg['Subject'] = str(topico)
        self.msg['From'] = str(e_mail_remetente)
        self.msg['To'] = (', ').join(lista_contatos)
        self.msg.set_content(conteudo_email)

    def anexar_imagem(self, lista_imagens):
        for imagem in lista_imagens:
            with open(imagem, 'rb') as arquivo:
                dados = arquivo.read()
                extensao_imagem = imghdr.what(arquivo.name)
                nome_arquivo = arquivo.name
            self.msg.add_attachment(dados, maintype='image',
                                    subtype=extensao_imagem, filename=nome_arquivo)

    def anexar_arquivos(self, lista_arquivos):
        for arquivo in lista_arquivos:
            with open(arquivo, 'rb') as a:
                dados = a.read()
                nome_arquivo = a.name
            self.msg.add_attachment(dados, maintype='application',
                                    subtype='octet-stream', filename=nome_arquivo)

    def enviar_email(self, intervalo_em_segundos):
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(user=self.email_origem, password=self.senha_email)
            smtp.send_message(self.msg)
            time.sleep(intervalo_em_segundos)