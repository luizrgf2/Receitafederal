from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep as tm
import os
from python_anticaptcha import AnticaptchaClient, ImageToTextTask
import base64



class Robo2018():

    def __init__(self, code, cnpj, cpf, ano, anticapcha):
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
        self.path = os.getcwd()+f'{self.raiz}{self.cnpj}'
        self.ano = ano

        if os.path.isdir(self.path):

            print('Já existe esse cliente!')

        else:

            os.mkdir(self.path)

        options = webdriver.ChromeOptions() 
        prefs = {'download.default_directory' : f'{self.path}'}
        options.add_experimental_option('prefs', prefs)

        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),chrome_options=options)

        self.driver.get('https://www8.receita.fazenda.gov.br/SimplesNacional/controleAcesso/Autentica.aspx?id=60')

        tm(3)

    def acess(self):
        
        self.driver.find_element_by_name('ctl00$ContentPlaceHolder$txtCNPJ').send_keys(self.cnpj)
        self.driver.find_element_by_name('ctl00$ContentPlaceHolder$txtCPFResponsavel').send_keys(self.cpf)
        self.driver.find_element_by_name('ctl00$ContentPlaceHolder$txtCodigoAcesso').send_keys(self.code)
        tm(3)
        
        
    
        while(True):
            try:
                if self.anticapcha == True:
                
                    self.driver.find_element_by_id('txtTexto_captcha_serpro_gov_br').send_keys(self.quebracaptcha())
                    self.driver.find_element_by_name('ctl00$ContentPlaceHolder$btContinuar').click()
                    
                elif self.anticapcha == False:
                    
                    a= input('Digite o recaptcha e depois digite [c = continuar]!\n')
                    if a == 'c' or a == 'C':

                        self.driver.find_element_by_name('ctl00$ContentPlaceHolder$btContinuar').click()
                        tm(2)

                self.driver.get('https://www8.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/pgdasd2018.app/Consulta')
                
                tm(3)
                self.driver.find_element_by_id('ano').send_keys(self.ano)
                
                
                break
            except:
                
                print('Captcha ERRADA!')
                self.driver.get('https://www8.receita.fazenda.gov.br/SimplesNacional/controleAcesso/Autentica.aspx?id=60')
                tm(2)
                self.driver.find_element_by_name('ctl00$ContentPlaceHolder$txtCNPJ').send_keys(self.cnpj)
                self.driver.find_element_by_name('ctl00$ContentPlaceHolder$txtCPFResponsavel').send_keys(self.cpf)
                self.driver.find_element_by_name('ctl00$ContentPlaceHolder$txtCodigoAcesso').send_keys(self.code)
                
                
        
            
        
        tm(2) 
        self.driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[1]/form/div/button').click()
        tm(3)

    def Downloads(self):
        element = None
        buttons = []
        linhas = []
        tempos = self.driver.find_elements_by_class_name('pa')
        k = 0
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
        
        
        for i in range(len(tempos)):
            
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

        self.driver.close()
    def quebracaptcha(self):

        img = self.driver.find_element_by_id('captcha-img').get_attribute('src')

        image_base64 = img.split('data:image/png;base64,')[1]

        base64_img = image_base64.encode('utf-8')

         

        open('image.png','wb').write(base64.decodebytes(base64_img))

        api_key = 'fc123745c9de9f98a08ae253ea3dc226'
        captcha_fp = open('image.png', 'rb')
        client = AnticaptchaClient(api_key)
        task = ImageToTextTask(captcha_fp)
        job = client.createTask(task)
        job.join()
        print(job.get_captcha_text())
        return job.get_captcha_text()

