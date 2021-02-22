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
        return True if self.getid2()==None and self.getOperator()=='|' else False

    def deMorgan(self):
        if self.getOperator()=='|':
            tuple=Tuple(not self.getnotid1(),self.getid1(),not self.getnotid2(),self.getid2(),True,'&')
            return tuple
        elif self.getOperator()=='&':
            tuple = Tuple(not self.getnotid1(), self.getid1(), not self.getnotid2(), self.getid2(), True, '|')
            return tuple

    def simplify_Implication(self):
        tuple = Tuple(False, self.getid1(), self.getnotid2(),self.getid2(), True, '|')
        return tuple

    def simplify_Equivalence(self):
        if self.getid1().is_one_sided() and self.getid2().is_one_sided():
            tupleleft=Tuple(self.getid1().getnotid1(),self.getid1().getid1(),self.getid2().getnotid1(),self.getid2().getid1(),True,'&')
            tupleright=Tuple(not self.getid1().getnotid1(),self.getid1().getid1(),not self.getid2().getnotid1(),self.getid2().getid1(),True,'&')
            tuple=Tuple(True,tupleleft,True,tupleright,True,'|')
            return tuple
        else:
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
        if self.getOperator()=='|' and self.getid1().is_one_sided() and self.getid2().is_one_sided():
            tuple=Tuple(self.getid1().getnotid1(),self.getid1().getid1(),self.getid2().getnotid1(),self.getid2().getid1(),True,'|')
            return tuple

    def simplify(self):
        if self.getnotid1()!=self.getid1().getNegation():
            tupleleft=self.getid1().deMorgan()
        else:
            tupleleft=self.getid1()
        if self.getnotid2()!=self.getid2().getNegation():
            tupleright=self.getid2().deMorgan()
        else:
            tupleright=self.getid2()
        tuple = Tuple(tupleleft.getNegation(), tupleleft, tupleright.getNegation(), tupleright, self.getNegation(), self.getOperator())
        return tuple

    def expand(self):
        list = []
        if self.getOperator() == '|' and self.getid2().is_one_sided():
            tupleleft = Tuple(self.getid1().getnotid1(), self.getid1().getid1(), self.getid2().getnotid1(),
                              self.getid2().getid1(), True, self.getOperator())
            tupleright=Tuple(self.getid1().getnotid2(),self.getid1().getid2(),self.getid2().getnotid1(),self.getid2().getid1(),True,self.getOperator())
            #tuple=Tuple(tupleleft.getNegation(),tupleleft,tupleright.getNegation(),tupleright,True,'&')
            list.append(tupleleft)
            list.append(tupleright)
            return list
        elif self.getOperator() == '|':
            tuple1=Tuple(self.getid1().getnotid1(),self.getid1().getid1(),self.getid2().getnotid1(),self.getid2().getid1(),True,self.getOperator())
            tuple2=Tuple(self.getid1().getnotid1(),self.getid1().getid1(),self.getid2().getnotid2(),self.getid2().getid2(),True,self.getOperator())
            tuple3=Tuple(self.getid1().getnotid2(),self.getid1().getid2(),self.getid2().getnotid1(),self.getid2().getid1(),True,self.getOperator())
            tuple4=Tuple(self.getid1().getnotid2(),self.getid1().getid2(),self.getid2().getnotid2(),self.getid2().getid2(),True,self.getOperator())
            list.append(tuple1)
            list.append(tuple2)
            list.append(tuple3)
            list.append(tuple4)
            return list

    def generate_Statement(self):
        if self.getid1()==self.getid2() and self.getnotid1()!= self.getnotid2():
            return None
        elif self.getid1()==self.getid2() and self.getnotid1()== self.getnotid2():
            return ':- not '+self.getid1()+'.'
        elif self.getnotid1()==self.getnotid2() and self.getnotid1()==False:
            return ':- '+self.getid1()+', '+self.getid2()+'.'
        elif self.getnotid1() == self.getnotid2() and self.getnotid1() == True:
            return ':- not '+self.getid1()+', not '+self.getid2()+'.'
        elif self.getnotid1()==False:
            return ':- not '+self.getid1()+','+self.getid2()+'.'
        else:
            return ':- not '+self.getid1()+', '+self.getid2()+'.'

    def __repr__(self):
        return str(self.getNegation())+'('+str(self.getnotid1())+' '+str(self.getid1())+' '+self.getOperator()+' '+str(self.getnotid2())+' '+str(self.getid2())+')'

