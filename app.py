import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.listview import ListView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

# Funções do banco de dados
def criar_bancos_de_dados():
    conn_doacoes = sqlite3.connect('doacoes.db')
    cursor_doacoes = conn_doacoes.cursor()
    cursor_doacoes.execute('''
    CREATE TABLE IF NOT EXISTS doacoes (
        id INTEGER PRIMARY KEY,
        tipo TEXT NOT NULL,
        itens TEXT NOT NULL,
        doador TEXT NOT NULL
    )
    ''')
    conn_doacoes.commit()

    conn_ja_doados = sqlite3.connect('itens_ja_doados.db')
    cursor_ja_doados = conn_ja_doados.cursor()
    cursor_ja_doados.execute('''
    CREATE TABLE IF NOT EXISTS itens_removidos (
        id INTEGER PRIMARY KEY,
        tipo TEXT NOT NULL,
        itens TEXT NOT NULL,
        doador TEXT NOT NULL
    )
    ''')
    conn_ja_doados.commit()

    conn_necessidades = sqlite3.connect('necessidades.db')
    cursor_necessidades = conn_necessidades.cursor()
    cursor_necessidades.execute('''
    CREATE TABLE IF NOT EXISTS necessidades (
        id INTEGER PRIMARY KEY,
        descricao TEXT NOT NULL
    )
    ''')
    conn_necessidades.commit()
    
    return conn_doacoes, cursor_doacoes, conn_ja_doados, cursor_ja_doados, conn_necessidades, cursor_necessidades

class GerenciadorDoacoesApp(App):
    def build(self):
        self.conn_doacoes, self.cursor_doacoes, self.conn_ja_doados, self.cursor_ja_doados, self.conn_necessidades, self.cursor_necessidades = criar_bancos_de_dados()
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Campos de entrada
        self.entry_tipo = TextInput(hint_text='Tipo de Doação', multiline=False)
        layout.add_widget(self.entry_tipo)

        self.entry_itens = TextInput(hint_text='Quantidade de itens', multiline=False)
        layout.add_widget(self.entry_itens)

        self.entry_doador = TextInput(hint_text='Doador', multiline=False)
        layout.add_widget(self.entry_doador)

        # Botão para adicionar doação
        btn_adicionar = Button(text='Adicionar Doação')
        btn_adicionar.bind(on_press=self.adicionar_doacao)
        layout.add_widget(btn_adicionar)

        # ListView para mostrar doações
        self.list_view = ListView(item_strings=[], size_hint=(1, 0.5))
        layout.add_widget(self.list_view)

        # Botões adicionais
        btn_visualizar = Button(text='Visualizar Itens Já Doados')
        btn_visualizar.bind(on_press=self.visualizar_itens_ja_doados)
        layout.add_widget(btn_visualizar)

        btn_visualizar_necessidades = Button(text='Visualizar Necessidades')
        btn_visualizar_necessidades.bind(on_press=self.visualizar_necessidades)
        layout.add_widget(btn_visualizar_necessidades)

        return layout

    def adicionar_doacao(self, instance):
        tipo = self.entry_tipo.text
        itens = self.entry_itens.text
        doador = self.entry_doador.text

        if tipo and itens and doador:
            self.cursor_doacoes.execute('INSERT INTO doacoes (tipo, itens, doador) VALUES (?, ?, ?)', (tipo, itens, doador))
            self.conn_doacoes.commit()
            self.entry_tipo.text = ''
            self.entry_itens.text = ''
            self.entry_doador.text = ''
            self.atualizar_list_view()
            self.mostrar_popup('Sucesso', 'Doação adicionada com sucesso!')
        else:
            self.mostrar_popup('Atenção', 'Por favor, preencha todos os campos.')

    def atualizar_list_view(self):
        self.list_view.item_strings = []
        self.cursor_doacoes.execute('SELECT * FROM doacoes')
        for row in self.cursor_doacoes.fetchall():
            self.list_view.item_strings.append(f"ID: {row[0]}, Tipo: {row[1]}, Itens: {row[2]}, Doador: {row[3]}")

    def visualizar_itens_ja_doados(self, instance):
        # Implementação da visualização de itens já doados
        self.cursor_ja_doados.execute('SELECT * FROM itens_removidos')
        items = self.cursor_ja_doados.fetchall()
        if items:
            content = "\n".join([f"ID: {item[0]}, Tipo: {item[1]}, Itens: {item[2]}, Doador: {item[3]}" for item in items])
        else:
            content = "Nenhum item já doado."

        self.mostrar_popup('Itens Já Doados', content)

    def visualizar_necessidades(self, instance):
        # Implementação da visualização de necessidades
        self.cursor_necessidades.execute('SELECT * FROM necessidades')
        items = self.cursor_necessidades.fetchall()
        if items:
            content = "\n".join([f"ID: {item[0]}, Descrição: {item[1]}" for item in items])
        else:
            content = "Nenhuma necessidade registrada."

        self.mostrar_popup('Necessidades', content)

    def mostrar_popup(self, titulo, conteudo):
        popup = Popup(title=titulo, content=Label(text=conteudo), size_hint=(0.8, 0.5))
        popup.open()

    def on_stop(self):
        self.conn_doacoes.close()
        self.conn_ja_doados.close()
        self.conn_necessidades.close()

if __name__ == '__main__':
    GerenciadorDoacoesApp().run()
