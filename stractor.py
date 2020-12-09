from selenium import webdriver
import os
from time import sleep as tm
import requests
import datetime
import json


def get_plataform():

    import platform

    if platform.system() == 'Linux':
        return '/'
    else:
        return '\\'
def get_text_from_file(name_file:str,path:str):
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('ignore-certificate-errors')
    chrome_options.add_argument('--no-sandbox')
    import platform

    if platform.system() == 'Linux':

        driver = webdriver.Chrome(executable_path=os.getcwd()+get_plataform()+'chromedriver',chrome_options=chrome_options)
    else:
        
        driver = webdriver.Chrome(executable_path=os.getcwd()+get_plataform()+'chromedriver.exe',chrome_options=chrome_options)
        


    driver.get('https://www.aconvert.com/pdf/pdf-to-txt/#')
    while True:
        try:
            inputt = driver.find_element_by_id('file')
            inputt.send_keys(path+get_plataform()+name_file)
            break
        except Exception as e:
            print(e)
    while True:
        try:
            driver.find_element_by_id('submitbtn').click()
            break
        except Exception as e:
            print(e)
    response = None
    
    while True:
        try:
            
            link = driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[2]/div[1]/div[3]/div[1]/table/tbody/tr/td[2]/a').get_attribute('href')
            print(link)
            response = requests.get(link)
            
            
            driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[2]/div[1]/div[3]/div[1]/table/tbody/tr/td[4]/a[2]/span').click()
            break
        except Exception as e:
            print(e)     
    return response.text
def search_from_cpf(cnpj:str,text:str):

    text_cpf  = text
    aux1 = text_cpf.split(f': {cnpj}')[1]
    aux2 = aux1.split('Valor Informado: ')[1]
    value = aux2.split('\n')[0]
    value = value[0:len(value)-1]

    return value
def get_com_tributacao(cnpj:str,text:str):
    text_cpf  = text
    aux1 = text_cpf.split(f': {cnpj}')[1]
    
    if aux1.find('CNPJ: ')!= -1:
        aux1 = aux1.split('CNPJ: ')[0]
    
    elif aux1.find('CNPJ Estabelecimento: ') != -1:
        aux1 = aux1.split('CNPJ Estabelecimento: ')[0]
    
    aux2 =''
    result = None
    parcela = None
    lista = []
    if aux1.find('om substitui') != -1:
        aux2 = aux1.split('om substitui')[1]
        if aux2.find('Receita Bruta Informada: R$ ') != -1:

            aux3 = aux2.split('Receita Bruta Informada: R$ ')[1]
            aux4 = aux3.split('\n')[0]
            aux4 = aux4[0:len(aux4)-1]
            result = aux4.strip(' ')
        elif aux2.find('Valor Total (R$): ') != -1:
            
            aux3 = aux2.split('Valor Total (R$): ')[1]
            aux4 = aux3.split('\n')[0]
            aux4 = aux4[0:len(aux4)-1]
            result = aux4.strip(' ')
        elif aux2.find('Valor Total (R$):') != -1:
            
            aux3 = aux2.split('Valor Total (R$):')[1]
            aux4 = aux3.split('                                            ')[1].split('\n')[0]
            aux4 = aux4[0:len(aux4)-1]
            result = aux4.strip(' ')
        if aux2.find('Parcela 1:') != -1:

            try:
                aux4 = aux2.split('Parcela 1: R$ ')[1].split('\n')[0].strip(' ')
                aux4 = aux4[0:len(aux4)-1]
            except:
                aux4 = str(aux2.split('Parcela 1: ')[1].split('\n')[0].strip(' '))
                aux4 = aux4[0:len(aux4)-1]

            if aux4.find(result) != -1:
                lista.append(result)
                lista.append('parcela 1')
            else:
                lista.append(result)
                lista.append('mais de uma parcela')
            
        else:
            aux4 = aux2.split('Parcela 1 = ')[1].split('\n')[0].strip(' ')
            print(aux4)
            if aux4.find(result) != -1:
                lista.append(result)
                lista.append('parcela 1')
            else:
                lista.append(result)
                lista.append('mais de uma parcela')
            

    
    return lista
