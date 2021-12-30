from proof_parser import ProofParser, Proof
from tree_constructor import TreeConstructor
pp = ProofParser("testcases/test5")
proof = Proof(pp.proof_list)
tc = TreeConstructor(proof)
tc.syntax_init()
tc.syntax_grow()
print("syntax: ")
for i in range(len(tc.syntax)):
    print(tc.syntax[i])

tc.semantics()

# tc.syntax_to_semantics()
# # print("After semantics")
# size = tc.graph.size()
# print("size of tree: ", size)

print("semantics:")
for i in range(tc.graph.size()):
    curr_vertex = tc.graph.idx_to_vertex(i)
    print(curr_vertex.semantics)
    print("has contradiction: ",curr_vertex.contradiction)

