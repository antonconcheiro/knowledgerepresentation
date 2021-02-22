class Identifier:
    def __init__(self,name,negation):
        self.name=name
        self.negation=negation

    def getNegation(self):
        return self.negation

    def setPositive(self):
        self.negation=True

    def setNegative(self):
        if not self.getNegation():
            self.negation=True
        else:
            self.negation=False

class Tuple:
    def __init__(self,notid1,id1,notid2,id2,negation,operator):
        self.id1=id1
        self.notid1=notid1
        self.id2=id2
        self.notid2=notid2
        self.negation=negation
        self.operator=operator

    def getNegation(self):
        return self.negation

    def getOperator(self):
        return self.operator

    def setOperator(self,operator):
        self.operator=operator

    def setNegative(self):
        if not self.getNegation():
            self.negation=True
        else:
            self.negation=False

    def setPositive(self):
        self.negation=True

    def getid1(self):
        return self.id1

    def getid2(self):
        return self.id2

    def setid1(self,id1):
        self.id1=id1

    def setid2(self,id2):
        self.id2=id2

    def getnotid1(self):
        return self.notid1

    def setnotid1(self,value):
        if value==False and self.notid1==False:
            self.notid1=True
        else:
            self.notid1=value

    def getnotid2(self):
        return self.notid2

    def setnotid2(self,value):
        if value == False and self.notid2 == False:
            self.notid2 = True
        else:
            self.notid2 = value

    def is_one_sided(self):
        return True if self.getid2()==None and self.getOperator()=='V' else False

    def deMorgan(self):
        if not self.getNegation() and self.getnotid1() and self.getnotid2() and self.getOperator()=='|':
            self.setPositive()
            self.setnotid1(False)
            self.setnotid2(False)
            self.setOperator('&')
        elif not self.getNegation() and self.getnotid1() and self.getnotid2() and self.getOperator()=='&':
            self.setPositive()
            self.setnotid1(False)
            self.setnotid2(False)
            self.setOperator('|')

    def simplify_Implication(self):
        self.setOperator('|')
        self.setnotid1(False)

    def simplify_Equivalence(self):
        result1=Tuple(id1,id2,True,'>')
        result2=Tuple(id2,id1,True,'>')
        self.setid1(result1.simplify_Implication())
        self.setid2(result2.simplify_Implication())
        self.setPositive()
        self.setOperator('&')

    def simplify_xor(self):
        result1=Tuple(id1,id2,False,'&')
        result2=Tuple(id1,id2,True,'|')
        self.setid1(result1)
        self.setid2(result2)
        self.setOperator('&')

    def simplify_or(self):
        if self.getOperator()=='V' and self.getid1().is_one_sided() and self.getid2().is_one_sided():
            tuple=Tuple(self.getnotid1(),self.getid1().getid1(),self.getnotid2(),self.getid2().getid1(),True,'V')

def is_operator(word):
    symbols = ['&', '|', '-', '>', '=', '%', '0', '1']
    return True if any(word in s for s in symbols) else False

def is_identifier(word):
    return True if word[0].isalpha() and word[0].islower() else False

def write_comment(output,phrase):
    output.write('% ')
    output.write(phrase)
    output.write('\n\n')

def write_identifiers(output,identifiers,num_identifiers):
    output.write('{')
    for i in identifiers:
        output.write(i)
        if num_identifiers > 1 and identifiers[num_identifiers - 1] != i: output.write(';')
    output.write('}.\n\n')

def find_id1(words):
    if is_operator(words[0]) and words[0]!='-':
        build_Tuple(words[1:])
    elif words[0]=='-' and is_identifier(words[1]):
        return Tuple(Identifier(words[1],True),Identifier('False',True),False,'V')
    else:
        return Tuple(Identifier(words[0],True),Identifier('True',True),True,'V')

def find_id2():
    pass

def build_Tuple(words):
    if is_operator(words[0]) and words[0]!='-':
        id1=find_id1(words[1:])
        tuple=Tuple(id1,find_id2(),True,words[0])
        return tuple
    elif is_identifier(words[0]):
        id2=find_id1(words[1:])

def build_Iterator(words):
    reverse_List=words[::-1]
    stack=[]
    for word in reverse_List:
        if is_identifier(word):
            tuple=Tuple(True,word,True,None,True,'V')
            stack.append(tuple)
        elif word == '-':
            prev_tuple=stack.pop()
            prev_tuple.setnotid1(False)
            stack.append(prev_tuple)
        elif word == '|':
            tuple1=stack.pop()
            tuple2=stack.pop()
            new_tuple=Tuple(tuple1.getNegation(),tuple1,tuple2.getNegation(),tuple2,True,'V')
            new_tuple.simplify_or()
            stack.append(new_tuple)
        elif word == '&':
            tuple1=stack.pop()
            tuple2=stack.pop()
            new_tuple=Tuple(tuple1.getNegation(),tuple1,tuple2.getNegation(),tuple2,True,'&')
            stack.append(new_tuple)
        elif word == '>':
            tuple1=stack.pop()
            tuple2=stack.pop()
            new_tuple=Tuple(tuple1.getNegation(),tuple1,tuple2.getNegation(),tuple2,True,'>')
            new_tuple.simplify_Implication()
            stack.append(new_tuple)
        elif word == '=':
            tuple1=stack.pop()
            tuple2=stack.pop()
            new_tuple=Tuple(tuple1.getNegation(),tuple1,tuple2.getNegation(),tuple2,True,'=')
            new_tuple.simplify_Equivalence()
            stack.append(new_tuple)
        elif word == '%':
            tuple1=stack.pop()
            tuple2=stack.pop()
            new_tuple=Tuple(tuple1.getNegation(),tuple1,tuple2.getNegation(),tuple2,True,'%')
            stack.append(new_tuple)
    return stack[0]

def analyze_phrase(phrase,output):
    identifiers = []

    phrase=phrase[:-1]
    words = phrase.split()
    for i in range(len(words)):
        if not is_operator(words[i]) and is_identifier(words[i]) and not any(words[i] in s for s in identifiers):
            identifiers.append(words[i])

    num_identifiers = len(identifiers)
    if num_identifiers>0:
        write_identifiers(output,identifiers,num_identifiers)
        write_comment(output,phrase)

    #build_Tuple(words)
    build_Iterator(words)

def main():
    input = open("p0.txt", "r")
    output = open('output.txt', 'w')
    num_lines = sum(1 for line in input)
    input.seek(0)

    lines = []

    for i in range(num_lines):
        lines.append(input.readline().rstrip('\n'))
        analyze_phrase(lines[i],output)

if __name__ =='__main__':
    main()