# SHIFT REDUCE PARSER - CORRECTED VERSION
print("Enter grammar productions (E->E+E or E->id, type 'done' to finish):")
grammar = {}
while True:
    prod = input("Production: ")
    if prod.lower() == 'done': 
        break
    if '->' in prod:
        lhs, rhs = prod.split('->')
        lhs = lhs.strip()
        if lhs not in grammar:
            grammar[lhs] = []
        grammar[lhs].append(rhs.strip())

print("\nGrammar:", grammar)

def tokenize(s):
    tokens = []
    i = 0
    while i < len(s):
        if s[i].isalpha():
            j = i
            while j < len(s) and s[j].isalpha():
                j += 1
            tokens.append(s[i:j])
            i = j
        else:
            tokens.append(s[i])
            i += 1
    return tokens

while True:
    inp = input("\nEnter string (id+id, q to quit): ")
    if inp == 'q': 
        break
    
    tokens = tokenize(inp)
    print("Tokens:", tokens)
    
    stack = []
    ptr = 0
    input_len = len(tokens)
    
    print("\nStack          Input        Action")
    print("-" * 45)
    
    while True:
        # Try to reduce first (before shifting)
        reduced = False
        for lhs, rhs_list in grammar.items():
            for rhs in rhs_list:
                rhs_tokens = tokenize(rhs)
                if len(stack) >= len(rhs_tokens) and stack[-len(rhs_tokens):] == rhs_tokens:
                    for _ in range(len(rhs_tokens)):
                        stack.pop()
                    stack.append(lhs)
                    print(str(stack) + "          " + str(tokens[ptr:]) + "          REDUCE " + lhs + "->" + rhs)
                    reduced = True
                    break
            if reduced:
                break
        
        if reduced:
            continue
        
        # Check for accept
        if len(stack) == 1 and stack[0] in grammar and ptr == input_len:
            print(str(stack) + "          " + str(tokens[ptr:]) + "          ACCEPT")
            print("\n ACCEPTED")
            break
        
        # Shift
        if ptr < input_len:
            stack.append(tokens[ptr])
            ptr += 1
            print(str(stack) + "          " + str(tokens[ptr:]) + "          SHIFT")
        else:
            print("\n REJECTED")
            break
