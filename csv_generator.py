# write a file
import random
import string
import sys
import os

class CsvGenerator():

    class Exceptions():
        class FileNotFound(Exception):
            pass
        class FileAlreadyExists(Exception):
            pass
        class InvalidSize(Exception):
            pass
        class InvalidColumnNumber(Exception):
            pass
        class InvalidStringSize(Exception):
            pass

        def __init__(self) -> None:
            raise Exception("Não é possível instanciar essa classe")
    
    class Sizes():  
        GB = 1_073_741_824 # 1GB
        MB = 1_048_576 # 1MB
        KB = 1024 # 1KB

        def __init__(self) -> None:
            raise Exception("Não é possível instanciar essa classe")

    def __init__(self, filename: str, tamanho_pretendido: int, string_max_size: int = 20, n_columns: int= 10, reuse_file: str = None):
        """ 
        Gera um arquivo CSV com o tamanho pretendido

        Parameters
        ----------
            filename : str
                Nome do arquivo a ser gerado
            tamanho_pretendido : int
                Tamanho pretendido do arquivo em bytes
            string_max_size : int
                Tamanho máximo da string gerada
            n_columns : int
                Número de colunas do arquivo a ser gerado.
                Caso exista um arquivo para reutilizar, o número de colunas será definido pelo arquivo já existente
            reuse_file : str
                Nome do arquivo a ser reutilizado
        """
        if tamanho_pretendido < 0:
            raise self.Exceptions.InvalidSize("Tamanho inválido")
        if string_max_size < 1:
            raise self.Exceptions.InvalidStringSize("Tamanho inválido")

        self.filename = filename
        self.tamanho_pretendido = tamanho_pretendido
        self.string_max_size = string_max_size
        if reuse_file is not None:
            if not os.path.exists(reuse_file):
                raise self.Exceptions.FileNotFound("Arquivo não encontrado: "+reuse_file)
            self.reuseFile(reuse_file)
            file = open(self.filename, "r")
            self.n_columns = len(file.readline().split(";"))
            file.close()
        else:
            if n_columns < 1:
                raise self.Exceptions.InvalidColumnNumber("Número de colunas inválido")
            self.n_columns = n_columns
    
    def reuseFile(self, filename: str):
        # copia o conteudo de um arquivo para outro
        file = open(filename, "r")
        file2 = open(self.filename, "w")
        for line in file:
            file2.write(line)
        file.close()
        file2.close()


    def generateHeader(self):
        header = []
        for i in range(0, self.n_columns):
            header.append("coluna"+str(i+1))
        return header
    
    def formatSize(self, size, precision=2):
        if size < self.KB:
            return str(size)+" B"
        elif size < self.MB:
            return str(round(size/self.KB, precision))+" KB"
        elif size < self.GB:
            return str(round(size/self.MB, precision))+" MB"
        else:
            return str(round(size/self.GB, precision))+" GB"
    
    def generateRandomString(self):
        return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(1, self.string_max_size)))
    
    def generate(self):
        file = open(self.filename, "a")
        try:
            if file.tell() == 0: # se o arquivo estiver vazio
                file.write(";".join(self.generateHeader()) + "\n")
            else:
                file.seek(0, 2) # move o cursor para o final do arquivo
            
            while file.tell() < self.tamanho_pretendido:
                linha = []
                for j in range(1, self.n_columns): # para cada coluna
                    linha.append(self.generateRandomString())
                file.write(";".join(linha) + "\n")
                sys.stdout.write(
                    "\rPretendido: "+self.formatSize(self.tamanho_pretendido)+" | Tamanho: "+self.formatSize(file.tell())+" | Diferença: "+self.formatSize(self.tamanho_pretendido - file.tell())
                )
                sys.stdout.flush()
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            pass
        finally:
            file.close()

if __name__ == "__main__":
    # Usase assim:

    # Gera um arquivo de 1MB com 20 colunas
    CsvGenerator("1MB.csv", 1*CsvGenerator.Sizes.MB, n_columns=20).generate()

    # Gera um arquivo de 1GB com 200 colunas
    CsvGenerator("1GB.csv", 1*CsvGenerator.Sizes.GB, n_columns=200).generate()

    # Gera um arquivo de 2GB com 200 colunas reutilizando o arquivo 1GB.csv
    CsvGenerator("2GB.csv", 2*CsvGenerator.Sizes.GB, reuse_file="1GB.csv").generate()