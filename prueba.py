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

def next_term(words):
    words.pop(0)
    return words[0]


def analyze_phrase(phrase,output):
    identifiers = []

    words = phrase.split()
    for i in range(len(words)):
        if not is_operator(words[i]) and is_identifier(words[i]):
            identifiers.append(words[i])

    num_identifiers = len(identifiers)
    if num_identifiers>0:
        write_identifiers(output,identifiers,num_identifiers)
        write_comment(output,phrase)

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