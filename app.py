import json   

with open("db_mock.json", "r", encoding="utf-8") as f:  
    db = json.load(f)   
    
email = input("Email ou Telefone: ")  # pede que o usuário digite o email (ou telefone) e guarda na variável 'email'

# procurar usuário no JSON
usuario = None   # começa assumindo que nenhum usuário foi encontrado
for u in db["users"]:           # percorre a lista de usuários que está dentro da chave "users" no JSON
    if email == u["email"]:     # se o email digitado for igual ao email de um usuário
        usuario = u             # guarda esse usuário na variável 'usuario'
        break                   # para o laço (não precisa continuar procurando)

# se encontrou o usuário
if usuario != None:  # se a variável 'usuario' não está vazia, significa que encontrou o email no banco
    senha = input("Senha: ")   # pede que o usuário digite a senha
    if senha == usuario["senha"]:   # compara a senha digitada com a senha do banco
        print(usuario["nome"], ", seja Bem vinda(o)!")  # se for igual → mensagem de boas-vindas com o nome
    else:
        # se a senha não bateu → mostra mensagem de erro igual ao Google
        print("Senha incorreta. Tente novamente ou clique em Esqueceu a senha? para escolher outra.")
else:
    # se não encontrou o usuário (usuario ainda é None) → mostra mensagem de erro igual ao Google
    print("Não foi possível encontrar sua Conta do Google")
