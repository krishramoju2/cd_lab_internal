# ============================================
# EXPERIMENT 5: TARGET CODE GENERATION
# Three Address Code → Assembly Language
# WITH DIFFERENT REGISTERS EACH TIME
# ============================================

print("=" * 60)
print("TARGET CODE GENERATION")
print("Three Address Code → Assembly Language")
print("=" * 60)

# ============================================
# TARGET CODE GENERATION FUNCTION
# ============================================
def generate_target_code(tac_lines):
    """Convert TAC to Assembly language using different registers"""
    assembly = []
    reg_count = 0
    registers = ['R0', 'R1', 'R2', 'R3']
    
    for line in tac_lines:
        parts = line.split()
        # Format: t1 = a + b  →  ['t1', '=', 'a', '+', 'b']
        
        if len(parts) == 5:
            result = parts[0]
            operand1 = parts[2]
            operator = parts[3]
            operand2 = parts[4]
            
            # Use a new register for each operation
            reg = registers[reg_count % len(registers)]
            reg_count += 1
            
            # LOAD first operand
            if operand1.isdigit():
                assembly.append(f"MOV  #{operand1}, {reg}")
            else:
                assembly.append(f"LOAD {operand1}, {reg}")
            
            # Perform operation
            if operator == '+':
                if operand2.isdigit():
                    assembly.append(f"ADD  #{operand2}, {reg}")
                else:
                    assembly.append(f"ADD  {operand2}, {reg}")
            elif operator == '-':
                if operand2.isdigit():
                    assembly.append(f"SUB  #{operand2}, {reg}")
                else:
                    assembly.append(f"SUB  {operand2}, {reg}")
            elif operator == '*':
                if operand2.isdigit():
                    assembly.append(f"MUL  #{operand2}, {reg}")
                else:
                    assembly.append(f"MUL  {operand2}, {reg}")
            elif operator == '/':
                if operand2.isdigit():
                    assembly.append(f"DIV  #{operand2}, {reg}")
                else:
                    assembly.append(f"DIV  {operand2}, {reg}")
            
            # STORE result
            assembly.append(f"STORE {reg}, {result}")
            assembly.append("")  # Empty line
        
        elif len(parts) == 3:  # Copy statement: a = b
            reg = registers[reg_count % len(registers)]
            reg_count += 1
            assembly.append(f"LOAD {parts[2]}, {reg}")
            assembly.append(f"STORE {reg}, {parts[0]}")
            assembly.append("")
    
    return assembly

# ============================================
# MAIN PROGRAM - ENTER TAC MANUALLY
# ============================================
while True:
    print("\n" + "-" * 40)
    n = int(input("Enter number of TAC lines (0 to exit): "))
    
    if n == 0:
        break
    
    print("Enter TAC (e.g., t1 = a + b):")
    tac_lines = []
    for i in range(n):
        line = input(f"{i+1}: ")
        tac_lines.append(line)
    
    # Generate assembly code
    assembly = generate_target_code(tac_lines)
    
    # Display input TAC
    print("\n" + "=" * 50)
    print("INPUT: THREE ADDRESS CODE (TAC)")
    print("=" * 50)
    for line in tac_lines:
        print(f"  {line}")
    
    # Display output assembly
    print("\n" + "=" * 50)
    print("OUTPUT: TARGET CODE (ASSEMBLY)")
    print("=" * 50)
    for line in assembly:
        if line:
            print(f"  {line}")
        else:
            print()
    print("=" * 50)

print("\n" + "=" * 60)
print("TARGET CODE GENERATION COMPLETE")
print("=" * 60)
