# Login do Google
login_simples/
├─ app.py          # interface Tkinter + lógica de navegação (comentado)
└─ db_mock.json    # "banco" mockado separado (vários usuários)

### Funcionamento

- Lê usuários de um JSON (db_mock.json).
- Fluxo:
1) Tela E-MAIL: procura usuário por email/telefone (aqui é "email")
-> se não encontrar, mostra: "Não foi possível encontrar sua Conta do Google"
2) Tela SENHA: pede senha
-> se errar, mostra: "Senha incorreta. Tente novamente ou clique em Esqueceu a senha? para escolher outra."
3) Tela BEM-VINDO: mostra "Seja bem-vinda(o), <Nome>!" (sem exibir o e-mail)

### Lógica Aplicada

````Python
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
````

### Simulação do Bando de Dados Mock no Arquivo Json

Imagina que nosso arquivo **db_mock.json** é um banco.
Dentro dele temos uma “tabela” chamada _users_. 

 * Essa tabela tem as colunas (campos):

  1. nome
  2. email
  3. senha

E cada linha da tabela é um usuário.

````Json
{
  "users": [
    { "nome": "Anália",   "email": "analia",   "senha": "123" },
    { "nome": "Rafael",   "email": "rafa",     "senha": "abc" },
    { "nome": "Jaqueline","email": "jaque",    "senha": "456" },
    { "nome": "Eduardo",  "email": "dudu",     "senha": "xyz" }
  ]
}
````

### Codigo com a lógica Utilizando MOCKADOS

1. Importar a biblioteca JSON (serve para ler/transformar arquivos .json em dicionários Python)

````python
import json   
````

2. Carregar o banco de dados mockado, utilizando o comando 'with', que é um GERENCIADOR DE CONTEXTO que abre o arquivo, deixa a gente usar e FECHA automaticamente quando terminar o bloco.

open("db_mock.json", "r", encoding="utf-8"):
    - "db_mock.json" → nome do arquivo que vamos abrir
    - "r" → modo de abertura = "read" (somente leitura)
    - encoding="utf-8" → garante que caracteres especiais (acentos, ç) sejam lidos corretamente
    
    as f → o arquivo aberto será chamado de "f" (poderia ser outro nome)
    
    vantagem do 'with':
    - não precisamos usar f.close()
    - mesmo se der erro dentro do bloco, o arquivo é fechado automaticamente

````python
with open("db_mock.json", "r", encoding="utf-8") as f:  
````

3. Transforma o conteúdo JSON do arquivo em um dicionário Python e guarda na variável 'db'

````python
db = json.load(f)
````

# pedir o email/telefone

