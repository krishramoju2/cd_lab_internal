# EXPERIMENT 3: SYMBOL TABLE
# Assigns addresses to identifiers and constants from an expression

print("=" * 50)
print("SYMBOL TABLE - WITH ADDRESS ASSIGNMENT")
print("=" * 50)

symbol_table = {}
address = 1000

expr = input("\nEnter expression (e.g., a+b*c): ")

print("\nToken\t\tType\t\tAddress")
print("-" * 45)

i = 0
while i < len(expr):
    ch = expr[i]
    
    # Identifier (letter)
    if ch.isalpha():
        token = ""
        while i < len(expr) and expr[i].isalpha():
            token += expr[i]
            i += 1
        
        if token not in symbol_table:
            symbol_table[token] = address
            address += 1
        print(f"{token}\t\tIdentifier\t{symbol_table[token]}")
    
    # Number (digit)
    elif ch.isdigit():
        token = ""
        while i < len(expr) and expr[i].isdigit():
            token += expr[i]
            i += 1
        
        if token not in symbol_table:
            symbol_table[token] = address
            address += 1
        print(f"{token}\t\tConstant\t{symbol_table[token]}")
    
    # Operator or parenthesis
    elif ch in '+-*/=()':
        print(f"{ch}\t\tOperator\t-")
        i += 1
    
    # Skip spaces
    elif ch == ' ':
        i += 1
    
    else:
        print(f"{ch}\t\tUnknown\t\t-")
        i += 1

print("\n" + "=" * 50)
print("FINAL SYMBOL TABLE")
print("=" * 50)
print("Symbol\t\tAddress")
print("-" * 25)
for sym, addr in symbol_table.items():
    print(f"{sym}\t\t{addr}")
print("=" * 50)
