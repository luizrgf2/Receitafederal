from Simples2018 import Robo2018
from SimplesNacional import Robot


    
import argparse
    
parser = argparse.ArgumentParser()
parser.add_argument('password')
parser.add_argument('cnpj')
parser.add_argument('cpf')
parser.add_argument('year')
parser.add_argument('anticapcha')



args=parser.parse_args()
print(args)

controller = False

if args.anticapcha == 'true' or args.anticapcha == 'True':
    
    controller = True
    
check = int(args.year)
    
if check > 2017:
        
    robo = Robo2018(args.password,args.cnpj,args.cpf,args.year,controller)
    robo.acess()
    robo.Downloads()
    
else:
    robot= Robot(args.password,args.cnpj,args.cpf,args.year,controller)
    robot.acess()
    robot.Downloads()
        
        
