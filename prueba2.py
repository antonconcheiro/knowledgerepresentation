def is_operator(word):
    symbols = ['&', '|', '-', '>', '=', '%', '0', '1']
    return True if any(word in s for s in symbols) else False

def is_negator(word):
    return True if word == '-' else False

def is_identifier(word):
    return True if word[0].isalpha() and word[0].islower() else False

def get_identifiers(phrase):
    identifiers = set([])
    phrase = phrase[:-1]
    words = phrase.split()
    for i in range(len(words)):
        if not is_operator(words[i]) and is_identifier(words[i]):
            identifiers.add(words[i])
    return identifiers

def write_identifiers(identifiers,output):
    #print(identifiers)
    output.write('{')
    for i in identifiers:
        output.write(i)
        if len(identifiers) > 1 and list(identifiers)[len(identifiers) - 1] != i: output.write(';')
    output.write('}.\n\n')

def write_comment(output,phrase):
    output.write('% ')
    output.write(phrase)
    output.write('\n')

def stacking(words):
    wordsR = words[::-1]
    stack = []

    for word in wordsR:
        print(stack)
        if is_identifier(word):
            stack.append(word)
            print("adding identifier: ")
        elif is_negator(word):
            newWord = ("- " + stack.pop())
            stack.append(newWord)
            print("negating: " + newWord)
        elif is_operator(word):
            newWord = (stack.pop() + " " + word + " " + stack.pop())
            stack.append(newWord)
            print("concatenating: " + newWord)

    return stack


def analyze_phrase(phrase,output):
    phrase = phrase[:-1]
    words = phrase.split()

    write_comment(output,phrase)

    print(words)
    stacking(words)
    #build_Tuple(words)
    #tuple=build_Iterator(words)
    #list=convert_to_FNC(tuple)
    #write_output(list,output)

#def solver(words)


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