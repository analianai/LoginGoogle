import json
import tkinter as tk
from tkinter import ttk

# =========================
# Funções utilitárias (modelo)
# =========================

def carregar_db(caminho="db_mock.json"):
    """
    Lê o arquivo JSON com os usuários mockados e
    devolve a lista de usuários (ou lista vazia se não houver).
    """
    with open(caminho, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("users", [])

def encontrar_usuario_por_email(users, identidade):
    """
    Procura um usuário na lista pelo campo 'email'.
    - identidade: o texto digitado pelo aluno no campo de e-mail.
    Retorna o dicionário do usuário se achar; caso contrário, None.
    """
    identidade = identidade.strip()
    for u in users:
        if identidade == u["email"]:
            return u
    return None

# =========================
# Telas (View)
# =========================

class TelaEmail(ttk.Frame):
    """
    Tela 1: Captura o e-mail/telefone (aqui usamos 'email').
    - Se vazio → pede pra digitar algo.
    - Se não existir no JSON → mostra o erro "Não foi possível encontrar sua Conta do Google".
    - Se existir → chama a tela de senha.
    """
    def __init__(self, master, on_email_ok, users):
        """
        master: janela principal (App)
        on_email_ok: callback para ir à próxima tela passando o usuário encontrado
        users: lista de usuários carregados do JSON
        """
        super().__init__(master, padding=20)
        self.on_email_ok = on_email_ok
        self.users = users

        ttk.Label(self, text="Faça login", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, sticky="w")

        ttk.Label(self, text="Email ou Telefone").grid(row=1, column=0, sticky="w", pady=(12, 4))
        self.var_email = tk.StringVar()
        self.ent_email = ttk.Entry(self, textvariable=self.var_email, width=35)
        self.ent_email.grid(row=2, column=0, sticky="we")
        self.ent_email.focus()  # deixa o cursor já no campo ao abrir

        # Label para mensagens de erro (vermelha)
        self.var_erro = tk.StringVar(value="")
        ttk.Label(self, textvariable=self.var_erro, foreground="#b00020").grid(row=3, column=0, sticky="w", pady=(8, 0))

        # Botão para avançar
        ttk.Button(self, text="Próxima", command=self._proxima).grid(row=4, column=0, sticky="e", pady=(16, 0))

        self.columnconfigure(0, weight=1)

    def _proxima(self):
        """Ação do botão 'Próxima'."""
        identidade = self.var_email.get().strip()

        # UX mínima: se o aluno não digitou nada, pedimos pra digitar
        if not identidade:
            self.var_erro.set("Digite seu e-mail ou telefone.")
            return

        # Procura usuário no JSON mockado
        user = encontrar_usuario_por_email(self.users, identidade)

        if user:
            # Achou: limpamos o erro (se houver) e vamos pra tela de senha
            self.var_erro.set("")
            self.on_email_ok(user)  # passa o usuário encontrado para a próxima tela
        else:
            # Não achou: mostramos a mensagem de erro "estilo Google"
            self.var_erro.set("Não foi possível encontrar sua Conta do Google")


class TelaSenha(ttk.Frame):
    """
    Tela 2: Pede a senha do usuário que foi encontrado na tela anterior.
    - Se senha vazia → pede pra digitar
    - Se senha errada → mostra erro "estilo Google"
    - Se correta   → vai pra tela de boas-vindas
    """
    def __init__(self, master, on_login_ok):
        """
        master: janela principal (App)
        on_login_ok: callback que recebe 'nome' e abre a tela de boas-vindas
        """
        super().__init__(master, padding=20)
        self.on_login_ok = on_login_ok
        self.usuario_atual = None  # guardará {'nome', 'email', 'senha'}

        # Título da tela
        self.lbl_header = ttk.Label(self, text="Digite sua senha", font=("Segoe UI", 14, "bold"))
        self.lbl_header.grid(row=0, column=0, sticky="w")

        # Campo de senha (com bolinha)
        ttk.Label(self, text="Senha").grid(row=1, column=0, sticky="w", pady=(12, 4))
        self.var_senha = tk.StringVar()
        self.ent_senha = ttk.Entry(self, textvariable=self.var_senha, width=35, show="•")
        self.ent_senha.grid(row=2, column=0, sticky="we")
        self.ent_senha.focus()

        # Mensagem de erro (vermelha)
        self.var_erro = tk.StringVar(value="")
        ttk.Label(self, textvariable=self.var_erro, foreground="#b00020").grid(row=3, column=0, sticky="w", pady=(8, 0))

        # Botão para entrar
        ttk.Button(self, text="Entrar", command=self._entrar).grid(row=4, column=0, sticky="e", pady=(16, 0))

        self.columnconfigure(0, weight=1)

    def preparar_usuario(self, user_dict):
        """
        É chamada quando chegamos nesta tela:
        - Armazenamos os dados do usuário para checar a senha.
        - Limpamos campo e erro para uma nova tentativa.
        """
        self.usuario_atual = user_dict
        self.var_senha.set("")
        self.var_erro.set("")

    def _entrar(self):
        """Ação do botão 'Entrar'."""
        senha_digitada = self.var_senha.get()

        # UX mínima: se não digitou nada, pede pra digitar
        if not senha_digitada:
            self.var_erro.set("Digite sua senha.")
            return

        # Comparação simples com o mock do JSON
        if senha_digitada != self.usuario_atual["senha"]:
            # Erro "estilo Google" (texto pedido por você)
            self.var_erro.set("Senha incorreta. Tente novamente ou clique em Esqueceu a senha? para escolher outra.")
            return

        # Se chegou aqui, senha está ok → chama a próxima tela passando o NOME
        self.on_login_ok(self.usuario_atual["nome"])


class TelaBemVindo(ttk.Frame):
    """
    Tela 3: Boas-vindas simples.
    - Mostramos "Seja bem-vinda(o), <Nome>!"
    - NÃO exibimos e-mail
    """
    def __init__(self, master, on_sair):
        """
        master: janela principal (App)
        on_sair: callback para voltar ao login (reiniciar o fluxo)
        """
        super().__init__(master, padding=20)
        self.on_sair = on_sair

        # Texto que será atualizado com o nome
        self.var_msg = tk.StringVar(value="Seja bem-vinda(o)!")
        ttk.Label(self, textvariable=self.var_msg, font=("Segoe UI", 16, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 8))

        # Botão de sair (volta pra tela inicial)
        ttk.Button(self, text="Sair", command=self.on_sair).grid(row=1, column=0, sticky="w")

        self.columnconfigure(0, weight=1)

    def set_nome(self, nome):
        """Atualiza a mensagem com o nome do usuário."""
        self.var_msg.set(f"Seja bem-vinda(o), {nome}!")


# =========================
# Aplicação (Controller)
# =========================

class App(tk.Tk):
    """
    Janela principal que gerencia a troca de telas:
    - Começa com TelaEmail
    - Vai para TelaSenha
    - Finaliza em TelaBemVindo (ou volta para o início)
    """
    def __init__(self):
        super().__init__()
        self.title("Login simples (estilo Google)")
        self.geometry("480x240")

        # Carrega a "base" de usuários do JSON
        self.users = carregar_db("db_mock.json")

        # Instancia as telas
        self.tela_email = TelaEmail(self, on_email_ok=self._ir_para_senha, users=self.users)
        self.tela_senha = TelaSenha(self, on_login_ok=self._ir_para_bem_vindo)
        self.tela_bemvindo = TelaBemVindo(self, on_sair=self._voltar_login)

        # Exibe a tela inicial
        self.tela_email.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    # ---- Navegação entre telas ----

    def _ir_para_senha(self, user_dict):
        """Sai da TelaEmail e entra na TelaSenha, preparando o usuário atual."""
        self.tela_email.grid_forget()                # esconde tela atual
        self.tela_senha.preparar_usuario(user_dict)  # informa o usuário encontrado
        self.tela_senha.grid(row=0, column=0, sticky="nsew")  # mostra a tela de senha

    def _ir_para_bem_vindo(self, nome):
        """Sai da TelaSenha e entra na TelaBemVindo, informando o nome."""
        self.tela_senha.grid_forget()
        self.tela_bemvindo.set_nome(nome)
        self.tela_bemvindo.grid(row=0, column=0, sticky="nsew")

    def _voltar_login(self):
        """Sai da TelaBemVindo e volta para a tela inicial (TelaEmail)."""
        self.tela_bemvindo.grid_forget()
        # limpa possíveis mensagens/resíduos da TelaEmail
        self.tela_email.var_erro.set("")
        self.tela_email.var_email.set("")
        self.tela_email.grid(row=0, column=0, sticky="nsew")


# Ponto de entrada da aplicação
if __name__ == "__main__":
    App().mainloop()
