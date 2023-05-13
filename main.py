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
'''
# Função para verificar os arquivos no diretório
# Verifica se existe ao menos 1 arquivo para
# ser analisado
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

for arquivo in arquivos:
  arq = open(arquivo, 'r')
  linhas = arq.readlines()
'''


class BasicLexer(Lexer):
  tokens = {
    NAME, TYPE_INT, TYPE_REAL, INT, REAL, STRING, IF, THEN, ELSE, END, FOR,
    DIGITAL_READ, DIGITAL_WRITE, ANALOG_READ, ANALOG_WRITE, PIN_MODE, PIN_TYPE,
    DO, WHILE, FUN, TO, ARROW, EQEQ, BOOL, BIGGER_OR_EQUAL, SMALLER_OR_EQUAL,
    BIGGER, SMALLER
  }
  ignore = '\t\b '
  #http://www.java2s.com/Code/Python/String/EscapeCodesbtnar.htm
  literals = {'=', '+', '-', '/', '*', '(', ')', '{', '}', ',', ';'}

  # Define tokens
  IF = r'IF'
  THEN = r'THEN'
  ELSE = r'ELSE'
  FOR = r'FOR'
  DIGITAL_READ = r'DIGITAL_READ'
  DIGITAL_WRITE = r'DIGITAL_WRITE'
  ANALOG_READ = r'ANALOG_READ'
  ANALOG_WRITE = r'ANALOG_WRITE'
  PIN_MODE = r'PIN_MODE'
  DO = r'DO'
  WHILE = r'WHILE'
  END = r'END'
  FUN = r'FUN'
  TO = r'TO'
  ARROW = r'->'
  TYPE_INT = r'TYPE_INT'
  TYPE_REAL = r'TYPE_REAL'
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
    #print(t.value)
    #print("inteiro")
    t.value = int(t.value)
    return t

  @_(r'\d+.\d+')
  def REAL(self, t):
    #print("real")
    t.value = float(t.value)
    return t

  @_(r'#.*')
  def COMMENT(self, t):
    pass

  @_(r'\n+')
  def newline(self, t):
    self.lineno = t.value.count('\n')

  def error(self, t):
    print("O caractere '%s' não é aceito nesta linguagem!" % t.value[0])
    self.index += 1


class BasicParser(Parser):
  tokens = BasicLexer.tokens

  precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
  )

  def __init__(self):
    self.env = {}

  @_('')
  def statement(self, p):
    pass

  @_('FOR var_assign TO expr THEN statement')
  def statement(self, p):
    return ('for_loop', ('for_loop_setup', p.var_assign, p.expr), p.statement)

  @_('IF condition THEN statement END')
  def statement(self, p):
    return ('if_stmt', p.condition, ('branch', p.statement))

  @_('IF condition THEN statement ELSE statement END')
  def statement(self, p):
    return ('if_stmt_else', p.condition, ('branch', p.statement0,
                                          p.statement1))

  @_('DO "{" statement "}" WHILE "(" condition ")" END')
  def statement(self, p):
    print(p.DO)
    print(p.statement)
    print(p.condition)
    wait = input("Press Enter to continue.")
    return ('do_while', p.DO, p.statement, ('branch', p.condition))

  @_('WHILE "(" condition ")" "{" statement "}" END')
  def statement(self, p):
    print(p.WHILE)
    print(p.condition)
    print(p.statement)
    wait = input("Press Enter to continue.")
    return ('while', p.WHILE, ('branch', p.condition, p.statement))

  @_('DIGITAL_READ "(" expr ")"')
  def statement(self, p):
    print(p.DIGITAL_READ)
    print(p.expr)
    wait = input("Press Enter to continue.")
    return ('dig_read_call', p.DIGITAL_READ, p.expr)

  @_('DIGITAL_WRITE "(" expr "," expr ")"')
  def statement(self, p):
    print(p.DIGITAL_WRITE)
    print(p.expr0)
    print(p.expr1)
    wait = input("Press Enter to continue.")
    return ('dig_write_call', p.DIGITAL_WRITE, p.expr0, p.expr1)

  @_('ANALOG_READ "(" expr ")"')
  def statement(self, p):
    print(p.ANALOG_READ)
    print(p.expr)
    wait = input("Press Enter to continue.")
    return ('analog_read_call', p.ANALOG_READ, p.expr)

  @_('ANALOG_WRITE "(" expr "," expr ")"')
  def statement(self, p):
    print(p.ANALOG_WRITE)
    print(p.expr0)
    print(p.expr1)
    wait = input("Press Enter to continue.")
    return ('analog_write_call', p.ANALOG_WRITE, p.expr0, p.expr1)

  @_('PIN_MODE "(" expr "," PIN_TYPE ")"')
  def statement(self, p):
    print(p.PIN_MODE)
    print(p.expr)
    print(p.PIN_TYPE)
    wait = input("Press Enter to continue.")
    return ('pin_mode_call', p.PIN_MODE, ('branch', p.expr, p.PIN_TYPE))

  @_('FUN NAME "(" ")" ARROW statement')
  def statement(self, p):
    return ('fun_def', p.NAME, p.statement)

  @_('NAME "(" ")"')
  def statement(self, p):
    return ('fun_call', p.NAME)

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
    return ('typeint_var_assign', p.var_assign)

  @_('TYPE_REAL var_assign')
  def var_assign(self, p):
    return ('type_float_var_assign', p.var_assign)

  @_('NAME "=" expr')
  def var_assign(self, p):
    return ('var_assign', p.NAME, p.expr)

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

  @_('"-" expr %prec UMINUS')
  def expr(self, p):
    return p.expr

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


