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
    def __init__(self,id1,id2,negation,operator):
        self.id1=id1
        self.id2=id2
        self.negation=negation
        self.operator=operator

    def getNegation(self):
        return self.negation

    def getOperator(self):
        return self.operator

    def setOperator(self,operator):
        self.operator=operator

    def setNegative(self):
        if not getNegation:
            self.negation=True
        else:
            self.negation=False

    def setPositive(self):
        self.negation=True

    def setid1(self,id1):
        self.id1=id1

    def setid2(self,id2):
        self.id2=id2

    def deMorgan(self):
        if not self.getNegation() and id1.getNegation() and id2.getNegation() and self.getOperator()=='|':
            self.setPositive()
            self.id1.setNegative()
            self.id2.setNegative()
            self.setOperator('&')
        elif not self.getNegation() and id1.getNegation() and id2.getNegation() and self.getOperator()=='&':
            self.setPositive()
            self.id1.setNegative()
            self.id2.setNegative()
            self.setOperator('|')

    def simplify_Implication(self):
        self.setOperator('|')
        self.id1.setNegative()

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

    def print_Tuple(self):
        print(self.operator+" "+str(self.id1.getNegation())+" "+self.id1.name+" "+str(self.id2.getNegation())+" "+self.id2.name)


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

def is_single_Identifier(self,identifier,words):
    position=words.index(identifiers[i])
    return False if words[position+1]=='-' or is_identifier(words[position+1]) else True

def is_Negated(self,identifier,words):
    position = words.index(identifiers[i])
    return True if position>0 and words[position - 1] == '-' else False

def identify_Tuples(words,identifiers):
    for i in words:
        if is_identifier(words[i]):
            if is_Negated(words[i],words):
                if is_single_Identifier(words[i],words):
                    

    if len(identifiers)%2 == 0:
        i=0
        while i < int(len(identifiers)):
            pos1=words.index(identifiers[i])
            if pos1>0 and words[pos1-1]=='-':
                id1 = Identifier(identifiers[i], False)
                operator = words[pos1-2]
            else:
                id1 = Identifier(identifiers[i], True)
                operator = words[pos1 - 1]
            pos2 = words.index(identifiers[i+1])
            if words[pos2 - 1] == '-':
                id2 = Identifier(identifiers[i+1], False)
            else:
                id2 = Identifier(identifiers[i+1], True)
            tuple=Tuple(id1,id2,True,operator)
            tuple.print_Tuple()
            i=i+2
    else:
        i=0
        while i < int(len(identifiers)):
            pos1 = words.index(identifiers[i])
            if pos1 > 0 and words[pos1 - 1] == '-':
                id1 = Identifier(identifiers[i], False)
                operator = words[pos1 - 2]
            else:
                id1 = Identifier(identifiers[i], True)
                operator = words[pos1 - 1]
            pos2 = words.index(identifiers[i + 1])
            if words[pos2 - 1] == '-':
                id2 = Identifier(identifiers[i + 1], False)
            else:
                id2 = Identifier(identifiers[i + 1], True)
            tuple = Tuple(id1, id2, True, operator)
            tuple.print_Tuple()
            i = i + 2



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

    identify_Tuples(words,identifiers)

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