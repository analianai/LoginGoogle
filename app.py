email=input("Email ou Telefone: ")
emailBanco = "analia"
senhaBanco = "123"
NomeBanco = "Anália"
if(email == emailBanco):
  senha = input("Senha: ")
  if(senha == senhaBanco):
    print(NomeBanco,", seja Bem vinda!")
  else:
     print("Senha incorreta. Tente novamente ou clique em Esqueceu a senha? para escolher outra.") 
elif(email != emailBanco):
  print("Não foi possível encontrar sua Conta do Google")