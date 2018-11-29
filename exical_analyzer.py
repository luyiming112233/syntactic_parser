# 保留字
reserve_word = {
    'end': '0',
    'bool': '1',
    'char': '2',
    'class': '3',
    'double': '4',
    'else': '5',
    'false': '6',
    'if': '7',
    'int': '8',
    'private': '9',
    'protected': '10',
    'public': '11',
    'return': '12',
    'true': '13',
    'void': '14',
    'while': '15',

}
# 界符
delimiter = {
    '(': '17',
    ')': '18',
    ',': '19',
    ';': '20',
    '[': '21',
    ']': '22',
    '{': '23',
    '}': '24',
}
# 运算符
operator = {
    '-': '25',
    '*': '26',
    '/': '27',
    '+': '28',
    '<': '29',
    '<=': '30',
    '=': '31',
    '>': '32',
    '>=': '33',
    '==': '34',
}
# 标识符
identiflier = {}
# 数字
num = {}
output = {}


# 字符串预处理，去掉注释
def preprocessing(lines):
    L = []
    for line in lines:
        index = line.find('//')
        line = line[0:index]
        if line != '':
            L.append(line)
    return L


# 查找保留字
def searchReserve(word):
    return reserve_word.get(word)


def judgeChara(ch):
    if ch == ' ' or ch.isdigit() or ch.isalpha() or operator.get(ch) or delimiter.get(ch) or ch == '.':
        return True
    print("出现错误字符"+ch)
    return False



# 单行字符串词法分析
def lexical_analysis(line):
    for m in line:
        if judgeChara(m) == False:
            return False
    length = len(line)
    i = 0
    ch = line[i]
    while i + 1 < length:  # 最后会多一个换行符
        if not i == 0:  # 除了第一个字符，每次开始寻找单词时，将ch初始化为' '
            ch = ' '
        word = ''
        while ch == ' ':
            i = i + 1
            if i + 1 > length:
                break
            ch = line[i]
        # 开头是字母
        if ch.isalpha():
            word = word + ch
            i = i + 1
            ch = line[i]
            while ch.isalpha() or ch.isdigit():
                word = word + ch
                i = i + 1
                if i + 1 > length:
                    break
                ch = line[i]
            if searchReserve(word) == None:  # 如果无法在保留字中找到，那么为标识符
                if len(word) >= 6:
                    word = word[0:6]
                output[word] = '100'
                identiflier[word] = '100'
            else:
                output[word] = searchReserve(word)

        # 开头是数字
        elif ch.isdigit():
            word = word + ch
            i = i + 1
            ch = line[i]
            while ch.isdigit() or ch == '.':
                word = word + ch
                i = i + 1
                if i + 1 > length:
                    break
                ch = line[i]
            output[word] = '99'
            num[word] = '99'

        # 是界符
        elif delimiter.get(ch):
            output[ch] = delimiter[ch]

        # 是运算符
        elif operator.get(ch):
            if i + 1 < length and operator.get(line[i + 1:i + 2]):  # 判断是否是两位的运算符
                ch2 = line[i:i + 2]
                if operator.get(ch2):
                    i = i + 1
                    output[ch2] = operator[ch2]
            else:
                output[ch] = operator[ch]


def main():
    with open('test.txt') as file:
        lines = file.readlines()
    lines = preprocessing(lines)
    print('输出预处理后的代码')
    for line in lines:
        print(line)
    for line in lines:
        if lexical_analysis(line) == False:
            print("错误行："+line)
    print('---------------------------------------------------')
    print('输出所有单词')
    for key in output:
        print("( "+key + ':' + output[key]+" )")
    print('输出所有标识符')
    for key in identiflier:
        print("( "+key + ':' + identiflier[key]+" )")
    print('输出所有数字')
    for key in num:
        print("( "+key + ':' + num[key]+" )")


if __name__ == '__main__':
    main()
