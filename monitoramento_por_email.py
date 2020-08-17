'''Entender o problema-
Quero monitorar o preço do plano basico, e quando o preço for alterado, quero ser notificado
1 - Qual site iremos monitorar?
https://cursoautomacao.netlify.app/dinamico
2 - Qual estratégia esteremos usando
Selenium - Monitar o html da página e buscar mudanças de preço
3 - Montar o código e lógica que monitora o preço
'''
from selenium import webdriver
import schedule
import time
import os
from envio_email import Emailer
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
caminho_chromedriver = os.environ.get('CHROMEDRIVER_PATH')
#Configurações para rodar no Heroku
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path=caminho_chromedriver)
driver.get('https://cursoautomacao.netlify.app/dinamico')


def verificar_mudancas():
    # driver.get(driver.current_url)
    preco = driver.find_element_by_xpath("//li[@id='BasicPlan']")
    # Verificar se o preço é diferente de 'R$ 9.99 / ano'
    if preco.text != 'R$ 9.99 / ano':
        print(f'O preço foi alterado para {preco.text}')
        mensagem = f'O preço foi alterado para {preco.text}'
        # Enviar o e-mail
        #cardozo.danny20@gmail.com
        #mjc200217
        mail = Emailer(email_origem=os.environ.get('EMAIL_REMETENTE'),
                       senha_email=os.environ.get('SENHA_EMAIL'))
        lista_contatos = ['brito.danny@gmail.com']
        mail.definir_conteudo('Preço no site foi ALTERADO!',
                              'Daniel', lista_contatos, mensagem)
        mail.enviar_email(1)
    elif preco.text == 'R$ 9.99 / ano':
        print('O preço continua o mesmo')


schedule.every(2).minutes.do(verificar_mudancas)

while True:
    schedule.run_pending()
    time.sleep(1)
