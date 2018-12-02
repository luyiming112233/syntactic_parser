import numpy as np
from exical_analyzer import get_exical_analyze_list
from exical_analyzer import delimiter
from exical_analyzer import operator
from Stack import Stack
import time

terminalSymbolSet = set()
nonTerminalSymbolSet = set()
TSDict = {}
NTSDict = {}
transDict = {0: " ", 1: "<", 2: "=", 3: ">"}
identiflier = {}


def loadSymbol(grammers):
    for line in grammers:
        nonTerminalSymbolSet.add(line[0])
        i = 3
        while i < len(line):
            terminalSymbolSet.add(line[i])
            i = i + 1
    num = 0
    nonTerminalSymbolList = list(nonTerminalSymbolSet)
    nonTerminalSymbolList.sort()  # 使集合当中的字符有唯一顺序
    for ch in nonTerminalSymbolList:
        terminalSymbolSet.discard(ch)
        NTSDict[ch] = num
        num = num + 1
    terminalSymbolSet.discard('\n')
    terminalSymbolSet.discard('|')
    num = 0
    terminalSymbolList = list(terminalSymbolSet)
    terminalSymbolList.sort()
    for ch in terminalSymbolList:
        TSDict[ch] = num
        num = num + 1
    TSDict['#'] = num


def getFIRSTOP(grammers):
    NTSsize = len(nonTerminalSymbolSet)
    TSsize = len(terminalSymbolSet)
    FRISTOP = np.zeros((NTSsize, TSsize))
    stack = []  # 栈，用于计算FIRSTOP
    for line in grammers:
        nts = line[0]
        right = line[3:-1]  # 去掉换行符
        for part in right.split('|'):
            fix_part = part
            if len(part) > 1:  # 如果右部只有一个
                fix_part = part[:-1]
            for ch in fix_part:
                if ch in TSDict.keys():
                    FRISTOP[NTSDict[nts]][TSDict[ch]] = 1
                    stack.append([nts, ch])
    # 直到栈为空结束
    while stack:
        temp = stack.pop()
        ntsB = temp[0]
        ts = temp[1]
        for line in grammers:
            ntsA = line[0]
            right = line[3:-1]  # 去掉换行符
            for part in right.split('|'):
                if part[0] == ntsB and ntsA != ntsB:  # 满足A->B…
                    stack.append([ntsA, ts])
                    FRISTOP[NTSDict[ntsA]][TSDict[ts]] = 1
    return FRISTOP


def getLASTOP(grammers):
    NTSsize = len(nonTerminalSymbolSet)
    TSsize = len(terminalSymbolSet)
    LASTOP = np.zeros((NTSsize, TSsize))
    stack = []  # 栈，用于计算LASTOP
    for line in grammers:
        nts = line[0]
        right = line[3:-1]  # 去掉换行符
        for part in right.split('|'):
            fix_part = part
            if len(part) > 1:  # 如果右部只有一个
                fix_part = part[1:]
            for ch in fix_part:
                if ch in TSDict.keys():
                    LASTOP[NTSDict[nts]][TSDict[ch]] = 1
                    stack.append([nts, ch])
    # 直到栈为空结束
    while stack:
        temp = stack.pop()
        ntsB = temp[0]
        ts = temp[1]
        for line in grammers:
            ntsA = line[0]
            right = line[3:-1]  # 去掉换行符
            for part in right.split('|'):
                if part[-1] == ntsB and ntsA != ntsB:  # 满足A->…B
                    stack.append([ntsA, ts])
                    LASTOP[NTSDict[ntsA]][TSDict[ts]] = 1
    return LASTOP


def displayFIRSTOP(FIRSTOP):
    for nts in NTSDict.keys():
        str = "FIRSTOP(" + nts + ")={"
        t = 0
        for ts in TSDict.keys():
            if FIRSTOP[NTSDict[nts]][TSDict[ts]] == 1:
                if t == 0:
                    str = str + ts
                    t = 1
                else:
                    str = str + "," + ts
        str = str + "}"
        print(str)