class BasicExecute:

  def __init__(self, tree, env):
    self.env = env
    result = self.walkTree(tree)
    if result is not None and isinstance(result, int):
      print(float("{:.2f}".format(result)))
    if result is not None and isinstance(result, float):
      print(float("{:.2f}".format(result)))

    if isinstance(result, str) and result[0] == '"':
      print(result)

  def walkTree(self, node):

    if isinstance(node, int):
      return node
    if isinstance(node, float):
      return node
    if isinstance(node, str):
      return node

    if node is None:
      return None

    if node[0] == 'program':
      if node[1] == None:
        self.walkTree(node[2])
      else:
        self.walkTree(node[1])
        self.walkTree(node[2])

    if node[0] == 'num':
      return node[1]

    if node[0] == 'str':
      return node[1]

    if node[0] == 'if_stmt':
      result = self.walkTree(node[1])
      if result:
        return self.walkTree(node[2][1])
      return self.walkTree(node[2][2])

    if node[0] == 'condition_eqeq':
      return self.walkTree(node[1]) == self.walkTree(node[2])

    if node[0] == 'dig_read_call':
      print("foi")
      print(node[1])
      return self.walkTree(node[1])

    if node[0] == 'fun_def':
      self.env[node[1]] = node[2]

    if node[0] == 'fun_call':
      try:
        return self.walkTree(self.env[node[1]])
      except LookupError:
        print("Undefined function '%s'" % node[1])
        return 0

    if node[0] == 'add':
      return self.walkTree(node[1]) + self.walkTree(node[2])
    elif node[0] == 'sub':
      return self.walkTree(node[1]) - self.walkTree(node[2])
    elif node[0] == 'mul':
      return self.walkTree(node[1]) * self.walkTree(node[2])
    elif node[0] == 'div':
      return self.walkTree(node[1]) / self.walkTree(node[2])

    if node[0] == 'var_assign':
      self.env[node[1]] = self.walkTree(node[2])
      return node[1]

    if node[0] == 'var':
      try:
        return self.env[node[1]]
      except LookupError:
        print("Undefined variable '" + node[1] + "' found!")
        return 0

    if node[0] == 'for_loop':
      if node[1][0] == 'for_loop_setup':
        loop_setup = self.walkTree(node[1])

        loop_count = self.env[loop_setup[0]]
        loop_limit = loop_setup[1]

        for i in range(loop_count + 1, loop_limit + 1):
          res = self.walkTree(node[2])
          if res is not None:
            print(res)
          self.env[loop_setup[0]] = i
        del self.env[loop_setup[0]]

    if node[0] == 'for_loop_setup':
      return (self.walkTree(node[1]), self.walkTree(node[2]))


STDERR = ''


def new_stderr(old):

  def new(*args):
    # put your code here, you will intercept writes to stderr
    print('Intercepted: ' + repr(args))
    #global STDERR  # add new write to STDERR
    #STDERR += args[0]
    #old(*args)

  return new


sys.stderr.write = new_stderr(sys.stderr.write)

if __name__ == '__main__':
  lexer = BasicLexer()
  parser = BasicParser()
  env = {}
  while True:
    try:
      text = input('prog_made_by_dummies > ')
    except EOFError:
      break
    if text:
      try:
        #old_stderr = sys.stderr
        #sys.stderr = open(os.devnull, "w")
        #sys.stdout = open("file", "a")
        #tree = parser.parse(lexer.tokenize(text))
        #save_stdout = sys.stdout
        #sys.stdout = open('trash', 'w')
        tree = parser.parse(lexer.tokenize(text))
        #sys.stdout = save_stdout
      except:
        pass
      for token in lexer.tokenize(text):
       print(token)
      print(tree)
      #BasicExecute(tree, env)
