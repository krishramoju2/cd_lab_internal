# CANONICAL COLLECTION OF LR(0) ITEMS & SLR PARSING TABLE
# PYTHON 3 - WITH PROPER STATE ORDERING

print("=" * 60)
print("CANONICAL COLLECTION OF LR(0) ITEMS & SLR PARSING TABLE")
print("=" * 60)

# ============================================
# STEP 1: INPUT GRAMMAR FROM USER
# ============================================
print("\nEnter grammar productions (e.g., E->E+T, type 'done' to finish):")
productions = []
non_terminals = set()
terminals = set()

while True:
    prod = input("Production: ")
    if prod.lower() == 'done':
        break
    if '->' in prod:
        productions.append(prod)
        lhs = prod.split('->')[0].strip()
        non_terminals.add(lhs)

# Find terminals
for prod in productions:
    rhs = prod.split('->')[1].strip()
    for ch in rhs:
        if ch not in non_terminals and ch != 'ε' and ch != '|':
            terminals.add(ch)

terminals.add('$')

# Augment grammar - USE THE FIRST PRODUCTION'S LHS as START
start_symbol = productions[0].split('->')[0].strip()
productions.insert(0, start_symbol + "'->" + start_symbol)
non_terminals.add(start_symbol + "'")

print("\nGrammar:")
for i, p in enumerate(productions):
    print(f"{i}: {p}")

print(f"\nTerminals: {sorted(terminals)}")
print(f"Non-terminals: {sorted(non_terminals)}")
print(f"Start symbol: {start_symbol}")

# ============================================
# STEP 2: COMPUTE FIRST SETS
# ============================================
first = {}
for nt in non_terminals:
    first[nt] = set()
for t in terminals:
    first[t] = {t}

changed = True
while changed:
    changed = False
    for prod in productions:
        lhs, rhs = prod.split('->')
        lhs = lhs.strip()
        rhs = rhs.strip()
        
        if rhs == 'ε' or rhs == '':
            if 'ε' not in first[lhs]:
                first[lhs].add('ε')
                changed = True
        else:
            for sym in rhs:
                old_size = len(first[lhs])
                for fs in first[sym]:
                    if fs != 'ε':
                        first[lhs].add(fs)
                if len(first[lhs]) != old_size:
                    changed = True
                if 'ε' not in first[sym]:
                    break
            else:
                if 'ε' not in first[lhs]:
                    first[lhs].add('ε')
                    changed = True

# ============================================
# STEP 3: COMPUTE FOLLOW SETS
# ============================================
follow = {}
for nt in non_terminals:
    follow[nt] = set()
follow[productions[0].split('->')[0].strip()].add('$')

changed = True
while changed:
    changed = False
    for prod in productions:
        lhs, rhs = prod.split('->')
        lhs = lhs.strip()
        rhs = rhs.strip()
        if rhs == 'ε' or rhs == '':
            continue
        
        for i in range(len(rhs)):
            sym = rhs[i]
            if sym in non_terminals:
                beta = rhs[i+1:]
                first_beta = set()
                nullable = True
                
                for b in beta:
                    if 'ε' in first[b]:
                        for fs in first[b]:
                            if fs != 'ε':
                                first_beta.add(fs)
                    else:
                        for fs in first[b]:
                            first_beta.add(fs)
                        nullable = False
                        break
                
                if nullable:
                    first_beta.add('ε')
                
                old_size = len(follow[sym])
                for fs in first_beta:
                    if fs != 'ε':
                        follow[sym].add(fs)
                if len(follow[sym]) != old_size:
                    changed = True
                
                if 'ε' in first_beta or len(beta) == 0:
                    old_size = len(follow[sym])
                    for fl in follow[lhs]:
                        follow[sym].add(fl)
                    if len(follow[sym]) != old_size:
                        changed = True

# ============================================
# STEP 4: LR(0) ITEM FUNCTIONS
# ============================================
def closure(items):
    res = list(items)
    changed = True
    while changed:
        changed = False
        for item in res[:]:
            lhs, rhs = item.split('->')
            dot_pos = rhs.find('.')
            if dot_pos + 1 < len(rhs):
                sym = rhs[dot_pos + 1]
                if sym in non_terminals:
                    for prod in productions:
                        if prod.startswith(sym + '->'):
                            prod_rhs = prod.split('->')[1]
                            new_item = sym + '->.' + prod_rhs
                            if new_item not in res:
                                res.append(new_item)
                                changed = True
    return sorted(res)  # Sort for consistent ordering

