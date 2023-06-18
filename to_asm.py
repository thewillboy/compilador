import re

print("CONVERSION TO ASM:\n")


# Árvore sintática a ser analisada
verifyTree = """
('type_int_var_assign', 'TYPE_INT', ('var_assign', 'A', 1))
('type_int_var_assign', 'TYPE_INT', ('var_assign', 'B', 0))
('type_int_var_assign', 'TYPE_INT', ('var_assign', 'TEMPO', 1000))
('type_int_var_assign', 'TYPE_INT', ('var_assign', 'PIN_10', 10))
('pin_mode_call', 'PIN_MODE', ('branch', ('var', 'PIN_10'), 'OUTPUT'))
('open_while', 'WHILE', ('condition_bool', 'TRUE'))
('dig_write_call', 'DIGITAL_WRITE', ('var', 'PIN_10'), ('var', 'A'))
('delay_call', 'DELAY', ('var', 'TEMPO'))
('dig_write_call', 'DIGITAL_WRITE', ('var', 'PIN_10'), ('var', 'B'))
('delay_call', 'DELAY', ('var', 'TEMPO'))
('close_while', 'END')
"""


# Registradores disponíveis no ATmega2560
atmega2560_registers = {
  'R0': 'available',
  'R1': 'available',
  'R2': 'available',
  'R3': 'available',
  'R4': 'available',
  'R5': 'available',
  'R6': 'available',
  'R7': 'available',
  'R8': 'available',
  'R9': 'available',
  'R10': 'available',
  'R11': 'available',
  'R13': 'available',
  'R14': 'available',
  'R15': 'available',
  'R16': 'available',
  'R17': 'available',
  'R18': 'available',
  'R19': 'available',
  'R20': 'available',
  'R21': 'available',
  'R22': 'available',
  'R23': 'available',
  'R24': 'available',
  'R25': 'available',
  'R26': 'available',
  'R27': 'available',
  'R28': 'available',
  'R29': 'available',
  'R30': 'available',
  'R31': 'available'
}


# Registradores I/O (entrada ou saída) disponíveis no ATmega2560
atmega2560_digital_pins = {
  '10': ['PB4', '4', '0b00010000'],
  '11': ['PB5', '5', '0b00100000'],
  '12': ['PB6', '6', '0b01000000'],
  '13': ['PB7', '7', '0b10000000']
}


# Função "assembler" para atribuição de um número inteiro em um registrador
def type_int_var_assign(syntaxTree):
  if ((syntaxTree[2][2] > 255) and (syntaxTree[2][2] <= 65535)):
    binario = format(syntaxTree[2][2], '#018b')
    avl_reg_low = list(atmega2560_registers.keys())[list(
      atmega2560_registers.values()).index('available')]
    atmega2560_registers[avl_reg_low] = "low_reg_" + syntaxTree[2][
      1] + "_value_" + str(syntaxTree[2][2])
    avl_reg_high = list(atmega2560_registers.keys())[list(
      atmega2560_registers.values()).index('available')]
    atmega2560_registers[avl_reg_high] = "high_reg_" + syntaxTree[2][
      1] + "_value_" + str(syntaxTree[2][2])
    assembly = f"""\tLDI R16, LOW({binario})\n\tMOV {avl_reg_low}, R16\n\tLDI R16, HIGH({binario})\n\tMOV {avl_reg_high}, R16"""
  else:
    binario = format(syntaxTree[2][2], '#010b')
    avl_reg = list(atmega2560_registers.keys())[list(
      atmega2560_registers.values()).index('available')]
    atmega2560_registers[
      avl_reg] = "reg_" + syntaxTree[2][1] + "_value_" + str(syntaxTree[2][2])
    assembly = f"""\tLDI R16, {binario}\n\tMOV {avl_reg}, R16"""
  return assembly


# Função "assembler" para a alteração do comportamento de uma porta digital I/O (entrada ou saída)
def pin_mode_call(syntaxTree):
  for key, value in atmega2560_registers.items():
    if re.search(syntaxTree[2][1][1], value):
      pin = value.split("_value_")[1]
  if atmega2560_digital_pins[pin]:
    if syntaxTree[2][2] == 'INPUT':
      assembly = f"""\tLDI R16, {atmega2560_digital_pins[pin][2]}\n\tIN DDRB, R16"""
    else:
      assembly = f"""\tLDI R16, {atmega2560_digital_pins[pin][2]}\n\tOUT DDRB, R16"""
  else:
    print("PIN CONFIGURATION NOT IMPLEMENTED!")
  return assembly


# Função "assembler" para o início da declaração de um laço while
def open_while(syntaxTree):
  if syntaxTree[2][1] == 'TRUE':
    assembly = f"""\nWHILE:\n"""
  else:
    print("WHILE CONDITION NOT IMPLEMENTED!")
    assembly = f"""WHILE:"""
  return assembly


# Função "assembler" para o fim da declaração de um laço while
def close_while(syntaxTree):
  assembly = f"""\tRJMP WHILE"""
  return assembly


