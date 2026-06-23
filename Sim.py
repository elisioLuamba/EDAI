import sys
import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QTextEdit, QListWidget, 
    QMessageBox, QGroupBox, QInputDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# ==================== ESTRUTURAS DE DADOS (MANUAIS) ====================

class Veiculo:
    def __init__(self, placa):
        self.placa = placa
        self.data_hora_entrada = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        self.tempo_permanencia = 0
        self.tarifa_paga = 0.0

class PilhaEstacionamento:
    def __init__(self, capacidade=5):
        self.capacidade = capacidade
        self.carros = [None] * capacidade
        self.topo = -1

    def esta_cheia(self):
        return self.topo == self.capacidade - 1

    def esta_vazia(self):
        return self.topo == -1

    def push(self, veiculo):
        if not self.esta_cheia():
            self.topo += 1
            self.carros[self.topo] = veiculo
            return True
        return False

    def pop(self):
        if not self.esta_vazia():
            veiculo = self.carros[self.topo]
            self.carros[self.topo] = None
            self.topo -= 1
            return veiculo
        return None

class NodoFila:
    def __init__(self, veiculo):
        self.veiculo = veiculo
        self.proximo = None

class FilaEspera:
    def __init__(self):
        self.frente = None
        self.tras = None

    def esta_vazia(self):
        return self.frente is None

    def enfileirar(self, veiculo):
        novo = NodoFila(veiculo)
        if self.esta_vazia():
            self.frente = novo
            self.tras = novo
        else:
            self.tras.proximo = novo
            self.tras = novo

    def desenfileirar(self):
        if self.esta_vazia():
            return None
        temp = self.frente
        veiculo = temp.veiculo
        self.frente = self.frente.proximo
        if self.frente is None:
            self.tras = None
        return veiculo

class ListaSequencial:
    def __init__(self, max_registos=100):
        self.max_registos = max_registos
        self.registos = [None] * max_registos
        self.tamanho = 0

    def inserir(self, veiculo):
        if self.tamanho < self.max_registos:
            self.registos[self.tamanho] = veiculo
            self.tamanho += 1

# ==================== LÓGICA RECURSIVA ====================

def calcular_tarifa_progressiva(horas):
    if horas <= 1:
        return 5.00  # Caso base
    return 5.00 + (1.2 * calcular_tarifa_progressiva(horas - 1))  # Caso recursivo


# ==================== ESTILO MODERN WHITE (QSS) ====================

ESTILO_MODERNO = """
    QMainWindow {
        background-color: #FAFAFA;
    }
    
    QLabel {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
        color: #2C3E50;
        font-weight: 600;
    }
    
    QLineEdit {
        background-color: #FFFFFF;
        border: 2px solid #E0E0E0;
        border-radius: 6px;
        padding: 8px;
        font-size: 14px;
        color: #333333;
    }
    QLineEdit:focus {
        border: 2px solid #3498DB;
    }
    
    QGroupBox {
        background-color: #FFFFFF;
        border: 1px solid #E6E8EA;
        border-radius: 8px;
        margin-top: 15px;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 14px;
        font-weight: bold;
        color: #34495E;
        padding: 15px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 5px;
        left: 10px;
    }
    
    QPushButton {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
        font-weight: bold;
        color: white;
        border-radius: 6px;
        padding: 10px;
        min-height: 18px;
    }
    
    QPushButton#btnVerde {
        background-color: #2ECC71;
    }
    QPushButton#btnVerde:hover {
        background-color: #27AE60;
    }
    
    QPushButton#btnVermelho {
        background-color: #E74C3C;
    }
    QPushButton#btnVermelho:hover {
        background-color: #C0392B;
    }
    
    QPushButton#btnRoxo {
        background-color: #9B59B6;
    }
    QPushButton#btnRoxo:hover {
        background-color: #8E44AD;
    }
    
    QListWidget {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 6px;
        padding: 5px;
        font-size: 13px;
        color: #555555;
    }
    QListWidget::item {
        padding: 8px;
        border-bottom: 1px solid #F1F1F1;
    }
    QListWidget::item:hover {
        background-color: #E8F4F8;
        color: #2980B9;
        border-radius: 4px;
    }
    
    QTextEdit {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 6px;
        color: #333333;
        padding: 10px;
    }
"""

# ==================== INTERFACE GRÁFICA (PyQt6) ====================

