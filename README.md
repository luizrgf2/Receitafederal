# Tutorial instalação 

 
 

Para linux é necessário instalar apenas o pip , depois de instalar cole os comandos no terminal: 

 
 

pip install webdriver_manager 

pip install selenium 

pip install python_anticaptcha 

pip install argparse 

pip install PyPDF4

 
 

Para o windows é necessário baixar o python direto do site oficial e manter o pip junto da instalação, após isso apenas execute o install.bat 

 
 

## execução 

execute main.py para iniciar o servidor.

Use a url base http://127.0.0.1:5000
    
na rota /enviarpedido

    exemplo enviando dados para login e datas de download pgdas:
    
    POST REQUEST

    json_file = {
        "password":"337563864600",
        "cnpj":"00448750000120",
        "cpf":"60087846934",
        "antcap":true,
        "year_init":2017,
        "day_init":2,
        "year_final":2018,
        "day_final":9,
        "visible":false
        }



    json_file deve ser enviado no body da requisição para a url http://127.0.0.1:5000/enviarpedido.

na rota /enviarjson 

    exemplo enviando captcha para login:

    POST REQUEST

    json_file={

        "cnpj":"00448750000120",
        "cap":"teste"

    }
    
    
    json_file deve ser enviado no body da requisição para a url http://127.0.0.1:5000/enviarjson.

## possíveis rotas:
    /enviarpedido = request do tipo post enviando um json com todos os dados citados a cima, no body da requisição.
    /pegarlog = request do tipo post enviando o cnpj do cliente como STRING no body da requisição.
    /pegarimagem = request do tipo post enviando o cnpj do cliente como STRING no body da requisição.
    /pegarprogresso = request do tipo post enviando o cnpj do cliente como STRING no body da requisição.
    /enviarjson  = request do tipo post enviando um json com todos os dados citados a cima, no body da requisição.
 

