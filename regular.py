import state
import copy
class regular:
    def __init__(self):
        self.state_id = 0
        self.nfastack = []
        self.op = []
        self.alphabet = "$0123456789QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm"
        self.nfa=[]

    def compile(self, expression):
        expression = self.add_concat(expression)
        for i in range(len(expression)):
            c = expression[i]
            if self.is_in_alphabet(c):
                self.push_stack(c)
            elif len(self.op) == 0:
                self.op.append(c)
            elif c == "(":
                self.op.append(c)
            elif c == ")":
                while self.op[-1] != '(':
                    self.do_op()
                self.op.pop()
            else:
                while len(self.op) > 0 and self.prior(c, self.op[-1]):
                    self.do_op()
                self.op.append(c)
        while len(self.op) > 0:
            self.do_op()
        nfa = self.nfastack.pop()
        nfa[-1].is_end = True
        self.nfa=nfa
        return nfa

    def is_in_alphabet(self, symbol):
        if symbol in self.alphabet:
            return True
        return False

    def add_concat(self, symbol):
        new_str = ""
        for i in range(len(symbol)-1):
            if self.is_in_alphabet(symbol[i]) and self.is_in_alphabet(symbol[i+1]):
                new_str += symbol[i]+'_'
            elif self.is_in_alphabet(symbol[i]) and symbol[i+1] == "(":
                new_str += symbol[i]+'_'
            elif symbol[i] == ")" and self.is_in_alphabet(symbol[i+1]):
                new_str += symbol[i]+'_'
            elif symbol[i] == "*" and self.is_in_alphabet(symbol[i+1]):
                new_str += symbol[i]+'_'
            elif symbol[i] == "*" and symbol[i+1] == "(":
                new_str += symbol[i]+'_'
            elif symbol[i] == ")" and symbol[i+1] == "(":
                new_str += symbol[i]+'_'
            else:
                new_str += symbol[i]
        new_str += symbol[-1]
        return new_str

    def prior(self, first, second):
        if first == second:
            return True
        elif first == "*":
            return False
        elif second == "*":
            return True
        elif first == "_":
            return False
        elif second == "_":
            return True
        elif first == "|":
            return False
        else:
            return True

    def push_stack(self, char):
        s0=state.state(self.state_id)
        self.state_id+=1

        s1 = state.state(self.state_id)
        self.state_id += 1

        s0.add_transition(s1, char)
        nfa = []
        nfa.append(s0)
        nfa.append(s1)
        self.nfastack.append(nfa)

    def do_op(self):
        if len(self.op)>0:
            operator=self.op.pop()
            if operator == "*":
                self.star()
            elif operator == "_":
                self.concat()
            elif operator == "|":
                self.union()

    def star(self):
        nfa = self.nfastack.pop()
        s0 = state.state(self.state_id)
        self.state_id += 1

        s1 = state.state(self.state_id)
        self.state_id += 1

        s0.add_transition(nfa[0], "$")
        s0.add_transition(s1, "$")
        nfa[-1].add_transition(s1, "$")
        nfa[-1].add_transition(nfa[0], "$")
        nfa.insert(0, s0)
        nfa.append(s1)
        self.nfastack.append(nfa)

    def union(self):
        nfa2 = self.nfastack.pop()
        nfa1 = self.nfastack.pop()
        s0 = state.state(self.state_id)
        self.state_id += 1

        s1 = state.state(self.state_id)
        self.state_id += 1
        s0.add_transition(nfa1[0],"$")
        s0.add_transition(nfa2[0],"$")

        nfa1[-1].add_transition(s1, "$")
        nfa2[-1].add_transition(s1, "$")

        nfa1.insert(0, s0)
        nfa2.append(s1)

        for s in nfa2:
            nfa1.append(s)


        self.nfastack.append(nfa1)

    def concat(self):
        nfa2 = self.nfastack.pop()
        nfa1 = self.nfastack.pop()

        nfa1[-1].add_transition(nfa2[0], "$")
        for s in nfa2:
            nfa1.append(s)
        self.nfastack.append(nfa1)

    def match(self, s):
        s="$"+s+"$"
        current_state= set()
        current_state.add(self.nfa[0])

        for c in s:
            next_state=set()
            for state in current_state:
                T = state.get_transition(c)
                next_state.add(state)
                for st in T:
                    next_state.add(st)
            current_state = next_state

        for state in current_state:
            if state.is_end == True:
                return True
        return False
