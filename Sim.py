import sys
import datetime
import random
import time
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QTextEdit, QListWidget, 
    QMessageBox, QGroupBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# ==================== ESTRUTURAS DE DADOS (MANUAIS) ====================

class Veiculo:
    def __init__(self, placa):
        self.placa = placa
        self.timestamp_entrada = datetime.datetime.now()
        self.data_hora_entrada = self.timestamp_entrada.strftime("%d/%m/%Y %H:%M:%S")
        self.tempo_permanencia = 0
        self.tarifa_paga = 0.0

class PilhaEstacionamento:
    def __init__(self, capacidade=5):
        self.capacidade = capacity = capacidade
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
    def __init__(self, max_registos=200):
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
        return 500.00  # Caso base: Primeira hora fixa a 500 Kz
    # Caso recursivo: 500 Kz + acréscimo progressivo de 20% em relação à hora anterior
    return 500.00 + (1.2 * calcular_tarifa_progressiva(horas - 1))

# ==================== ESTILO PREMIUN MODERN WHITE ("COM MAIS PESO") ====================

ESTILO_PREMIUM = """
    QMainWindow {
        background-color: #F8FAFC;
    }
    
    QLabel {
        font-family: 'Segoe UI', system-ui, sans-serif;
        color: #1E293B;
    }
    
    QGroupBox {
        background-color: #FFFFFF;
        border: 2px solid #CBD5E1;
        border-radius: 12px;
        margin-top: 18px;
        font-family: 'Segoe UI';
        font-size: 14px;
        font-weight: 700;
        color: #0F172A;
        padding: 15px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 8px;
        left: 15px;
        color: #0F172A;
    }
    
    QLineEdit {
        background-color: #F1F5F9;
        border: 2px solid #CBD5E1;
        border-radius: 8px;
        padding: 10px;
        font-size: 14px;
        font-weight: 600;
        color: #0F172A;
    }
    QLineEdit:focus {
        background-color: #FFFFFF;
        border: 2px solid #2563EB;
    }
    
    QPushButton {
        font-family: 'Segoe UI', sans-serif;
        font-size: 13px;
        font-weight: 700;
        color: #FFFFFF;
        border-radius: 8px;
        padding: 12px;
        border: none;
    }
    
    QPushButton#btnPrimario {
        background-color: #1E293B;
        border: 1px solid #0F172A;
    }
    QPushButton#btnPrimario:hover {
        background-color: #0F172A;
    }
    
    QPushButton#btnSucesso {
        background-color: #10B981;
    }
    QPushButton#btnSucesso:hover {
        background-color: #059669;
    }
    
    QPushButton#btnAlerta {
        background-color: #EF4444;
    }
    QPushButton#btnAlerta:hover {
        background-color: #DC2626;
    }
    
    QPushButton#btnInfo {
        background-color: #3B82F6;
    }
    QPushButton#btnInfo:hover {
        background-color: #2563EB;
    }
    
    QListWidget {
        background-color: #FFFFFF;
        border: 2px solid #CBD5E1;
        border-radius: 8px;
        padding: 5px;
        font-size: 13px;
        font-weight: 600;
        color: #334155;
    }
    QListWidget::item {
        background-color: #F8FAFC;
        margin: 5px 0px;
        padding: 12px;
        border-radius: 6px;
        border: 1px solid #E2E8F0;
    }
    
    QTextEdit {
        background-color: #0F172A;
        border: none;
        border-radius: 10px;
        color: #38BDF8;
        padding: 15px;
    }
"""

# ==================== INTERFACE GRÁFICA ====================

