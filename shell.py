import os
from pathlib import Path
import threading
import sys
import multiprocessing

man = '''COMANDOS:

    cd — cambiar el directorio de trabajo  
    cd [ directorio ]
    Si el argumento <directorio> no aparece, devuelve el directorio actual. 
    Si el directorio no existe el sistema lanza un mensaje de error.
    
    clr - borra la pantalla del terminal.
    
    dir <directory> – lista el contenido de <directorio>.
    
    environ – muestra todas las variables de entorno.
    
    echo <comentario> – muestra <comentario> en la pantalla seguido de una nueva línea (espacios
    múltiples o tabuladores se reducen a un espacio sencillo).
    
    help – muestra el manual de usuario usando el filtro more.
    
    pause – detiene la ejecución del intérprete de mandatos hasta que se pulse ‘Intro’.
    
    quit – sale del intérprete de mandatos.'''

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
            self.help()
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
    def help(self):
        x = 2
        print("\n"+man[:222])
        tecla = input()
        while tecla !='q':
            if(x == 2): 
                print(man[223:269])
            if(x == 3): 
                print(man[270:332])
            if(x == 4):
                print(man[333:391])
            if(x == 5):
                print(man[392:556])
            if(x == 6):
                print(man[557:624])
            if(x == 7):
                print(man[625:717])    
            if(x == 8):
                print(man[718:770])   
            if(x == 9): break
            tecla = input()
            x += 1


if __name__ == '__main__'   :
    os.system("cls")
    print("****************************************************************************")
    print("myShell..")
    print("----------------------------------------------------------------------------")
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
    
