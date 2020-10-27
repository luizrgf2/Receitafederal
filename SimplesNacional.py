from selenium import webdriver
from time import sleep as tm
import os
from python_anticaptcha import AnticaptchaClient, ImageToTextTask
import base64
import sys
import json
import pickle


class Robot():

    def __init__(self, code, cnpj, cpf,anticaptcha, visivel):
        self.anticaptcha = anticaptcha  
        self.code = code
        self.cnpj = cnpj
        self.cpf = cpf
        self.path = os.getcwd()+f'/{self.cnpj}'
        self.ano = '2015'


        options = webdriver.ChromeOptions() 
        prefs = {'download.default_directory' : f'{self.path}'}
        options.add_experimental_option('prefs', prefs)
        
        options.add_argument("--start-maximized")
        
        if visivel == False:
            options.add_argument("--headless")
        options.add_argument('ignore-certificate-errors')
        options.add_argument('--no-sandbox')

        self.driver = webdriver.Chrome(executable_path=os.getcwd()+'/'+'chromedriver',chrome_options=options)

        self.driver.get('https://www8.receita.fazenda.gov.br/SimplesNacional/controleAcesso/Autentica.aspx?id=6')

        tm(1)
        cookies = pickle.load(open(f"{self.path}/cookies.pkl", "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        tm(3)
        self.driver.get('https://www8.receita.fazenda.gov.br/SimplesNacional/controleAcesso/Autentica.aspx?id=6')
        tm(3)


        self.verificacao()

        tm(2)
    def Downloads(self,ano,init,final):
        
        self.ano = ano
        
        tm(4)

        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[6]/a/span').click()

        tm(2)

        self.driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[2]/div[1]/input').send_keys(self.ano)

        tm(3)
        
        self.driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[3]/a[3]').click()

        tm(3)
        
        
        i = 0
        tempos = self.driver.find_elements_by_class_name('pa')
        linhas = []
        buttons_finals = []

        while(True):
            
            i=i+1
            try:
                linhas.append(self.driver.find_element_by_xpath(f'/html/body/div[2]/div[3]/div[2]/div[1]/div[1]/div[2]/table[2]/tbody/tr[{i}]'))

            except:

                i = 0
                break
        
        count = 0
        for k in range(len(linhas)):

            try:


                atual = linhas[k].find_element_by_class_name('pa').text
                print(atual)

                if count > 0:

                    buttons_finals.append(self.driver.find_element_by_xpath(f'/html/body/div[2]/div[3]/div[2]/div[1]/div[1]/div[2]/table[2]/tbody/tr[{count}]/td[1]/a')) 
                    
                    print(count)

            except:


                
                count = k+1

        buttons_finals.append(self.driver.find_element_by_xpath(f'/html/body/div[2]/div[3]/div[2]/div[1]/div[1]/div[2]/table[2]/tbody/tr[{len(linhas)}]/td[1]/a'))               
        scroll = 50
        
        if final == 0:
        
            morte = len(buttons_finals)
        else:
            morte= final
        

        
        
        
        for i in range(init,morte):

            

            self.driver.execute_script(f'var e = document.getElementsByClassName("pa"); e[{init}].scrollIntoView();')
            
            
            self.driver.execute_script(f'window.scrollBy(0,{scroll})')

            scroll = scroll + 100

            tm(1)

            buttons_finals[i].click()

            tm(4)

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

            self.driver.execute_script('window.scrollBy(0,50)')       
    def verificacao(self):

        try:

            self.driver.find_element_by_id('details-button').click()
            tm(2)
            self.driver.find_element_by_xpath('/html/body/div/div[3]/p[2]/a').click()

        except:

            return



