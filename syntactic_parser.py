import numpy as np

terminalSymbolSet = set()
nonTerminalSymbolSet = set()
TSDict = {}
NTSDict = {}
transDict = {0: " ", 1: "<", 2: "=", 3: ">"}


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
    opePreMat = np.zeros((TSsize+1, TSsize+1))  # 0:没有关系 1:小于 2：等于 3：大于
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
    return opePreMat


def displayOpePreMat(opePreMat):
    print(opePreMat)
    TSsize = len(terminalSymbolSet)
    str = "   "
    for ch in TSDict.keys():
        str = str + ch + "  "
    print(str+"#")
    for ch in TSDict.keys():
        str = ch + "  "
        for i in range(TSsize):
            str = str+transDict[opePreMat[TSDict[ch]][i]]+"  "
        print(str+transDict[opePreMat[TSDict[ch]][-1]])
    str = "#  "
    for i in range(TSsize):
        str = str+transDict[opePreMat[-1][i]]+"  "
    print(str)


def main():
    with open('grammar.txt') as file:
        grammers = file.readlines()
    loadSymbol(grammers)
    NTSsize = len(nonTerminalSymbolSet)
    TSsize = len(terminalSymbolSet)
    FIRSTOP = getFIRSTOP(grammers)
    LASTOP = getLASTOP(grammers)
    displayFIRSTOP(FIRSTOP)
    displayLASTOP(LASTOP)
    opePreMat = getOperatorPrecedenceMatrix(grammers, FIRSTOP, LASTOP)
    displayOpePreMat(opePreMat)


if __name__ == '__main__':
    main()