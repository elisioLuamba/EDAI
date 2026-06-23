import sys
import datetime
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QComboBox, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QTextEdit, QTabWidget, QMessageBox)
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont

# ==========================================
# 1. ESTRUTURAS DE DADOS MANUAIS (PRESERVADAS)
# ==========================================

class NoPilha:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None

class Pilha:
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
# 2. ENTIDADES DO SISTEMA
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
        self.categoria = categoria  # "cliente" ou "tecnico"
        self.historico_chamados = Pilha()

    def registrar_evento(self, mensagem):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.historico_chamados.empilhar(f"[{timestamp}] {mensagem}")


class SistemaSuporte:
    def __init__(self):
        self.usuarios = ListaDuplamenteEncadeada()
        self.fila_atendimento = ListaDuplamenteEncadeada()
        self.total_criados = 0
        self.total_resolvidos = 0


# ==========================================
# 3. INTERFACE GRÁFICA (RESPONSIVA & PREMIUM WHITE)
# ==========================================

ESTILO_WHITE_PREMIUM = """
    QMainWindow {
        background-color: #F8FAFC;
    }
    
    QLabel {
        font-family: 'Segoe UI', -apple-system, sans-serif;
        color: #1E293B;
        font-weight: 600;
    }
    
    QLineEdit, QComboBox, QTextEdit {
        background-color: #FFFFFF;
        border: 2px solid #CBD5E1;
        border-radius: 8px;
        color: #0F172A;
        padding: 10px;
        font-size: 14px;
        font-weight: 600;
    }
    QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
        border: 2px solid #2563EB;
        background-color: #FFFFFF;
    }
    
    QPushButton {
        font-family: 'Segoe UI', sans-serif;
        font-size: 13px;
        font-weight: 700;
        color: #FFFFFF;
        border-radius: 8px;
        padding: 12px 18px;
        border: none;
    }
    
    QPushButton#btnAzul { background-color: #2563EB; }
    QPushButton#btnAzul:hover { background-color: #1D4ED8; }
    
    QPushButton#btnVerde { background-color: #10B981; }
    QPushButton#btnVerde:hover { background-color: #059669; }
    
    QPushButton#btnRoxo { background-color: #8B5CF6; }
    QPushButton#btnRoxo:hover { background-color: #7C3AED; }
    
    QPushButton#btnCinza { background-color: #475569; }
    QPushButton#btnCinza:hover { background-color: #334155; }

    QTabWidget::pane {
        border: 2px solid #CBD5E1;
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 15px;
    }
    QTabBar::tab {
        background-color: #E2E8F0;
        color: #475569;
        padding: 12px 24px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        margin-right: 6px;
        font-weight: bold;
    }
    QTabBar::tab:selected {
        background-color: #FFFFFF;
        color: #2563EB;
        border-bottom: 3px solid #2563EB;
    }
    
    QTableWidget {
        background-color: #FFFFFF;
        border: 2px solid #CBD5E1;
        gridline-color: #E2E8F0;
        color: #1E293B;
        border-radius: 8px;
    }
    QHeaderView::section {
        background-color: #F1F5F9;
        color: #0F172A;
        padding: 10px;
        border: 1px solid #CBD5E1;
        font-weight: bold;
        font-size: 13px;
    }
"""

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sistema = SistemaSuporte()
        self.init_massa_dados()
        self.init_ui()

    def init_massa_dados(self):
        # Base de dados operacional inicial
        self.sistema.usuarios.inserir_no_fim(Usuario("Janete_Silva", "cliente"))
        self.sistema.usuarios.inserir_no_fim(Usuario("Mateus_Manuel", "cliente"))
        self.sistema.usuarios.inserir_no_fim(Usuario("Carlos_Sambu", "cliente"))
        self.sistema.usuarios.inserir_no_fim(Usuario("Rui_Tecnico", "tecnico"))
        self.sistema.usuarios.inserir_no_fim(Usuario("Analtina_Suporte", "tecnico"))

    def init_ui(self):
        self.setWindowTitle("Nexus Support PRO — Gestão Corporativa de Chamados")
        self.setMinimumSize(QSize(1050, 700))
        self.setStyleSheet(ESTILO_WHITE_PREMIUM)

        self.abas = QTabWidget()
        self.setCentralWidget(self.abas)

        self.aba_painel = QWidget()
        self.aba_usuarios = QWidget()
        self.aba_historico = QWidget()

        self.abas.addTab(self.aba_painel, "⚡ Painel Atendimento")
        self.abas.addTab(self.aba_usuarios, "👥 Gestão Usuários")
        self.abas.addTab(self.aba_historico, "📜 Histórico Individual")

        self.montar_aba_painel()
        self.montar_aba_usuarios()
        self.montar_aba_historico()
        
        self.atualizar_tabela_fila()
        self.atualizar_estatisticas()

    def montar_aba_painel(self):
        layout_global = QHBoxLayout(self.aba_painel)
        layout_global.setContentsMargins(10, 10, 10, 10)
        layout_global.setSpacing(20)

        # ---- LADO ESQUERDO: Painel de Controlo Fixo Contido ----
        container_esquerdo = QWidget()
        container_esquerdo.setMinimumWidth(360)
        container_esquerdo.setMaximumWidth(420)
        lado_esquerdo = QVBoxLayout(container_esquerdo)
        lado_esquerdo.setContentsMargins(0, 0, 0, 0)
        lado_esquerdo.setSpacing(15)
        
        # Secção de Clientes
        lbl_card_chamado = QLabel("🎯 ABERTURA DE INCIDENTES")
        lbl_card_chamado.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        lbl_card_chamado.setStyleSheet("color: #2563EB;")
        
        layout_ocr_cliente = QHBoxLayout()
        self.txt_cliente_chamado = QLineEdit()
        self.txt_cliente_chamado.setPlaceholderText("Username do Cliente")
        btn_face_cliente = QPushButton("📷 FaceID")
        btn_face_cliente.setObjectName("btnCinza")
        btn_face_cliente.clicked.connect(lambda: self.simular_reconhecimento_facial("cliente"))
        layout_ocr_cliente.addWidget(self.txt_cliente_chamado, 7)
        layout_ocr_cliente.addWidget(btn_face_cliente, 3)

        self.txt_desc_chamado = QTextEdit()
        self.txt_desc_chamado.setPlaceholderText("Descreva detalhadamente o problema técnico aqui...")
        self.txt_desc_chamado.setMinimumHeight(120)
        
        btn_enviar_chamado = QPushButton("🚀 Enviar para Fila de Suporte")
        btn_enviar_chamado.setObjectName("btnVerde")
        btn_enviar_chamado.setMinimumHeight(42)
        btn_enviar_chamado.clicked.connect(self.ui_abrir_chamado)

        # Secção de Técnicos
        lbl_card_tecnico = QLabel("🛠️ RESOLUÇÃO E TRIAGEM (FIFO)")
        lbl_card_tecnico.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        lbl_card_tecnico.setStyleSheet("color: #8B5CF6;")
        
        layout_ocr_tecnico = QHBoxLayout()
        self.txt_tecnico_atende = QLineEdit()
        self.txt_tecnico_atende.setPlaceholderText("Username do Técnico")
        btn_face_tecnico = QPushButton("📷 FaceID")
        btn_face_tecnico.setObjectName("btnCinza")
        btn_face_tecnico.clicked.connect(lambda: self.simular_reconhecimento_facial("tecnico"))
        layout_ocr_tecnico.addWidget(self.txt_tecnico_atende, 7)
        layout_ocr_tecnico.addWidget(btn_face_tecnico, 3)
        
        btn_atender = QPushButton("✅ Resolver Próximo Chamado")
        btn_atender.setObjectName("btnRoxo")
        btn_atender.setMinimumHeight(42)
        btn_atender.clicked.connect(self.ui_atender_chamado)

        # Dashboard de Métricas Integrado
        self.lbl_stats = QLabel()
        self.lbl_stats.setStyleSheet("background-color: #F1F5F9; border: 2px solid #CBD5E1; padding: 15px; border-radius: 8px; font-weight: bold; color: #1E293B;")
        self.lbl_stats.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lado_esquerdo.addWidget(lbl_card_chamado)
        lado_esquerdo.addLayout(layout_ocr_cliente)
        lado_esquerdo.addWidget(self.txt_desc_chamado)
        lado_esquerdo.addWidget(btn_enviar_chamado)
        lado_esquerdo.addSpacing(10)
        lado_esquerdo.addWidget(lbl_card_tecnico)
        lado_esquerdo.addLayout(layout_ocr_tecnico)
        lado_esquerdo.addWidget(btn_atender)
        lado_esquerdo.addStretch()
        lado_esquerdo.addWidget(self.lbl_stats)

        # ---- LADO DIREITO: Monitorização Elástica ----
        container_direito = QWidget()
        lado_direito = QVBoxLayout(container_direito)
        lado_direito.setContentsMargins(0, 0, 0, 0)
        
        lbl_titulo_fila = QLabel("📥 FILA DE ATENDIMENTO CRONOLÓGICA ATIVA")
        lbl_titulo_fila.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        
        self.tabela_fila = QTableWidget(0, 3)
        self.tabela_fila.setHorizontalHeaderLabels(["ID Ticket", "Utilizador / Cliente", "Descrição Ocorrência"])
        
        # Ajuste Automático Responsivo de Colunas
        header = self.tabela_fila.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.tabela_fila.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        lado_direito.addWidget(lbl_titulo_fila)
        lado_direito.addWidget(self.tabela_fila)

        # Acoplamento dos containers principais
        layout_global.addWidget(container_esquerdo, 4)
        layout_global.addWidget(container_direito, 6)

    def montar_aba_usuarios(self):
        layout_global = QHBoxLayout(self.aba_usuarios)
        layout_global.setContentsMargins(10, 10, 10, 10)
        layout_global.setSpacing(25)

        form_panel = QWidget()
        form_panel.setMinimumWidth(320)
        form_panel.setMaximumWidth(400)
        form_layout = QVBoxLayout(form_panel)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(15)

        lbl_cad = QLabel("👤 REGISTO DE UTILIZADORES")
        lbl_cad.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        lbl_cad.setStyleSheet("color: #2563EB;")

        self.txt_novo_username = QLineEdit()
        self.txt_novo_username.setPlaceholderText("Username único corporativo")

        self.cb_categoria = QComboBox()
        self.cb_categoria.addItems(["Cliente", "Técnico"])

        btn_cadastrar = QPushButton("➕ Inserir na Infraestrutura")
        btn_cadastrar.setObjectName("btnAzul")
        btn_cadastrar.setMinimumHeight(40)
        btn_cadastrar.clicked.connect(self.ui_cadastrar_usuario)
        
        form_layout.addWidget(lbl_cad)
        form_layout.addWidget(self.txt_novo_username)
        form_layout.addWidget(self.cb_categoria)
        form_layout.addWidget(btn_cadastrar)
        form_layout.addStretch()

        tabelas_container = QWidget()
        tabelas_layout = QVBoxLayout(tabelas_container)
        tabelas_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_lista_c = QLabel("👥 Clientes Habilitados")
        lbl_lista_c.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.table_clientes = QTableWidget(0, 1)
        self.table_clientes.setHorizontalHeaderLabels(["Nome de Conta"])
        self.table_clientes.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

        lbl_lista_t = QLabel("🛠️ Especialistas Técnicos")
        lbl_lista_t.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.table_tecnicos = QTableWidget(0, 1)
        self.table_tecnicos.setHorizontalHeaderLabels(["Nome de Conta"])
        self.table_tecnicos.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

        tabelas_layout.addWidget(lbl_lista_c, 1)
        tabelas_layout.addWidget(self.table_clientes, 4)
        tabelas_layout.addSpacing(10)
        tabelas_layout.addWidget(lbl_lista_t, 1)
        tabelas_layout.addWidget(self.table_tecnicos, 4)

        layout_global.addWidget(form_panel, 4)
        layout_global.addWidget(tabelas_container, 6)
        
        self.atualizar_tabelas_usuarios()

    def montar_aba_historico(self):
        layout = QVBoxLayout(self.aba_historico)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        topo = QHBoxLayout()
        self.txt_busca_historico = QLineEdit()
        self.txt_busca_historico.setPlaceholderText("Identifique a conta por digitação ou biometria lateral...")
        
        btn_face_hist = QPushButton("📷 Escanear Rosto")
        btn_face_hist.setObjectName("btnCinza")
        btn_face_hist.clicked.connect(lambda: self.simular_reconhecimento_facial("todos"))
        
        btn_buscar = QPushButton("🔍 Consultar Histórico (LIFO)")
        btn_buscar.setObjectName("btnAzul")
        btn_buscar.clicked.connect(self.ui_exibir_historico)
        
        topo.addWidget(self.txt_busca_historico, 6)
        topo.addWidget(btn_face_hist, 2)
        topo.addWidget(btn_buscar, 2)

        self.txt_area_historico = QTextEdit()
        self.txt_area_historico.setReadOnly(True)
        self.txt_area_historico.setFont(QFont("Courier New", 11))
        self.txt_area_historico.setStyleSheet("background-color: #0F172A; color: #38BDF8; padding: 15px; border-radius: 8px;")

        layout.addLayout(topo)
        layout.addWidget(self.txt_area_historico)

    # ==========================================================
    # LÓGICA DO BACKEND INTEGRADA E AUTOMATISMOS
    # ==========================================================

    def simular_reconhecimento_facial(self, categoria_filtro):
        """ Inicialização automatizada de varredura biométrica com dados da estrutura """
        lista_disponiveis = []
        for user in self.sistema.usuarios.iterar():
            if categoria_filtro == "todos" or user.categoria == categoria_filtro:
                lista_disponiveis.append(user.username)
        
        if not lista_disponiveis:
            QMessageBox.warning(self, "Módulo Biométrico", "Nenhum registo correspondente localizado na base local.")
            return

        escolhido = random.choice(lista_disponiveis)
        
        if categoria_filtro == "cliente":
            self.txt_cliente_chamado.setText(escolhido)
        elif categoria_filtro == "tecnico":
            self.txt_tecnico_atende.setText(escolhido)
        else:
            self.txt_busca_historico.setText(escolhido)
            self.ui_exibir_historico()

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
            self.tabela_fila.setItem(row, 0, QTableWidgetItem(f"TK-{chamado.id:04d}"))
            self.tabela_fila.setItem(row, 1, QTableWidgetItem(chamado.cliente))
            self.tabela_fila.setItem(row, 2, QTableWidgetItem(chamado.descricao))

    def atualizar_estatisticas(self):
        fila_atual = self.sistema.fila_atendimento.tamanho
        txt = f"Abertos Globais: {self.sistema.total_criados}   |   Concluídos: {self.sistema.total_resolvidos}   |   Retidos na Fila: {fila_atual}"
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

    def ui_cadastrar_usuario(self):
        nome = self.txt_novo_username.text().strip()
        cat = self.cb_categoria.currentText().lower()
        if not nome: return

        if self.buscar_usuario_interno(nome):
            QMessageBox.warning(self, "Cadastro Invalido", "Utilizador já se encontra indexado ao sistema.")
            return

        novo_user = Usuario(nome, cat)
        self.sistema.usuarios.inserir_no_fim(novo_user)
        self.txt_novo_username.clear()
        self.atualizar_tabelas_usuarios()

    def ui_abrir_chamado(self):
        nome_c = self.txt_cliente_chamado.text().strip()
        desc = self.txt_desc_chamado.toPlainText().strip()
        if not nome_c or not desc:
            QMessageBox.warning(self, "Aviso", "Preencha a conta de cliente e a descrição do incidente.")
            return

        cliente = self.buscar_usuario_interno(nome_c)
        if not cliente or cliente.categoria != "cliente":
            QMessageBox.warning(self, "Falha de Autenticação", "Utilizador cliente inválido ou não cadastrado.")
            return

        self.sistema.total_criados += 1
        novo_c = Chamado(self.sistema.total_criados, nome_c, desc)
        self.sistema.fila_atendimento.inserir_no_fim(novo_c)
        
        cliente.registrar_evento(f"Abertura de ticket TK-{novo_c.id:04d}: '{desc}'")
        
        self.txt_cliente_chamado.clear()
        self.txt_desc_chamado.clear()
        self.atualizar_tabela_fila()
        self.atualizar_estatisticas()

    def ui_atender_chamado(self):
        nome_t = self.txt_tecnico_atende.text().strip()
        if not nome_t:
            QMessageBox.warning(self, "Erro Operacional", "Identifique o técnico responsável pelo atendimento.")
            return

        tecnico = self.buscar_usuario_interno(nome_t)
        if not tecnico or tecnico.categoria != "tecnico":
            QMessageBox.warning(self, "Falha de Credenciais", "O operador introduzido não pertence à equipa técnica.")
            return

        if self.sistema.fila_atendimento.esta_vazia():
            QMessageBox.information(self, "Fila Vazia", "Não existem chamados retidos na fila de espera neste momento.")
            return

        chamado = self.sistema.fila_atendimento.remover_do_inicio()
        chamado.status = "Resolvido"
        self.sistema.total_resolvidos += 1

        cliente = self.buscar_usuario_interno(chamado.cliente)
        if cliente:
            cliente.registrar_evento(f"Ticket TK-{chamado.id:04d} RESOLVIDO na triagem por {nome_t}.")
        tecnico.registrar_evento(f"Processou e concluiu o Ticket TK-{chamado.id:04d} associado a {chamado.cliente}.")

        self.txt_tecnico_atende.clear()
        self.atualizar_tabela_fila()
        self.atualizar_estatisticas()

    def ui_exibir_historico(self):
        nome = self.txt_busca_historico.text().strip()
        if not nome: return

        user = self.buscar_usuario_interno(nome)
        if not user:
            self.txt_area_historico.setText("❌ Registo de utilizador inexistente na base ativa.")
            return

        texto = f"=== HISTÓRICO DE AUDITORIA LIFO: {user.username.upper()} [{user.categoria.upper()}] ===\n\n"
        if user.historico_chamados.esta_vazia():
            texto += "Sem logs operacionais indexados à pilha deste utilizador."
        else:
            for evento in user.historico_chamados.iterar():
                texto += f"{evento}\n"
        
        self.txt_area_historico.setText(texto)


# ==========================================
# INICIALIZAÇÃO DA APLICAÇÃO
# ==========================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec())