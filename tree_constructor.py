from graph import Graph
import copy

class TreeConstructor(object):
    def __init__(self,proof):
        self.proof = proof
        self.syntax = []    # syntax is a list of lists, each list is a possible world
        # self.graph = self.tree_init()

    def syntax_init(self):
        # intialize a world, with premises and the negation of the conclusion
        to_add = []
        for i in range(len(self.proof.premises)):
            to_add.append(self.strip_parentheses(self.proof.premises[i]))
        # to_add.extend(self.proof.premises)
        conclusion = self.strip_parentheses(self.proof.conclusion)
        if self.is_compound(conclusion):
            to_add.append("~("+conclusion+')')
        else:
            to_add.append('~'+conclusion)
        self.syntax.append(to_add)

    def syntax_grow(self):
        # go through the proof
        # handle proof with extra assumptions in the form of conditional
        # create worlds where needed. In this case, worlds models nested box proofs, and therefore are in a linear fashion
        # for example:
        # L,q [],p,[],r,t |- t
        # w1: L, q-> q
        # w2: p->p
        # w3: r->r
        init_syntax_list = copy.deepcopy(self.syntax[0])
        for i in range(1,len(self.proof.subproof_list)-1):
            curr_subproof = self.proof.subproof_list[i]
            assumptions = []
            starting_idx = len(self.proof.premises)
            if curr_subproof.premises[:starting_idx+1]==init_syntax_list:
                assumptions = curr_subproof.premises[starting_idx+1:]
            elif self.is_sublist(self.proof.premises[:starting_idx],self.proof.premises):
                assumptions = curr_subproof.premises[starting_idx:]
            else:
                print(curr_subproof)
                raise Exception("wrong premises")
            
            num_box = assumptions.count("[]")
            if num_box==0:
                to_append = self.pack_conditional(assumptions,curr_subproof.conclusion)
                if to_append!="" and to_append not in self.syntax[0]:
                    self.syntax[0].append(to_append)
                continue
            else:
                box_count = 0
                antecedent = []
                for j in range(len(assumptions)):
                    if assumptions[j]=="[]":
                        box_count+=1
                        to_append = self.pack_conditional(antecedent)
                        if to_append!="" and to_append not in self.syntax[box_count-1]:
                            self.syntax[box_count-1].append(to_append)
                        while len(self.syntax)<box_count+1:
                            self.syntax.append([])
                        antecedent = []
                    else:
                        antecedent.append(assumptions[j])
                to_append = self.pack_conditional(antecedent,curr_subproof.conclusion)
                if to_append != "" and to_append not in self.syntax[box_count]:
                    self.syntax[box_count].append(to_append)
        
                






            



    # def tree_init(self):
    #     graph=Graph(directed=True)
    #     syntax = []
    #     premises = self.proof.premises
    #     for i in range(len(premises)):
    #         syntax.append(str(premises[i]))
    #     conclusion = str(self.proof.conclusion)
    #     neg_conclusion = self.neg_conclusion(conclusion)
    #     syntax.append(neg_conclusion)
    #     graph.insert_vertex(syntax)
    #     return graph
    # # syntax list
    # def tree_grow(self):
    #     init_syntax_list = copy.deepcopy(self.graph.idx_to_vertex(0).syntax)
    #     for i in range(1,len(self.proof.subproof_list)-1):
    #         curr_subproof = self.proof.subproof_list[i]
    #         # if curr_subproof.premises==self.proof.premises or curr_subproof.premises==init_syntax_list:
    #         #     self.graph.idx_to_vertex(0).append(curr_subproof.conclusion)
    #         #     continue
            
    #         assumptions = []
    #         starting_idx = len(self.proof.premises)
    #         if curr_subproof[:starting_idx+1]==init_syntax_list:
    #             assumptions = curr_subproof[starting_idx+1:]
    #         elif curr_subproof[:starting_idx]==self.proof.premises:
    #             assumptions = curr_subproof[starting_idx:]
    #         else:
    #             print(curr_subproof)
    #             raise Exception("wrong premises")
    #         box_count = 0
    #         for j in range(len(assumptions)):
    #             if assumptions[j]=="[]":
    #                 box_count+=1


    #         box_count = curr_subproof.premises.count("[]")
    #         if box_count <= self.graph.size()-1:
    #             # append conclusion to the vertex with the corresponding vertex
    #             curr_vertex = self.graph.idx_to_vertex(box_count)
    #             if curr_subproof.conclusion not in curr_vertex.syntax:
    #                 # no repeated sentences
    #                 curr_vertex.syntax.append(curr_subproof.conclusion)
    #         else:
    #             # add a new vertex
    #             for j in range(self.graph.size(),box_count):
    #                 self.graph.insert_vertex([])
    #             syntax = [curr_subproof.conclusion]
    #             self.graph.insert_vertex(syntax)

    # def syntax_to_semantics(self):
        
    #     # recursive. breakdown complex sentences
    #     for i in range(self.graph.size()):
    #         syntax_list = self.graph.idx_to_vertex(i).syntax
    #         # print(i)
    #         # print(self.graph.idx_to_vertex(i).semantics)
    #         for j in range(len(syntax_list)):
    #             curr_sentence = syntax_list[j].strip()
    #             self.apply_tree_rules(curr_sentence,i)

    #             # contradiction

    # def apply_tree_rules(self,curr_sentence,curr_vertex,curr_branch=""):
    #     # print("curr_sentence: ",curr_sentence)
    #     # print("curr_vertex: ",curr_vertex)

    #     curr_sentence = self.strip_parentheses(curr_sentence)
    #     self.graph.idx_to_vertex(curr_vertex).semantics.append(curr_sentence,curr_branch)
    #     # # contradiction
    #     # path = self.graph.idx_to_vertex(curr_vertex).semantics.path(curr_branch)
    #     # a recursive function that finds contradiction

    #     # print(self.graph.idx_to_vertex(curr_vertex).semantics)
    #     # print("curr_branch: ",curr_branch)
    #     # path = self.graph.idx_to_vertex(curr_vertex).semantics.path(curr_branch)
    #     # print("path: ", path)
    #     # print("\n")

    #     # double negation
    #     num_neg, inner_sentence = self.num_neg(curr_sentence)
    #     if num_neg%2==0:
    #         new_sentence = inner_sentence
    #     else:
    #         if self.is_compound(inner_sentence):
    #             new_sentence = "~("+inner_sentence+')'
    #         else:
    #             new_sentence = '~'+inner_sentence
    #     if num_neg>1 and new_sentence != curr_sentence:
    #         self.apply_tree_rules(new_sentence,curr_vertex,curr_branch)
        
    #     conditional_false = self.conditional_false(curr_sentence)
    #     box_in = self.box_in(curr_sentence)
    #     conditional_truth = self.conditional_truth(curr_sentence)
    #     is_disjunction = self.is_disjunction(curr_sentence)
    #     # negation false
    #     if conditional_false:
    #         # self.graph.vertices()[curr_vertex].semantics.append(curr_sentence,curr_branch)
    #         for i in conditional_false:
    #             self.graph.vertices()[curr_vertex].semantics.append(i,curr_branch)
    #         for i in conditional_false:
    #             self.apply_tree_rules(i,curr_vertex,curr_branch)

    #     # elif box_in:
    #     #     # self.graph.idx_to_vertex(curr_vertex).semantics.append(curr_sentence,curr_branch)
    #     #     if curr_vertex!=0:
    #     #         self.graph.idx_to_vertex(curr_vertex-1).semantics.append(box_in,curr_branch)
    #     #         self.apply_tree_rules(box_in,curr_vertex-1,curr_branch)

    #     elif conditional_truth:
    #         if len(conditional_truth)!=2:
    #             raise Exception("conditional clauses number is not 2")
    #         u,v = conditional_truth
    #         # self.graph.idx_to_vertex(curr_vertex).semantics.append([u,v],curr_branch)
    #         self.apply_tree_rules(u,curr_vertex,curr_branch+'l')
    #         self.apply_tree_rules(v,curr_vertex,curr_branch+'r')

    #     elif is_disjunction:
    #         if len(is_disjunction)!=2:
    #             raise Exception("disjuncts number is not 2")
    #         u,v = is_disjunction
    #         # self.graph.idx_to_vertex(curr_vertex).semantics.append([u,v],curr_branch)
    #         self.apply_tree_rules(u,curr_vertex,curr_branch+'l')
    #         self.apply_tree_rules(v,curr_vertex,curr_branch+'r')

    #     # for i in range(self.graph.size()):
    #     #     print(self.graph.idx_to_vertex(i).semantics)

    #     return

    # def tree_check(self):
    #     pass
        
    # def conditional_false(self,input_sentence):
    #     # if a conditional false sentence, return a tuple of two simpler sentence
    #     # else, return 0
    #     curr_sentence = self.strip_parentheses(input_sentence)

    #     # curr_sentence = input_sentence.strip()
    #     # if curr_sentence[0]=='(' and curr_sentence[-1]==')':
    #     #     curr_sentence=curr_sentence[1:-1].strip()
    #     if curr_sentence[0]!='~':
    #         return 0

    #     in_paranthesis = 0
    #     # conditional_false = 0
    #     curr_sentence = self.strip_parentheses(curr_sentence[1:])
    #     # print(curr_sentence)

    #     for k in range(len(curr_sentence)):
    #         if curr_sentence[k]== '(':
    #             in_paranthesis+=1
    #         elif curr_sentence[k]==')':
    #             in_paranthesis-=1
    #         elif k < len(curr_sentence)-1 and curr_sentence[k:k+2]=="->" and in_paranthesis==0:
    #             to_return1 = self.strip_parentheses(curr_sentence[:k])
    #             to_return2 = self.strip_parentheses(curr_sentence[k+2:])
    #             if self.is_compound(to_return2):
    #                 to_return2 = "~("+to_return2+')'
    #             else:
    #                 to_return2 = '~'+to_return2
    #             # print(to_return1, to_return2)
    #             return to_return1,to_return2

    #     return 0

    def num_neg(self,input_sentence,num=0):
        input_sentence = self.strip_parentheses(input_sentence)
        if self.is_compound(input_sentence):
            return num, input_sentence
        
        if input_sentence[0]!='~':
            return num, input_sentence
        input_sentence = self.strip_parentheses(input_sentence[1:])
        # if self.is_compound(input_sentence):
        #         return num+1, input_sentence
        # else:
        return self.num_neg(input_sentence,num+1)

    def is_compound(self,input_sentence):
        # return True if the input sentence is a compound sentence
        # a compound sentence mains the main connective is and, or, conditional
        input_sentence = self.strip_parentheses(input_sentence)
        # input_sentence = input_sentence.strip()
        # if input_sentence[0] == '(' and input_sentence == ')':
        #     input_sentence = input_sentence[1:-1].strip()
        in_paranthesis = 0
        for i in input_sentence:
            if i=='(':
                in_paranthesis+=1
            elif i == ')':
                in_paranthesis-=1
            elif i=='&' or i == '∨' or i=='-':
                if in_paranthesis==0:
                    return True
        return False


    # def box_in(self,input_sentence):
    #     input_sentence = input_sentence.strip()
    #     if input_sentence[0:2]=='[]':
    #         to_return = input_sentence[2:]
    #         to_return = self.strip_parentheses(to_return)
    #         return to_return
    #     return False

    # def conditional_truth(self,input_sentence):
    #     # check whether the main connective of a sentence is a conditional
    #     # if yes, return a 2-tuple of its conjuncts
    #     # if no, return 0
    #     input_sentence = self.strip_parentheses(input_sentence)
    #     in_parentheses = 0
    #     for i in range(len(input_sentence)):
    #         if input_sentence[i]=='(':
    #             in_parentheses += 1
    #         elif input_sentence[i]==')':
    #             in_parentheses -= 1
    #         elif i < len(input_sentence)-1 and input_sentence[i:i+1]=='->' and in_parentheses==0:
    #             u,v = input_sentence[:i], input_sentence[i+2:]
    #             u = self.strip_parentheses(u)
    #             if self.is_compound(u):
    #                 u = '~('+u+'~'
    #             else:
    #                 u = '~'+u
    #             v = self.strip_parentheses(v)
    #             return u,v
    #     return 0

    # def is_disjunction(self,input_sentence):
    #     # check whether the main connective of a sentence is a conjunction
    #     # if yes, return a 2-tuple of its conjuncts
    #     # if no, return 0
    #     input_sentence = self.strip_parentheses(input_sentence)
    #     in_parentheses = 0
    #     for i in range(len(input_sentence)):
    #         if input_sentence[i]=='(':
    #             in_parentheses += 1
    #         elif input_sentence[i]==')':
    #             in_parentheses -= 1
    #         elif input_sentence[i]=='∨' and in_parentheses==0:
    #             u,v = input_sentence[:i], input_sentence[i+1:]
    #             u = self.strip_parentheses(u)
    #             v = self.strip_parentheses(v)
    #             return u,v
    #     return 0

    # def neg_conclusion(self,conclusion):
    #     if self.is_compound and self.parentheses_needed:
    #         to_return = "~("+conclusion+')'
    #     else:
    #         to_return = '~'+conclusion
    #     return to_return

    # def parentheses_needed(self,conclusion):
    #     in_parentheses = 0
    #     add_parentheses = 0
    #     for i in range(len(conclusion)):
    #         if conclusion[i]=='(':
    #             in_parentheses+=1
    #         elif conclusion[i]==')':
    #             in_parentheses-=1
    #         if in_parentheses==0:
    #             if conclusion[i] in ['&', '∨','-']:
    #                 add_parentheses+=1
    #         if add_parentheses>0:
    #             return 1
    #     return 0

    def strip_parentheses(self,curr_sentence):
        curr_sentence = curr_sentence.strip()
        if curr_sentence[0]!='(' or curr_sentence[-1]!=')':
            return curr_sentence
        in_parentheses = 1
        for i in range(1,len(curr_sentence)):
            if in_parentheses==0 and i!=len(curr_sentence)-1:
                return curr_sentence
            return self.strip_parentheses(curr_sentence[1:-1])

    def pack_conditional(self,antecedent, consequent=""):
        if len(antecedent)==0:
            return consequent
        # input: a list of antecedents, consequent
        for i in range(len(antecedent)):
            if self.is_compound(antecedent[i]):
                antecedent[i] = '('+antecedent[i]+')'
        if len(antecedent)>1:
            antecedent_str = " & ".join(antecedent)
            antecedent_str = '(' + antecedent_str + ')'
        else:
            antecedent_str = antecedent[0]
        if consequent=="":
            return antecedent_str + ' -> ' + antecedent_str
        if self.is_compound(consequent):
                consequent = '(' + consequent + ')'
        to_append = antecedent_str+ ' -> ' + consequent
        return to_append

    def is_sublist(self,l1,l2):
        # return true if l1 is a sublist of l2
        for i in l1:
            if i not in l2:
                return False
        return True
    








