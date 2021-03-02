class Node:
    def __init__(self,data):
        self.root=data
        self.left=None
        self.right=None

    def is_operator(self):
        symbols = ['&', '|', '-', '>', '=', '%']
        return True if any(self.root in s for s in symbols) else False

class BST:
    def __init__(self):
        self.root=None

    def is_the_rightmost_element_of_the_left_subtree_an_identifier(self,node):
        if node.is_operator() and node.right is not None and node.right.is_operator():
            return True if self.is_the_rightmost_element_of_the_left_subtree_an_identifier(node.right) else False
        elif not node.is_operator() or (node.is_operator() and node.right is not None and not node.right.is_operator()):
            return True #returns True
        else:
            return False #returns False

    def recursBST(self,node,data):
        if node is None:
            node=Node(data)
            self.root=node
        elif node.root=='-':
            if not node.right:
                node.right=Node(data)
            else:
                self.recursBST(node.right,data)
        elif (node.left is not None) and self.is_the_rightmost_element_of_the_left_subtree_an_identifier(node.left):
            if node.right is None:
                node.right=Node(data)
            else:
                self.recursBST(node.right,data)
        else:
            if node.left is not None:
                thebool=self.is_the_rightmost_element_of_the_left_subtree_an_identifier(node.left)
            if node.left is None:
                node.left=Node(data)
            else:
                self.recursBST(node.left,data)

    def insert(self,data):
        if self.root is None:
            self.root=Node(data)
        else:
            self.recursBST(self.root,data)

    def copy(self,node):
        if node:
            copynode=Node(node.root)
            if node.left:
                copynode.left=self.copy(node.left)
            if node.right:
                copynode.right = self.copy(node.right)
            return copynode

    def printTree(self):
        if self.root is not None:
            self.auxPrintTree(self.root)

    def auxPrintTree(self,node):
        if node is not None:
            self.auxPrintTree(node.left)
            print(node.root+' ')
            self.auxPrintTree(node.right)

    def find1or0(self, node, count = 0):
        if node is None:
            return count
        elif node.root == "1" or node.root == "0":
            return self.find1or0(node.left, self.find1or0(node.right, count + 1))
        else:
            return self.find1or0(node.left, self.find1or0(node.right, count))

    def replace(self, node, nodeR):
        node.root = nodeR.root
        node.left = nodeR.left
        node.right = nodeR.right

    def negate(self,node):
        if node.root == "-":
            self.replace(node,node.right)
            return node
        else:
            newNode = self.copy(node)
            node.right = newNode
            node.left = None
            node.root = "-"
            return node

    def deMorgan(self,node):
        if node is not None:
            if node.root=='-' and node.left==None and node.right is not None and node.right.is_operator():
                if node.right.root=='&':node.root='|'
                elif node.right.root=='|':node.root='&'
                if node.right.left is not None:node.left=self.negate(node.right.left)
                if node.right.right is not None:node.right=self.negate(node.right.right)
        if node.left is not None:
            self.deMorgan(node.left)
        if node.right is not None:
            self.deMorgan(node.right)

    def simplify(self,node):
        if node is not None:
            if node.root == "-" and node.right is not None and node.right.root == "|":
                self.replace(node,node.right)
                self.convert_disjunction(node)
            if node.root == "-" and node.right is not None and node.right.root == "&":
                self.replace(node,node.right)
                self.convert_conjunction_once(node)
        if node.left is not None:
            self.simplify(node.left)
        if node.right is not None:
            self.simplify(node.right)

    def convert_implication(self,node):
        if node is not None:
            if node.root == ">":
                node.root = "|"
                self.negate(node.left)
        if node.left is not None:
            self.convert_implication(node.left)
        if node.right is not None:
            self.convert_implication(node.right)

    def convert_xor(self,node):
        if node is not None:
            if node.root == "%":
                node.root = "|"
                treeleft=Node('&')
                treeright=Node('&')
                treeleft.left=self.copy(node.left)
                treeright.right=self.copy(node.right)
                treeleft.right=self.copy(self.negate(node.right))
                treeright.left=self.copy(self.negate(node.left))

                node.left=treeleft
                node.right=treeright
        if node.left is not None:
            self.convert_xor(node.left)
        if node.right is not None:
            self.convert_xor(node.right)

    def convert_equivalence(self,node):
        if node is not None:
            if node.root == "=":
                node.root = "|"
                treeleft=Node('&')
                treeleft.left=self.copy(node.left)
                treeleft.right=self.copy(node.right)
                treeright=Node('&')
                treeright.left=self.copy(self.negate(node.left))
                treeright.right=self.copy(self.negate(node.right))
                node.left=treeleft
                node.right=treeright
        if node.left is not None:
            self.convert_equivalence(node.left)
        if node.right is not None:
            self.convert_equivalence(node.right)

    def convert_disjunction(self,node):
        if node is not None:
            if node.root == "|":
                node.root = "&"
                self.negate(node.left)
                self.negate(node.right)
                self.simplify(node)
        if node.left is not None:
            self.convert_disjunction(node.left)
        if node.right is not None:
            self.convert_disjunction(node.right)

    def convert_conjunction_once(self,node):
        if node is not None:
            if node.root == "&":
                print("found disjunction")
                node.root = "|"
                self.negate(node.left)
                self.negate(node.right)
                self.simplify(node)

    def depth(self,node):
        return max(self.depth(node.left) if node.left else 0, self.depth(node.right) if node.right else 0) + 1

    def distribution(self,node):
        if node is not None:
            if node.root=='|' and node.left is not None and node.right is not None and (node.left.root=='&' or node.right.root=='&'):
                tree1 = Node(node.root)
                tree2 = Node(node.root)
                if (self.depth(node.left)> self.depth(node.right) and node.left.root=='&') or node.right.root!='&':
                    node.root = node.left.root
                    tree1.left = node.left.left
                    tree1.right = node.right
                    tree2.left = node.left.right
                    tree2.right = node.right
                    node.left = tree1
                    node.right = tree2
                elif node.right.root=='&':
                    node.root = node.right.root
                    tree1.left = node.left
                    tree1.right = node.right.left
                    tree2.left = node.left
                    tree2.right = node.right.right
                    node.left = tree1
                    node.right = tree2
            elif node.root=='|' and node.left is not None and node.right is not None and node.left.root=='&':
                node.root='&'
                treeleft=Node('|')
                treeleft.left=node.left.left
                treeleft.right=node.right
                treeright=Node('|')
                treeright.left=node.left.right
                treeright.right=node.right
                node.left=treeleft
                node.right=treeright
        if node.left is not None:
            self.distribution(node.left)
        if node.right is not None:
            self.distribution(node.right)

    def is_identifier(self,node):
        if node is not None:
            return True if not node.is_operator() or (node.root=='-' and node.left is None and node.right is not None and not node.right.is_operator()) else False

    def is_True(self,solution):
        solutions=solution.split(',')[:-1]
        if len(solutions)==2:
            if ('not' in solutions[0] and 'not' not in solutions[1]) or ('not' not in solutions[0] and 'not' in solutions[1]):
                newset=[]
                for x in solutions:
                    newset.append(x.replace('not','').strip())
                if(newset[0]==newset[1]):
                    return True
        return False

    def simplify01(self,node):
        if node and node.left and node.right:
            if node.root=='|':
                if (node.left.root=='0') or (node.left.root=='-' and node.left.right and node.left.right.root=='1'):
                    self.replace(node, node.right)
                elif(node.right.root=='0') or (node.right.root=='-' and node.right.right and node.right.right.root=='1'):
                    self.replace(node, node.left)
                elif (node.left.root=='1' or node.right.root=='1') or (node.left.root=='-' and node.left.right and node.left.right.root=='0') or (node.right.root=='-' and node.right.right and node.right.right.root=='0'):
                    self.replace(node,Node("1"))
            elif node.root=='&':
                if (node.left.root=='1') or (node.left.root=='-' and node.left.right and node.left.right.root=='0'):
                    self.replace(node, node.right)
                elif(node.right.root=='1') or (node.right.root=='-' and node.right.right and node.right.right.root=='0'):
                    self.replace(node, node.left)
                elif (node.left.root=='0' or node.right.root=='0') or (node.left.root=='-' and node.left.right and node.left.right.root=='1') or (node.right.root=='-' and node.right.right and node.right.right.root=='1'):
                    self.replace(node,Node("0"))
        if node.left:
            self.simplify01(node.left)
        if node.right:
            self.simplify01(node.right)

    def eliminate10(self,node):
        if self.find1or0(node) == 0 or self.find1or0(node) == 1:
            self.simplify01(node)
            return
        else:
            self.simplify01(node)
            self.eliminate10(node)


    def getsolutionsaux(self,node,solution):
        if node.root=='&':
            if node.left is not None:
                if self.is_identifier(node.left) and node.left.root=='-':
                    solution=solution+node.left.right.root+', '
                elif self.is_identifier(node.left):
                    solution=solution+'not '+node.left.root+', '
                else:
                    solution=self.getsolutionsaux(node.left,solution)+';'
            if node.right is not None:
                if self.is_identifier(node.right) and node.right.root=='-':
                    solution=solution+node.right.right.root+', '
                elif self.is_identifier(node.right):
                    solution=solution+'not '+node.right.root+', '
                else:
                    solution=self.getsolutionsaux(node.right,solution)+';'
        elif node.root=='|':
            if node.left is not None:
                if self.is_identifier(node.left) and node.left.root=='-':
                    solution=solution+node.left.right.root+', '
                elif self.is_identifier(node.left):
                    solution=solution+'not '+node.left.root+', '
                else:
                    solution=self.getsolutionsaux(node.left,solution)
            if node.right is not None:
                if self.is_identifier(node.right) and node.right.root=='-':
                    solution=solution+node.right.right.root+', '
                elif self.is_identifier(node.right):
                    solution=solution+'not '+node.right.root+', '
                else:
                    solution=self.getsolutionsaux(node.right,solution)+';'
        elif node.root=='-':
            solution=solution+node.right.root+'  ;'
        elif node.root.is_identifier():
            solution=solution+'not '+node.root+'  ;'
        return solution

    def getsolutions(self,node):
        result=set([])
        if node:
            solutions=self.getsolutionsaux(node,"").split(';')
            for solution in solutions:
                if solution!="":
                    if not self.is_True(solution):
                        result.add(':- '+solution[:-2]+'.')
        return list(result)

    def auxGetList(self,node):
        if node is None:
            return []
        return self.auxGetList(node.left) + [node.root] + self.auxGetList(node.right)

    def getlist(self):
        list=[]
        if self.root is not None:
            list=self.auxGetList(self.root)
        return list

    def calculateSolutions(self,list):
        solution=":- "
        i=0
        while i < len(list):
            if list[i]=='-':
                solution=solution+list[i+1]
                i=i+1
            elif list[i]=='|':
                solution=solution+', '
            else:
                solution=solution+'not '+list[i]
            i=i+1
        return solution+'.'

    def doSolutions(self):
        list=self.getlist()
        list.append('&')
        newlist=[]
        listsolutions=[]
        for i in list:
            if i!='&':
                newlist.append(i)
            else:
                listsolutions.append(self.calculateSolutions(newlist))
                newlist.clear()
        return listsolutions


