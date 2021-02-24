class Node:
    def __init__(self,data):
        self.root=data
        self.left=None
        self.right=None

    def is_operator(self):
        symbols = ['&', '|', '-', '>', '=', '%', '0', '1']
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
            node.right=Node(data)
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

    def printTree(self):
        if self.root is not None:
            self.auxPrintTree(self.root)

    def auxPrintTree(self,node):
        if node is not None:
            self.auxPrintTree(node.left)
            print(node.root+' ')
            self.auxPrintTree(node.right)

def is_identifier(word):
    return True if word[0].isalpha() and word[0].islower() else False

def is_operator(self):
        symbols = ['&', '|', '-', '>', '=', '%', '0', '1']
        return True if any(self.root in s for s in symbols) else False

def write_comment(output,phrase):
    output.write('% ')
    output.write(phrase)
    output.write('\n')

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
        line=input.readline().rstrip('\n')
        if line.strip():
            line = line[:-1]
            for i in line.split():
                lines.append(i)

    print(lines)
    bst=BST()

    identifiers = set([])
    for i in lines:
        if is_identifier(i):
        	identifiers.add(i)
    write_identifiers(identifiers,output)

    for i in lines:
        bst.insert(i)
    bst.printTree()

if __name__ =='__main__':
    main()