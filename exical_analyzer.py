# 保留字
reserve_word = {

}
# 界符
delimiter = {
    '#': -1,
    '(': 1,
    ')': 2,
}
# 运算符
operator = {
    '-': 3,
    '*': 4,
    '/': 5,
    '+': 6,
    '=': 7
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
    print("出现错误字符" + ch)
    return False


# 单行字符串词法分析(单独用于词法分析)
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
                # 往下多读一个
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
            i = i - 1

        # 开头是数字
        elif ch.isdigit():
            word = word + ch
            i = i + 1
            ch = line[i]
            while ch.isdigit() or ch == '.':
                word = word + ch
                # 往下多读一个
                i = i + 1
                if i + 1 > length:
                    break
                ch = line[i]
            output[word] = '99'
            num[word] = '99'
            i = i - 1

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


# 应用于语法分析的词法分析函数，对每一行返回一个字典，记录单词信息
def getLexicalAnalysisDict(line):
    line = line + " "
    Dict = {}
    wordID = 0
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
            if ch.isalpha() or ch.isdigit():
                while ch.isalpha() or ch.isdigit():
                    word = word + ch
                    i = i + 1
                    if i + 1 > length:
                        break
                    ch = line[i]
            if searchReserve(word) == None:  # 如果无法在保留字中找到，那么为标识符
                if len(word) >= 6:
                    word = word[0:6]
                Dict[wordID] = ['i', 100, 0, word]
            else:
                Dict[wordID] = [word, reserve_word[word], 'null', word]
            i = i - 1
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
            Dict[wordID] = ['i', 99, int(word), 'num']
            i = i - 1  # 读入无用字符，回退一位

        # 是界符
        elif delimiter.get(ch):
            Dict[wordID] = [ch, delimiter[ch], "null", ch]

        # 是运算符
        elif operator.get(ch):
            if i + 1 < length and operator.get(line[i + 1:i + 2]):  # 判断是否是两位的运算符
                ch2 = line[i:i + 2]
                if operator.get(ch2):
                    i = i + 1
                    Dict[wordID] = [ch2, operator[ch2], "null", ch2]
            else:
                Dict[wordID] = [ch, operator[ch], "null", ch]
        wordID = wordID + 1
    return Dict


# 提供给语法分析的词法分析接口：输入文件名，以列表的形式返回词法分析结果
def get_exical_analyze_list(filename):
    with open(filename) as file:
        lines = file.readlines()
    lines = preprocessing(lines)
    noError = True
    wordList = []
    for line in lines:
        value = getLexicalAnalysisDict(line)
        if value == False:
            noError = False
            print("错误行：" + line)
        wordList.append(value)
    return wordList


def main():
    with open('test.txt') as file:
        lines = file.readlines()
    lines = preprocessing(lines)
    print('输出预处理后的代码')
    for line in lines:
        print(line)
    for line in lines:
        if lexical_analysis(line) == False:
            print("错误行：" + line)
    print('---------------------------------------------------')
    print('输出所有单词')
    for key in output:
        print("( " + key + ':' + output[key] + " )")
    print('输出所有标识符')
    for key in identiflier:
        print("( " + key + ':' + identiflier[key] + " )")
    print('输出所有数字')
    for key in num:
        print("( " + key + ':' + num[key] + " )")


if __name__ == '__main__':
    # main()
    a = get_exical_analyze_list('test.txt')
    for v in a:
        print(v)