def displayLASTOP(LASTOP):
    for nts in NTSDict.keys():
        str = "LASTOP(" + nts + ")={"
        t = 0
        for ts in TSDict.keys():
            if LASTOP[NTSDict[nts]][TSDict[ts]] == 1:
                if t == 0:
                    str = str + ts
                    t = 1
                else:
                    str = str + "," + ts
        str = str + "}"
        print(str)


def getOperatorPrecedenceMatrix(grammers, FIRSTOP, LASTOP):
    TSsize = len(terminalSymbolSet)
    opePreMat = np.zeros((TSsize + 1, TSsize + 1))  # 0:没有关系 1:小于 2：等于 3：大于
    for line in grammers:
        right = line[3:-1]  # 去掉换行符
        for part in right.split('|'):
            for i in range(len(part) - 1):
                # A->…ab…
                if part[i] in TSDict.keys() and part[i + 1] in TSDict.keys():
                    opePreMat[TSDict[part[i]]][TSDict[part[i + 1]]] = 2
                # A->…aBb…
                elif i < len(part) - 2 and part[i] in TSDict.keys() and part[i + 1] in NTSDict.keys() and part[
                    i + 2] in TSDict.keys():
                    opePreMat[TSDict[part[i]]][TSDict[part[i + 2]]] = 2
                # A->…aB…
                if part[i] in TSDict.keys() and part[i + 1] in NTSDict.keys():
                    for j in range(TSsize):
                        if FIRSTOP[NTSDict[part[i + 1]]][j] == 1:
                            opePreMat[TSDict[part[i]]][j] = 1
                # A->…Ba…
                elif part[i] in NTSDict.keys() and part[i + 1] in TSDict.keys():
                    for j in range(TSsize):
                        if LASTOP[NTSDict[part[i]]][j] == 1:
                            opePreMat[j][TSDict[part[i + 1]]] = 3
    for i in range(TSsize):
        opePreMat[-1][i] = 1
        opePreMat[i][-1] = 3
    opePreMat[-1][-1] = 2
    return opePreMat


def displayOpePreMat(opePreMat):
    print(opePreMat)
    TSsize = len(terminalSymbolSet)
    str = "   "
    for ch in TSDict.keys():
        str = str + ch + "  "
    print(str)
    for ch in TSDict.keys():
        str = ch + "  "
        for i in range(TSsize):
            str = str + transDict[opePreMat[TSDict[ch]][i]] + "  "
        print(str + transDict[opePreMat[TSDict[ch]][-1]])


