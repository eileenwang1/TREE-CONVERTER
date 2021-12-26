# coding: utf-8
# -*- coding: utf-8 -*-
# proof
# premise + conclusion
import copy

class ProofParser(object):
    def __init__(self,filename):
        self.filename = filename
        self.content_list = self.read_file()
        self.proof_list = self.parse_subproof()

    def read_file(self):
        f = open(self.filename, mode="r")
        line = f.readline()
        content_list = []
        while line:
            line = line.strip()
            if len(line)==0 or line[0] == "#":
                continue
            content_list.append(line)
            line = f.readline()
        f.close()
        return content_list

    def parse_subproof(self):
        subproof_list = []
        for i in range(len(self.content_list)):
            curr_subproof = Subproof(self.content_list[i])
            subproof_list.append(copy.deepcopy(curr_subproof))
        return subproof_list

class Subproof(object):
    def __init__(self, line_string):
        self.premises, self.conclusion = self.parse_line(line_string)

    def __str__(self):
        return ", ".join(self.premises) + "\n" + self.conclusion

    def parse_line(self,line_string):
        l = line_string.split("|-")
        premises_string = l[0].strip()
        conclusion_string = l[1].strip()
        premises_list = premises_string.split(",")
        for i in range(len(premises_list)): premises_list[i] = premises_list[i].strip()
        # premises_list = premise_list[i].strip() for i in range(len(premises_list))
        return premises_list, conclusion_string

class Proof(object):
    def __init__(self, subproof_list):
        self.subproof_list = subproof_list
        self.premises = self.subproof_list[-1].premises
        self.conclusion = self.subproof_list[-1].conclusion
        


# sp1 = Subproof("[](p∨q), [](p->r), [](q->r) |- []r")

# # for i in range(len(sp1.premises)):
# #     print(sp1.premises[i])
# print(sp1.premises)
# print(sp1.conclusion)

# pp = ProofParser("testcases/test1")
# pp.read_file()





