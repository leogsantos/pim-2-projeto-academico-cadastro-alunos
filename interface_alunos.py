"""
INTERFACE GRÁFICA PARA SISTEMA DE CADASTRO DE ALUNOS
Integração entre programa C (cadastro) e Python (visualização)
Utiliza Tkinter para interface gráfica
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import csv
import os
import sys
from pathlib import Path

class InterfaceAlunos:
    def __init__(self, root):
        """
        Inicializa a interface principal
        """
        self.root = root
        self.root.title("Sistema de Cadastro de Alunos - Interface Gráfica")
        self.root.geometry("900x650")
        self.root.configure(bg='#f0f0f0')
        
        # Determina o diretório base do script
        if getattr(sys, 'frozen', False):
            # Se executando como executável (pyinstaller)
            self.base_dir = Path(sys.executable).parent
        else:
            # Se executando como script Python
            self.base_dir = Path(__file__).parent
        
        # Caminhos dos arquivos (absolutos)
        self.exe_path = self.base_dir / "output" / "cadastro_alunos.exe"
        self.csv_path = self.base_dir / "output" / "alunos.csv"
        
        # Garante que o diretório output existe
        output_dir = self.base_dir / "output"
        if not output_dir.exists():
            output_dir.mkdir(exist_ok=True)
        
        # Configurar interface
        self.criar_widgets()
        self.carregar_dados()
    
    def criar_widgets(self):
        """
        Cria todos os widgets da interface
        """
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights para responsividade
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="📚 Sistema de Cadastro de Alunos", 
                          font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Frame de controles
        controles_frame = ttk.LabelFrame(main_frame, text="Controles", padding="10")
        controles_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        controles_frame.columnconfigure(3, weight=1)  # Para expandir o status label
        
        # Botão para abrir cadastro
        self.btn_cadastrar = ttk.Button(controles_frame, text="🎓 Abrir Cadastro de Alunos", 
                                       command=self.abrir_cadastro, style='Accent.TButton')
        self.btn_cadastrar.grid(row=0, column=0, padx=(0, 10))
        
        # Botão para atualizar dados
        self.btn_atualizar = ttk.Button(controles_frame, text="🔄 Atualizar Dados", 
                                       command=self.carregar_dados)
        self.btn_atualizar.grid(row=0, column=1, padx=(0, 10))
        
        # Label de status
        self.status_label = ttk.Label(controles_frame, text="Pronto", foreground="green")
        self.status_label.grid(row=0, column=2, padx=(20, 0), sticky=tk.W)
        
        # Frame para lista de alunos
        lista_frame = ttk.LabelFrame(main_frame, text="Alunos Cadastrados", padding="10")
        lista_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        lista_frame.columnconfigure(0, weight=1)
        lista_frame.rowconfigure(0, weight=1)
        
        # Scrollable frame para os alunos
        self.canvas = tk.Canvas(lista_frame, bg='white')
        self.scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configurar scroll com mouse
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        # Label para quando não há dados
        self.no_data_label = ttk.Label(self.scrollable_frame, 
                                      text="Nenhum aluno cadastrado ainda.\nUse o botão 'Abrir Cadastro de Alunos' para adicionar alunos.",
                                      font=('Arial', 12), foreground="gray", justify="center")
    
    def _on_mousewheel(self, event):
        """
        Permite scroll com a roda do mouse
        """
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def abrir_cadastro(self):
        """
        Abre o programa de cadastro em C
        """
        try:
            self.status_label.config(text="Abrindo programa de cadastro...", foreground="blue")
            self.root.update()
            
            # Verifica se o executável existe
            if not self.exe_path.exists():
                raise FileNotFoundError(f"Executável não encontrado: {self.exe_path}")
            
            # Executa o programa C no diretório correto
            output_dir = self.exe_path.parent
            processo = subprocess.Popen([str(self.exe_path)], cwd=str(output_dir))
            
            # Espera o processo terminar
            processo.wait()
            
            # Atualiza os dados após fechar o programa
            self.status_label.config(text="Programa fechado. Atualizando dados...", foreground="orange")
            self.root.update()
            
            self.carregar_dados()
            
        except FileNotFoundError as e:
            messagebox.showerror("Erro", f"Arquivo não encontrado:\n{e}")
            self.status_label.config(text="Erro: Arquivo não encontrado", foreground="red")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao executar programa:\n{e}")
            self.status_label.config(text="Erro ao executar programa", foreground="red")
    
    def carregar_dados(self):
        """
        Carrega dados do arquivo CSV e atualiza a interface
        """
        try:
            # Limpa alunos existentes de forma segura
            for widget in list(self.scrollable_frame.winfo_children()):
                try:
                    widget.destroy()
                except tk.TclError:
                    pass  # Widget já foi destruído
            
            # Verifica se arquivo CSV existe
            if not self.csv_path.exists():
                self.no_data_label = ttk.Label(self.scrollable_frame, 
                                              text="Nenhum aluno cadastrado ainda.\nUse o botão 'Abrir Cadastro de Alunos' para adicionar alunos.",
                                              font=('Arial', 12), foreground="gray", justify="center")
                self.no_data_label.grid(row=0, column=0, pady=50)
                self.status_label.config(text="Arquivo CSV não encontrado", foreground="orange")
                return
            
            # Lê dados do CSV
            alunos = []
            with open(str(self.csv_path), 'r', encoding='utf-8') as arquivo:
                leitor = csv.DictReader(arquivo)
                alunos = list(leitor)
            
            # Se não há alunos, mostra mensagem
            if not alunos:
                self.no_data_label = ttk.Label(self.scrollable_frame, 
                                              text="Nenhum aluno cadastrado ainda.\nUse o botão 'Abrir Cadastro de Alunos' para adicionar alunos.",
                                              font=('Arial', 12), foreground="gray", justify="center")
                self.no_data_label.grid(row=0, column=0, pady=50)
                self.status_label.config(text="Nenhum aluno encontrado no arquivo", foreground="orange")
                return
            
            # Cria frames para cada aluno
            self.criar_frames_alunos(alunos)
            
            # Atualiza status
            self.status_label.config(text=f"✅ {len(alunos)} aluno(s) carregado(s)", foreground="green")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados:\n{e}")
            self.status_label.config(text="Erro ao carregar dados", foreground="red")
    
    def criar_frames_alunos(self, alunos):
        """
        Cria um frame para cada aluno com suas informações em layout horizontal
        """
        for i, aluno in enumerate(alunos):
            # Frame individual do aluno com layout horizontal
            aluno_frame = ttk.LabelFrame(self.scrollable_frame, text=f"Aluno {i+1}", padding="15")
            aluno_frame.grid(row=i, column=0, sticky=(tk.W, tk.E), pady=8, padx=15)
            aluno_frame.columnconfigure(1, weight=1)  # Nome expande
            aluno_frame.columnconfigure(4, weight=1)  # Espaço flexível
            
            # Nome do aluno (ocupando mais espaço)
            ttk.Label(aluno_frame, text="Nome:", font=('Arial', 11, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
            nome_label = ttk.Label(aluno_frame, text=aluno['NOME'], font=('Arial', 11))
            nome_label.grid(row=0, column=1, sticky=tk.W, padx=(0, 30))
            
            # Separador visual
            ttk.Separator(aluno_frame, orient='vertical').grid(row=0, column=2, sticky=(tk.N, tk.S), padx=20)
            
            # Frame para notas em layout compacto horizontal
            notas_frame = ttk.Frame(aluno_frame)
            notas_frame.grid(row=0, column=3, sticky=tk.W, padx=(0, 30))
            
            # Notas em linha horizontal
            colunas_notas = ['NP1', 'NP2', 'PIM']
            for j, nota_tipo in enumerate(colunas_notas):
                # Container para cada nota
                nota_container = ttk.Frame(notas_frame)
                nota_container.grid(row=0, column=j, padx=(0, 25))
                
                # Label do tipo de nota
                ttk.Label(nota_container, text=f"{nota_tipo}:", font=('Arial', 10, 'bold')).grid(row=0, column=0)
                
                # Valor da nota com cor baseada no valor
                nota_valor = float(aluno[nota_tipo])
                cor_nota = self.get_cor_nota(nota_valor)
                
                nota_label = ttk.Label(nota_container, text=f"{nota_valor:.1f}", 
                                     font=('Arial', 11, 'bold'), foreground=cor_nota)
                nota_label.grid(row=1, column=0)
            
            # Separador visual
            ttk.Separator(aluno_frame, orient='vertical').grid(row=0, column=4, sticky=(tk.N, tk.S), padx=(20, 20))
            
            # Média e status na direita
            self.adicionar_media_horizontal(aluno_frame, aluno, column=5)
            
        # Configurar scrollable frame para expandir completamente
        self.scrollable_frame.columnconfigure(0, weight=1)
    
    def adicionar_media_horizontal(self, parent_frame, aluno, column):
        """
        Calcula e adiciona a média do aluno no frame (layout horizontal)
        """
        try:
            # Calcula média simples
            np1 = float(aluno['NP1'])
            np2 = float(aluno['NP2'])
            pim = float(aluno['PIM'])
            media = (np1 + np2 + pim) / 3
            
            # Container para média e status
            media_container = ttk.Frame(parent_frame)
            media_container.grid(row=0, column=column, sticky=tk.E, padx=(10, 0))
            
            # Média
            ttk.Label(media_container, text="Média:", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=(0, 5))
            
            # Valor da média com cor
            cor_media = self.get_cor_nota(media)
            ttk.Label(media_container, text=f"{media:.1f}", 
                     font=('Arial', 12, 'bold'), foreground=cor_media).grid(row=0, column=1, padx=(0, 15))
            
            # Status
            status = "APROVADO" if media >= 7.0 else "REPROVADO"
            cor_status = "green" if media >= 7.0 else "red"
            status_label = ttk.Label(media_container, text=status, 
                                   font=('Arial', 10, 'bold'), foreground=cor_status)
            status_label.grid(row=0, column=2)
            
        except ValueError:
            # Se houver erro na conversão, não mostra média
            pass
    
    def adicionar_media(self, parent_frame, aluno):
        """
        Calcula e adiciona a média do aluno no frame (layout vertical - mantido para compatibilidade)
        """
        try:
            # Calcula média simples
            np1 = float(aluno['NP1'])
            np2 = float(aluno['NP2'])
            pim = float(aluno['PIM'])
            media = (np1 + np2 + pim) / 3
            
            # Frame para média
            media_frame = ttk.Frame(parent_frame)
            media_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
            
            # Label média
            ttk.Label(media_frame, text="Média:", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=(0, 10))
            
            # Valor da média com cor
            cor_media = self.get_cor_nota(media)
            status = "APROVADO" if media >= 7.0 else "REPROVADO"
            
            ttk.Label(media_frame, text=f"{media:.2f}", 
                     font=('Arial', 10, 'bold'), foreground=cor_media).grid(row=0, column=1, padx=(0, 20))
            
            # Status
            cor_status = "green" if media >= 7.0 else "red"
            ttk.Label(media_frame, text=status, 
                     font=('Arial', 10, 'bold'), foreground=cor_status).grid(row=0, column=2)
            
        except ValueError:
            # Se houver erro na conversão, não mostra média
            pass
    
    def get_cor_nota(self, nota):
        """
        Retorna cor baseada no valor da nota
        """
        if nota >= 8.0:
            return "green"
        elif nota >= 6.0:
            return "orange"
        else:
            return "red"

def main():
    """
    Função principal - inicializa a aplicação com tratamento de erros
    """
    try:
        # Configura o ambiente Python
        root = tk.Tk()
        
        # Previne erro de path do Tkinter
        root.tk.eval('set tcl_platform(threaded) 0')
        
        # Configura o estilo
        try:
            style = ttk.Style()
            style.theme_use('clam')  # Tema mais moderno
        except:
            # Se não conseguir usar o tema clam, usa o padrão
            pass
        
        # Cria a aplicação
        app = InterfaceAlunos(root)
        
        # Centraliza a janela na tela
        try:
            root.update_idletasks()
            x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
            y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
            root.geometry(f"+{x}+{y}")
        except:
            # Se não conseguir centralizar, usa posição padrão
            pass
        
        # Inicia o loop principal
        root.mainloop()
        
    except Exception as e:
        # Mostra erro em uma messagebox se possível
        try:
            root = tk.Tk()
            root.withdraw()  # Esconde a janela principal
            messagebox.showerror("Erro Fatal", f"Erro ao inicializar aplicação:\n{e}")
        except:
            # Se nem messagebox funcionar, imprime no console
            print(f"Erro fatal: {e}")
            input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