def is_operator(word):
    symbols = ['&', '|', '-', '>', '=', '%', '0', '1']
    return True if any(word in s for s in symbols) else False

def is_identifier(word):
    return True if word[0].isalpha() and word[0].islower() else False

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

def find_id1(words):
    if is_operator(words[0]) and words[0]!='-':
        build_Tuple(words[1:])
    elif words[0]=='-' and is_identifier(words[1]):
        return Tuple(Identifier(words[1],True),Identifier('False',True),False,'|')
    else:
        return Tuple(Identifier(words[0],True),Identifier('True',True),True,'|')

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
            tuple=Tuple(True,word,True,None,True,'|')
            stack.append(tuple)
        elif word == '-':
            prev_tuple=stack.pop()
            prev_tuple.setnotid1(False)
            stack.append(prev_tuple)
        elif word == '|':
            tuple1=stack.pop()
            tuple2=stack.pop()
            new_tuple=Tuple(tuple1.getNegation(),tuple1,tuple2.getNegation(),tuple2,True,'|')
            new_tuple2=new_tuple.simplify_or()
            stack.append(new_tuple2)
        elif word == '&':
            tuple1=stack.pop()
            tuple2=stack.pop()
            new_tuple=Tuple(tuple1.getNegation(),tuple1,tuple2.getNegation(),tuple2,True,'&')
            stack.append(new_tuple)
        elif word == '>':
            tuple1=stack.pop()
            tuple2=stack.pop()
            new_tuple=Tuple(tuple1.getNegation(),tuple1,tuple2.getNegation(),tuple2,True,'>')
            new_tuple2=new_tuple.simplify_Implication()
            stack.append(new_tuple2)
        elif word == '=':
            tuple1=stack.pop()
            tuple2=stack.pop()
            new_tuple=Tuple(tuple1.getNegation(),tuple1,tuple2.getNegation(),tuple2,True,'=')
            new_tuple2=new_tuple.simplify_Equivalence()
            stack.append(new_tuple2)
        elif word == '%':
            tuple1=stack.pop()
            tuple2=stack.pop()
            new_tuple=Tuple(tuple1.getNegation(),tuple1,tuple2.getNegation(),tuple2,True,'%')
            stack.append(new_tuple)
    return stack[0]

def convert_to_FNC(tuple):
    print(tuple)
    tuple=tuple.simplify()
    list=tuple.expand()
    print(list)
    return_list=[]
    for i in list:
        sentence=i.generate_Statement()
        if sentence!=None:
            return_list.append(sentence)
    return return_list

def analyze_phrase(phrase,output):
    phrase = phrase[:-1]
    words = phrase.split()

    write_comment(output,phrase)

    #build_Tuple(words)
    tuple=build_Iterator(words)
    list=convert_to_FNC(tuple)
    write_output(list,output)

def get_identifiers(phrase):
    identifiers = set([])
    phrase = phrase[:-1]
    words = phrase.split()
    for i in range(len(words)):
        if not is_operator(words[i]) and is_identifier(words[i]):
            identifiers.add(words[i])
    return identifiers

def main():
    input = open("p0.txt", "r")
    output = open('output.txt', 'w')
    num_lines = sum(1 for line in input)
    input.seek(0)

    lines = []

    for i in range(num_lines):
        line=input.readline().rstrip('\n')
        if line.strip():
            lines.append(line)

    identifiers=set([])
    for i in range(num_lines):
        new_identifiers=get_identifiers(lines[i])
        identifiers.update(new_identifiers)
    write_identifiers(identifiers,output)


    for i in range(num_lines):
        analyze_phrase(lines[i],output)

if __name__ =='__main__':
    main()