class JanelaEstacionamento(QMainWindow):
    def __init__(self):
        super().__init__()
        self.estacionamento = PilhaEstacionamento(capacidade=5)
        self.fila_espera = FilaEspera()
        self.historico = ListaSequencial(max_registos=200)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("SmartPark PRO — Gestão Integrada por Escaneamento OCR")
        self.setGeometry(100, 100, 1050, 680)
        self.setStyleSheet(ESTILO_PREMIUM)
        
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QHBoxLayout(widget_central)
        layout_principal.setSpacing(20)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        
        # ---------------- PAINEL ESQUERDO: Controlos e OCR ----------------
        layout_esquerda = QVBoxLayout()
        layout_esquerda.setSpacing(15)
        
        lbl_marca = QLabel("SmartPark PRO 🇦🇴")
        lbl_marca.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        lbl_marca.setStyleSheet("color: #0F172A; letter-spacing: -1px;")
        layout_esquerda.addWidget(lbl_marca)
        
        grupo_entrada = QGroupBox("Terminal de Entrada Inteligente")
        layout_input = QVBoxLayout()
        layout_input.setSpacing(10)
        
        self.txt_placa = QLineEdit()
        self.txt_placa.setPlaceholderText("Introduza ou Escaneie...")
        
        self.btn_ocr = QPushButton("📷 Escanear Matrícula (Câmara OCR)")
        self.btn_ocr.setObjectName("btnPrimario")
        self.btn_ocr.clicked.connect(self.simular_escaneamento_ocr)
        
        self.btn_entrada = QPushButton("Validar e Entrar no Parque")
        self.btn_entrada.setObjectName("btnSucesso")
        self.btn_entrada.clicked.connect(self.processar_entrada)
        
        layout_input.addWidget(QLabel("Matrícula do Veículo:"))
        layout_input.addWidget(self.txt_placa)
        layout_input.addWidget(self.btn_ocr)
        layout_input.addWidget(self.btn_entrada)
        grupo_entrada.setLayout(layout_input)
        
        grupo_operacoes = QGroupBox("Painel de Controlo Operacional")
        layout_operacoes = QVBoxLayout()
        layout_operacoes.setSpacing(10)
        
        self.btn_saida = QPushButton("🚪 Efetuar Saída e Cobrança (LIFO)")
        self.btn_saida.setObjectName("btnAlerta")
        self.btn_saida.clicked.connect(self.processar_saida)
        
        self.btn_relatorio = QPushButton("📊 Gerar Relatório de Auditoria")
        self.btn_relatorio.setObjectName("btnInfo")
        self.btn_relatorio.clicked.connect(self.exibir_relatorio)
        
        layout_operacoes.addWidget(self.btn_saida)
        layout_operacoes.addWidget(self.btn_relatorio)
        grupo_operacoes.setLayout(layout_operacoes)
        
        layout_esquerda.addWidget(grupo_entrada)
        layout_esquerda.addWidget(grupo_operacoes)
        layout_esquerda.addStretch()
        
        # ---------------- PAINEL CENTRAL: Estado Físico ----------------
        layout_centro = QVBoxLayout()
        layout_centro.setSpacing(15)
        
        grupo_pilha = QGroupBox("Vagas Internas (PILHA — Último a entrar sai primeiro)")
        layout_pilha = QVBoxLayout()
        self.lista_pilha = QListWidget()
        layout_pilha.addWidget(self.lista_pilha)
        grupo_pilha.setLayout(layout_pilha)
        
        grupo_fila = QGroupBox("Fila de Espera de Acesso (FILA — Ordem de Chegada)")
        layout_fila = QVBoxLayout()
        self.lista_fila = QListWidget()
        layout_fila.addWidget(self.lista_fila)
        grupo_fila.setLayout(layout_fila)
        
        layout_centro.addWidget(grupo_pilha)
        layout_centro.addWidget(grupo_fila)
        
        # ---------------- PAINEL DIREITO: Consola Operacional ----------------
        layout_direita = QVBoxLayout()
        grupo_logs = QGroupBox("Consola do Sistema e Faturação em Tempo Real")
        layout_log_box = QVBoxLayout()
        self.txt_logs = QTextEdit()
        self.txt_logs.setReadOnly(True)
        self.txt_logs.setFont(QFont("Courier New", 11))
        layout_log_box.addWidget(self.txt_logs)
        grupo_logs.setLayout(layout_log_box)
        layout_direita.addWidget(grupo_logs)
        
        # Montagem Estrutural
        layout_principal.addLayout(layout_esquerda, 3)
        layout_principal.addLayout(layout_centro, 4)
        layout_principal.addLayout(layout_direita, 5)
        
        self.atualizar_ecran()
        self.log_mensagem("SmartPark Core carregado. Faturação configurada em Kwanzas (AOA).")

    # ---------------- LÓGICA AVANÇADA / INTELIGÊNCIA ----------------

    def simular_escaneamento_ocr(self):
        """ Simula o processo de foco de câmara e leitura OCR """
        self.txt_logs.clear()
        self.log_mensagem("📷 [OCR] A iniciar módulo de captação de imagem...")
        self.log_mensagem("📷 [OCR] A processar frames... [||||||||||----] 50%")
        
        # Estruturação de matrículas reais de Angola
        provincias = ["LD", "HU", "BG", "CB", "CC", "BA"]
        prov = random.choice(provincias)
        num1 = random.randint(10, 99)
        num2 = random.randint(10, 99)
        letras = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=2))
        matricula_digitalizada = f"{prov}-{num1}-{num2}-{letras}"
        
        self.log_mensagem(f"📷 [OCR] Processamento Concluído! Matrícula detetada: [{matricula_digitalizada}]")
        self.txt_placa.setText(matricula_digitalizada)

    def processar_entrada(self):
        placa = self.txt_placa.text().strip().upper()
        if not placa:
            QMessageBox.warning(self, "Erro OCR", "Nenhuma matrícula foi inserida ou escaneada.")
            return
        
        novo_carro = Veiculo(placa)
        self.txt_placa.clear()
        
        if not self.estacionamento.esta_cheia():
            self.estacionamento.push(novo_carro)
            self.log_mensagem(f"ENTRADA 🟢 | Vaga {self.estacionamento.topo + 1} ocupada pelo veículo [{placa}].")
        else:
            self.fila_espera.enfileirar(novo_carro)
            self.log_mensagem(f"FILA 🟡    | Estacionamento esgotado! [{placa}] movido para a fila exterior.")
            
        self.atualizar_ecran()

    def processar_saida(self):
        if self.estacionamento.esta_vazia():
            QMessageBox.information(self, "Aviso", "O estacionamento não tem carros no momento.")
            return
        
        carro_saindo = self.estacionamento.pop()
        
        # Lógica de simulação de tempo rápida para testes:
        # 1 segundo real que o carro passou na pilha passa a valer 1 hora no simulador.
        agora = datetime.datetime.now()
        segundos_decorridos = int((agora - carro_saindo.timestamp_entrada).total_seconds())
        
        horas_faturadas = segundos_decorridos if segundos_decorridos > 0 else 1
        
        carro_saindo.tempo_permanencia = horas_faturadas
        carro_saindo.tarifa_paga = calcular_tarifa_progressiva(horas_faturadas)
        
        self.historico.inserir(carro_saindo)
        
        self.log_mensagem(
            f"SAÍDA 🔴   | Veículo [{carro_saindo.placa}] saiu do topo.\n"
            f"            • Tempo de Permanência: {horas_faturadas} hora(s) simulada(s)\n"
            f"            • Tarifa Progressiva (Recursiva): {carro_saindo.tarifa_paga:,.2f} Kz"
        )
        
        # Entrada automática do primeiro elemento da Fila de Espera
        if not self.fila_espera.esta_vazia():
            proximo = self.fila_espera.desenfileirar()
            proximo.timestamp_entrada = datetime.datetime.now()
            proximo.data_hora_entrada = proximo.timestamp_entrada.strftime("%d/%m/%Y %H:%M:%S")
            self.estacionamento.push(proximo)
            self.log_mensagem(f"FLUXO 🔵   | Fila avançou. Veículo [{proximo.placa}] entrou para a vaga libertada.")
            
        self.atualizar_ecran()

    def exibir_relatorio(self):
        self.txt_logs.clear()
        self.txt_logs.append("========================================================\n")
        self.txt_logs.append("           RELATÓRIO FINANCEIRO DE ARRECADAÇÃO         \n")
        self.txt_logs.append("========================================================\n")
        self.txt_logs.append(f"{'Matrícula':<16}{'Entrada':<12}{'Permanência':<14}{'Valor Pago'}\n")
        self.txt_logs.append("-" * 56 + "\n")
        
        total_acumulado = 0.0
        for i in range(self.historico.tamanho):
            v = self.historico.registos[i]
            hora_entrada_limpa = v.data_hora_entrada.split()[1]
            self.txt_logs.append(f"{v.placa:<16}{hora_entrada_limpa:<12}{str(v.tempo_permanencia)+'h':<14}{v.tarifa_paga:,.2f} Kz\n")
            total_acumulado += v.tarifa_paga
            
        self.txt_logs.append("-" * 56 + "\n")
        self.txt_logs.append(f"TOTAL FATURADO NO PARQUE: {total_acumulado:,.2f} Kz\n")
        self.txt_logs.append("========================================================\n")

    # ---------------- ATUALIZAÇÃO DA INTERFACE VISUAL ----------------

    def atualizar_ecran(self):
        # Desenhar estado gráfico da Pilha
        self.lista_pilha.clear()
        if self.estacionamento.esta_vazia():
            self.lista_pilha.addItem("   [ ⭕ PARQUE TOTALMENTE LIVRE ]")
        else:
            for i in range(self.estacionamento.topo, -1, -1):
                carro = self.estacionamento.carros[i]
                status_topo = " 🚨 [PRÓXIMO A SAIR - TOPO]" if i == self.estacionamento.topo else ""
                self.lista_pilha.addItem(f" Vaga {i+1} ➔ {carro.placa} | Entrada: {carro.data_hora_entrada.split()[1]} {status_topo}")
                
        # Desenhar estado gráfico da Fila
        self.lista_fila.clear()
        if self.fila_espera.esta_vazia():
            self.lista_fila.addItem("   [ ✅ SEM VIATURAS RETIDAS NA FILA ]")
        else:
            atual = self.fila_espera.frente
            pos = 1
            while atual is not None:
                self.lista_fila.addItem(f" Posição {pos}º ➔ {atual.veiculo.placa} (Aguardando vaga livre)")
                atual = atual.proximo
                pos += 1

    def log_mensagem(self, msg):
        horario = datetime.datetime.now().strftime("%H:%M:%S")
        self.txt_logs.append(f"[{horario}] {msg}\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = JanelaEstacionamento()
    janela.show()
    sys.exit(app.exec())