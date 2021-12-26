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
            if box_count <= self.graph.size()-1:
                # append conclusion to the vertex with the corresponding vertex
                curr_vertex = self.graph.idx_to_vertex(box_count)
                if curr_subproof.conclusion in curr_vertex.syntax:
                    continue    # no repeated sentences
                curr_vertex.syntax.append(curr_subproof.conclusion)
            else:
                # add a new vertex
                for j in range(self.graph.size()-1,box_count-1):
                    self.graph.insert_vertex([])
                syntax = [curr_subproof.conclusion]
                self.graph.insert_vertex(syntax)

    def apply_tree_rules(self):
        pass
        # # recursive. breakdown complex sentences
        # for i in range(self.graph.size()):
        #     syntax_list = self.graph.vertices()[i].syntax
        #     for j in range(len(syntax_list)):
        #         curr_sentence = syntax_list[j].strip()
        #         # disjunction
        #         if '∨' in syntax_list[j]:
        #             conjuncts = syntax_list[j].split('∨')
        #             conjuncts = [i.strip() for i in conjuncts]
        #             self.graph.vertices()[i].semantics.append(syntax_list[j])
        #             self.graph.vertices()[i].semantics.append(conjuncts)
        #             # iteration on conjunctions
                    
        #         # conditional false
        #         conditional_false = self.conditional_false()
        #         if conditional_false:
        #             self.graph.vertices()[i].semantics.append(syntax_list[j])
        #             self.graph.vertices()[i].semantics.extend(conditional_false)
        #             # the antecedent and consequent are not simple sentences

        #         # box in
        #         if i > 0 and j==len(syntax_list)-1:
        #             pass
        #         # contradiction
                
    def tree_check(self):
        pass
        
    def conditional_false(self,input_sentence):
        input_sentence = input_sentence.strip()
        if input_sentence[0]!='~':
            return 0
        in_paranthesis = 0
        conditional_false = 0
        curr_sentence = input_sentence[1:].strip()
        for k in range(1,len(curr_sentence)):
            if curr_sentence[k]== '(':
                in_paranthesis+=1
            elif curr_sentence[k]==')':
                in_paranthesis-=1
            elif k < len(curr_sentence)-1 and curr_sentence[k:k+2]=="->" and in_paranthesis==1:
                return curr_sentence[1:k].strip(), curr_sentence[k+2:].strip()
            return 0
        

    def neg_conclusion(self,conclusion):
        if self.parathesis_needed:
            to_return = "~("+conclusion+')'
        else:
            to_return = '~'+conclusion
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
                elif conclusion[i:i+2]=='->':
                    add_parathesis+=1
            if add_parathesis>0:
                return 1
        return 0





