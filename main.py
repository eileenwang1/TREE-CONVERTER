from proof_parser import ProofParser, Proof
from tree_constructor import TreeConstructor
pp = ProofParser("testcases/test5")
proof = Proof(pp.proof_list)
tc = TreeConstructor(proof)
tc.tree_grow()
size = tc.graph.size()
print("size of tree: ", size)
for i in range(tc.graph.size()):
    print(tc.graph.idx_to_vertex(i).syntax)

