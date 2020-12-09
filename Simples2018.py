from selenium import webdriver
from time import sleep as tm
import os
from python_anticaptcha import AnticaptchaClient, ImageToTextTask
import base64
import sys
import json
import pickle
import requests
import stractor


class Robo2018():

    def __init__(self, code, cnpj, cpf, anticapcha, visivel):

        
        self.code = code
        self.cnpj = cnpj
        self.cpf = cpf
        self.path = os.getcwd()+self.detect_plataform()+f'{self.cnpj}'
        self.ano = '2015'



        options = webdriver.ChromeOptions() 
        prefs = {'download.default_directory' : f'{self.path}'}
        options.add_experimental_option('prefs', prefs)
        if visivel == False:
            options.add_argument("--headless")
        options.add_argument('ignore-certificate-errors')
        options.add_argument('--no-sandbox')

        import platform

        if platform.system() == 'Linux':

            self.driver = webdriver.Chrome(executable_path=os.getcwd()+self.detect_plataform()+'chromedriver',chrome_options=options)
        else:
            self.driver = webdriver.Chrome(executable_path=os.getcwd()+self.detect_plataform()+'chromedriver.exe',chrome_options=options)




        self.driver.get('https://www8.receita.fazenda.gov.br/SimplesNacional/controleAcesso/Autentica.aspx?id=60')

        tm(1)

        cookies = pickle.load(open(self.path+self.detect_plataform()+"cookies.pkl", "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        tm(3)

        self.driver.get('https://www8.receita.fazenda.gov.br/SimplesNacional/controleAcesso/Autentica.aspx?id=60')

        tm(2)

        self.verificacao()

        tm(2)
    def Downloads(self,ano,init,final):
        porcentagem_conclusao = 0




        file_json = json.loads(open(self.cnpj+self.detect_plataform()+"log.json",'r').read())
        file_json['progress'] = porcentagem_conclusao
        data = json.dumps(file_json,indent=4)
        open(self.cnpj+self.detect_plataform()+"log.json",'w').write(data)

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

            print('Nao existe dados para este ano!')
            file_json = json.loads(open(self.cnpj+self.detect_plataform()+"log.json",'r').read())
            file_json['pgdas'] = "Nao existe dados para este ano!"
            data = json.dumps(file_json,indent=4)
            open(self.cnpj+self.detect_plataform()+"log.json",'w').write(data)
            return
        else:

            
            file_json = json.loads(open(self.cnpj+self.detect_plataform()+"log.json",'r').read())
            file_json['pgdas'] = None
            data = json.dumps(file_json,indent=4)
            open(self.cnpj+self.detect_plataform()+"log.json",'w').write(data)
            
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
                    
                    element = self.driver.find_element_by_xpath(f'/html/body/div[1]/div/div[2]/div[2]/div[2]/div/div/div[1]/table/tbody/tr[{count}]/td[5]/a')
                   
                    
                except:
                    
                    element=element
        
        for i in range(len(linhas)+1):
            
            
            try:
                element = self.driver.find_element_by_xpath(f'/html/body/div[1]/div/div[2]/div[2]/div[2]/div/div/div[1]/table/tbody/tr[{i}]/td[5]/a')
            except:
                element = element
                
        buttons.append(element)
        
        
        for i in range(init,morte):
            
            

            cookies = self.driver.get_cookies()
            

            cookie = None

            try:
                cookie = cookies[0]['name']+'='+cookies[0]['value']+'; '+cookies[1]['name']+'='+cookies[1]['value']+'; '+cookies[2]['name']+'='+cookies[2]['value']+'; '+cookies[3]['name']+'='+cookies[3]['value']+'; '+cookies[4]['name']+'='+cookies[4]['value']+'; '+cookies[5]['name']+'='+cookies[5]['value']+'; '
            except:
                cookie = cookies[0]['name']+'='+cookies[0]['value']+'; '+cookies[1]['name']+'='+cookies[1]['value']+'; '+cookies[2]['name']+'='+cookies[2]['value']+'; '+cookies[3]['name']+'='+cookies[3]['value']+'; '+cookies[4]['name']+'='+cookies[4]['value']+'; '


            headers = {


                'Host': 'www8.receita.fazenda.gov.br',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Upgrade-Insecure-Requests': '1',
                'Origin': 'https://www8.receita.fazenda.gov.br',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
                'Referer': 'https://www8.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/pgdasd.app/default.aspx',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cookie':cookie
                



            }
            link = str(buttons[i].get_attribute('href'))
            response = requests.post(link,headers=headers,verify=False)
            
            
            
            

             
            
            texto = tempos[i].text.split('/')
            texto_final = texto[0]+'_'+texto[1]

            if os.path.isdir(self.path+self.detect_plataform()+f'{self.ano}'):

                print('Ja existe o diretorio!!')

            else:

                os.mkdir(self.path+self.detect_plataform()+f'{self.ano}')

            directory = self.path+self.detect_plataform()+str(self.ano)+self.detect_plataform()+texto_final+'.pdf'

            open(directory,'wb').write(response.content)

            stractor.main(texto_final+'.pdf',texto_final,self.cnpj,self.ano,self.path+self.detect_plataform()+f'{self.ano}')

            porcentagem_conclusao =  porcentagem_conclusao + 100/(morte-init)
            print(porcentagem_conclusao)
            
            file_json = open(self.cnpj+self.detect_plataform()+'log.json','r').read()
            data = json.loads(file_json)
            data['progress'] = porcentagem_conclusao
            dates = json.dumps(data,indent=4)
            open(self.cnpj+self.detect_plataform()+'log.json','w').write(dates)
    def verificacao(self):

        try:

            self.driver.find_element_by_id('details-button').click()
            tm(2)
            self.driver.find_element_by_xpath('/html/body/div/div[3]/p[2]/a').click()

        except:

            return
    def detect_plataform(self):

        import platform

        if platform.system() == 'Linux':
            return '/'
        else:
            return '\\'
