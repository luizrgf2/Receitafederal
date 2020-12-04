from selenium import webdriver
from time import sleep as tm
import os
from python_anticaptcha import AnticaptchaClient, ImageToTextTask
import base64
import sys
import json
import pickle
import requests
import glob
import stractor
import _thread

class Robot():

    def __init__(self, code, cnpj, cpf,anticaptcha, visivel):
        self.anticaptcha = anticaptcha  
        self.code = code
        self.cnpj = cnpj
        self.cpf = cpf
        self.path = os.getcwd()+self.detect_plataform()+f'{self.cnpj}'
        self.ano = '2015'


        options = webdriver.ChromeOptions() 
        prefs = {'download.default_directory' : f'{self.path}'}
        options.add_experimental_option('prefs', prefs)
        
        options.add_argument("--start-maximized")
        
        if visivel == False:
            options.add_argument("--headless")
        options.add_argument('ignore-certificate-errors')
        options.add_argument('--no-sandbox')
        
        import platform

        if platform.system() == 'Linux':

            self.driver = webdriver.Chrome(executable_path=os.getcwd()+self.detect_plataform()+'chromedriver',chrome_options=options)
        else:
            self.driver = webdriver.Chrome(executable_path=os.getcwd()+self.detect_plataform()+'chromedriver.exe',chrome_options=options)



        self.driver.get('https://www8.receita.fazenda.gov.br/SimplesNacional/controleAcesso/Autentica.aspx?id=6')

        tm(1)
        cookies = pickle.load(open(f"{self.path}"+self.detect_plataform()+"cookies.pkl", "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        tm(3)
        self.driver.get('https://www8.receita.fazenda.gov.br/SimplesNacional/controleAcesso/Autentica.aspx?id=6')
        tm(3)


        self.verificacao()

        tm(2)
    def Downloads(self,ano,init,final):
        porcentagem_conclusao = 0

        file_json = json.loads(open(self.cnpj+self.detect_plataform()+"log.json",'r').read())
        file_json['progress'] = porcentagem_conclusao
        data = json.dumps(file_json,indent=4)
        open(self.cnpj+self.detect_plataform()+"log.json",'w').write(data)
        arquivos = []


        file_json = json.loads(open(self.cnpj+self.detect_plataform()+"log.json",'r').read())
        file_json['pgdas'] = None
        data = json.dumps(file_json,indent=4)
        open(self.cnpj+self.detect_plataform()+"log.json",'w').write(data)
        
        self.ano = ano
        
        tm(2)

        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[6]/a/span').click()

        tm(2)

        self.driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[2]/div[1]/input').send_keys(self.ano)

        tm(2)
        
        self.driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[3]/a[3]').click()

        tm(2)
        
        
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

            cookies = self.driver.get_cookies()
            print(cookies)

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
                'Cookie':'ARRAffinity='+cookies[5]['value']+'; '+'cookieAcessoPJ='+cookies[1]['value']+'; '+'cookieAcessoPJValidade='+cookies[3]['value']+'; '+'sinac.quantidadeMensagens=2; '+'sinac.urlRedirecionamento=/SimplesNacional/Aplicacoes/ATSPO/pgdasd.app/default.aspx; '+'ASP.NET_SessionId='+cookies[0]['value']
                



            }

            response = requests.post('https://www8.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/pgdasd.app/ImprimirApuracao.aspx',headers=headers,data={'idApuracao': buttons_finals[i].text},verify=False)
            
            

            

            

            texto = tempos[i].text.split('/')
            texto_final = texto[0]+'_'+texto[1]

            if os.path.isdir(self.path+self.detect_plataform()+f'{self.ano}'):

                print('Ja existe o diretorio!!')

            else:

                os.mkdir(self.path+self.detect_plataform()+f'{self.ano}')
  
            directory = self.path+self.detect_plataform()+f'{self.ano}'+self.detect_plataform()+f'{texto_final}.pdf'
            open(directory,'wb').write(response.content)
            
            stractor.main(texto_final+'.pdf',texto_final,self.cnpj,self.ano,self.path+self.detect_plataform()+f'{self.ano}')

            

            
        
            self.driver.execute_script('window.scrollBy(0,50)')
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