def goto(items, X):
    move = []
    for item in items:
        lhs, rhs = item.split('->')
        dot_pos = rhs.find('.')
        if dot_pos + 1 < len(rhs) and rhs[dot_pos + 1] == X:
            new_rhs = rhs[:dot_pos] + X + '.' + rhs[dot_pos + 2:]
            move.append(lhs + '->' + new_rhs)
    return closure(move)

def items_equal(i1, i2):
    return set(i1) == set(i2)

# ============================================
# STEP 5: BUILD CANONICAL COLLECTION
# ============================================
print("\n" + "=" * 60)
print("CANONICAL COLLECTION OF LR(0) ITEMS")
print("=" * 60)

start_prod = productions[0]
start_lhs, start_rhs = start_prod.split('->')
I0 = closure([start_lhs + '->.' + start_rhs])

states = [I0]

changed = True
while changed:
    changed = False
    all_symbols = sorted(terminals) + sorted(non_terminals)
    
    for i in range(len(states)):
        for sym in all_symbols:
            g = goto(states[i], sym)
            if g:
                exists = False
                for s in states:
                    if items_equal(s, g):
                        exists = True
                        break
                if not exists:
                    states.append(g)
                    changed = True

# Display states with proper ordering
for i, state in enumerate(states):
    print(f"\nI{i}:")
    for item in state:
        print(f"   {item}")

# ============================================
# STEP 6: BUILD SLR PARSING TABLE
# ============================================
print("\n" + "=" * 60)
print("SLR PARSING TABLE")
print("=" * 60)

# Initialize tables
action = [{} for _ in range(len(states))]
goto_table = [{} for _ in range(len(states))]

# Build tables
for i, state in enumerate(states):
    for item in state:
        lhs, rhs = item.split('->')
        dot_pos = rhs.find('.')
        
        # SHIFT
        if dot_pos + 1 < len(rhs):
            next_sym = rhs[dot_pos + 1]
            if next_sym in terminals:
                g = goto(state, next_sym)
                for j, s in enumerate(states):
                    if items_equal(s, g):
                        action[i][next_sym] = f"S{j}"
                        break
        
        # REDUCE
        elif dot_pos == len(rhs) - 1:
            prod_rhs = rhs.replace('.', '')
            prod_num = -1
            for idx, prod in enumerate(productions):
                p_lhs, p_rhs = prod.split('->')
                if p_lhs == lhs and p_rhs == prod_rhs:
                    prod_num = idx
                    break
            
            if lhs == productions[0].split('->')[0] and prod_rhs == productions[0].split('->')[1]:
                action[i]['$'] = "ACC"
            else:
                for t in follow[lhs]:
                    if t in terminals:
                        action[i][t] = f"R{prod_num}"
    
    # GOTO
    for nt in non_terminals:
        g = goto(state, nt)
        if g:
            for j, s in enumerate(states):
                if items_equal(s, g):
                    goto_table[i][nt] = j
                    break

# ============================================
# VERY BASIC DISPLAY
# ============================================
term_list = sorted(terminals)
nonterm_list = sorted([nt for nt in non_terminals if nt != productions[0].split('->')[0]])

print("\nACTION TABLE:")
for i in range(len(states)):
    print(f"I{i}: ", end="")
    for t in term_list:
        val = action[i].get(t, "-")
        print(f"{t}={val} ", end="")
    print()

print("\nGOTO TABLE:")
for i in range(len(states)):
    print(f"I{i}: ", end="")
    for nt in nonterm_list:
        val = goto_table[i].get(nt, "-")
        print(f"{nt}={val} ", end="")
    print()

print("\nPRODUCTIONS:")
for idx, prod in enumerate(productions):
    print(f"{idx}: {prod}")

print("\nFOLLOW SETS:")
for nt in sorted(non_terminals):
    print(f"FOLLOW({nt}) = {follow[nt]}")

print("\nLEGEND: Sx=Shift, Rx=Reduce, ACC=Accept, -=blank")