def is_identifier(word):
    return True if word[0].isalpha() and word[0].islower() else False

def write_comment(output,list):
    output.write('% ')
    for word in list[:-1]:
        output.write(word+' ')
    output.write(list[-1]+'.\n')

def write_identifiers(identifiers,output):
    output.write('{')
    for i in identifiers:
        output.write(i)
        if len(identifiers) > 1 and list(identifiers)[len(identifiers) - 1] != i: output.write(';')
    output.write('}.\n\n')

def write_output(list,output):
    for i in list:
        output.write(i)
        output.write('\n')
    output.write('\n')

def main():
    input = open("input.txt", "r")
    output = open('output.lp', 'w')
    num_lines = sum(1 for line in input)
    input.seek(0)

    lines = []

    for i in range(num_lines):
        auxline=[]
        line=input.readline().rstrip('\n')
        if line.strip():
            line = line[:-1]
            for i in line.split():
                auxline.append(i)
            lines.append(auxline)

    identifiers = set([])
    for words in lines:
        for word in words:
            if is_identifier(word):
                identifiers.add(word)
    write_identifiers(identifiers,output)

    print(lines)

    for words in lines:
        bst = BST()
        print("----------------------------- Input:")
        print(words)
        write_comment(output,words)
        for word in words:
            bst.insert(word)
        print("----------------------------- New Tree:")
        bst.printTree()

        print("----------------------------- Convert implication:")
        bst.convert_implication(bst.root)
        bst.printTree()
        print("----------------------------- Convert equivalence:")
        bst.convert_equivalence(bst.root)
        bst.printTree()
        print("----------------------------- Convert XOR:")
        bst.convert_xor(bst.root)
        bst.printTree()
        print("----------------------------- deMorgan:")
        bst.deMorgan(bst.root)
        bst.printTree()
        print("----------------------------- Simplify 0 1:")
        bst.eliminate10(bst.root)
        bst.printTree()
        print("----------------------------- Distribution:")
        bst.distribution(bst.root)
        bst.printTree()
        print("----------------------------- Final:")
        #bst.convert_disjunction(bst.root)
        bst.printTree()

        print("----------------------------- Output:")
        #newlist=bst.getlist()
        list_solutions=bst.doSolutions()
        print(list_solutions)
        #list_solutions=bst.getsolutions(bst.root)
        write_output(list_solutions,output)
        print("\n\n")

if __name__ =='__main__':
    main()