# Função "assembler" para a alteração de valor de uma porta digital
def dig_write_call(syntaxTree):
  #print(syntaxTree[2][1])
  #print(syntaxTree[3][1])
  for key, value in atmega2560_registers.items():
    if re.search(syntaxTree[2][1], value):
      pin = value.split("_value_")[1]
  for key, value in atmega2560_registers.items():
    if re.search(syntaxTree[3][1], value):
      val = value.split("_value_")[1]
  if ((val == '0') or (val == 'FALSE')):
    assembly = f"""\tCBI PORTB, {atmega2560_digital_pins[pin][1]}"""
  else:
    assembly = f"""\tSBI PORTB, {atmega2560_digital_pins[pin][1]}"""
  return assembly


# Função "assembler" para a chamada da função de delay
def delay_call(syntaxTree):
  for key, value in atmega2560_registers.items():
    if re.search(syntaxTree[2][1], value):
      val = value.split("_value_")[1]
  if (int(val) > 255):
    for key, value in atmega2560_registers.items():
      if re.search("high_reg_" + syntaxTree[2][1], value):
        reg_high = key
    for key, value in atmega2560_registers.items():
      if re.search("low_reg_" + syntaxTree[2][1], value):
        reg_low = key
    assembly = f"""\tMOV R16, {reg_low}\n\tMOV R18, {reg_high}\n\tRCALL DELAY_255_PLUS"""
  else:
    assembly = f"""\tLDI R16, {val}\n\tRCALL DELAY"""
  return assembly


# String para armazenar o resultado da conversão do código para assembly
body = ''


# Vefifica o tipo da árvore sintática lida e encaminha para a função "assembler" específica
def verifySyntaxTree(line):
  print("\nSYNTAX TREE:\n")
  print(line)
  if (line[0] == 'type_int_var_assign'):
    print("\n... IS A TYPE INT VAR ASSIGN\n")
    to_asm_setup = type_int_var_assign(line)
    print("ASSEMBLY CONVERSION:\n")
    print(to_asm_setup)
  elif (line[0] == 'pin_mode_call'):
    print("\n... IS A PIN MODE STATEMENT\n")
    to_asm_setup = pin_mode_call(line)
    print("ASSEMBLY CONVERSION:\n")
    print(to_asm_setup)
  elif (line[0] == 'open_while'):
    print("\n... IS A OPEN WHILE STATEMENT\n")
    to_asm_setup = open_while(line)
    print("ASSEMBLY CONVERSION:\n")
    print(to_asm_setup)
  elif (line[0] == 'dig_write_call'):
    print("\n... IS A DIGITAL WRITE STATEMENT\n")
    to_asm_setup = dig_write_call(line)
    print("ASSEMBLY CONVERSION:\n")
    print(to_asm_setup)
  elif (line[0] == 'delay_call'):
    print("\n... IS A DELAY CALL STATEMENT\n")
    to_asm_setup = delay_call(line)
    print("ASSEMBLY CONVERSION:\n")
    print(to_asm_setup)
  elif (line[0] == 'close_while'):
    print("\n... IS A CLOSE WHILE STATEMENT\n")
    to_asm_setup = close_while(line)
    print("ASSEMBLY CONVERSION:\n")
    print(to_asm_setup)
  else:
    print(line)
    print("SYNTAX TREE NOT RECOGNIZED!")
  return to_asm_setup


# Envia para validação linha por linha das árvores sintáticas geradas pelo compilador
for line in verifyTree.splitlines():
  if line != '':
    ret = verifySyntaxTree(eval(line))
    body = body + "\n" + ret

print("\n\n\nCONVERSION RESULT:")

header = f"""
.INCLUDE <M2560DEF.INC>

.ORG 0

; Stack pointer ser igual a RAMEND
; SP = RAMEND = Ox08FF

	LDI R16, 0X08 ; HIGH(RAMEND)
	OUT SPH, R16
	LDI R16, 0XFF ; LOW(RAMEND)
	OUT SPL, R16

SETUP:
"""

footer = f"""
DELAY:
	CPI R16,0
	BREQ FIM

	;NOP
	
	; Chamar outro delay (laço dentro do laço para criar tempo)
	; Loop
	LDI R17, 250 ; Quantidade de execuções do loop de delay
	RCALL DELAY2

	DEC R16
	RJMP DELAY
FIM:
	RET
 
DELAY_255_PLUS:
	CPI R16,0
	BREQ FIM_DELAY_255_PLUS

	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP

	; Chamar outro delay (laço dentro do laço para criar tempo)
	; Loop
	LDI R17, 255 ; Quantidade de execuções do loop de delay
	RCALL DELAY2

	CPI R18,0
	DEC R16
	CPI R18,0
	RJMP DELAY_255_PLUS
	DEC R18
	RJMP DELAY_255_PLUS
FIM_DELAY_255_PLUS:
	RET

DELAY2:
	CPI R17,0
	BREQ FIM2

	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP
	NOP

	DEC R17
	RJMP DELAY2
FIM2:
	RET
"""

print(header + "\n" + body + "\n" + footer)
