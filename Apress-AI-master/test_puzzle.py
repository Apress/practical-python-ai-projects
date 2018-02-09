
from my_or_tools   import newSolver, SolVal
from puzzle import solve_maxrook, solve_maxpiece, solve_sudoku, solve_smm, solve_lady_or_tiger
def main():
    import sys, random, tableutils, time
    if len(sys.argv)<=1:
        print('Usage is main [maxrook|rook|queen|bishop|sudoku|sudokus|smm|lady] [seed]')
        return
    elif len(sys.argv)>=2:
        n = int(sys.argv[2])
        header = [i+1 for i in range(n)]
    if sys.argv[1]=='maxrook':
        rc,x = solve_maxrook(n)
        tableutils.printmat(tableutils.wrapmat(x,header,header))
    elif sys.argv[1]=='rook':
        rc,x = solve_maxpiece(n,'R')
        tableutils.printmat(tableutils.wrapmat(x,header,header))
    elif sys.argv[1]=='queen':
        rc,x = solve_maxpiece(n,'Q')
        tableutils.printmat(tableutils.wrapmat(x,header,header))
    elif sys.argv[1]=='bishop':
        rc,x = solve_maxpiece(n,'B')
        tableutils.printmat(tableutils.wrapmat(x,header,header))
    elif sys.argv[1]=='sudoku':
        G = [[None,None,None,2   ,6   ,None,7   ,None,1   ],
             [6   ,8   ,None,None,7   ,None,None,9   ,None],
             [1   ,9   ,None,None,None,4   ,5   ,None,None],
             [8   ,2   ,None,1   ,None,None,None,4,   None],
             [None,None,4   ,6   ,None,2   ,9   ,None,None],
             [None,5   ,None,None,None,3   ,None,2   ,8   ],
             [None,None,9   ,3   ,None,None,None,7   ,4   ],
             [None,4   ,None,None,5   ,None,None,3   ,6   ],
             [7   ,None,3   ,None,1   ,8   ,None,None,None]]
        f = open('sudoku17.txt')
        #f = open('top1465.txt')
        G=[[0 for _ in range(9)] for _ in range(9)]
        for i in range(n):
            l = f.readline()
        l=f.readline()
        f.close()
        for i in range(9):
            for j in range(9):
                G[i][j] = int(l[i*9+j]) if l[i*9+j]>='1' and l[i*9+j]<='9' else None
        rc,x = solve_sudoku(G)
        #tableutils.printmat(tableutils.wrapmat(x,header,header))
        if rc != 0:
            tableutils.printmat(G)
        else:
            xx=[]
            for i in range(len(G)):
                row=[]
                for j in range(len(G[0])):
                    if G[i][j]:
                        row.append('*'+str(G[i][j])+'*')
                    else:
                        row.append(x[i][j])
                xx.append(row)
            tableutils.printmat(xx,False,0)
    elif sys.argv[1]=='sudokus':
        #f = open('sudoku17.txt')
        count = 0
        with open('top1465.txt') as f:
            for l in f:
                count += 1
                #if count > 10:
                #    break
                G=[[0 for _ in range(9)] for _ in range(9)]
                for i in range(9):
                    for j in range(9):
                        G[i][j] = int(l[i*9+j]) if l[i*9+j]>='1' and l[i*9+j]<='9' else None
                start = time.clock()
                rc,x = solve_sudoku(G)
                end = time.clock()
                if rc != 0:
                    print(count, 'WTF!!!!!!!')
                print('{0:06d},{1:8.0f}'.format(count,(end-start)*1000))
    elif sys.argv[1]=='smm':
        rc,x = solve_smm()
        if rc == 0:
            x = [['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y'],x]
            tableutils.printmat(x,True,0)
        else:
            print('Infeasible')
    elif sys.argv[1]=='smm':
        rc,x = solve_smm()
        if rc == 0:
            x = [['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y'],x]
            tableutils.printmat(x,True,0)
        else:
            print('Infeasible')
    elif sys.argv[1]=='lady':
        STA=["The lady is in an odd-numbered room.",
             "This room is empty.",
             "Either sign 5 is right or sign 7 is wrong.",
             "Sign 1 is wrong.",
             "Either sign 2 or sign 4 is right.",
             "Sign 3 is wrong.",
             "The lady is not in room 1.",
             "This room contains a tiger and room 9 is empty.",
             "This room contains a tiger and sign 6 is wrong."]

        rc,S,R = solve_lady_or_tiger()
        if rc == 0:
            x=[]
            for i in range(9):
                x.append([i+1,STA[i],['False','True'][int(S[i])], ['','Lady','Tiger'][int(R[i][0])]])
            tableutils.printmat(x)
        else:
            print('Infeasible')

main()
