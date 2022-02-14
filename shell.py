import os
from pathlib import Path
import threading
import sys
import multiprocessing

class interprete:
    def __init__(self):
        self.status = True
        self.pwd = self.shell = Path(__file__).parent.absolute()
        self.threads = []

    def identificar(self, input):
        input = input.split()
        if input[0] == 'cd':
            self.cd(input)
        elif input[0] == 'dir':
            self.dir(input)
        elif input[0] == 'environ':
            print("pwd : "+ str(self.pwd))
            print("shell : "+ str(self.shell))
        elif input[0] == 'echo':
            self.echo(input)
        elif input[0] == 'help':
            ## Falta help
            pass
        else:
            os.system(input[0])
            # thread_ejecucion = threading.Thread(target = lambda: os.system(input[0]))
            # thread_ejecucion.daemon = True
            # self.threads.append(thread_ejecucion)
            # self.threads[len(self.threads) - 1].start()
       
    def cd(self, input):
        if len(input) < 2:
            os.chdir(self.pwd)         
            return
        try:
            source = ''
            cont = 0
            for word in input:
                if cont > 0:
                    source += " " + word
                cont += 1
            os.chdir(Path(source.strip()))
            self.pwd = Path(source.strip()).parent.absolute()
        except:
            print('error: directorio no valido ')

    def dir(self, input):
        if len(input) < 2:
            lista_directorios = os.listdir(Path(os.getcwd()))
            for directorio in lista_directorios:
                print(directorio)
            return
        try:
            source = ''
            cont = 0
            for word in input:
                if cont > 0:
                    source += " " + word
                cont += 1
            print(source)
            if source.find(">") == -1 and source.find(">>") == -1:
                print("sadasd")
                lista_directorios = os.listdir(Path(source.strip()))
                for directorio in lista_directorios:
                    print(directorio)
                return
        except:
            print('error: directorio no valido ')

        if source.find(">>") != -1:
            source = source.split('>>')
            self.dir_file2(source, '>>')
            return
        elif source.find(">") != -1:
            source = source.split(">")
            self.dir_file1(source, ">")
            return
        else:
            print('error : la sitaxis del comando es incorrecta')

    def dir_file1(self, source):
        if source[0] == '':
            lista_directorios = os.listdir(self.pwd)
        else:
            lista_directorios = os.listdir(Path(source[0].strip()))
        file = open(source[1].strip(), "w+")       
        for directorio in lista_directorios:
            file.write(directorio + '\n')
        file.close()
    
    def dir_file2(self, source):
        if source[0] == '':
            lista_directorios = os.listdir(self.pwd)
            print(lista_directorios)
        else:
            lista_directorios = os.listdir(Path(source[0].strip()))   
        file = open(source[1].strip(), "a+")
        for directorio in lista_directorios:
            file.write(directorio + '\n')
        file.close()
          
    def echo(self, input):
        cont = 0
        for word in input:
            if cont > 0:
                print(word)
            cont += 1

    def terminar_Threads(self):
        for thread in self.threads:
            thread.join()
        
if __name__ == '__main__':
    print("-------------------------------------")
    os.system("cls")
    if len(sys.argv) > 1:
        print("Fichero de lotes") 
        archivo = open(sys.argv[1], 'r')
        lineas = archivo.readlines()
        parser_lotes = interprete()
        for linea in lineas:
            parser_lotes.identificar(linea.replace('\n', ''))
        archivo.close()
    else:
        parser = interprete()
        while True:
            a = input(str(os.getcwd()+" "))
            if a == "pause": parser.status = False
            if parser.status == True and a != '':
                if a == "quit":
                    # parser.terminar_Threads()
                    sys.exit()
                elif a == "cls":
                    if os.name == "nt":
                        os.system("cls")
                    else:
                        os.system("clear")
                else:
                    parser.identificar(a)
            else:
                if a == '':
                    parser.status = True
                else:
                    print("En pausa")
    
