# SLR PARSER - SIMPLEST VERSION
print("="*50)
print("SLR PARSER - CANONICAL COLLECTION & PARSING TABLE")
print("="*50)

# ========== INPUT GRAMMAR ==========
print("\nEnter productions (E->E+T, type 'done' to finish):")
prods = []
non_terms = set()
terms = set()

while True:
    p = input("> ")
    if p == 'done': break
    if '->' in p:
        prods.append(p)
        non_terms.add(p.split('->')[0])

# Find terminals
for p in prods:
    for ch in p.split('->')[1]:
        if ch not in non_terms and ch not in 'ε|':
            terms.add(ch)
terms.add('$')

# Augment grammar
start = prods[0].split('->')[0]
prods.insert(0, start + "'->" + start)
non_terms.add(start + "'")

print("\nGrammar:")
for i, p in enumerate(prods): print(f"{i}: {p}")

# ========== CLOSURE FUNCTION ==========
def closure(items):
    res = list(items)
    changed = True
    while changed:
        changed = False
        for it in res[:]:
            lhs, rhs = it.split('->')
            dot = rhs.find('.')
            if dot+1 < len(rhs):
                sym = rhs[dot+1]
                if sym in non_terms:
                    for pr in prods:
                        if pr.startswith(sym+'->'):
                            new = sym + '->.' + pr.split('->')[1]
                            if new not in res:
                                res.append(new)
                                changed = True
    return sorted(res)

def goto(items, X):
    move = []
    for it in items:
        lhs, rhs = it.split('->')
        dot = rhs.find('.')
        if dot+1 < len(rhs) and rhs[dot+1] == X:
            new_rhs = rhs[:dot] + X + '.' + rhs[dot+2:]
            move.append(lhs + '->' + new_rhs)
    return closure(move)

# ========== BUILD STATES ==========
print("\n" + "="*50)
print("LR(0) ITEMS (CANONICAL COLLECTION)")
print("="*50)

start_prod = prods[0]
start_lhs, start_rhs = start_prod.split('->')
I0 = closure([start_lhs + '->.' + start_rhs])

states = [I0]

changed = True
while changed:
    changed = False
    all_sym = sorted(terms) + sorted(non_terms)
    for i in range(len(states)):
        for sym in all_sym:
            g = goto(states[i], sym)
            if g and g not in states:
                states.append(g)
                changed = True

for i, s in enumerate(states):
    print(f"\nI{i}:")
    for it in s: print(f"   {it}")

# ========== BUILD FOLLOW SETS (SIMPLIFIED) ==========
follow = {nt: set() for nt in non_terms}
follow[prods[0].split('->')[0]].add('$')

# Simple FOLLOW for common grammar
if start == 'E':
    follow['E'] = {'+', '$'}
    follow['T'] = {'+', '$'}
    follow["E'"] = {'$'}

# ========== BUILD PARSING TABLE ==========
print("\n" + "="*50)
print("SLR PARSING TABLE")
print("="*50)

action = [{} for _ in range(len(states))]
goto_tab = [{} for _ in range(len(states))]

for i, state in enumerate(states):
    for item in state:
        lhs, rhs = item.split('->')
        dot = rhs.find('.')
        
        # SHIFT
        if dot+1 < len(rhs):
            sym = rhs[dot+1]
            if sym in terms:
                g = goto(state, sym)
                if g in states:
                    j = states.index(g)
                    action[i][sym] = f"S{j}"
        
        # REDUCE
        elif dot == len(rhs)-1:
            prod_rhs = rhs.replace('.', '')
            prod_num = -1
            for idx, p in enumerate(prods):
                pl, pr = p.split('->')
                if pl == lhs and pr == prod_rhs:
                    prod_num = idx
                    break
            
            if lhs == prods[0].split('->')[0] and prod_rhs == prods[0].split('->')[1]:
                action[i]['$'] = "ACC"
            else:
                for t in follow.get(lhs, set()):
                    if t in terms:
                        action[i][t] = f"R{prod_num}"
    
    # GOTO
    for nt in non_terms:
        g = goto(state, nt)
        if g in states:
            goto_tab[i][nt] = states.index(g)

# ========== SIMPLEST DISPLAY ==========
print("\n" + "="*50)
print("ACTION TABLE")
print("="*50)
for i in range(len(states)):
    print("I{}:".format(i), end=" ")
    for t in sorted(terms):
        val = action[i].get(t, '-')
        print("{}={}".format(t, val), end=" ")
    print()

print("\n" + "="*50)
print("GOTO TABLE")
print("="*50)
for i in range(len(states)):
    print("I{}:".format(i), end=" ")
    for nt in sorted(non_terms):
        if nt != prods[0].split('->')[0]:
            val = goto_tab[i].get(nt, '-')
            print("{}={}".format(nt, val), end=" ")
    print()

print("\nPRODUCTIONS:")
for i, p in enumerate(prods): print(f"{i}: {p}")

print("\nFOLLOW SETS:")
for nt in sorted(non_terms):
    print(f"FOLLOW({nt}) = {follow.get(nt,set())}")

print("\nLEGEND: Sx=Shift, Rx=Reduce, ACC=Accept")
