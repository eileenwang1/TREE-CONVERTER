from graph import Graph

class TreeConstructor(object):
    def __init__(self,proof):
        self.proof = proof
        self.graph = self.tree_init()

    def tree_init(self):
        graph=Graph(directed=True)
        syntax = []
        premises = self.proof.premises
        for i in range(len(premises)):
            syntax.append(str(premises[i]))
        conclusion = str(self.proof.conclusion)
        neg_conclusion = self.neg_conclusion(conclusion)
        syntax.append(neg_conclusion)
        graph.insert_vertex(syntax)
        return graph

    def tree_grow(self):
        box_count = 0
        for i in range(1,len(self.proof.subproof_list)-1):
            curr_subproof = self.proof.subproof_list[i]
            box_count = curr_subproof.premises.count("[]")
            if box_count <= self.graph.size():
                # append conclusion to the vertex with the corresponding vertex
                curr_vertex = self.graph.idx_to_vertex(box_count)
                curr_vertex.syntax.append(curr_subproof.conclusion)
            else:
                # add a new vertex
                for j in range(self.graph.size(),box_count-1):
                    self.graph.insert_vertex([])
                syntax = [curr_subproof.conclusion]
                self.graph.insert_vertex(syntax)
                

    def tree_check(self):
        pass
        
    def neg_conclusion(self,conclusion):
        if self.parathesis_needed:
            to_return = "~("++conclusion++')'
        else:
            to_return = '~'++conclusion
        return to_return

    def parathesis_needed(self,conclusion):
        in_parathesis = 0
        add_parathesis = 0
        for i in range(len(conclusion)):
            if conclusion(i)=='(':
                in_parathesis+=1
            elif conclusion(i)==')':
                in_parathesis-=1
            if in_parathesis==0:
                if conclusion(i) in ['&', '∨']:
                    add_parathesis+=1
                elif conclusion[i:i+1]=='->':
                    add_parathesis+=1
            if add_parathesis>0:
                return 1
        return 0





