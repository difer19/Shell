import os
from pathlib import Path
import sys
import threading
import platform


man = """COMANDOS:

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
    
    quit – sale del intérprete de mandatos."""

class interprete:
    def __init__(self):
        self.status = True
        self.pwd = self.shell = Path(__file__).parent.absolute()
        self.threads = []

    def identificar(self, input):
        input = input.split()
        if input[0] == 'cd':
            if '<' not in input:
                self.cd(input)
            else:
                self.stdin_cd(input)
        elif input[0] == 'dir':
            if '<' in input and ('>' not in input and '>>' not in input):
                self.dir_stdin(input)
            elif '<' not in input and ('>' in input or '>>' in input):
                self.dir_stdout(input)
            elif '<' in input and ('>' in input or '>>' in input):
                self.dir_stdio(input)
            else:
                self.dir(input)
        elif input[0] == 'environ':
            try:
                if len(input) == 1:
                    print("pwd : "+ str(self.pwd))
                    print("shell : "+ str(self.shell))
                elif input[1] == '>':
                    self.environ_stdout(input, '>')
                elif input[1] == '>>':
                    self.environ_stdout(input, '>>')
                else:
                    print("error : comando no valido")
            except:
                print("error : directorio no valido")
        elif input[0] == 'echo':
            if '<' in input and ('>' not in input and '>>' not in input):
                self.echo_stdin(input)
            elif '<' not in input and ('>' in input or '>>' in input):
                self.echo_stdout(input)
            elif '<' in input and ('>' in input or '>>' in input):
                self.echo_stdio(input)
            else:
                self.echo(input)
        elif input[0] == 'help':
            if len(input) == 1:
                self.help()
            elif len(input) >= 3:
                try:
                    self.help_stdout(input)
                except:
                    print("error : directorio no valido" )
            else:
                print("error : comando no valido")
        else:
            if len(input) == 1:
                os.system(input[0])
            elif len(input) == 2 and input[1] == '&':
                thread_ejecucion = threading.Thread(target = lambda: os.system(input[0]))
                thread_ejecucion.daemon = True
                self.threads.append(thread_ejecucion)
                self.threads[len(self.threads) - 1].start()
            else:
                print("error : sintaxis incorrecta")

       
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
    
    def stdin_cd(self, input):
        source = ''
        cont = 0
        flag = 0
        for word in input:
            if cont > 0 and flag == 1:
                source += " " + word
            elif flag == 0 and word == '<': 
                flag = 1
            cont += 1
        source = source.strip()
        path_destino = self.input_stream(source)
        os.chdir(Path(path_destino.strip()))
        self.pwd = Path(path_destino.strip()).parent.absolute()

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
            lista_directorios = os.listdir(Path(source.strip()))
            for directorio in lista_directorios:
                print(directorio)
            return
        except:
            print('error: directorio no valido ')
    
    def dir_stdin(self, input):
        if len(input) < 3:
            print("error : sintaxis incorrecta")
            return
        cont = 0
        source = ''
        for word in input:
            if cont > 0 and word != '<':
                source += " " + word
            cont += 1 
        source = source.strip()
        if self.input_stream(source) != 'error':
            lista_directorios = os.listdir(Path(self.input_stream(source)))
            for directorio in lista_directorios:
                print(directorio)
        else:
            print("error : directorio no valido")
    
    def dir_stdout(self, input):
        input_sep = "".join(input)
        if '>' in input:
            input_sep = input_sep.split('>')
        elif '>>' in input:
            input_sep = input_sep.split('>>')
        source = input_sep[0][3:].strip()
        try:
            if source == '':
                lista_directorios = os.listdir(self.pwd)
            else:
                lista_directorios = os.listdir(Path(source))
            if '>' in input:
                file = open(input_sep[1].strip(), "w+")       
                for directorio in lista_directorios:
                    file.write(directorio + '\n')
            elif '>>' in input:
                file = open(input_sep[1].strip(), "a+")
                for directorio in lista_directorios:
                    file.write(directorio + '\n')
            file.close()
        except:
            print("error : directorio no valido")
    
    def dir_stdio(self, input):
        if '>' in input:
            source_input = "".join(input).split('>')[0][4:].strip()
            source_output = "".join(input).split('>')[1].strip()
        elif '>>' in input:
            source_input = "".join(input).split('>>')[0][4:].strip()
            source_output = "".join(input).split('>>')[1].strip()
        
        try:
            lista_directorios = os.listdir(Path(self.input_stream(source_input)))
        except:
            print("error : el archivo de entrada no tiene una directorio valido o no existe")
            return     
        try:
            if '>' in input:
                file = open(source_output, "w+")       
                for directorio in lista_directorios:
                    file.write(directorio + '\n')
            elif '>>' in input:
                file = open(source_output, "a+")
                for directorio in lista_directorios:
                    file.write(directorio + '\n')
        except:
            print("error : directorio no valido")
            return
        
    def input_stream(self, source, command = True):
        if command:
            try:
                file = open(source, 'r', encoding="utf-8")
                lines = file.readlines() 
                if len(lines) == 1:
                    return lines[0]
                else:
                    print("error : el archivo tiene mas de una linea")
            except:
                return 'error'
                print('error : directorio no valido')
        else:
            try:
                file = open(source, 'r', encoding="utf-8")
                lines = file.readlines() 
                return lines
            except:
                return 'error'
    
    def environ_stdout(self, source, sep):
        source_f = ''
        cont = 0
        for word in source:
            if cont > 0 and word != '>' and word != '>>':
                source_f += " " + word
            cont += 1
        source_f = source_f.strip()
        if source_f == '':
            print("error : falta directorio")
            return
        if sep == '>':
            file = open(source_f, "w+")
            file.write("pwd : "+ str(self.pwd) + '\n')
            file.write("shell : "+ str(self.shell) + '\n')
        elif sep == '>>':
            file = open(source_f, "a+")
            file.write("pwd : "+ str(self.pwd) + '\n')
            file.write("shell : "+ str(self.shell) + '\n')
        file.close()
          
    def echo(self, input):
        cont = 0
        for word in input:
            if cont > 0:
                print(word)
            cont += 1

    def echo_stdin(self, input):
        source_input = "".join(input).split('<')[1].strip()
        lines = self.input_stream(source_input, False)
        if lines == 'error':
            print("error : el fichero de entrada no existe")
            return
        elif len(lines) > 0:
            for line in lines:
                words = line.split()
                for word in words:
                    print(word)
          
    def echo_stdout(self, input):
        if '>' in input:
            source_output = "".join(input).split('>')[1].strip()
        elif '>>' in input:
             source_output = "".join(input).split('>>')[1].strip()
        
        words = []
        cont = 0
        flag = 0
        for word in input:
            if word == '>' or word == '>>':
                flag = 1
            if cont > 0 and flag == 0:
                words.append(word)
            cont += 1

        try:
            if '>' in input:
                file = open(source_output, "w+")
                for word in words:
                    file.write(word + '\n')
            elif '>>' in input:
                file = open(source_output, "a+")
                for word in words:
                    file.write(word + '\n') 
            file.close()
        except:
            print("error : directorio no valido")
    
    def echo_stdio(self, input):
        if '>' in input:
            source_output = "".join(input).split('>')[1].strip()
            source_input = "".join(input).split('>')[0][5:].strip()
        elif '>>' in input:
            source_output = "".join(input).split('>>')[1].strip()
            source_input = "".join(input).split('>>')[0][5:].strip()
        print(source_output)
        print(source_input)
        lines = self.input_stream(source_input, False)
        if lines == 'error':
            print("error : el fichero de entrada no existe")
            return
        lista_words = []
        for line in lines:
            words = line.split()
            for word in words:
                lista_words.append(word)     
        try:
            if '>' in input:
                file = open(source_output, "w+")
                for word in lista_words:
                    file.write(word + '\n')
            elif '>>' in input:
                file = open(source_output, "a+")
                for word in lista_words:
                    file.write(word + '\n') 
            file.close()
        except:
            print("error : directorio no valido")
        
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
        
    def help_stdout(self, input):
        source = ''
        cont = 0
        for word in input:
            if cont > 0 and word != '>' and word != '>>':
                source += ' ' + word
            cont += 1
        source = source.strip()
        if input[1] == '>':
            file = open(source, "w+", encoding="utf-8")
            file.writelines(str(man))
        elif input[1] == '>>':
            file = open(source, "a+", encoding="utf-8")
            file.writelines(str(man))
        file.close()


if __name__ == '__main__':
    os.system("cls")
    print(platform.system())
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
                    sys.exit()
                elif a == "cls":
                    if platform.system() == "Windows":
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
    
