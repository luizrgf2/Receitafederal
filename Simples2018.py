from selenium import webdriver
from time import sleep as tm
import os
from python_anticaptcha import AnticaptchaClient, ImageToTextTask
import base64
import sys
import json
import pickle



class Robo2018():

    def __init__(self, code, cnpj, cpf, anticapcha, visivel):

        
        self.code = code
        self.cnpj = cnpj
        self.cpf = cpf
        self.path = os.getcwd()+f'/'+f'{self.cnpj}'
        self.ano = '2015'



        options = webdriver.ChromeOptions() 
        prefs = {'download.default_directory' : f'{self.path}'}
        options.add_experimental_option('prefs', prefs)
        if visivel == False:
            options.add_argument("--headless")
        options.add_argument('ignore-certificate-errors')
        options.add_argument('--no-sandbox')

        self.driver = webdriver.Chrome(executable_path=os.getcwd()+'/'+'chromedriver',chrome_options=options)

        self.driver.get('https://www8.receita.fazenda.gov.br/SimplesNacional/controleAcesso/Autentica.aspx?id=60')

        tm(1)

        cookies = pickle.load(open(f"{self.path}/cookies.pkl", "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        tm(3)

        self.driver.get('https://www8.receita.fazenda.gov.br/SimplesNacional/controleAcesso/Autentica.aspx?id=60')

        tm(2)

        self.verificacao()

        tm(2)
    def Downloads(self,ano,init,final):

        self.driver.get('https://www8.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/pgdasd2018.app/Consulta')
        self.ano = ano
        tm(2)
        
        self.driver.find_element_by_id('ano').send_keys(self.ano)
        self.driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[1]/form/div/button').click()
        tm(3)
        element = None
        buttons = []
        linhas = []
        
        tempos = self.driver.find_elements_by_class_name('pa')
        k = 0
        
        if len(tempos) == 0:

            print('Não existe dados para este ano!')
            return
        
        morte = 0
        
        if final == 0:
            
            morte = len(tempos)
        else:
            
            morte = final
        
        
        while(True):
                    
            k=k+1
            try:
                linhas.append(self.driver.find_element_by_xpath(f'/html/body/div[1]/div/div[2]/div[2]/div[2]/div/div/div/table/tbody/tr[{k}]'))



            except:

                i = 0
                break
        
        count = 1
        for i in range(len(linhas)):

           
            try:
                count=count+1
                atual = linhas[i].find_element_by_class_name('pa').text

                print(atual)

                if count > 0 and element != None:
                    
                    buttons.append(element)


            except:
                
                
                try:
                    
                    element = self.driver.find_element_by_xpath(f'/html/body/div[1]/div/div[2]/div[2]/div[2]/div/div/div/table/tbody/tr[{count}]/td[5]/a')
                    
                except:
                    
                    element=element
        
        for i in range(len(linhas)+1):
            
            
            try:
                element = self.driver.find_element_by_xpath(f'/html/body/div[1]/div/div[2]/div[2]/div[2]/div/div/div/table/tbody/tr[{i}]/td[5]/a')
            except:
                element = element
                
        buttons.append(element)
        
        
        for i in range(init,morte):
            
            buttons[i].click()
            
            tm(3)
            
            arquivos = [_ for _ in os.listdir(self.path) if _.endswith(r'.pdf')]

            print(arquivos)  
            
            texto = tempos[i].text.split('/')
            texto_final = texto[0]+'_'+texto[1]

            if os.path.isdir(self.path+f'/{self.ano}'):

                print('Ja existe o diretorio!!')

            else:

                os.mkdir(self.path+f'/{self.ano}')

            


            file = open(self.path+f'/{arquivos[0]}','rb')

            filecreate = open(self.path+f'/{self.ano}/{texto_final}.pdf','wb')
            filecreate.write(file.read())
            filecreate.close()

            file.close()

            os.remove(self.path+f'/{arquivos[0]}')    
    def verificacao(self):

        try:

            self.driver.find_element_by_id('details-button').click()
            tm(2)
            self.driver.find_element_by_xpath('/html/body/div/div[3]/p[2]/a').click()

        except:

            return

