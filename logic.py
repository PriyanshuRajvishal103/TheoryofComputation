import json
from collections import OrderedDict

# Read input data from input.json
with open('input.json') as file:
    data = json.load(file)

# Initialize DFA components
dfa_letters = data["letters"]
dfa_start = data["start"]
dfa_t_func = []
dfa_final = []
q = [(dfa_start,)]
nfa_transitions = {}
dfa_transitions = {}

# Populate nfa_transitions dictionary
for transition in data["t_func"]:
    nfa_transitions[(transition[0], transition[1])] = transition[2]

# Construct DFA transitions
for in_state in q:
    for symbol in dfa_letters:
        if len(in_state) == 1 and (in_state[0], symbol) in nfa_transitions:
            dfa_transitions[(in_state, symbol)] = nfa_transitions[(in_state[0], symbol)]

            if tuple(dfa_transitions[(in_state, symbol)]) not in q:
                q.append(tuple(dfa_transitions[(in_state, symbol)]))
        else:
            dest = []
            f_dest = []

            for n_state in in_state:
                if (n_state, symbol) in nfa_transitions and nfa_transitions[(n_state, symbol)] not in dest:
                    dest.append(nfa_transitions[(n_state, symbol)])

            if dest:
                for d in dest:
                    for value in d:
                        if value not in f_dest:
                            f_dest.append(value)

                dfa_transitions[(in_state, symbol)] = f_dest

                if tuple(f_dest) not in q:
                    q.append(tuple(f_dest))