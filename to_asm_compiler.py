print("TO ASM\n")

verificaArvore = ('type_int_var_assign', 'TYPE_INT', ('var_assign', 'A', 1))

verifyTree = """
('type_int_var_assign', 'TYPE_INT', ('var_assign', 'A', 1))
('type_int_var_assign', 'TYPE_INT', ('var_assign', 'B', 0))
('type_int_var_assign', 'TYPE_INT', ('var_assign', 'TEMPO', 1000))
('type_int_var_assign', 'TYPE_INT', ('var_assign', 'PIN_10', 10))
('open_while', 'WHILE', ('condition_bool', 'TRUE'))
"""

textData = """
RESULTADO DO COMPILADOR
L1: TYPE_INT A = 1
Tree('type_int_var_assign', 'TYPE_INT', ('var_assign', 'A', 1))
L2: TYPE_INT B = 0
Tree('type_int_var_assign', 'TYPE_INT', ('var_assign', 'B', 0))
L3: TYPE_INT TEMPO = 1000
Tree('type_int_var_assign', 'TYPE_INT', ('var_assign', 'TEMPO', 1000))
L4: TYPE_INT PIN_10 = 10
Tree('type_int_var_assign', 'TYPE_INT', ('var_assign', 'PIN_10', 10))
L5: PIN_MODE (PIN_10, OUTPUT)
Tree('pin_mode_call', 'PIN_MODE', ('branch', ('var', 'PIN_10'), 'OUTPUT'))
L6: WHILE (TRUE) {
Tree('open_while', 'WHILE', ('condition_bool', 'TRUE'))
L7: DIGITAL_WRITE (PINO_10, A)
Tree('dig_write_call', 'DIGITAL_WRITE', ('var', 'PINO_10'), ('var', 'A'))
L8: DELAY (TEMPO)
Tree('delay_call', 'DELAY', ('var', 'TEMPO'))
L9: DIGITAL_WRITE (PINO_10, B)
Tree('dig_write_call', 'DIGITAL_WRITE', ('var', 'PINO_10'), ('var', 'B'))
L10: DELAY (TEMPO)
Tree('delay_call', 'DELAY', ('var', 'TEMPO'))
L11: } END
Tree('close_statement', 'END')
"""

#https://ww1.microchip.com/downloads/en/devicedoc/atmel-2549-8-bit-avr-microcontroller-atmega640-1280-1281-2560-2561_datasheet.pdf
#http://www.rjhcoding.com/avr-asm-registers.php

atmega2560_registers = {
  'r0': 'available',
  'r1': 'available',
  'r2': 'available',
  'r3': 'available',
  'r4': 'available',
  'r5': 'available',
  'r6': 'available',
  'r7': 'available',
  'r8': 'available',
  'r9': 'available',
  'r10': 'available',
  'r11': 'available',
  'r13': 'available',
  'r14': 'available',
  'r15': 'available',
  'r16': 'available',
  'r17': 'available',
  'r18': 'available',
  'r19': 'available',
  'r20': 'available',
  'r21': 'available',
  'r22': 'available',
  'r23': 'available',
  'r24': 'available',
  'r25': 'available',
  'r26': 'available',
  'r27': 'available',
  'r28': 'available',
  'r29': 'available',
  'r30': 'available',
  'r31': 'available'
}


# Função "assembler" para atribuição de um número inteiro em um registrador
def type_int_var_assign(syntaxTree):
  #print("ATRIBUIÇÃO DE INTEIRO\n")
  #print("VARIÁVEL: ", syntaxTree[2][1])
  #print("VALOR: ", syntaxTree[2][2])
  if ((syntaxTree[2][2] > 255) and (syntaxTree[2][2] <= 65535)):
    binario = format(syntaxTree[2][2], '#018b')
    #print("VALOR BINÁRIO: ", binario)
    avl_reg_low = list(atmega2560_registers.keys())[list(
      atmega2560_registers.values()).index('available')]
    #print(avl_reg_low)
    atmega2560_registers[avl_reg_low] = syntaxTree[2][1] + "_low_reg"
    #print(atmega2560_registers[avl_reg_low])
    avl_reg_high = list(atmega2560_registers.keys())[list(
      atmega2560_registers.values()).index('available')]
    #print(avl_reg_high)
    atmega2560_registers[avl_reg_high] = syntaxTree[2][1] + "_high_reg"
    #print(atmega2560_registers[avl_reg_high])
    assembly = f"""ldi r16, low({binario})\nmov {avl_reg_low}, r16\nldi r16, high({binario})\nmov {avl_reg_high}, r16"""
    #print(assembly)
    return assembly
  else:
    binario = format(syntaxTree[2][2], '#010b')
    #print("VALOR BINÁRIO: ", binario)
    avl_reg = list(atmega2560_registers.keys())[list(
      atmega2560_registers.values()).index('available')]
    #print(avl_reg)
    atmega2560_registers[avl_reg] = syntaxTree[2][1] + "_reg"
    #print(atmega2560_registers[avl_reg])
    #assembly = "ldi r16, " + binario
    assembly = f"""ldi r16, {binario}\nmov {avl_reg}, r16"""
    return assembly


# Vefifica o tipo da árvore sintática lida e encaminha para a função "assembler" específica
def verifySyntaxTree(line):
  print("\nSYNTAX TREE:\n")
  print(line)
  if (line[0] == 'type_int_var_assign'):
    print("\n... IS A TYPE INT VAR ASSIGN\n")
    to_asm_setup = type_int_var_assign(line)
    print("ASSEMBLY CONVERSION:\n")
    print(to_asm_setup)
  elif (line[0] == 'open_while'):
    print("\n... IS A OPEN WHILE STATEMENT\n")
  else:
    print(line)
    print("SYNTAX TREE NOT RECOGNIZED!")


# Envia para validação linha por linha das árvores sintáticas geradas pelo compilador
for line in verifyTree.splitlines():
  if line != '':
    verifySyntaxTree(eval(line))
