import sys
import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QComboBox, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QTextEdit, QTabWidget, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor

# ==========================================
# 1. ESTRUTURAS DE DADOS (Manuais) [cite: 55]
# ==========================================

class NoPilha:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None

class Pilha:
    """Pilha (LIFO) para o histórico de interações[cite: 57]."""
    def __init__(self):
        self.topo = None
        self.tamanho = 0

    def empilhar(self, dado):
        novo_no = NoPilha(dado)
        novo_no.proximo = self.topo
        self.topo = novo_no
        self.tamanho += 1

    def desempilhar(self):
        if self.esta_vazia():
            return None
        removido = self.topo.dado
        self.topo = self.topo.proximo
        self.tamanho -= 1
        return removido

    def esta_vazia(self):
        return self.topo is None

    def iterar(self):
        atual = self.topo
        while atual:
            yield atual.dado
            atual = atual.proximo


class NoDuplo:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None
        self.anterior = None

class ListaDuplamenteEncadeada:
    """Lista Duplamente Encadeada para Usuários e Chamados[cite: 55]."""
    def __init__(self):
        self.cabeca = None
        self.cauda = None
        self.tamanho = 0

    def inserir_no_fim(self, dado):
        novo_no = NoDuplo(dado)
        if not self.cabeca:
            self.cabeca = novo_no
            self.cauda = novo_no
        else:
            self.cauda.proximo = novo_no
            novo_no.anterior = self.cauda
            self.cauda = novo_no
        self.tamanho += 1

    def remover_do_inicio(self):
        if not self.cabeca:
            return None
        removido = self.cabeca.dado
        if self.cabeca == self.cauda:
            self.cabeca = None
            self.cauda = None
        else:
            self.cabeca = self.cabeca.proximo
            self.cabeca.anterior = None
        self.tamanho -= 1
        return removido

    def esta_vazia(self):
        return self.tamanho == 0

    def iterar(self):
        atual = self.cabeca
        while atual:
            yield atual.dado
            atual = atual.proximo


# ==========================================
# 2. ENTIDADES DO SISTEMA [cite: 51, 52]
# ==========================================

class Chamado:
    def __init__(self, id_chamado, cliente, descricao):
        self.id = id_chamado
        self.cliente = cliente
        self.descricao = descricao
        self.status = "Pendente"
        self.data_criacao = datetime.datetime.now()

class Usuario:
    def __init__(self, username, categoria):
        self.username = username
        self.categoria = categoria  # "cliente" ou "tecnico" [cite: 57]
        self.historico_chamados = Pilha()  # [cite: 57]

    def registrar_evento(self, mensagem):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.historico_chamados.empilhar(f"[{timestamp}] {mensagem}")


# LÓGICA DO BACKEND INTEGRADA
class SistemaSuporte:
    def __init__(self):
        self.usuarios = ListaDuplamenteEncadeada()
        self.fila_atendimento = ListaDuplamenteEncadeada()
        self.total_criados = 0
        self.total_resolvidos = 0


# ==========================================
# 3. INTERFACE GRÁFICA (UI COM DESIGN MODERNO)
# ==========================================

