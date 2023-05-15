'''
Projeto:
- Compilador: Análise léxica e sintática

Disciplina:
- Linguagens Formais e Compiladores

Professor:
- Frank Coelho de Alcantara

Grupo: 
- Grupo 03

Integrantes:
- Diego Barreto Pedroso Simões
- Muriel Tramontin Von Linsingen
- Vinicius Ramos Garcia
- William Hoeflich Woinarowski

Linguagem:
- Python

Descrição:

Desenvolver um analisador léxico e sintático (parser) para
a linguagem de programação proposta no documento a seguir:

https://github.com/thewillboy/compilador

'''

# Importa as bibliotecas usadas no código
from sly import Lexer
from sly import Parser
import os
import sys


class BasicLexer(Lexer):
  tokens = {
    NAME, TYPE_INT, TYPE_REAL, TYPE_STRING, INT, REAL, STRING, IF, THEN, ELSE,
    END, FOR, TO, DIGITAL_READ, DIGITAL_WRITE, ANALOG_READ, ANALOG_WRITE,
    PIN_MODE, PIN_TYPE, DO, WHILE, EQEQ, BOOL, BIGGER_OR_EQUAL,
    SMALLER_OR_EQUAL, BIGGER, SMALLER, DELAY, LBRACE, RBRACE
  }
  ignore = '\t\b\n '
  literals = {'=', '+', '-', '/', '*', '(', ')', '{', '}', '}', ',', ';'}

  # Define tokens
  IF = r'IF'
  THEN = r'THEN'
  ELSE = r'ELSE'
  FOR = r'FOR'
  DIGITAL_READ = r'DIGITAL_READ'
  DIGITAL_WRITE = r'DIGITAL_WRITE'
  ANALOG_READ = r'ANALOG_READ'
  ANALOG_WRITE = r'ANALOG_WRITE'
  DELAY = r'DELAY'
  PIN_MODE = r'PIN_MODE'
  WHILE = r'WHILE'
  DO = r'DO'
  LBRACE = r'{'
  RBRACE = r'}'
  END = r'END'
  TO = r'TO'
  TYPE_INT = r'TYPE_INT'
  TYPE_REAL = r'TYPE_REAL'
  TYPE_STRING = r'TYPE_STRING'
  PIN_TYPE = r'OUTPUT|INPUT'
  BOOL = r'TRUE|FALSE'
  NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
  STRING = r'\".*?\"'
  EQEQ = r'=='
  BIGGER_OR_EQUAL = r'>='
  SMALLER_OR_EQUAL = r'<='
  BIGGER = r'>'
  SMALLER = r'<'

  @_(r'\d+$')
  def INT(self, t):
    t.value = int(t.value)
    return t

  @_(r'\d+.\d+')
  def REAL(self, t):
    t.value = float(t.value)
    return t

  @_(r'#.*')
  def COMMENT(self, t):
    pass

  @_(r'\n+')
  def newline(self, t):
    self.lineno = t.value.count('\n')

  def error(self, t):
    sys.stderr.write(f'O caractere {t.value[0]} não é aceito nesta linguagem!')
    self.index += 1


