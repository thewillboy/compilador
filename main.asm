.INCLUDE <M2560DEF.INC>

.ORG 0

; Stack pointer ser igual a RAMEND
; SP = RAMEND = Ox08FF

    LDI R16, 0X08 ; HIGH(RAMEND)
    OUT SPH, R16
    LDI R16, 0XFF ; LOW(RAMEND)
    OUT SPL, R16

SETUP:


    LDI R16, 0b00000001
    MOV R0, R16
    LDI R16, 0b00000000
    MOV R1, R16
    LDI R16, LOW(0b0000001111101000)
    MOV R2, R16
    LDI R16, HIGH(0b0000001111101000)
    MOV R3, R16
    LDI R16, 0b00001010
    MOV R4, R16
    LDI R16, 0b00010000
    OUT DDRB, R16

WHILE:

    SBI PORTB, 4
    MOV R16, R2
    MOV R18, R3
    RCALL DELAY_255_PLUS
    CBI PORTB, 4
    MOV R16, R2
    MOV R18, R3
    RCALL DELAY_255_PLUS
    RJMP WHILE

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