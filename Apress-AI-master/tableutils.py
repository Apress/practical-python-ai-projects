
import copy
def flatten(l):
    return [e for s in l for e in s]
def set2string(S):
    s='{ '
    if S is not None:
      for i in range(len(S)):
          s=s+str(S[i])
          if i < len(S)-1:
            s=s+'; '
          else:
            s=s+' '
    s=s+'}'
    return s
def wrapmat(M,left,header):
    T=copy.deepcopy(M)
    m,n=len(T),len(T[0])
    for i in range(len(left)):
        T[i].insert(0,left[i]);
    if header != None:
      if len(header) < len(T[0]):
        T.insert(0,['']+header)
      else:
        T.insert(0,header)
    return T
def formatmat(M,zeroes=False,decimals=4):
    T=copy.deepcopy(M)
    for i in range(len(M)):
        for j in range(len(M[i])):
            el = T[i][j]
            if type(el)==int:
                if el or zeroes:
                    el = '{0:4d}'.format(el)
                else:
                    el = ''
                T[i][j] = el
            elif type(el)==float:
                if el or zeroes :
                    if decimals==4:
                        el = '{0:.4f}'.format(el)
                    elif decimals==3:
                        el = '{0:.3f}'.format(el)
                    elif decimals==2:
                        el = '${0:.2f}'.format(el)
                    elif decimals==1:
                        el = '{0:.1f}'.format(el)
                    elif decimals==0:
                        el = '{0:.0f}'.format(el)
                else:
                    el = ''
                T[i][j] = el
            elif el is None:
                el = ''
                T[i][j] = el
    return T
def printmat(M,zeroes=False,decimals=4):
    T = formatmat(M,zeroes,decimals)
    output = []
    for row in T:
        l=''
        for i in range(len(row)):
            l = l+str(row[i])
            if i < len(row)-1:
                l=l+','
        print(l)
  
def splitwrapmat(M,left,header):
    T=wrapmat(M,left,None)
    if len(T) % 2:
        T.append([])
    T2 = [T[i]+T[i+1] for i in range(0,len(T),2)]
    return wrapmat(T2,[],header+header)