class BasicParser(Parser):
  tokens = BasicLexer.tokens

  precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
  )

  def __init__(self):
    self.env = {}

  @_('')
  def statement(self, p):
    pass

  @_('FOR "(" var_assign ")" TO "(" expr ")" THEN "{" statement "}" END')
  def statement(self, p):
    wait = input("Pressione enter para continuar...")
    return ('for_loop', ('for_loop_setup', p.var_assign, p.expr), p.statement0)

  @_('IF "(" condition ")" THEN "{" statement "}" END')
  def statement(self, p):
    return ('if_stmt', p.condition, ('branch', p.statement))

  @_('IF "(" condition ")" THEN "{" statement "}" ELSE "{" statement "}" END')
  def statement(self, p):
    return ('if_stmt_else', p.condition, ('branch', p.statement0,
                                          p.statement1))

  @_('WHILE "(" condition ")" LBRACE')
  def statement(self, p):
    return ('open_while', p.WHILE, p.condition)

  @_('WHILE "(" condition ")" statement END')
  def statement(self, p):
    return ('while', p.WHILE, ('branch', p.condition, p.statement))

  @_('RBRACE END')
  def statement(self, p):
    return ('close_statement', p.END)

  @_('DO "{" statement "}" WHILE "(" condition ")" END')
  def statement(self, p):
    return ('do_while', p.DO, ('branch', p.WHILE, p.condition), p.statement)

  @_('DIGITAL_READ "(" expr ")"')
  def statement(self, p):
    return ('dig_read_call', p.DIGITAL_READ, p.expr)

  @_('DIGITAL_WRITE "(" expr "," expr ")"')
  def statement(self, p):
    return ('dig_write_call', p.DIGITAL_WRITE, p.expr0, p.expr1)

  @_('ANALOG_READ "(" expr ")"')
  def statement(self, p):
    return ('analog_read_call', p.ANALOG_READ, p.expr)

  @_('ANALOG_WRITE "(" expr "," expr ")"')
  def statement(self, p):
    return ('analog_write_call', p.ANALOG_WRITE, p.expr0, p.expr1)

  @_('PIN_MODE "(" expr "," PIN_TYPE ")"')
  def statement(self, p):
    return ('pin_mode_call', p.PIN_MODE, ('branch', p.expr, p.PIN_TYPE))

  @_('DELAY "(" expr ")"')
  def statement(self, p):
    return ('delay_call', p.DELAY, p.expr)

  @_('BOOL')
  def condition(self, p):
    return ('condition_bool', p.BOOL)

  @_('expr EQEQ expr')
  def condition(self, p):
    return ('condition_eqeq', p.expr0, p.expr1)

  @_('expr BIGGER_OR_EQUAL expr')
  def condition(self, p):
    return ('condition_bigger_equal', p.expr0, p.expr1)

  @_('expr SMALLER_OR_EQUAL expr')
  def condition(self, p):
    return ('condition_smaller_equal', p.expr0, p.expr1)

  @_('expr BIGGER expr')
  def condition(self, p):
    return ('condition_bigger', p.expr0, p.expr1)

  @_('expr SMALLER expr')
  def condition(self, p):
    return ('condition_smaller', p.expr0, p.expr1)

  @_('var_assign')
  def statement(self, p):
    return p.var_assign

  @_('TYPE_INT var_assign')
  def statement(self, p):
    return ('type_int_var_assign', p.TYPE_INT, p.var_assign)

  @_('TYPE_REAL var_assign')
  def statement(self, p):
    return ('type_float_var_assign', p.TYPE_REAL, p.var_assign)

  @_('TYPE_STRING var_assign')
  def statement(self, p):
    return ('type_string_var_assign', p.TYPE_STRING, p.var_assign)

  @_('NAME "=" INT')
  def var_assign(self, p):
    return ('var_assign', p.NAME, p.INT)

  @_('NAME "=" REAL')
  def var_assign(self, p):
    return ('var_assign', p.NAME, p.REAL)

  @_('NAME "=" STRING')
  def var_assign(self, p):
    return ('var_assign', p.NAME, p.STRING)

  @_('expr')
  def statement(self, p):
    return (p.expr)

  @_('expr "+" expr')
  def expr(self, p):
    return ('add', p.expr0, p.expr1)

  @_('expr "-" expr')
  def expr(self, p):
    return ('sub', p.expr0, p.expr1)

  @_('expr "*" expr')
  def expr(self, p):
    return ('mul', p.expr0, p.expr1)

  @_('expr "/" expr')
  def expr(self, p):
    return ('div', p.expr0, p.expr1)

  @_('PIN_TYPE')
  def expr(self, p):
    return ('pin_type', p.PIN_TYPE)

  @_('NAME')
  def expr(self, p):
    return ('var', p.NAME)

  @_('INT')
  def expr(self, p):
    return ('num', p.INT)

  @_('REAL')
  def expr(self, p):
    return ('num', float(p.REAL))


erro = ""


# Classe para capturar os erros léxicos e sintáticos do compilador
class LogErro():
  STDERR = ''

  def new_stderr(old):

    def new(*args):
      #print('Intercepted: ' + repr(args))
      global erro
      erro = 'Erro identificado: ' + repr(args)

    return new

  sys.stderr.write = new_stderr(sys.stderr.write)


# Apresentação inicial com instruções de uso do compilador
print("PROG MADE BY DUMMIES - 2023")
print("GITHUB: /thewillboy/compilador")
print("\n\n")
print("Para utilizar este compilador:")
print("1 - Crie um arquivo com seu código no mesmo diretório do compilador")
print("2 - Indique um arquivo como parâmetro na execução do compilador")
print(
  "3 - Selecione a opção default (qualquer tecla) do menu para testar o código no compilador"
)
print("\n\n")
wait = input("Pressione enter para continuar...")


# Leitura dos arquivos para análise
def identificaArquivo():
  arquivos = []
  for arquivo in os.listdir("."):
    if arquivo.endswith(".txt"):
      arquivos.append(arquivo)
  return arquivos


# Verifica se existem arquivos para análise
# ou se foram informados na chamada do programa
if sys.argv[1:]:
  arquivos = sys.argv[1:]
else:
  arquivos = identificaArquivo()

# Inicializando o programa
if __name__ == '__main__':
  lexer = BasicLexer()
  parser = BasicParser()
  LogErro()
  env = {}
  while True:
    opcao = input(
      '\n\nprog_made_by_dummies ([0] read_file/arg_file / [default] input_text) > '
    )
    if opcao == '0':
      x = 0
      for arquivo in arquivos:
        arq = open(arquivo, 'r')
        print("\n####### Analisando o arquivo:", arquivo)
        print("\n")
        wait = input("Pressione enter para continuar...\n")
        linhas = arq.readlines()
        for linha in linhas:
          x += 1
          text = linha.strip()
          print("L{}: {}".format(x, text))
          if text:
            try:
              tree = parser.parse(lexer.tokenize(text))
              if tree == None:
                print("L{}: Erro identificado".format(x))
                print(erro)
            except:
              pass
            for token in lexer.tokenize(text):
              print(token)
            if tree != None:
              print("Tree" + str(tree))
    else:
      try:
        text = input('prog_made_by_dummies > ')
      except EOFError:
        break
      if text:
        tree = parser.parse(lexer.tokenize(text.strip()))
        if tree == None:
          print(erro)
        else:
          for token in lexer.tokenize(text.strip()):
            print(token)
          print("Tree" + str(tree))
