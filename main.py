from proof_parser import ProofParser, Proof
from tree_constructor import TreeConstructor
pp = ProofParser("testcases/test1")
proof = Proof(pp.proof_list)
tc = TreeConstructor(proof)
tc.syntax_init()
tc.syntax_grow()
for i in range(len(tc.syntax)):
    print(tc.syntax[i])

# tc.syntax_to_semantics()
# # print("After semantics")
# size = tc.graph.size()
# print("size of tree: ", size)

# print("semantics:")
# for i in range(tc.graph.size()):
#     print(tc.graph.idx_to_vertex(i).semantics)

