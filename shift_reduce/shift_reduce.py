# SHIFT REDUCE PARSER - SIMPLIFIED
print("Enter grammar (E->E+E, type 'done' to finish):")
grammar = {}
while True:
    p = input("> ")
    if p == 'done': break
    if '->' in p:
        lhs, rhs = p.split('->')
        lhs = lhs.strip()
        if lhs not in grammar:
            grammar[lhs] = []
        grammar[lhs].append(rhs.strip())

print("\nGrammar:", grammar)

# Pre-tokenize grammar RHS
gram_tokens = {}
for lhs, rhs_list in grammar.items():
    gram_tokens[lhs] = []
    for rhs in rhs_list:
        # Simple tokenization for grammar
        tokens = []
        i = 0
        while i < len(rhs):
            if rhs[i].isalpha():
                j = i
                while j < len(rhs) and rhs[j].isalpha():
                    j += 1
                tokens.append(rhs[i:j])
                i = j
            else:
                tokens.append(rhs[i])
                i += 1
        gram_tokens[lhs].append(tokens)

while True:
    inp = input("\nEnter string (id+id, q to quit): ")
    if inp == 'q': break
    
    # Tokenize input
    tokens = []
    i = 0
    while i < len(inp):
        if inp[i].isalpha():
            j = i
            while j < len(inp) and inp[j].isalpha():
                j += 1
            tokens.append(inp[i:j])
            i = j
        else:
            tokens.append(inp[i])
            i += 1
    
    print("Tokens:", tokens)
    
    stack = []
    pos = 0
    n = len(tokens)
    
    print("\nStack          Input        Action")
    print("-" * 45)
    
    while True:
        # REDUCE
        reduced = False
        for lhs, rhs_list in gram_tokens.items():
            for rhs in rhs_list:
                if len(stack) >= len(rhs) and stack[-len(rhs):] == rhs:
                    for _ in range(len(rhs)):
                        stack.pop()
                    stack.append(lhs)
                    print(str(stack) + "          " + str(tokens[pos:]) + "          REDUCE " + lhs)
                    reduced = True
                    break
            if reduced:
                break
        
        if reduced:
            continue
        
        # ACCEPT
        if len(stack) == 1 and stack[0] in grammar and pos == n:
            print(str(stack) + "          " + str(tokens[pos:]) + "          ACCEPT")
            print("\n✅ ACCEPTED")
            break
        
        # SHIFT
        if pos < n:
            stack.append(tokens[pos])
            pos += 1
            print(str(stack) + "          " + str(tokens[pos:]) + "          SHIFT")
        else:
            print("\n❌ REJECTED")
            break
