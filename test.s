.data

.balign 4
value: .word 10000000

.text
.global asmLoop
asmLoop:
	PUSH {LR}
	PUSH {R4-R12}
	
innerLoop:
	// get the distance
//	LDR R0, address_of_value
//	LDR R0, [R0]
//	BL hsleep
//	BL getDistance
//	BL hi
	BL getDistance
	
	// compare the distance to 55 cm
	CMP R0, #130
	BGT innerLoop

	CMP R0, #35
	MOV R4, #0
	MOVGT R4, #1

	// do things if it is far
	BLGT far
	CMP R4, #1
	BEQ innerLoop

	// do things if it is close
	BL closer
	B innerLoop
	
	POP {R4-R12}   
	POP {PC} 	

far:
	CMP R5, #1
	MOV R5, #0

	// Turn on the motor
	BEQ wipe
	B innerLoop

wipe:
	MOV R0, #0
	MOV R1, #0
	BL writePin
	LDR R0, address_of_value
	LDR R0, [R0]
	BL hsleep
	MOV R0, #0
	MOV R1, #1
	BL writePin

	B innerLoop

closer:
	MOV R5, #1
	BX LR

address_of_value: .word value
