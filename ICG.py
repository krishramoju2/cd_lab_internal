# ============================================
# EXPERIMENT 4: INTERMEDIATE CODE GENERATION
# Three Address Code (TAC) + Quadruples + Triples
# ============================================

print("=" * 60)
print("INTERMEDIATE CODE GENERATION")
print("Infix Expression → TAC → Quadruples → Triples")
print("=" * 60)

# ============================================
# STEP 1: OPERATOR PRECEDENCE
# ============================================
def precedence(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0

# ============================================
# STEP 2: INFIX TO POSTFIX CONVERSION
# ============================================
def infix_to_postfix(expression):
    """Convert infix expression to postfix using Shunting Yard algorithm"""
    stack = []
    output = []
    
    for ch in expression:
        # Operand (variable or number)
        if ch.isalnum():
            output.append(ch)
        
        # Left parenthesis
        elif ch == '(':
            stack.append(ch)
        
        # Right parenthesis
        elif ch == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # Remove '('
        
        # Operator
        else:
            while (stack and stack[-1] != '(' and 
                   precedence(stack[-1]) >= precedence(ch)):
                output.append(stack.pop())
            stack.append(ch)
    
    # Pop remaining operators
    while stack:
        output.append(stack.pop())
    
    return output

# ============================================
# STEP 3: GENERATE THREE ADDRESS CODE (TAC)
# ============================================
def generate_tac(postfix):
    """Generate Three Address Code from postfix expression"""
    stack = []
    temp_count = 1
    tac_instructions = []
    
    for token in postfix:
        if token.isalnum():
            stack.append(token)
        else:
            # Operator: pop two operands
            right = stack.pop()
            left = stack.pop()
            temp_var = f"t{temp_count}"
            temp_count += 1
            
            instruction = f"{temp_var} = {left} {token} {right}"
            tac_instructions.append(instruction)
            stack.append(temp_var)
    
    return tac_instructions

# ============================================
# STEP 4: GENERATE QUADRUPLES
# ============================================
def generate_quadruples(tac_instructions):
    """Convert TAC to quadruples (op, arg1, arg2, result)"""
    quadruples = []
    for instr in tac_instructions:
        parts = instr.split()
        # parts = [result, '=', arg1, op, arg2]
        quadruple = (parts[3], parts[2], parts[4], parts[0])
        quadruples.append(quadruple)
    return quadruples

# ============================================
# STEP 5: GENERATE TRIPLES
# ============================================
def generate_triples(tac_instructions):
    """Convert TAC to triples (op, arg1, arg2)"""
    triples = []
    for instr in tac_instructions:
        parts = instr.split()
        triple = (parts[3], parts[2], parts[4])
        triples.append(triple)
    return triples

# ============================================
# MAIN PROGRAM - RUN MULTIPLE EXPRESSIONS
# ============================================
while True:
    print("\n" + "-" * 40)
    expr = input("Enter expression (a+b*c, q to quit): ")
    
    if expr.lower() == 'q':
        break
    
    print(f"\n📌 INPUT: {expr}")
    
    # Step 1: Convert to Postfix
    postfix = infix_to_postfix(expr)
    postfix_str = ''.join(postfix)
    print(f"\n📌 POSTFIX: {postfix_str}")
    
    # Step 2: Generate TAC
    tac = generate_tac(postfix)
    print(f"\n📌 THREE ADDRESS CODE (TAC):")
    for line in tac:
        print(f"     {line}")
    
    # Step 3: Generate Quadruples
    quadruples = generate_quadruples(tac)
    print(f"\n📌 QUADRUPLES (op, arg1, arg2, result):")
    for i, quad in enumerate(quadruples, 1):
        print(f"     {i}: {quad}")
    
    # Step 4: Generate Triples
    triples = generate_triples(tac)
    print(f"\n📌 TRIPLES (op, arg1, arg2):")
    for i, trip in enumerate(triples):
        print(f"     {i}: {trip}")

print("\n" + "=" * 60)
print("INTERMEDIATE CODE GENERATION COMPLETE")
print("=" * 60)
