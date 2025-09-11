import json   

with open("db_mock.json", "r", encoding="utf-8") as f:  
    db = json.load(f)   
    
email = input("Email ou Telefone: ")  

usuario = None   
for u in db["users"]:           
    if email == u["email"]:     
        usuario = u             
        break                   
    
if usuario != None:  
    senha = input("Senha: ")   
    if senha == usuario["senha"]:   
        print(usuario["nome"], ", seja Bem vinda(o)!")  
    else:
        print("Senha incorreta. Tente novamente ou clique em Esqueceu a senha? para escolher outra.")
else:
    print("Não foi possível encontrar sua Conta do Google")
