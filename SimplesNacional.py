from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep as tm
import os
from python_anticaptcha import AnticaptchaClient, ImageToTextTask
import base64


class Robot():

    def __init__(self, code, cnpj, cpf, ano):

        
        self.code = code
        self.cnpj = cnpj
        self.cpf = cpf
        self.path = os.getcwd()+f'\\{self.cnpj}'
        self.ano = ano

        if os.path.isdir(self.path):

            print('Já existe esse cliente!')

        else:

            os.mkdir(self.path)

        options = webdriver.ChromeOptions() 
        prefs = {'download.default_directory' : f'{self.path}'}
        options.add_experimental_option('prefs', prefs)

        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),chrome_options=options)

        self.driver.get('https://www8.receita.fazenda.gov.br/SimplesNacional/controleAcesso/Autentica.aspx?id=6')

        tm(3)

    def acess(self):

        self.driver.find_element_by_name('ctl00$ContentPlaceHolder$txtCNPJ').send_keys(self.cnpj)
        self.driver.find_element_by_name('ctl00$ContentPlaceHolder$txtCPFResponsavel').send_keys(self.cpf)
        self.driver.find_element_by_name('ctl00$ContentPlaceHolder$txtCodigoAcesso').send_keys(self.code)
        tm(3)
        
        a= input('Deseja usar o ANTCAPTCHA [s = sim, n = não]!\n')

        if a == 's' or a == 'S':
            
            self.driver.find_element_by_id('txtTexto_captcha_serpro_gov_br').send_keys(self.quebracaptcha())
            self.driver.find_element_by_name('ctl00$ContentPlaceHolder$btContinuar').click()
            
        elif a == 'n' or a == 'N':
            
            a= input('Digite o recaptcha e depois digite [c = continuar]!\n')
            if a == 'c' or a == 'C':

                self.driver.find_element_by_name('ctl00$ContentPlaceHolder$btContinuar').click()

        tm(3)

        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[6]/a/span').click()

        tm(4)

        

        self.driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[2]/div[1]/input').send_keys(self.ano)

        tm(3)
        
        self.driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[3]/a[3]').click()

        tm(3)

    def Downloads(self):
        i = 0
        tempos = self.driver.find_elements_by_class_name('pa')
        retificacoes = self.driver.find_elements_by_xpath('//*[@tipo="R"]')
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


            except:


                
                count = k+1

        buttons_finals.append(self.driver.find_element_by_xpath(f'/html/body/div[2]/div[3]/div[2]/div[1]/div[1]/div[2]/table[2]/tbody/tr[{len(linhas)}]/td[1]/a'))               
        scroll = 50
        for i in range(len(buttons_finals)):

            self.driver.execute_script(f'window.scrollBy(0,{scroll})')

            scroll = scroll + 50

            tm(1)

            buttons_finals[i].click()

            tm(2)

            arquivos = [_ for _ in os.listdir(self.path) if _.endswith(r'.pdf')]

            print(arquivos)

            texto = tempos[i].text.split('/')
            texto_final = texto[0]+'_'+texto[1]

            if os.path.isdir(self.path+f'\\{self.ano}'):

                print('Ja existe o diretorio!!')

            else:

                os.mkdir(self.path+f'\\{self.ano}')

            


            file = open(self.path+f'\\{arquivos[0]}','rb')

            filecreate = open(self.path+f'\\{self.ano}\\{texto_final}.pdf','wb')
            filecreate.write(file.read())
            filecreate.close()

            file.close()

            os.remove(self.path+f'\\{arquivos[0]}')

            self.driver.execute_script('window.scrollBy(0,50)')

        


                
 










        print(len(buttons_finals))

    def quebracaptcha(self):

        img = self.driver.find_element_by_id('captcha-img').get_attribute('src')

        image_base64 = img.split('data:image/png;base64,')[1]

        base64_img = image_base64.encode('utf-8')

         

        open('image.png','wb').write(base64.decodebytes(base64_img))

        api_key = 'f482d7c8bebbda3a85950a588e53a40f'
        captcha_fp = open('image.png', 'rb')
        client = AnticaptchaClient(api_key)
        task = ImageToTextTask(captcha_fp)
        job = client.createTask(task)
        job.join()
        print(job.get_captcha_text())
        return job.get_captcha_text()



robo= Robot(cpf='60087846934',cnpj='00448750000120',code='337563864600',ano='2016')

robo.acess()
robo.Downloads()





