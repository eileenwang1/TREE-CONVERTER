from graph import Graph
import copy

class TreeConstructor(object):
    def __init__(self,proof):
        self.proof = proof
        self.syntax = []    # syntax is a list of lists, each list is a possible world
        self.graph = Graph(directed=True)

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
        
    def tree_init(self):
        self.graph=Graph(directed=True)

    def semantics(self):
        # create root vertex
        root_vertex = self.graph.insert_vertex()
        self.tree_grow(0,root_vertex)
        # copy stuff in syntax[0] into the root node
        # until there is the need to create a new world-create a new world, and copy the corresponding stuff from syntax into the new world
        # check whether there is a contradiction in the new world, if yes, stop; if no, continue with iterating syntax[0]
        # check if every world has contradiction
        to_print = self.vertex_contradiction(root_vertex)
        # print("final check: ",to_print)


    def box_false(self,curr_sentence):
        # if ~[]p. return ~p
        # else, return False
        curr_sentence = self.strip_parentheses(curr_sentence)
        if curr_sentence[0]!='~' or self.is_compound(curr_sentence):
            return False
        inner_sentence = self.strip_parentheses(curr_sentence[1:])
        if inner_sentence[0:2]!="[]" or self.is_compound(inner_sentence):
            return False
        to_return = self.strip_parentheses(inner_sentence[2:])
        if self.is_compound(to_return):
            to_return = '~(' + to_return+')'
        else:
            to_return = '~' + to_return
        return to_return

    def tree_grow(self, syntax_idx,curr_vertex):
        if syntax_idx>len(self.syntax):
            raise Exception("wrong syntax_idx") 
        if not isinstance(curr_vertex,Graph.Vertex):
            raise Exception("wrong vertex")
        curr_syntax = self.syntax[syntax_idx]
        for i in range(len(curr_syntax)):
            curr_sentence = self.strip_parentheses(curr_syntax[i])
            curr_vertex.semantics.append(curr_sentence)
            box_false = self.box_false(curr_sentence)
            if box_false:
                # create a new vertex
                new_vertex = self.graph.insert_vertex()
                # edge from the old world to the new world
                self.graph.insert_edge(curr_vertex,new_vertex)
                # find its distance from root node
                new_syntax_idx = self.graph.path_length(new_vertex)
                new_vertex.semantics.append(box_false)
                self.tree_grow(new_syntax_idx,new_vertex)
            # check whether there is contradiction
            if self.vertex_contradiction(curr_vertex):
                return
        return 

    def list_contradiction(self,path):
        # return True if there is contradiction in a list
        # does not cover the cases of logical equivalence
        list_neg = []
        list_inner = []
        for i in range(len(path)):
            num,inner = self.num_neg(path[i])
            list_neg.append(num)
            list_inner.append(inner)
        for i in range(len(path)):
            for j in range(i+1,len(path)):
                if list_inner[i]==list_inner[j] and (list_neg[i]+list_neg[j])%2:
                    return True
        return False

    def vertex_contradiction(self,vertex):
        # return True and mark the vertex.contradiction = True
        # there are two conditions that a vertex can have contradiction
        # (1) all its accessible worlds are contradictory
        # (2) all paths in the vertex have contradictions
        # the first option
        if vertex.contradiction==True:
            return True
        children = list(self.graph._outgoing[vertex].keys())
        if len(children)!=0:
            contra_children = 0
            for i in range(len(children)):
                if self.vertex_contradiction(children[i]):
                    contra_children += 1
            if contra_children == len(children):
                vertex.contradiction = True
                return True
        # the second option
        all_paths = vertex.semantics.path()
        if len(all_paths)==0:
            return False
        contra_path = 0
        for i in range(len(all_paths)):
            if self.list_contradiction(all_paths[i]):
                contra_path += 1
        if contra_path==len(all_paths):
            vertex.contradiction = True

            return True
            
        return False  

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

    def strip_parentheses(self,curr_sentence):
        curr_sentence = curr_sentence.strip()
        if curr_sentence=="":
            return ""
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
    








