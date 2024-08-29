import tkinter as tk
from tkinter import filedialog, messagebox
import re
import xml.etree.ElementTree as ET

class XMLExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("XML Extractor")

        # Configurar o tamanho da janela
        self.root.geometry("800x600")  # Largura x Altura

        # Configurar o layout da interface
        self.label = tk.Label(root, text="Escolha arquivos XML:", font=("Arial", 12))
        self.label.pack(pady=20)

        self.load_button = tk.Button(root, text="Carregar XMLs", command=self.load_files, font=("Arial", 12))
        self.load_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 16))
        self.result_label.pack(pady=20)

        # Adicionar o botão Fechar e posicioná-lo no canto superior direito
        self.close_button = tk.Button(root, text="Fechar", command=self.root.quit, font=("Arial", 12))
        self.close_button.place(x=760, y=10, anchor='ne')  # Ajuste a posição conforme necessário

        # Adicionar o botão Importar abaixo do botão Fechar
        self.import_button = tk.Button(root, text="Importar", command=self.save_to_txt, font=("Arial", 12))
        self.import_button.place(x=760, y=50, anchor='ne')  # Ajuste a posição conforme necessário

        self.numbers = []

    def load_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("XML files", "*.xml")])
        if file_paths:
            self.numbers = []  # Limpar números anteriores
            for file_path in file_paths:
                try:
                    # Processar o XML
                    tree = ET.parse(file_path)
                    root = tree.getroot()

                    # Definir o namespace
                    namespace = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

                    # Extraindo a informação da nota
                    infAdic = root.find('.//nfe:infNFe/nfe:infAdic', namespace)
                    if infAdic is not None:
                        infCpl = infAdic.find('nfe:infCpl', namespace)
                        if infCpl is not None:
                            informação = infCpl.text

                            # Usar expressão regular para encontrar o número após "DOCUMENTO FATURAMENTO:"
                            match = re.search(r'DOCUMENTO FATURAMENTO:\s*(\d+)', informação)
                            if match:
                                numero = match.group(1)
                                self.numbers.append(numero)
                            else:
                                self.numbers.append("Número após 'DOCUMENTO FATURAMENTO:' não encontrado")
                        else:
                            self.numbers.append("Elemento infCpl não encontrado")
                    else:
                        self.numbers.append("Elemento infAdic não encontrado")
                except Exception as e:
                    self.numbers.append(f"Erro ao processar o arquivo {file_path}: {e}")

            # Exibir todos os números encontrados
            result_text = "\n".join(self.numbers)
            self.result_label.config(text=result_text)

    def save_to_txt(self):
        if self.numbers:
            with open("numeros_encontrados.txt", "w") as file:
                file.write("\n".join(self.numbers))
            messagebox.showinfo("Sucesso", "Números salvos no arquivo 'numeros_encontrados.txt'.")
        else:
            messagebox.showwarning("Aviso", "Nenhum número encontrado para salvar.")

if __name__ == "__main__":
    root = tk.Tk()
    app = XMLExtractorApp(root)
    root.mainloop()
