from Simples2018 import Robo2018
from SimplesNacional import Robot
from login import *
from flask import Flask,request
import _thread
import random
import string

from random import randint



app = Flask('Receita')



def detect_plataform():

    import platform

    if platform.system() == 'Linux':
        return '/'
    else:
        return '\\'
def Escolha(year1,year2,controller,day_init,day_final,visivel,password,cnpj,cpf):
    
    dif_anual = year2-year1+1
    
    ano_atual = year1
    
    
    
    inicial = 0
    
    for i in range(dif_anual):
        
        
        
        if ano_atual>2017:
            
            if inicial ==0:
                
                if i == 0:
                    robo = Robo2018(password,cnpj,cpf,controller,visivel)
                    
                else:
                    robo = Robo2018(password,cnpj,cpf,controller,visivel)
                       
            
            if i == 0:

               
               robo.Downloads(str(ano_atual),day_init,0)
            elif i > 0 and i<dif_anual-1:
                
                robo.Downloads(str(ano_atual),0,0)
            elif i == dif_anual-1:
                
                robo.Downloads(str(ano_atual),0,day_final)
                
            ano_atual=ano_atual+1
            inicial = inicial+1
        else:
            
            if i == 0:
               robot = Robot(password,cnpj,cpf,controller,visivel)
               
               robot.Downloads(str(ano_atual),day_init,0)
            elif i > 0 and i<dif_anual-1:
                
                robot.Downloads(str(ano_atual),0,0)
            elif i == dif_anual-1:
               
                robot.Downloads(str(ano_atual),0,day_final)
                
            ano_atual=ano_atual+1
               
def main(password,cnpj,cpf,ant,year_init,day_init,year_final,day_final,visivel):
    
    try:
        os.remove(os.getcwd()+detect_plataform()+cnpj+detect_plataform()+'log.json')
    except:
        print()
    
    if int(year_init) != int(year_final):
        count_pgds_aux = int(year_final)-int(year_init)-1
        count_pgds = (12-int(day_init))+(count_pgds_aux*12)+int(day_final)
    else:
        
        count_pgds = (int(day_init)-int(day_final))

        if count_pgds < 0:
            count_pgds = (count_pgds*-1)+1

    print(count_pgds)
    
    
    login = Login(visivel,cpf,password,cnpj,ant,count_pgds)
    login.login()
        

    
    if year_final != year_init:
        Escolha(year_init,year_final,ant,day_init,day_final,visivel,password,cnpj,cpf)
        open(os.getcwd()+detect_plataform()+cnpj+detect_plataform()+'progress.txt','w').truncate(0)
        open(os.getcwd()+detect_plataform()+cnpj+detect_plataform()+cnpj+'.txt','w').truncate(0)
        open(os.getcwd()+detect_plataform()+cnpj+detect_plataform()+'image.txt','w').truncate(0)
    else:
        
        if year_init > 2017:
            
            robo = Robo2018(password,cnpj,cpf,ant,visivel)
            
            robo.Downloads(year_init,day_init,day_final)
        else:
            robo = Robot(password,cnpj,cpf,ant,visivel)
            
            robo.Downloads(year_init,day_init,day_final)
            open(os.getcwd()+detect_plataform()+cnpj+detect_plataform()+'progress.txt','w').truncate(0)
            open(os.getcwd()+detect_plataform()+cnpj+detect_plataform()+cnpj+'.txt','w').truncate(0)
            open(os.getcwd()+detect_plataform()+cnpj+detect_plataform()+'image.txt','w').truncate(0)
@app.route('/enviarpedido',methods=['POST'])
def init_api():

    json_file = request.get_json()
    print(json_file)
    


    _thread.start_new_thread(main,(json_file['password'],json_file['cnpj'],json_file['cpf'],json_file['antcap'],json_file['year_init'],json_file['day_init']-1,json_file['year_final'],json_file['day_final'],json_file['visible']))

    return json_file['cnpj']
@app.route('/pegarlog',methods=["POST"])
def check_log():

    texto = request.get_data().decode('utf8')
    
    try:
        file_read = open(os.getcwd()+detect_plataform()+texto+detect_plataform()+texto+'.txt','r').read()
        return file_read
    except:
        return 'O arquivo não foi encontrado'

@app.route('/pegarimagem',methods=["POST"])
def get_image():

    texto = request.get_data().decode('utf8')
    
    try:
        file_read = open(os.getcwd()+detect_plataform()+texto+detect_plataform()+'image.txt','r').read()
        return file_read
    except:
        return 'O arquivo não foi encontrado'
@app.route('/pegarprogresso',methods=["POST"])
def get_progres_download():

    texto = request.get_data().decode('utf8')
    
    try:
        file_read = open(os.getcwd()+detect_plataform()+texto+detect_plataform()+'progress.txt','r').read()
        return file_read
    except:
        return 'O arquivo não foi encontrado'
@app.route('/enviarjson',methods=["POST"])
def set_json():

    texto = request.get_json()

    open(os.getcwd()+detect_plataform()+texto['cnpj']+detect_plataform()+'cap.json','w').write(json.dumps(texto))

    return 'Enviado com Sucesso!'

    


   


app.run()
    