def get_sem_tributacao(cnpj:str,text:str):
    text_cpf  = text
    aux1 = text_cpf.split(f': {cnpj}')[1]
    
    if aux1.find('CNPJ: ')!= -1:
        aux1 = aux1.split('CNPJ: ')[0]
    
    elif aux1.find('CNPJ Estabelecimento: ') != -1:
        aux1 = aux1.split('CNPJ Estabelecimento: ')[0]
        print(aux1)
    
    aux2 =''
    result = None
    lista = []
    if aux1.find('em substitui') != -1:
        aux2 = aux1.split('em substitui')[1]
        if aux2.find('Receita Bruta Informada: R$ ') != -1:

            aux3 = aux2.split('Receita Bruta Informada: R$ ')[1]
            aux4 = aux3.split('\n')[0]
            aux4 = aux4[0:len(aux4)-1]
            result = aux4.strip(' ')
        elif aux2.find('Valor Total (R$): ') != -1:
            
            aux3 = aux2.split('Valor Total (R$): ')[1]
            aux4 = aux3.split('\n')[0]
            aux4 = aux4[0:len(aux4)-1]
            result = aux4.strip(' ')
        elif aux2.find('Valor Total (R$):') != -1:
            
            aux3 = aux2.split('Valor Total (R$):')[1]
            aux4 = aux3.split('                                            ')[1].split('\n')[0]
            aux4 = aux4[0:len(aux4)-1]
            result = aux4.strip(' ')
        if aux2.find('Parcela 1:') != -1:

            try:
                aux4 = aux2.split('Parcela 1: R$ ')[1].split('\n')[0].strip(' ')
                aux4 = aux4[0:len(aux4)-1]
            except:
                aux4 = aux2.split('Parcela 1: ')[1].split('\n')[0].strip(' ')
                aux4 = aux4[0:len(aux4)-1]

            if result == aux4:
                lista.append(result)
                lista.append('parcela 1')
            else:
                lista.append(result)
                lista.append('mais de uma parcela')
            
        else:
            aux4 = aux2.split('Parcela 1 = ')[1].split('\n')[0].strip(' ')
            aux4 = aux4[0:len(aux4)-1]
            if result == aux4:
                lista.append(result)
                lista.append('parcela 1')
            else:
                lista.append(result)
                lista.append('mais de uma parcela')
    
    return lista
def get_prestacao_servicos(cnpj:str,text:str):
    text_cpf  = text
    aux1 = text_cpf.split(f': {cnpj}')[1]
    
    if aux1.find('CNPJ: ')!= -1:
        aux1 = aux1.split('CNPJ: ')[0]
    
    elif aux1.find('CNPJ Estabelecimento: ') != -1:
        aux1 = aux1.split('CNPJ Estabelecimento: ')[0]
        print(aux1)
    
    aux2 =''
    result = None
    lista = []
    if aux1.find('Presta') != -1:
        aux2 = aux1.split('Presta')[1]
        if aux2.find('Receita Bruta Informada: R$ ') != -1:

            aux3 = aux2.split('Receita Bruta Informada: R$ ')[1]
            aux4 = aux3.split('\n')[0]
            aux4 = aux4[0:len(aux4)-1]
            result = aux4.strip(' ')
        elif aux2.find('Valor Total (R$): ') != -1:
            
            aux3 = aux2.split('Valor Total (R$): ')[1]
            aux4 = aux3.split('\n')[0]
            aux4 = aux4[0:len(aux4)-1]
            result = aux4.strip(' ')
        elif aux2.find('Valor Total (R$):') != -1:
            
            aux3 = aux2.split('Valor Total (R$):')[1]
            aux4 = aux3.split('                                            ')[1].split('\n')[0]
            aux4 = aux4[0:len(aux4)-1]
            result = aux4.strip(' ')
        if aux2.find('Parcela 1:') != -1:

            try:
                aux4 = aux2.split('Parcela 1: R$ ')[1].split('\n')[0].strip(' ')
                aux4 = aux4[0:len(aux4)-1]
            except:
                aux4 = aux2.split('Parcela 1: ')[1].split('\n')[0].strip(' ')
                aux4 = aux4[0:len(aux4)-1]
            if result == aux4:
                lista.append(result)
                lista.append('parcela 1')
            else:
                lista.append(result)
                lista.append('mais de uma parcela')
            
        else:
            aux4 = aux2.split('Parcela 1 = ')[1].split('\n')[0].strip(' ')
            aux4 = aux4[0:len(aux4)-1]
            if result == aux4:
                lista.append(result)
                lista.append('parcela 1')
            else:
                lista.append(result)
                lista.append('mais de uma parcela')
    
    return lista
