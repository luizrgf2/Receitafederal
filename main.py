from Simples2018 import Robo2018
from SimplesNacional import Robot
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('password')
parser.add_argument('cnpj')
parser.add_argument('cpf')
parser.add_argument('ant')
parser.add_argument('year_init')
parser.add_argument('day_init')
parser.add_argument('year_final')
parser.add_argument('day_final')
parser.add_argument('visivel')
args = parser.parse_args()


def Escolha(year1,year2,controller,day_init,day_final,visivel):
    
    dif_anual = year2-year1+1
    
    ano_atual = year1
    
    
    
    inicial = 0
    
    for i in range(dif_anual):
        
        
        
        if ano_atual>2017:
            
            if inicial ==0:
                
                if i == 0:
                    robo = Robo2018(args.password,args.cnpj,args.cpf,controller,visivel)
                    robo.acess()
                else:
                    robo = Robo2018(args.password,args.cnpj,args.cpf,controller,visivel)
                    robo.acess()    
            
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
               robot = Robot(args.password,args.cnpj,args.cpf,controller,visivel)
               robot.acess()
               robot.Downloads(str(ano_atual),day_init,0)
            elif i > 0 and i<dif_anual-1:
                robot.Downloads(str(ano_atual),0,0)
            elif i == dif_anual-1:
                robot.Downloads(str(ano_atual),0,day_final)
                
            ano_atual=ano_atual+1
                
def main():
    

    visivel= False
    controller = False
    
    if args.ant == 'true' or args.ant == 'True':
        
        controller= True
        
    if args.visivel == 'true' or args.visivel == 'True':
        
        visivel= True
    
    
        
    day_init = int(args.day_init)-1
    year_init = int(args.year_init)
    day_final = int(args.day_final)
    year_final = int(args.year_final)
    
    if year_final != year_init:
        Escolha(year_init,year_final,controller,day_init,day_final,visivel)
    else:
        
        if year_init > 2017:
            
            robo = Robo2018(args.password,args.cnpj,args.cpf,controller,visivel)
            robo.acess()
            robo.Downloads(year_init,day_init,day_final)
        else:
            robo = Robot(args.password,args.cnpj,args.cpf,controller,visivel)
            robo.acess()
            robo.Downloads(year_init,day_init,day_final)
            
    
main()