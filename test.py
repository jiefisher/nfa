import regular
re =regular.regular()
nfa = re.compile("(ab)*")
# print(nfa)
# for i in range(len(nfa)):
#     for key in nfa[i].next_state:
#         print(key)

print("res",re.match("abab"))
