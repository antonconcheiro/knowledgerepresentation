import copy

class Node:
    def __init__(self,data):
        self.root=data
        self.left=None
        self.right=None

    def is_operator(self):
        symbols = ['&', '|', '-', '>', '=', '%', '0', '1']
        return True if any(self.root in s for s in symbols) else False

    def is_implication(self):
        return True if (self.root == '>') else False

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

    def negate(self,node):
        if node.root == "-":
            node.root = node.right.root
            node.left = node.right.left
            node.right = node.right.right
            return node
        else:
            newNode = Node(node.root)
            newNode.right = node.right
            newNode.left = node.left
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
                node.root = node.right.root
                node.left = node.right.left
                node.right = node.right.right
                self.convert_disjunction(node)
            if node.root == "-" and node.right is not None and node.right.root == "&":
                node.root = node.right.root
                node.left = node.right.left
                node.right = node.right.right
                self.convert_conjunction_once(node)
        if node.left is not None:
            self.simplify(node.left)
        if node.right is not None:
            self.simplify(node.right)

    def convert_implication(self,node):
        if node is not None:
            if node.root == ">":
                node.root = "|"
                #self.auxPrintTree(node.right)
                #print("arbol izquierdo")
                self.negate(node.left)
                #self.auxPrintTree(node.left)
                #print("arbol derecho")
                #self.negate(node.right)
                #self.auxPrintTree(node.right)
                #print("arbol total")
                #self.printTree()
                #print("-----------------------------")
                #self.simplify(node)
        if node.left is not None:
            self.convert_implication(node.left)
        if node.right is not None:
            self.convert_implication(node.right)

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
                print("found disjunction")
                node.root = "&"
                self.negate(node.left)
                print("arbol izquierdo")
                self.auxPrintTree(node.left)
                print("arbol derecho")
                self.negate(node.right)
                self.auxPrintTree(node.right)
                print("arbol total")
                self.printTree()
                print("-----------------------------")
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

    def distribution(self,node):
        if node is not None:
            if node.root=='|' and node.left is not None and node.right is not None and node.left.root=='&' and node.right.root=='&':
                node.root='&'
                tree1=Node('|')
                tree1.left=node.left.left
                tree1.right=node.right.left
                tree2 = Node('|')
                tree2.left = node.left.left
                tree2.right = node.right.right
                tree3 = Node('|')
                tree3.left = node.left.right
                tree3.right = node.right.left
                tree4 = Node('|')
                tree4.left = node.left.right
                tree4.right = node.right.right
                treeleft=Node('&')
                treeleft.left=tree1
                treeleft.right=tree2
                treeright = Node('&')
                treeright.left = tree3
                treeright.right = tree4
                node.left=treeleft
                node.right=treeright
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
                    solution=self.getsolutionsaux(node.left,solution)+';'
            if node.right is not None:
                if self.is_identifier(node.right) and node.right.root=='-':
                    solution=solution+node.right.right.root+', '
                elif self.is_identifier(node.right):
                    solution=solution+'not '+node.right.root+', '
                else:
                    solution=self.getsolutionsaux(node.right,solution)+';'
        return solution

    def getsolutions(self,node):
        result=set([])
        if node:
            solutions=self.getsolutionsaux(node,"").split(';')
            for solution in solutions[:-1]:
                if solution!="":
                    if not self.is_True(solution):
                        result.add(':- '+solution[:-2]+'.')
        return list(result)

def is_identifier(word):
    return True if word[0].isalpha() and word[0].islower() else False

def is_operator(self):
        symbols = ['&', '|', '-', '>', '=', '%', '0', '1']
        return True if any(self.root in s for s in symbols) else False

def write_comment(output,list):
    output.write('% ')
    for word in list[:-1]:
        output.write(word+' ')
    output.write(list[-1]+'.\n')

def write_identifiers(identifiers,output):
    #print(identifiers)
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
    input = open("p0.txt", "r")
    output = open('output.txt', 'w')
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
        print("----------------------------- deMorgan:")
        bst.deMorgan(bst.root)
        bst.printTree()
        print("----------------------------- Distribution:")
        bst.distribution(bst.root)
        bst.printTree()
        print("----------------------------- Final:")
        #bst.convert_disjunction(bst.root)
        bst.printTree()

        print("----------------------------- Output:")
        print(bst.getsolutions(bst.root))
        list_solutions=bst.getsolutions(bst.root)
        write_output(list_solutions,output)
        print("\n\n")

if __name__ =='__main__':
    main()