class JanelaEstacionamento(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.estacionamento = PilhaEstacionamento(capacidade=5)
        self.fila_espera = FilaEspera()
        self.historico = ListaSequencial(max_registos=100)
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("SmartPark — Gestão de Estacionamento Inteligente")
        self.setGeometry(100, 100, 950, 600)
        
        # Aplicar o tema visual moderno
        self.setStyleSheet(ESTILO_MODERNO)
        
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QHBoxLayout(widget_central)
        layout_principal.setSpacing(15)
        layout_principal.setContentsMargins(15, 15, 15, 15)
        
        # ---------------- ESQUERDA: Painel de Controlos ----------------
        layout_esquerda = QVBoxLayout()
        layout_esquerda.setSpacing(15)
        
        # Título do Sistema
        lbl_titulo = QLabel("SmartPark PRO")
        lbl_titulo.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        lbl_titulo.setStyleSheet("color: #2C3E50; margin-bottom: 5px;")
        layout_esquerda.addWidget(lbl_titulo)
        
        grupo_entrada = QGroupBox("Entrada de Veículo")
        layout_input = QVBoxLayout()
        layout_input.setSpacing(8)
        self.lbl_placa = QLabel("Matrícula / Placa:")
        self.txt_placa = QLineEdit()
        self.txt_placa.setPlaceholderText("Ex: LD-00-00-AA")
        
        self.btn_entrada = QPushButton("Registar Entrada")
        self.btn_entrada.setObjectName("btnVerde")
        self.btn_entrada.clicked.connect(self.processar_entrada)
        
        layout_input.addWidget(self.lbl_placa)
        layout_input.addWidget(self.txt_placa)
        layout_input.addWidget(self.btn_entrada)
        grupo_entrada.setLayout(layout_input)
        
        grupo_acoes = QGroupBox("Operações")
        layout_acoes = QVBoxLayout()
        layout_acoes.setSpacing(10)
        
        self.btn_saida = QPushButton("Libertar Vaga (Saída LIFO)")
        self.btn_saida.setObjectName("btnVermelho")
        self.btn_saida.clicked.connect(self.processar_saida)
        
        self.btn_relatorio = QPushButton("Gerar Relatório Financeiro")
        self.btn_relatorio.setObjectName("btnRoxo")
        self.btn_relatorio.clicked.connect(self.exibir_relatorio)
        
        layout_acoes.addWidget(self.btn_saida)
        layout_acoes.addWidget(self.btn_relatorio)
        grupo_acoes.setLayout(layout_acoes)
        
        layout_esquerda.addWidget(grupo_entrada)
        layout_esquerda.addWidget(grupo_acoes)
        layout_esquerda.addStretch()
        
        # ---------------- CENTRO: Estado das Estruturas ----------------
        layout_centro = QVBoxLayout()
        layout_centro.setSpacing(15)
        
        grupo_pilha = QGroupBox("Estacionamento Físico (Pilha)")
        layout_pilha = QVBoxLayout()
        self.lista_pilha = QListWidget()
        layout_pilha.addWidget(self.lista_pilha)
        grupo_pilha.setLayout(layout_pilha)
        
        grupo_fila = QGroupBox("Fila de Espera Externa (Fila)")
        layout_fila = QVBoxLayout()
        self.lista_fila = QListWidget()
        layout_fila.addWidget(self.lista_fila)
        grupo_fila.setLayout(layout_fila)
        
        layout_centro.addWidget(grupo_pilha)
        layout_centro.addWidget(grupo_fila)
        
        # ---------------- DIREITA: Monitor e Logs ----------------
        layout_direita = QVBoxLayout()
        grupo_logs = QGroupBox("Consola de Monitorização e Relatórios")
        layout_log_box = QVBoxLayout()
        self.txt_logs = QTextEdit()
        self.txt_logs.setReadOnly(True)
        # CORREÇÃO DA LINHA: Passado para o inteiro 11 para evitar o TypeError
        self.txt_logs.setFont(QFont("Courier New", 11))
        layout_log_box.addWidget(self.txt_logs)
        grupo_logs.setLayout(layout_log_box)
        layout_direita.addWidget(grupo_logs)
        
        # Adicionar painéis ao layout principal
        layout_principal.addLayout(layout_esquerda, 2)
        layout_principal.addLayout(layout_centro, 3)
        layout_principal.addLayout(layout_direita, 4)
        
        self.atualizar_ecran()
        self.log_mensagem("Sistema online. Aguardando veículos.")

    # ---------------- MÉTODOS DE AÇÃO ----------------

    def processar_entrada(self):
        placa = self.txt_placa.text().strip().upper()
        if not placa:
            QMessageBox.warning(self, "Aviso", "Por favor, introduza uma matrícula válida.")
            return
        
        novo_carro = Veiculo(placa)
        self.txt_placa.clear()
        
        if not self.estacionamento.esta_cheia():
            self.estacionamento.push(novo_carro)
            self.log_mensagem(f"🟢 ENTRADA: Carro [{placa}] entrou diretamente numa vaga.")
        else:
            self.fila_espera.enfileirar(novo_carro)
            self.log_mensagem(f"🟡 FILA: Estacionamento cheio! [{placa}] movido para a fila de espera.")
            
        self.atualizar_ecran()

    def processar_saida(self):
        if self.estacionamento.esta_vazia():
            QMessageBox.information(self, "Informação", "Nenhum veículo estacionado para efetuar a saída.")
            return
        
        horas, ok = QInputDialog.getInt(self, "Cálculo de Tarifa", "Quantas horas o veículo permaneceu no local?", value=1, min=1, max=168)
        
        if ok:
            carro_saindo = self.estacionamento.pop()
            carro_saindo.tempo_permanencia = horas
            
            # Executa a função recursiva de cálculo de tarifa
            carro_saindo.tarifa_paga = calcular_tarifa_progressiva(horas)
            
            # Regista na Lista Sequencial
            self.historico.inserir(carro_saindo)
            
            self.log_mensagem(f"🔴 SAÍDA: Carro [{carro_saindo.placa}] saiu do topo.\n  - Tempo total: {horas}h\n  - Faturação (Recursiva): Ezk {carro_saindo.tarifa_paga:.2f}")
            
            # Puxa o próximo da fila se houver vagas livres
            if not self.fila_espera.esta_vazia():
                proximo_carro = self.fila_espera.desenfileirar()
                proximo_carro.data_hora_entrada = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                self.estacionamento.push(proximo_carro)
                self.log_mensagem(f"🔵 VAGA PREENCHIDA: Carro [{proximo_carro.placa}] avançou da fila de espera para a vaga aberta.")
                
            self.atualizar_ecran()

    def exibir_relatorio(self):
        self.txt_logs.clear()
        self.txt_logs.append("==================================================\n")
        self.txt_logs.append("        RELATÓRIO DE FATURAÇÃO E AUDITORIA        \n")
        self.txt_logs.append("==================================================\n")
        self.txt_logs.append(f"{'Matrícula':<15}{'Data/Hora':<18}{'Tempo':<8}{'Tarifa'}\n")
        self.txt_logs.append("-" * 50 + "\n")
        
        total_faturado = 0.0
        for i in range(self.historico.tamanho):
            v = self.historico.registos[i]
            self.txt_logs.append(f"{v.placa:<15}{v.data_hora_entrada:<18}{str(v.tempo_permanencia)+'h':<8}Ezk {v.tarifa_paga:.2f}\n")
            total_faturado += v.tarifa_paga
            
        self.txt_logs.append("-" * 50 + "\n")
        self.txt_logs.append(f"TOTAL ARRECADADO NO DIA: Ezk {total_faturado:.2f}\n")
        self.txt_logs.append("==================================================\n")

    # ---------------- ATUALIZAÇÃO DA INTERFACE ----------------

    def atualizar_ecran(self):
        # Atualizar a Pilha Visual (LIFO)
        self.lista_pilha.clear()
        if self.estacionamento.esta_vazia():
            self.lista_pilha.addItem("⚠️ [ Estacionamento Totalmente Livre ]")
        else:
            for i in range(self.estacionamento.topo, -1, -1):
                carro = self.estacionamento.carros[i]
                self.lista_pilha.addItem(f" Vaga {i+1} (Topo): {carro.placa}  ➔ Entrada: {carro.data_hora_entrada}")
                
        # Atualizar a Fila de Espera Visual (FIFO)
        self.lista_fila.clear()
        if self.fila_espera.esta_vazia():
            self.lista_fila.addItem("✅ [ Sem carros em espera ]")
        else:
            atual = self.fila_espera.frente
            pos = 1
            while atual is not None:
                self.lista_fila.addItem(f" Pos {pos}º ➔ {atual.veiculo.placa}")
                atual = atual.proximo
                pos += 1

    def log_mensagem(self, message):
        horario = datetime.datetime.now().strftime("%H:%M:%S")
        self.txt_logs.append(f"[{horario}] {message}\n")

# ==================== EXECUÇÃO DO PROGRAMA ====================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = JanelaEstacionamento()
    janela.show()
    sys.exit(app.exec())