def MainProc_Analysis(line_words):
    my_stack = Stack()
    temp_stack = Stack()
    W0 = ['#', -1, 'null', '#']  # 第一个压入'#'
    my_stack.push(W0)
    temp_word = W0
    for wo in line_words:
        word = line_words[wo]
        if word[3] in identiflier.keys():
            word[2] = identiflier[word[3]]
        print('-------------------------')
        print('word', wo, line_words[wo])
        peek_word = my_stack.peek()
        k = my_stack.size() - 1
        while k > -1:
            if my_stack.items[k][1] in [0, 1, 2, 3, 4, 5, 6, 7, 99, 100]:
                temp_word = my_stack.items[k]
                break
            k = k - 1
        if myOpePreMat[TSDict[temp_word[0]]][TSDict[word[0]]] == 1:
            my_stack.push(word)
            print('添加了新的字符', word[0])
            my_stack.display()
        elif myOpePreMat[TSDict[temp_word[0]]][TSDict[word[0]]] == 2:
            if temp_word[0] == '#' and word[0] == '#':
                if my_stack.size() == 2:
                    print('value', peek_word[2])
                    return True
                else:
                    return False
            else:
                my_stack.push(word)
                print('添加了新的字符', word[0])
                my_stack.display()
        elif myOpePreMat[TSDict[temp_word[0]]][TSDict[word[0]]] == 3:
            prior_Relation = 3
            temp_word = my_stack.peek()
            newN = ['N', -1, 0, '']
            # 进行规约
            while prior_Relation == 3:
                judge = temp_word[1]
                if judge in [99, 100]:  # 判断栈顶元素是否是标识符或者数字，规约为N
                    newN[2] = temp_word[2]
                    newN[1] = 0 - judge  # 将的值取反
                    my_stack.pop()
                    my_stack.push(newN)
                    print("将栈顶的标识符/数字归约为N")

                # 加法归约
                if judge == 6:  # N1+N2
                    N2 = my_stack.pop()
                    Nadd = my_stack.pop()
                    N1 = my_stack.pop()
                    if Nadd[1] != 6:
                        print("加号归约错误")
                    N1[2] = N1[2] + N2[2]
                    my_stack.push(N1)
                    print("加号归约")

                # 减法归约
                if judge == 3:  # N1-N2
                    N2 = my_stack.pop()
                    Nsub = my_stack.pop()
                    N1 = my_stack.pop()
                    if Nsub[1] != 3:
                        print("减号归约错误")
                    N1[2] = N1[2] - N2[2]
                    my_stack.push(N1)
                    print("减号归约")

                # 乘法归约
                if judge == 4:  # N1*N2
                    N2 = my_stack.pop()
                    Nmul = my_stack.pop()
                    N1 = my_stack.pop()
                    if Nmul[1] != 4:
                        print("乘号归约错误")
                    N1[2] = N1[2] * N2[2]
                    my_stack.push(N1)
                    print("乘号归约")

                # 除法归约
                if judge == 5:  # N1*N2
                    N2 = my_stack.pop()
                    Ndiv = my_stack.pop()
                    N1 = my_stack.pop()
                    if Ndiv[1] != 5:
                        print("除号归约错误")
                    N1[2] = N1[2] / N2[2]
                    my_stack.push(N1)
                    print("除号归约")

                # 右括号归约
                if judge == 2:  # (N)
                    Nright = my_stack.pop()
                    N = my_stack.pop()
                    Nleft = my_stack.pop()
                    if Nright[1] != 2:
                        print("括号归约错误")
                    my_stack.push(N)
                    print("括号归约")

                # 等号归约
                if judge == 7:  # N1=N2
                    N2 = my_stack.pop()
                    Neq = my_stack.pop()
                    N1 = my_stack.pop()
                    if Neq[1] != 7 and not N1[1] in [100, -100]:
                        print("等号归约错误")
                    else:
                        N1[2] = N2[2]
                        identiflier[N1[3]] = N1[2]
                        print('identiflier', identiflier)
                        print('N1', N1)
                        print('N2', N2)
                    my_stack.push(N1)
                    print("等号归约")

                # 更新temp_word
                k = my_stack.size() - 1
                while (k > -1):
                    if my_stack.items[k][1] in [-1, 0, 1, 2, 3, 4, 5, 6, 7, 99, 100]:
                        temp_word = my_stack.items[k]
                        break
                    k = k - 1
                prior_Relation = myOpePreMat[TSDict[temp_word[0]]][TSDict[word[0]]]
                my_stack.display()
            # 规约结束后，添加字符
            if prior_Relation == 2:
                if temp_word[0] == '#' and word[0] == '#':
                    if my_stack.size() == 2:
                        print('---------------------------------')
                        print('归约成功')
                        print('value', my_stack.peek()[2])
                        return True
                    else:
                        return False
            my_stack.push(word)
            print('添加了新的字符', word[0])
            my_stack.display()


def main():
    with open('grammar.txt') as file:
        grammers = file.readlines()
    loadSymbol(grammers)
    NTSsize = len(nonTerminalSymbolSet)
    TSsize = len(terminalSymbolSet)
    print(TSDict)
    FIRSTOP = getFIRSTOP(grammers)
    LASTOP = getLASTOP(grammers)
    # displayFIRSTOP(FIRSTOP)
    # displayLASTOP(LASTOP)
    global myOpePreMat
    myOpePreMat = getOperatorPrecedenceMatrix(grammers, FIRSTOP, LASTOP)
    displayOpePreMat(myOpePreMat)
    lines = get_exical_analyze_list('test.txt')
    for line in lines:
        MainProc_Analysis(line)
    print(identiflier)


if __name__ == '__main__':
    main()
