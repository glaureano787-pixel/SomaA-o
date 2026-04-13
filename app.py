import sys
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QTextEdit, 
                             QPushButton, QFrame, QGridLayout, QSpacerItem, 
                             QSizePolicy)
from PySide6.QtGui import QFont, QIcon, QColor

class SomaAcoUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SOMA AÇO - Sistema de Gestão Industrial")
        self.resize(1100, 700)
        self.setMinimumSize(900, 600)

        # Configuração do Tema Dark Industrial
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0f172a;
            }
            QWidget {
                color: #e2e8f0;
                font-family: 'Segoe UI', sans-serif;
            }
            QFrame#Card {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
            }
            QLabel#Title {
                color: #3b82f6;
                font-weight: bold;
                font-size: 14px;
                text-transform: uppercase;
            }
            QLabel#HeaderTitle {
                color: white;
                font-weight: 800;
                font-size: 20px;
                letter-spacing: 1px;
            }
            QLabel#HeaderSub {
                color: #94a3b8;
                font-size: 11px;
                text-transform: uppercase;
            }
            QLineEdit, QTextEdit {
                background-color: #020617;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 10px;
                color: white;
                font-size: 13px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #3b82f6;
            }
            QPushButton#PrimaryBtn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b82f6, stop:1 #1d4ed8);
                border-radius: 8px;
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 15px;
            }
            QPushButton#PrimaryBtn:hover {
                background: #2563eb;
            }
            QPushButton#SecondaryBtn {
                background-color: #334155;
                border-radius: 6px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton#SecondaryBtn:hover {
                background-color: #475569;
            }
            QLabel#EmptyStateTitle {
                color: #94a3b8;
                font-size: 18px;
                font-weight: bold;
            }
            QLabel#EmptyStateSub {
                color: #475569;
                font-size: 12px;
            }
        """)

        # Widget Central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(30, 20, 30, 20)

        self.setup_header()
        
        # Conteúdo Principal (2 Colunas)
        self.content_layout = QHBoxLayout()
        self.content_layout.setSpacing(25)
        
        self.setup_left_panel()
        self.setup_right_panel()
        
        self.main_layout.addLayout(self.content_layout)
        self.setup_footer()

    def setup_header(self):
        header_layout = QHBoxLayout()
        
        # Esquerda: Logo e Nome
        logo_container = QVBoxLayout()
        h_logo = QHBoxLayout()
        
        icon_box = QLabel("S")
        icon_box.setFixedSize(45, 45)
        icon_box.setAlignment(Qt.AlignCenter)
        icon_box.setStyleSheet("background-color: #3b82f6; border-radius: 10px; color: white; font-weight: bold; font-size: 24px;")
        
        title_vbox = QVBoxLayout()
        lbl_name = QLabel("SOMA AÇO")
        lbl_name.setObjectName("HeaderTitle")
        lbl_sub = QLabel("ALGORITMO DE AGRUPAMENTO E CONFERÊNCIA DE LOTES")
        lbl_sub.setObjectName("HeaderSub")
        
        title_vbox.addWidget(lbl_name)
        title_vbox.addWidget(lbl_sub)
        
        h_logo.addWidget(icon_box)
        h_logo.addLayout(title_vbox)
        header_layout.addLayout(h_logo)
        
        header_layout.addStretch()
        
        # Direita: Menu Status
        status_vbox = QVBoxLayout()
        lbl_painel = QLabel("Painel de Operações")
        lbl_painel.setStyleSheet("color: #3b82f6; font-weight: bold; font-size: 12px;")
        lbl_version = QLabel("Industrial v1.0")
        lbl_version.setAlignment(Qt.AlignRight)
        lbl_version.setStyleSheet("color: #475569; font-size: 11px;")
        
        status_vbox.addWidget(lbl_painel)
        status_vbox.addWidget(lbl_version)
        header_layout.addLayout(status_vbox)
        
        self.main_layout.addLayout(header_layout)
        self.main_layout.addSpacing(20)

    def setup_left_panel(self):
        panel = QFrame()
        panel.setObjectName("Card")
        panel.setFixedWidth(450)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        lbl_section = QLabel("ENTRADA DE DADOS")
        lbl_section.setObjectName("Title")
        layout.addWidget(lbl_section)

        # Seção 1: Lotes
        layout.addWidget(QLabel("1. ADICIONAR LOTES REAIS"))
        
        grid_lote = QGridLayout()
        grid_lote.addWidget(QLabel("ID DO LOTE"), 0, 0)
        grid_lote.addWidget(QLabel("META PESO (KG)"), 0, 1)
        grid_lote.addWidget(QLabel("QTD. ROLOS"), 0, 2)

        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("Ex: Lote 181")
        self.input_meta = QLineEdit()
        self.input_meta.setPlaceholderText("Ex: 5430")
        self.input_qtd = QLineEdit()
        self.input_qtd.setPlaceholderText("Ex: 9")
        
        btn_add = QPushButton("+")
        btn_add.setFixedSize(40, 40)
        btn_add.setObjectName("SecondaryBtn")

        grid_lote.addWidget(self.input_id, 1, 0)
        grid_lote.addWidget(self.input_meta, 1, 1)
        grid_lote.addWidget(self.input_qtd, 1, 2)
        grid_lote.addWidget(btn_add, 1, 3)
        layout.addLayout(grid_lote)

        layout.addSpacing(10)

        # Seção 2: Estoque
        layout.addWidget(QLabel("2. ESTOQUE DISPONÍVEL (PESOS DOS ROLOS)"))
        self.txt_estoque = QTextEdit()
        self.txt_estoque.setPlaceholderText("Digite os pesos dos rolos separados por vírgula ou espaço. Ex: 600, 550, 595...")
        layout.addWidget(self.txt_estoque)

        # Botões de Ação
        btn_layout = QHBoxLayout()
        btn_process = QPushButton(" ▶   PROCESSAR AGRUPAMENTO")
        btn_process.setObjectName("PrimaryBtn")
        btn_process.setCursor(Qt.PointingHandCursor)
        
        btn_refresh = QPushButton(" ⟳ ")
        btn_refresh.setObjectName("SecondaryBtn")
        btn_refresh.setFixedSize(50, 50)
        
        btn_layout.addWidget(btn_process)
        btn_layout.addWidget(btn_refresh)
        layout.addLayout(btn_layout)

        self.content_layout.addWidget(panel)

    def setup_right_panel(self):
        panel = QFrame()
        panel.setObjectName("Card")
        panel.setStyleSheet("QFrame#Card { border: 2px dashed #334155; }")
        
        layout = QVBoxLayout(panel)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        icon_calc = QLabel("⌨") # Representando a calculadora via texto (pode usar QIcon/Imagem)
        icon_calc.setStyleSheet("font-size: 60px; color: #334155;")
        icon_calc.setAlignment(Qt.AlignCenter)
        
        lbl_empty = QLabel("Aguardando Lotes & Estoque")
        lbl_empty.setObjectName("EmptyStateTitle")
        
        lbl_desc = QLabel("Cadastre as metas de peso por lote e o estoque de rolos disponível.\nO algoritmo processará as melhores combinações para cada requisito.")
        lbl_desc.setObjectName("EmptyStateSub")
        lbl_desc.setAlignment(Qt.AlignCenter)

        layout.addStretch()
        layout.addWidget(icon_calc)
        layout.addWidget(lbl_empty)
        layout.addWidget(lbl_desc)
        layout.addStretch()

        self.content_layout.addWidget(panel)

    def setup_footer(self):
        footer = QLabel("© 2026 SomaAço. Desenvolvido por Laureano Romagnole 38.")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #475569; font-size: 11px; margin-top: 20px;")
        self.main_layout.addWidget(footer)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SomaAcoUI()
    window.show()
    sys.exit(app.exec())