# Estilos CSS modernos (QSS) para criar o tema escuro/neon
ESTILO_DARK = """
    QMainWindow {
        background-color: #121214;
    }
    QLabel {
        color: #E1E1E6;
        font-size: 14px;
    }
    QLineEdit, QComboBox, QTextEdit {
        background-color: #202024;
        border: 2px solid #29292E;
        border-radius: 6px;
        color: #FFFFFF;
        padding: 8px;
        font-size: 14px;
    }
    QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
        border: 2px solid #00ADB5;
    }
    QPushButton {
        background-color: #00ADB5;
        color: #FFFFFF;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 13px;
    }
    QPushButton:hover {
        background-color: #008F95;
    }
    QPushButton:pressed {
        background-color: #006C71;
    }
    QTabWidget::pane {
        border: 1px solid #29292E;
        background-color: #121214;
        border-radius: 8px;
    }
    QTabBar::tab {
        background-color: #1A1A1E;
        color: #A8A8B3;
        padding: 12px 24px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        margin-right: 4px;
    }
    QTabBar::tab:selected {
        background-color: #202024;
        color: #00ADB5;
        border-bottom: 3px solid #00ADB5;
        font-weight: bold;
    }
    QTableWidget {
        background-color: #1A1A1E;
        border: 1px solid #29292E;
        gridline-color: #29292E;
        color: #E1E1E6;
        border-radius: 6px;
    }
    QHeaderView::section {
        background-color: #202024;
        color: #00ADB5;
        padding: 8px;
        border: 1px solid #29292E;
        font-weight: bold;
    }
"""

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sistema = SistemaSuporte()
        self.init_massa_dados()
        self.init_ui()

    def init_massa_dados(self):
        # Usuários iniciais de teste
        self.sistema.usuarios.inserir_no_fim(Usuario("Janete", "cliente"))
        self.sistema.usuarios.inserir_no_fim(Usuario("Carlos", "cliente"))
        self.sistema.usuarios.inserir_no_fim(Usuario("Rui_Tecnico", "tecnico"))

    def init_ui(self):
        self.setWindowTitle("🔥 Nexus Support - Sistema de Gestão de Chamados")
        self.setMinimumSize(QSize(900, 650))
        self.setStyleSheet(ESTILO_DARK)

        # Widget Central e Tabs
        self.abas = QTabWidget()
        self.setCentralWidget(self.abas)

        # Inicializar as Abas da aplicação
        self.aba_painel = QWidget()
        self.aba_usuarios = QWidget()
        self.aba_historico = QWidget()

        self.abas.addTab(self.aba_painel, "⚡ Painel de Atendimento")
        self.abas.addTab(self.aba_usuarios, "👥 Gestão de Usuários")
        self.abas.addTab(self.aba_historico, "📜 Histórico Individual (Pilha)")

        self.montar_aba_painel()
        self.montar_aba_usuarios()
        self.montar_aba_historico()
        
        self.atualizar_tabela_fila()
        self.atualizar_estatisticas()

    # --- MONTAGEM DA INTERFACE ---

    def montar_aba_painel(self):
        layout = QHBoxLayout(self.aba_painel)

        # Lado Esquerdo: Ações (Abrir chamado / Atender)
        lado_esquerdo = QVBoxLayout()
        
        lbl_titulo_chamado = QLabel("🎯 NOVO CHAMADO")
        lbl_titulo_chamado.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        lbl_titulo_chamado.setStyleSheet("color: #00ADB5;")
        
        self.txt_cliente_chamado = QLineEdit()
        self.txt_cliente_chamado.setPlaceholderText("Username do Cliente")
        
        self.txt_desc_chamado = QTextEdit()
        self.txt_desc_chamado.setPlaceholderText("Descreva detalhadamente o problema técnico...")
        self.txt_desc_chamado.setMaximumHeight(120)
        
        btn_enviar_chamado = QPushButton("🚀 Enviar para a Fila")
        btn_enviar_chamado.clicked.connect(self.ui_abrir_chamado)

        # Seção do Técnico
        lbl_titulo_tecnico = QLabel("🛠️ ATENDIMENTO")
        lbl_titulo_tecnico.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        lbl_titulo_tecnico.setStyleSheet("color: #FF2E93;")
        
        self.txt_tecnico_atende = QLineEdit()
        self.txt_tecnico_atende.setPlaceholderText("Username do Técnico")
        
        btn_atender = QPushButton("✅ Atender Próximo Chamado (FIFO)")
        btn_atender.setStyleSheet("background-color: #FF2E93;")
        btn_atender.clicked.connect(self.ui_atender_chamado)

        # Seção de Estatísticas rápidas [cite: 58]
        self.lbl_stats = QLabel("Abertos: 0  |  Resolvidos: 0  |  Fila: 0")
        self.lbl_stats.setStyleSheet("background-color: #1A1A1E; padding: 15px; border-radius: 6px; font-weight: bold; text-align: center;")
        self.lbl_stats.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lado_esquerdo.addWidget(lbl_titulo_chamado)
        lado_esquerdo.addWidget(self.txt_cliente_chamado)
        lado_esquerdo.addWidget(self.txt_desc_chamado)
        lado_esquerdo.addWidget(btn_enviar_chamado)
        lado_esquerdo.addSpacing(20)
        lado_esquerdo.addWidget(lbl_titulo_tecnico)
        lado_esquerdo.addWidget(self.txt_tecnico_atende)
        lado_esquerdo.addWidget(btn_atender)
        lado_esquerdo.addStretch()
        lado_esquerdo.addWidget(self.lbl_stats)

        # Lado Direito: Visualização da Fila
        lado_direito = QVBoxLayout()
        lbl_titulo_fila = QLabel("📥 FILA DE ATENDIMENTO ATUAL")
        lbl_titulo_fila.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        
        self.tabela_fila = QTableWidget(0, 3)
        self.tabela_fila.setHorizontalHeaderLabels(["ID", "Cliente", "Descrição do Problema"])
        self.tabela_fila.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.tabela_fila.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        lado_direito.addWidget(lbl_titulo_fila)
        lado_direito.addWidget(self.tabela_fila)

        layout.addLayout(lado_esquerdo, 4)
        layout.addLayout(lado_direito, 6)

    def montar_aba_usuarios(self):
        layout = QHBoxLayout(self.aba_usuarios)

        # Form de Cadastro
        form_layout = QVBoxLayout()
        lbl_cad = QLabel("👤 CADASTRAR NOVO USUÁRIO")
        lbl_cad.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        lbl_cad.setStyleSheet("color: #00ADB5;")

        self.txt_novo_username = QLineEdit()
        self.txt_novo_username.setPlaceholderText("Username único")

        self.cb_categoria = QComboBox()
        self.cb_categoria.addItems(["Cliente", "Técnico"])

        btn_cadastrar = QPushButton("➕ Adicionar Usuário")
        btn_cadastrar.clicked.connect(self.ui_cadastrar_usuario)
        
        form_layout.addWidget(lbl_cad)
        form_layout.addWidget(self.txt_novo_username)
        form_layout.addWidget(self.cb_categoria)
        form_layout.addWidget(btn_cadastrar)
        form_layout.addStretch()

        # Tabelas de Visualização (Filtros por categoria) [cite: 57]
        tabelas_layout = QVBoxLayout()
        
        lbl_lista_c = QLabel("👥 Clientes Ativos")
        lbl_lista_c.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.table_clientes = QTableWidget(0, 1)
        self.table_clientes.setHorizontalHeaderLabels(["Nome do Cliente"])
        self.table_clientes.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

        lbl_lista_t = QLabel("🛠️ Corpo Técnico")
        lbl_lista_t.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.table_tecnicos = QTableWidget(0, 1)
        self.table_tecnicos.setHorizontalHeaderLabels(["Nome do Técnico"])
        self.table_tecnicos.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

        tabelas_layout.addWidget(lbl_lista_c)
        tabelas_layout.addWidget(self.table_clientes)
        tabelas_layout.addWidget(lbl_lista_t)
        tabelas_layout.addWidget(self.table_tecnicos)

        layout.addLayout(form_layout, 4)
        layout.addLayout(tabelas_layout, 6)
        
        self.atualizar_tabelas_usuarios()

    def montar_aba_historico(self):
        layout = QVBoxLayout(self.aba_historico)

        topo = QHBoxLayout()
        self.txt_busca_historico = QLineEdit()
        self.txt_busca_historico.setPlaceholderText("Introduza o username para ver a Pilha de Histórico...")
        
        btn_buscar = QPushButton("🔍 Consultar Histórico (LIFO)")
        btn_buscar.clicked.connect(self.ui_exibir_historico)
        
        topo.addWidget(self.txt_busca_historico)
        topo.addWidget(btn_buscar)

        self.txt_area_historico = QTextEdit()
        self.txt_area_historico.setReadOnly(True)
        self.txt_area_historico.setFont(QFont("Courier New", 11))
        self.txt_area_historico.setStyleSheet("background-color: #1A1A1E; color: #00FF66; border: 1px solid #29292E;")

        layout.addLayout(topo)
        layout.addWidget(self.txt_area_historico)

    # --- FUNÇÕES DE ATUALIZAÇÃO DA INTERFACE (MÉTODOS INTERNOS) ---

    def buscar_usuario_interno(self, username):
        for user in self.sistema.usuarios.iterar():
            if user.username.lower() == username.lower():
                return user
        return None

    def atualizar_tabela_fila(self):
        self.tabela_fila.setRowCount(0)
        for chamado in self.sistema.fila_atendimento.iterar():
            row = self.tabela_fila.rowCount()
            self.tabela_fila.insertRow(row)
            self.tabela_fila.setItem(row, 0, QTableWidgetItem(str(chamado.id)))
            self.tabela_fila.setItem(row, 1, QTableWidgetItem(chamado.cliente))
            self.tabela_fila.setItem(row, 2, QTableWidgetItem(chamado.descricao))

    def atualizar_estatisticas(self):
        fila_atual = self.sistema.fila_atendimento.tamanho
        txt = f"Abertos: {self.sistema.total_criados}  |  Resolvidos: {self.sistema.total_resolvidos}  |  Na Fila: {fila_atual}"
        self.lbl_stats.setText(txt)

    def atualizar_tabelas_usuarios(self):
        self.table_clientes.setRowCount(0)
        self.table_tecnicos.setRowCount(0)
        for u in self.sistema.usuarios.iterar():
            if u.categoria == "cliente":
                row = self.table_clientes.rowCount()
                self.table_clientes.insertRow(row)
                self.table_clientes.setItem(row, 0, QTableWidgetItem(u.username))
            else:
                row = self.table_tecnicos.rowCount()
                self.table_tecnicos.insertRow(row)
                self.table_tecnicos.setItem(row, 0, QTableWidgetItem(u.username))

    # --- TRATAMENTO DE EVENTOS DOS BOTÕES (SLOTS) ---

    def ui_cadastrar_usuario(self):
        nome = self.txt_novo_username.text().strip()
        cat = self.cb_categoria.currentText().lower()
        if not nome: return

        if self.buscar_usuario_interno(nome):
            self.txt_novo_username.setText("⚠️ Já existe!")
            return

        novo_user = Usuario(nome, cat)
        self.sistema.usuarios.inserir_no_fim(novo_user)
        self.txt_novo_username.clear()
        self.atualizar_tabelas_usuarios()

    def ui_abrir_chamado(self):
        nome_c = self.txt_cliente_chamado.text().strip()
        desc = self.txt_desc_chamado.toPlainText().strip()
        if not nome_c or not desc: return

        cliente = self.buscar_usuario_interno(nome_c)
        if not cliente or cliente.categoria != "cliente":
            self.txt_cliente_chamado.setText("⚠️ Cliente inválido")
            return

        self.sistema.total_criados += 1
        novo_c = Chamado(self.sistema.total_criados, nome_c, desc)
        self.sistema.fila_atendimento.inserir_no_fim(novo_c)
        
        cliente.registrar_evento(f"Criou o chamado ID {novo_c.id}: '{desc}'")
        
        self.txt_cliente_chamado.clear()
        self.txt_desc_chamado.clear()
        self.atualizar_tabela_fila()
        self.atualizar_estatisticas()

    def ui_atender_chamado(self):
        nome_t = self.txt_tecnico_atende.text().strip()
        if not nome_t: return

        tecnico = self.buscar_usuario_interno(nome_t)
        if not tecnico or tecnico.categoria != "tecnico":
            self.txt_tecnico_atende.setText("⚠️ Técnico inválido")
            return

        if self.sistema.fila_atendimento.esta_vazia():
            return

        chamado = self.sistema.fila_atendimento.remover_do_inicio()
        chamado.status = "Resolvido"
        self.sistema.total_resolvidos += 1

        cliente = self.buscar_usuario_interno(chamado.cliente)
        if cliente:
            cliente.registrar_evento(f"Chamado ID {chamado.id} RESOLVIDO por {nome_t}.")
        tecnico.registrar_evento(f"Resolveu o chamado ID {chamado.id} de {chamado.cliente}.")

        self.txt_tecnico_atende.clear()
        self.atualizar_tabela_fila()
        self.atualizar_estatisticas()

    def ui_exibir_historico(self):
        nome = self.txt_busca_historico.text().strip()
        if not nome: return

        user = self.buscar_usuario_interno(nome)
        if not user:
            self.txt_area_historico.setText("❌ Usuário não encontrado no sistema.")
            return

        texto = f"=== HISTÓRICO LIFO DE: {user.username.upper()} ({user.categoria.upper()}) ===\n\n"
        if user.historico_chamados.esta_vazia():
            texto += "Nenhuma atividade recente gravada na pilha."
        else:
            for evento in user.historico_chamados.iterar():
                texto += f"{evento}\n"
        
        self.txt_area_historico.setText(texto)


# ==========================================
# RUN APLICANÇÃO
# ==========================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec())