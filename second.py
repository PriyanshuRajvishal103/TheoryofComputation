import json
from collections import OrderedDict
from automathon import DFA
from prettytable import PrettyTable

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
        dest = []
        for n_state in in_state:
            if (n_state, symbol) in nfa_transitions:
                dest.extend(nfa_transitions[(n_state, symbol)])
        dest = sorted(set(dest))
        if dest:
            dfa_transitions[(in_state, symbol)] = dest
            if tuple(dest) not in q:
                q.append(tuple(dest))

# Format DFA transitions for output
for key, value in dfa_transitions.items():
    temp_list = [list(key[0]), key[1], value]
    dfa_t_func.append(temp_list)

# Identify final states of DFA
for q_state in q:
    for f_state in data["final"]:
        if any(state in f_state for state in q_state):
            dfa_final.append(q_state)

# Create ordered dictionary for DFA
dfa = OrderedDict()
dfa["states"] = q
dfa["letters"] = dfa_letters
dfa["t_func"] = dfa_t_func
dfa["start"] = dfa_start
dfa["final"] = dfa_final

# Write DFA data to output.json
with open('output.json', 'w+') as output_file:
    json.dump(dfa, output_file, separators=(',', ':'))

# Read DFA data from output.json
with open('output.json') as file:
    data = json.load(file)

# Extract components from JSON data
dfa_letters = data["letters"]
dfa_start = data["start"]
dfa_t_func = data["t_func"]
dfa_final = data["final"]

# Construct DFA components
q = set()
for state in data["states"]:
    q.add(tuple(state))  # Convert nested list to tuple

sigma = set(dfa_letters)
initial_state = dfa_start
f = set()
for final_state in dfa_final:
    f.add(tuple(final_state))  # Convert nested list to tuple

delta = {}
for transition in dfa_t_func:
    state = tuple(transition[0])
    symbol = transition[1]
    dest_state = tuple(transition[2])
    delta[state] = delta.get(state, {})
    delta[state][symbol] = dest_state

# Print the transformed components in a table format
print("States:")
states_table = PrettyTable(["q"])
for state in q:
    states_table.add_row([state])
print(states_table)

print("Alphabet:")
alphabet_table = PrettyTable(["sigma"])
for letter in sigma:
    alphabet_table.add_row([letter])
print(alphabet_table)

print("Transition Function:")
transition_table = PrettyTable(["State", "Symbol", "Destination"])
for state in delta:
    for symbol in delta[state]:
        transition_table.add_row([state, symbol, delta[state][symbol]])
print(transition_table)

print("Initial State:")
initial_state_table = PrettyTable(["initial_state"])
initial_state_table.add_row([initial_state])
print(initial_state_table)

print("Final States:")
final_states_table = PrettyTable(["f"])
for state in f:
    final_states_table.add_row([state])
print(final_states_table)

# Create and visualize the DFA
automata = DFA(q, sigma, delta, initial_state, f)
automata.is_valid()  # True

automata.view(
    file_name="DFA Visualization",
    node_attr={'fontsize': '20'},
    edge_attr={'fontsize': '20pt'}
)
