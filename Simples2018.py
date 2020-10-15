from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep as tm
import os
from python_anticaptcha import AnticaptchaClient, ImageToTextTask
import base64
import sys
import json



class Robo2018():

    def __init__(self, code, cnpj, cpf, anticapcha, visivel):
        self.raiz = ''
        self.anticapcha = anticapcha
        import platform
        if platform.system() == 'Windows':
            
            self.raiz = '\\'
            
        else:
            
            self.raiz = '/'
        
        self.code = code
        self.cnpj = cnpj
        self.cpf = cpf
        self.path = '/home/pgdas/'+f'{self.cnpj}'
        self.ano = '2015'

        if os.path.isdir(self.path):

            print('Já existe esse cliente!')

        else:

            os.mkdir(self.path)

        options = webdriver.ChromeOptions() 
        prefs = {'download.default_directory' : f'{self.path}'}
        options.add_experimental_option('prefs', prefs)
        if visivel == False:
            options.add_argument("--headless")
        options.add_argument('ignore-certificate-errors')

        self.driver = webdriver.Chrome(executable_path=os.getcwd()+self.raiz+'chromedriver',chrome_options=options)

        self.driver.get('https://www8.receita.fazenda.gov.br/SimplesNacional/controleAcesso/Autentica.aspx?id=60')

        tm(3)

        self.verificacao()

        tm(2)

    def acess(self):
        tm(3)
        self.driver.find_element_by_name('ctl00$ContentPlaceHolder$txtCNPJ').send_keys(self.cnpj)
        self.driver.find_element_by_name('ctl00$ContentPlaceHolder$txtCPFResponsavel').send_keys(self.cpf)
        self.driver.find_element_by_name('ctl00$ContentPlaceHolder$txtCodigoAcesso').send_keys(self.code)
        tm(3)
        
        
    
        while(True):
        
            if self.anticapcha == True:
                try:
                    self.driver.find_element_by_id('txtTexto_captcha_serpro_gov_br').send_keys(self.quebracaptcha())
                    self.driver.find_element_by_name('ctl00$ContentPlaceHolder$btContinuar').click()
                except:
                    self.anticapcha = False
                    print('Não existe saldo para o uso do antcaptcha!')
                    
                    
                    
                    
                    
            elif self.anticapcha == False:
                
                self.get_image()
                             
                
                
                self.driver.find_element_by_xpath('/html/body/form/div[3]/div[2]/div[2]/div[1]/div/div[2]/input').send_keys(self.get_json())

                os.remove(self.path+f'{self.raiz}cap.json')

                self.driver.find_element_by_name('ctl00$ContentPlaceHolder$btContinuar').click()
                tm(2)

            self.driver.get('https://www8.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/pgdasd2018.app/Consulta')
                
            tm(3)
            
            try:
                self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/div[2]/div/div/div/div/div/h4')
                self.driver.get('https://www8.receita.fazenda.gov.br/SimplesNacional/controleAcesso/Autentica.aspx?id=60')
                tm(2)
                self.driver.find_element_by_name('ctl00$ContentPlaceHolder$txtCNPJ').send_keys(self.cnpj)
                self.driver.find_element_by_name('ctl00$ContentPlaceHolder$txtCPFResponsavel').send_keys(self.cpf)
                self.driver.find_element_by_name('ctl00$ContentPlaceHolder$txtCodigoAcesso').send_keys(self.code)
            except:
                print('Captcha errada!')
                break    
                       
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

            if os.path.isdir(self.path+f'{self.raiz}{self.ano}'):

                print('Ja existe o diretorio!!')

            else:

                os.mkdir(self.path+f'{self.raiz}{self.ano}')

            


            file = open(self.path+f'{self.raiz}{arquivos[0]}','rb')

            filecreate = open(self.path+f'{self.raiz}{self.ano}{self.raiz}{texto_final}.pdf','wb')
            filecreate.write(file.read())
            filecreate.close()

            file.close()

            os.remove(self.path+f'{self.raiz}{arquivos[0]}')    
      
    def quebracaptcha(self):



        api_key = 'fc123745c9de9f98a08ae253ea3dc226'
        captcha_fp = self.get_image()
        client = AnticaptchaClient(api_key)
        task = ImageToTextTask(captcha_fp)
        job = client.createTask(task)
        job.join()
        print(job.get_captcha_text())
        return job.get_captcha_text()

    def verificacao(self):

        try:

            self.driver.find_element_by_id('details-button').click()
            tm(2)
            self.driver.find_element_by_xpath('/html/body/div/div[3]/p[2]/a').click()

        except:

            return
    def get_image(self):


        img = self.driver.find_element_by_id('captcha-img').get_attribute('src')

        image_base64 = img.split('data:image/png;base64,')[1]

        base64_img = image_base64.encode('utf-8')

         

        open(f'{self.path}{self.raiz}image.png','wb').write(base64.decodebytes(base64_img))
        return open(f'{self.path}{self.raiz}image.png','rb')

    def get_json(self):

        while(True):

            try:

                file = open(f'{self.path}{self.raiz}cap.json','r')
                break
            except:

                print('Aguardando!....')
                tm(3)
        dados = json.load(file)
        return dados['cap']