def get_total_receita_bruta(text:str):
    text_cnpj = text
    string_data_apuracao = ''
    string_data_abertura = ''
    mes_ap = None
    ano_ap = None
    mes_init = None
    ano_init = None
    receita_bruta = None

    if text_cnpj.find('(PA): ') != -1:
        string_data_apuracao = text_cnpj.split('(PA): ')[1].split('\n')[0]
    elif text_cnpj.find('odo de Apura') != -1:
        string_data_apuracao = str(text_cnpj.split('odo de Apura')[1].split('/')[1]+'/'+text_cnpj.split('odo de Apura')[1].split('/')[2]).split(' ')[0]
    if text_cnpj.find('Data de Abertura no CNPJ: ') != -1:
        string_data_abertura = text_cnpj.split('Data de Abertura no CNPJ: ')[1].strip(' ').split('\n')[0].split('/')[1]+'/'+text_cnpj.split('Data de Abertura no CNPJ: ')[1].strip(' ').split('\n')[0].split('/')[2]
    elif text_cnpj.find('Data de Abertura: ') != -1:
        string_data_abertura = str(text_cnpj.split('Data de Abertura: ')[1].strip(' ').split('\n')[0].split('/')[1]+'/'+text_cnpj.split('Data de Abertura: ')[1].strip(' ').split('\n')[0].split('/')[2]).split(' ')[0]
    elif text_cnpj.find('Data de abertura no CNPJ:') != -1:
        string_data_abertura = text_cnpj.split('Data de abertura no CNPJ: ')[1].strip(' ').split('\n')[0].split('/')[1]+'/'+text_cnpj.split('Data de abertura no CNPJ: ')[1].strip(' ').split('\n')[0].split('/')[2]
    
    
    ano_init = int(string_data_abertura.split('/')[1].split(' ')[0])
    mes_init = int(string_data_abertura.split('/')[0])
    ano_ap = int(string_data_apuracao.split('/')[1])
    mes_ap = int(string_data_apuracao.split('/')[0])

    if ano_init == ano_ap:
        receita_bruta = text_cnpj.split('(RBT12p)')[1].strip(' ').split(' ')[0]
    elif ano_init+1 == ano_ap:

        value_in_meses = (12 - mes_init)+mes_ap
        

        if value_in_meses >= 13:
            receita_bruta = text_cnpj.split('(RBT12)')[1].strip(' ').split(' ')[0]
            
        else:
            receita_bruta = text_cnpj.split('(RBT12p)')[1].strip(' ').split(' ')[0]

    else:
        receita_bruta = text_cnpj.split('(RBT12)')[1].strip(' ').split(' ')[0]


        

            





   

        
    return receita_bruta
def main(name_file,name_file_out,cnpj,data_init,path):
    data = datetime.datetime.now().year
    transfrom_cnpj = cnpj
    if cnpj.find('.') == -1:

        transfrom_cnpj = cnpj[0:2]+'.'+cnpj[2:5]+'.'+cnpj[5:8]+'/'+cnpj[8:12]+'-'+cnpj[12:14]
    
    if data_init >= data - 5 and data_init != 2015:
        text = get_text_from_file(name_file,path)
        text_lines = []

        if text.find('CNPJ Estabelecimento: ') != -1:
            text_lines = text.split('CNPJ Estabelecimento: ')
            for text_line in text_lines:
                
                cnpj_atual = text_line[0:18]
               
                try:
                    total_estabelecimento = search_from_cpf(cnpj_atual,text)
              
                    com_icms = get_com_tributacao(cnpj_atual,text)
                    sem_icms = get_sem_tributacao(cnpj_atual,text)
                    prestacao = get_prestacao_servicos(cnpj_atual,text)
                    total_receita_bruta = get_total_receita_bruta(text)
                    dicionario = {

                        'totais_do_estabelecimento':total_estabelecimento,
                        'com_icms' : com_icms,
                        'sem_icms' : sem_icms,
                        'prestacao_de_servircos': prestacao,
                        'total_receita_bruta': total_receita_bruta

                    }
                    
                    cnpj_com_mascara_separado_por_pontos = cnpj_atual.split('.')   
                    cnpj_sem_mascara = cnpj_com_mascara_separado_por_pontos[0]+cnpj_com_mascara_separado_por_pontos[1]+cnpj_com_mascara_separado_por_pontos[2].split('/')[0]+cnpj_com_mascara_separado_por_pontos[2].split('/')[1].split('-')[0]+cnpj_atual.split('-')[1]
                    open(path+get_plataform()+name_file_out+'_'+cnpj_sem_mascara+'.json','w').write(json.dumps(dicionario,indent=4))
                except Exception as e:
                    print(e)
        else:
            text_lines = text.split('CNPJ: ')
            print(len(text_lines))
            for text_line in text_lines:
                
                cnpj_atual = text_line[0:18]
                print(cnpj_atual)
                try:
                    total_estabelecimento = search_from_cpf(cnpj_atual,text)
                    com_icms = get_com_tributacao(cnpj_atual,text)
                    sem_icms = get_sem_tributacao(cnpj_atual,text)
                    prestacao = get_prestacao_servicos(cnpj_atual,text)
                    total_receita_bruta = get_total_receita_bruta(text)
                    dicionario = {

                        'totais_do_estabelecimento':total_estabelecimento,
                        'com_icms' : com_icms,
                        'sem_icms' : sem_icms,
                        'prestacao_de_servircos': prestacao,
                        'total_receita_bruta': total_receita_bruta

                    }
                    
                    print(dicionario)
                    cnpj_com_mascara_separado_por_pontos = cnpj_atual.split('.')   
                    cnpj_sem_mascara = cnpj_com_mascara_separado_por_pontos[0]+cnpj_com_mascara_separado_por_pontos[1]+cnpj_com_mascara_separado_por_pontos[2].split('/')[0]+cnpj_com_mascara_separado_por_pontos[2].split('/')[1].split('-')[0]+cnpj_atual.split('-')[1]
                    open(path+get_plataform()+name_file_out+'_'+cnpj_sem_mascara+'.json','w').write(json.dumps(dicionario,indent=4))
                except:
                    print('')
            

        




