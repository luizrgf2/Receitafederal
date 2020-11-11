from selenium import webdriver
import pickle
import json
from selenium.webdriver import ChromeOptions
from python_anticaptcha import AnticaptchaClient, ImageToTextTask
import os
from time import sleep as tm
import base64

class Login():

    def __init__(self,visible,cpf,password,cnpj,captcha):

        self.captcha = captcha
        json_file = open('atrr.json','r')
        cache = json.loads(json_file.read())
        
        self.cpf = cpf
        self.cnpj = cnpj
        self.password = password
        self.path = os.getcwd()+'/'+self.cnpj
        
        if os.path.isdir(self.path):

            print('Ja existe esse cliente!')

        else:

            os.mkdir(self.path)


        options = ChromeOptions()

        if(visible == False):

            options.add_argument(cache['driver'][0])
        prefs = {cache['prefs'] : f'{self.path}'}
        options.add_experimental_option('prefs', prefs)
        options.add_argument(cache['driver'][1])
        options.add_argument(cache['driver'][2])
        self.driver = webdriver.Chrome(executable_path=os.getcwd()+'/'+'chromedriver',chrome_options=options)
        self.driver.get('https://www8.receita.fazenda.gov.br/SimplesNacional/controleAcesso/Autentica.aspx?id=60')
        tm(3)
    def login(self):

        self.driver.find_element_by_name('ctl00$ContentPlaceHolder$txtCNPJ').send_keys(self.cnpj)
        self.driver.find_element_by_name('ctl00$ContentPlaceHolder$txtCPFResponsavel').send_keys(self.cpf)
        self.driver.find_element_by_name('ctl00$ContentPlaceHolder$txtCodigoAcesso').send_keys(self.password)
        tm(3)
        self.sistema_capcha()
        self.driver.close()
    def sistema_capcha(self):
        
        while(True):
            if self.captcha == True:
                try:
                    try:
                        tm(3)
                        self.driver.find_element_by_name('ctl00$ContentPlaceHolder$txtCodigoAcesso').send_keys(self.password)
                    except:
                        tm(3)
                        self.saving_session()
                        break
                    
                    self.driver.find_element_by_xpath('/html/body/form/div[3]/div[2]/div[2]/div[1]/div/div[2]/input').send_keys(self.quebracaptcha())
                    self.driver.find_element_by_xpath('/html/body/form/div[3]/div[2]/div[2]/div[1]/div[1]/div[3]/input').click()
                    tm(5)

                    try:
                        self.driver.find_elements_by_id('ctl00_ContentPlaceHolder_lblErro')
                        print('Captcha errado')
                    except:
                        break
                except:
                    print('Não existe saldo para o uso do sistema de antcaptcha!')
                    self.captcha = False
            elif self.captcha == False:
                try:
                    tm(3)
                    self.driver.find_element_by_name('ctl00$ContentPlaceHolder$txtCodigoAcesso').send_keys(self.password)
                except:
                    
                    self.saving_session()
                    break
                tm(3)
                self.get_image()
                
                self.driver.find_element_by_xpath('/html/body/form/div[3]/div[2]/div[2]/div[1]/div/div[2]/input').send_keys(self.get_json())
                tm(2)
                self.driver.find_element_by_xpath('/html/body/form/div[3]/div[2]/div[2]/div[1]/div[1]/div[3]/input').click()
                
            self.get_element_error_login()
                    

        tm(4)
    def quebracaptcha(self):



        api_key = 'fc123745c9de9f98a08ae253ea3dc226'
        captcha_fp = self.get_image()
        client = AnticaptchaClient(api_key)
        task = ImageToTextTask(captcha_fp)
        job = client.createTask(task)
        job.join()
        print(job.get_captcha_text())
        return job.get_captcha_text()   
    def get_image(self):


        img = self.driver.find_element_by_id('captcha-img').get_attribute('src')

        image_base64 = img.split('data:image/png;base64,')[1]

        base64_img = image_base64.encode('utf-8')


         

        open(f'{self.path}/image.png','wb').write(base64.decodebytes(base64_img))
        return open(f'{self.path}/image.png','rb')
    def saving_session(self):
        pickle.dump( self.driver.get_cookies() , open(f"{self.path}/cookies.pkl","wb"))   
    def get_json(self):

        while(True):

            try:

                file = open(f'{self.path}/cap.json','r')
                break
            except:

                print('Aguardando!....')
                tm(3) 
                



        dados = json.load(file)['cap']
        os.remove(f'{self.path}/cap.json')
        return dados
    def get_element_error_login(self):
        import sys
        file_log = None
        try:
            element_error = self.driver.execute_script('var a = document.getElementsByClassName("label erro"); return a[0].innerText;')
            print(element_error)
            if element_error == 'Caracteres anti-robô inválidos. Tente novamente.':
                element_error = 'Captcha errado!'
            elif element_error == 'Número de CNPJ fornecido não cadastrado no CNPJ':
                element_error = 'CNPJ fornecido nao cadastrado no CNPJ!'
                
                
            elif element_error == 'CPF inválido não cadastrado na base CPF':
                element_error = 'CPF invalido!'
                
            elif element_error == 'Código de acesso deve ser informado com 12 dígitos':
                element_error = 'Codigo de acesso deve ser informado com 12 dígitos'
                
            elif element_error.find('Código de acesso inválido')!= -1:
                print(element_error)
                element_error = 'Codigo de acesso invalido'
                


            file_log = open(self.path+'/log.json','r')
            dados = json.loads(file_log.read())
            dados['login_error'] = element_error
            data = json.dumps(dados,indent=4)
            open(self.path+'/log.json','w',-1, "utf-8").write(data)

        except Exception as e:
            if str(e).find('Message: javascript error: Cannot read property') != -1:
                print('')
            if str(e).find('[Errno 2] No such file or directory:') != -1:

                dados = {

                    "progress":0,
                    "login_error":element_error,
                    "pgdas":None


                }
                data = json.dumps(dados,indent=4)
                open(self.path+'/log.json','w',-1, "utf-8").write(data)

            

