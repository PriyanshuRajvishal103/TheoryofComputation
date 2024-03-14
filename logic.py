import json  # Importing the JSON module to work with JSON files
from collections import OrderedDict  # Importing OrderedDict to create ordered dictionaries
from automathon import DFA  # Importing DFA class from the automathon module
from prettytable import PrettyTable  # Importing PrettyTable for creating formatted tables

# Read input data from input.json
with open('input.json') as file:
    data = json.load(file)  # Loading JSON data from the file into a Python dictionary

# Initialize DFA components
dfa_letters = data["letters"]  # Extracting the alphabet of the DFA
dfa_start = data["start"]  # Extracting the start state of the DFA
dfa_t_func = []  # List to store DFA transition function
dfa_final = []  # List to store final states of the DFA
q = [(dfa_start,)]  # List to store states of the DFA, initialized with the start state
nfa_transitions = {}  # Dictionary to store NFA transitions
dfa_transitions = {}  # Dictionary to store DFA transitions

# Populate nfa_transitions dictionary
for transition in data["t_func"]:
    nfa_transitions[(transition[0], transition[1])] = transition[2]  # Mapping NFA transitions

# Construct DFA transitions
for in_state in q:
    for symbol in dfa_letters:
        if len(in_state) == 1 and (in_state[0], symbol) in nfa_transitions:
            # If current state has only one element and the transition exists in NFA
            dfa_transitions[(in_state, symbol)] = nfa_transitions[(in_state[0], symbol)]

            # Add new state to list of states if not already present
            if tuple(dfa_transitions[(in_state, symbol)]) not in q:
                q.append(tuple(dfa_transitions[(in_state, symbol)]))
        else:
            dest = []  # List to store destination states
            f_dest = []  # List to store flattened destination states

            for n_state in in_state:
                # Check for transitions for each state in current state set
                if (n_state, symbol) in nfa_transitions and nfa_transitions[(n_state, symbol)] not in dest:
                    dest.append(nfa_transitions[(n_state, symbol)])  # Adding destination state to list

            if dest:
                # Flatten destination states
                for d in dest:
                    for value in d:
                        if value not in f_dest:
                            f_dest.append(value)  # Flattening destination states

                # Add transition to DFA transitions
                dfa_transitions[(in_state, symbol)] = f_dest

                # Add new state to list of states if not already present
                if tuple(f_dest) not in q:
                    q.append(tuple(f_dest))  # Adding new state to the list of states
