def print1():
	print('word,sentence count \n')
	print('''%option noyywrap
%{
	#include<stdio.h>
	#include<conio.h>
	int D=0,W=0,C=0;
	int CL=0,SL=0; 
	int li=1;
	int T=0;
%}
digit [0-9]+
Words [a-zA-Z]+
line [\n]
%%
{digit} {D++;}
{Words} {W++;C=C+yyleng;}
{line} {li++;}
. {T++;}
%%
int main()
{
yyin = fopen("file.txt","r");
yylex();
T=T+D+C;
printf("Number of Digits:%d",D);
printf("Number of Characters:%d",T);
printf("Number of Words:%d",W);
printf("Number of Lines:%d",li);
return 0;
}
			--------------------------------text file
			hello 
			1 2 3
		''')
def print2():
	print('keyword identifier\n')
	print('''
		%option noyywrap
%{
	#include<stdio.h>
	#include<ctype.h>
	int lno=1;
	int ws=0;
%}
letter [a-zA-Z]
digit [0-9]
id {letter}({letter}|{digit})*
num {digit}+
keywd "main"|"while"|"float"|"void"|"int"|"if"|"else"|"then"
sp[.,;"]
%%
[] {lno++;}					<-bracket maine slash n
[\t] {ws++;}				<-bracket maine slash t
{sp} {printf("Special symbol=%s",yytext);}
"#include" printf("Preprocersor=%s",yytext);
"<stdio.h>" printf("Libary=%s",yytext);
"<"|">"|"<="|">=" {printf("Relational Operator=%s",yytext);}
"=" {printf("Assignment operator= %s",yytext);}
"+"|"-"|"*"|"/" {printf("Arithmetic operator=%s",yytext);}
"["|"]"|"("|")"|"{"|"}" {printf("Parenthesis=%s",yytext);}
{keywd} {printf("Keyword=%s",yytext);}
{id} {printf("Identifier=%s",yytext);}
{num} {printf("Number=%s",yytext);}
%%
void main()
{
yyin=fopen("file.c","r");
yylex();
}
--------------------------------text file
#include<stdio.h>
void main()
{
int a=2,b=5,c;
c=a+b;
printf( ,c);
}
		''')
def print3():
	print('validate expression')
	print('''
%{
#include<stdio.h>
#include "y.tab.h"
extern int yylval;
%}
%%
[0-9]+ {
          yylval=atoi(yytext);
          return NUMBER;
       }
[] ;			<-bracket maine slash t
[] return 0;	<-bracket maine slash n
. return yytext[0];
%%
int yywrap()
{
return 1;
}

Yacc code
%{
    #include<stdio.h>
    int flag=0;
%}
%token NUMBER
%left '+' '-'
%left '*' '/' '%'
%left '(' ')'
%%
ArithmeticExpression: E{
         printf("Result=%d",$$);
         return 0;
        };
E:E'+'E {$$=$1+$3;}
 |E'-'E {$$=$1-$3;}
 |E'*'E {$$=$1*$3;}
 |E'/'E {$$=$1/$3;}
 |E'%'E {$$=$1%$3;}
 |'('E')' {$$=$2;}
 | NUMBER {$$=$1;}
;
%%
void main()
{
   printf("Enter Any Arithmetic Expression which can have operations Addition, Subtraction, Multiplication, Divison, Modulus and Round brackets:");
   yyparse();
  if(flag==0)
   printf("Entered arithmetic expression is Valid");
}
yyerror()
{
   printf("Entered arithmetic expression is Invalid");
   flag=1;
}

		''')
def print4():
	print('ll1 parser')
	print('''
tlist  = input("Enter Terminal Symbol: ").split(",")
ntlist = input("Enter non-Terminal Symbol: ").split(",")
prodlist= []
def production(nonterminallist):
    for nonterminal in nonterminallist:
        p = input("Enter production of {} ->".format(nonterminal))
        prodlist.append({nonterminal: p})
print(tlist)
print(ntlist)
# tlist = ["a", "b"]
# ntlist = ["S", "A", "B"]
# prodlist = [{'S': 'ABb'}, {'A': 'c/@'}, {"B": "b/@"}]
production(ntlist)


#for i in prodlist:
#    print(i.keys())
first_follow = {"non-terminal": [{"first": []}, {"follow": []}]}
firstfollowlist = []
firstfollowlist.append(first_follow)


def init():
    for nonterminal in ntlist:
        fnf = {nonterminal:
               [{"first": []}, {"follow": []}
                ]}
        firstfollowlist.append(fnf)


def find_first(ntlist):
    inc = 0
    for nonterminal in ntlist:
        print(nonterminal)
        dat = prodlist[inc][nonterminal]

        print(dat)

        dat = dat.split("/")
        for i in dat:
            for j in firstfollowlist:
                for key, value in j.items():
                    if key == nonterminal:
                        value[0]["first"].append(i[0])
        inc += 1

print(prodlist)
init()
find_first(ntlist)
print(firstfollowlist)

for i in ntlist:
    for j in firstfollowlist:
        for key, value in j.items():
            for i in value[0]["first"]:
                if i in ntlist:
                    for ffl in firstfollowlist:
                        for key1, value1 in ffl.items():
                            if key1 == i:
                                value[0]["first"].remove(i)
                                for item in value1[0]["first"]:
                                    value[0]["first"].append(item)
                                    a = set(value[0]["first"])
                                    value[0]["first"] = list(a)

for item in firstfollowlist:
    print(item)
inc = 0
ntset = set(ntlist)
print(ntset)
a = set()
for i in prodlist:
    for key, value in i.items():
        for l in value:
            if l in ntlist:
                a.add(l)

nofollow = list(ntset - a)

for d in nofollow:
    for j in firstfollowlist:
        for key, value in j.items():
            if key == d:
                print(value[1]["follow"].append("$"))
for i in firstfollowlist:
    print(i)
for i in nofollow:
    ntlist.remove(i)
for i in prodlist:
    for key, value in i.items():
        value2 = value.split("/")
        for fl in value2:
            for l in fl:
                if l in ntlist:
                    p = fl.find(l)
                    c = len(fl) - (p+1)


                    if (c >= 1) and (l in ntlist):
                        #print("c===1")
                        print()
                        # print(p, l, fl, c, len(fl), len(fl)-1)
                        for j in firstfollowlist:
                            for key1, value1 in j.items():
                                if key1 == l:
                                    print(value, key1, l)
                                    if fl[p+1] in tlist:
                                        value1[1]["follow"].append(fl[p+1])
                                    for item in firstfollowlist:
                                        for key3, value3 in item.items():
                                            if key3 == fl[p+1]:
                                                for item2 in value3[0]["first"]:
                                                    if item2 != '@':
                                                        value1[1]["follow"].append(
                                                            item2)

                    if c == 0:
                        # print("c=================0")
                        for j in firstfollowlist:
                            for key1, value1 in j.items():
                                if key1 == l:
                                    for item in firstfollowlist:
                                        for key3, value3 in item.items():
                                            if key3 == key:
                                                for item2 in value3[1]["follow"]:

                                                    value1[1]["follow"].append(
                                                        item2)


for i in firstfollowlist:
    print(i)

---------------------------------------------------input
a,b
S,A,B
ABb
a/@
b/@
		''')

def print5():
	print('3ac')
	print('''
print("icg")
exp = "( A + B ) * ( C + D )"

import queue
class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)

    def show(self):
        return self.items


stack = Stack()


def infixToPostfix(infixexpr):
    prec = {}
    prec["*"] = 3
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    opStack = Stack()
    postfixList = []
    tokenList = infixexpr.split()

    for token in tokenList:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
                    (prec[opStack.peek()] >= prec[token]):
                postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return " ".join(postfixList)


tablelist = []
# for index,val in enumerate(tablelist):
#     for key , values in val.items():
#         print(values)
#         print(len(values))
print(exp)
postexp = infixToPostfix(exp)
print(postexp)
stack = Stack()
q = queue.Queue()
op = ["+", "-", "*", "/"]
j = 1
for i in postexp:
    if i in op:
        t = []

        if not q.empty():
            while not q.empty():
                t.append(q.get())
            tb = []
            for k in t:
                if k != " ":
                    if len(tb) == 1:
                        tb.append(i)
                    tb.append(k)
            tablelist.append({"t"+str(j):tb})
            j+=1
        else :
            tb = []
            second = [n for n in tablelist[j-2].keys()]
            first  =[n for n in tablelist[j-3].keys()]
            tb.append(first[0])
            tb.append(i)
            tb.append(second[0]) 
            tablelist.append({"t"+str(j):tb})
            j+=1
    else:
        if i != " ":
         q.put(i)

for i in tablelist:
    print(i)

		''')
def print6():
	print('optimize 3ac')
	print('''
tablelist =[{'t1': ['A', '+', 'B']}, {'t2': ['A', '+', 'B']}, {'t3': ['t1', '*', 't2']}]
for i in tablelist:
    for keys,value in i.items():
        value = "".join(value)
        for j in tablelist:
            for keys1,value1 in j.items():
                value1 = "".join(value1)
                if keys != keys1:       
                    if value == value1:    
                        value1 = keys
                        j.update({keys1:value1})
for i in tablelist:
    for keys,value in i.items():
        if len(keys) == 2 and len(value) == 2 :
            for j in tablelist:
                for keys1,value1 in j.items():
                    diflist = []
                    if keys1 != keys:
                        diflist = []
                        for K in value1:
                            diflist.append(K)
                            if K == keys:
                                diflist.remove(K)
                                diflist.append(value)
                        j.update({keys1:diflist})   
print([i for i in tablelist])
tablelist1 =[]
for i in tablelist:
    for keys,value in i.items():
        passl = True
        if len(keys) == 2 and len(value) == 2 :
            passl = False
        if passl:
            tablelist1.append(i)
print(tablelist1)

		''')
def print7():
	print('generate code statement')
	print('''
def getop(st):
    for i in range (len(st)):
        if st[i]=='+' or st[i]=='-' or st[i]=='*' or st[i]=='/':
            op.append(st[i])
    #print(op)
def ass(st):
    for i in range (len(st)):
        if st[i]=='=':
            res=st[i-1]
        if st[i] in op:
            print("mov\treg1,",st[i-1])
            if st[i]=='+':
                s='add'
            elif st[i]=='-':
                s='sub'
            elif st[i]=='*':
                s='mul'
            elif st[i]=='/':
                s='div'
            print("{}\treg1,{}".format(s,st[i+1]))
            print("mov\t{},reg1".format(res))
op=[]    
st=input("enter an exp : ")
str1=st.split( )
#print(str1)
print("*** code ***")
getop(str1)
ass(str1)
---------------------------input
t3 = t1 * t2
		''')
def print8():
	print('parse 1 assembler')
	print('''
import re
f=open("spcc.asm","r")
IS={"STOP":00,"ADD":1,"SUB":2,"MULT":3,"MOVR":4,"MOVM":5,"COMP":6,"BC":7,"DIV":8,"READ":9,"PRINT":10}
AS={"START":1,"END":2,"ORIGIN":3,"EQU":4,"LTORG":5}
DS={"DS":2,"DC":1}
input1=f.read()
ml=input1.split()[1]
m_loc_tab={}
a=['0','1','2','3','4','5','6','7','8','9']
b=[0,1,2,3,4,5,6,7,8,9]
reg={"AREG","BREG"}
test=[]
test2=[]
test3=[]
reg_tab=[]
p="='"
lt_no=list()
LT=[]
CT=[]
isrD=[]
pooltab=[]
def cal(ml):
    for j in input1.split(""):                          <------------yaha slash n
        m_loc_tab.update({j.split()[0]:int(ml)-1})
        ml=int(ml)+1
        #print(j)
        lt_no.append(j[j.find(",='")+3])
        if re.findall("REG",j):
            c=j.find("REG")-1
            if 'A' not in reg_tab and 'B' not in reg_tab:
                reg_tab.append(j[c])
    for i in input1.split():
        for k in i:
            if k not in a:
               test.append(i)
    for key in AS:
        test2.append(key)
    for j in IS:
        test3.append(j)
    sym_tab=list(set(test)-set(test2)-set(test3)-set(a))
    sym_tab2={k: m_loc_tab[k] for k in m_loc_tab.keys() & set(sym_tab)}
    for sym in sym_tab2:
        isrD.append([sym,"S",list(sym_tab2).index(sym)])
    print("Symbol table" ,sym_tab2)
    lit_set=set(a)&set(lt_no)
    v=1
    for i in lit_set:
        LT.append(",='{}'".format(i))
        
        pooltab.append("#{}".format(v))
        v=v+1
    print("litral table",LT)
    print("Pool Table",pooltab)

def isr(IDS,n):
    str1=""
    if n ==1:
        str1="AS"
    elif n==2:
        str1="IS"
    else:
        str1="DS"

    for k in input1.split():
        for key,value in IDS.items():
            if k==key:
                isrD.append([key,str1,"0"+str(value)])

        
    
cal(ml)
isr(AS,1)
isr(IS,2)
isr(DS,3)
print("ISR Table")

for i in input1.split():
    if i[0] in a :
            isrD.append([i,"C"])
for l in LT:
    isrD.append([l,"L"])
    

for r in reg_tab:
    if r=='A':
        isrD.append(["AREG",1])
    elif r=='B':
        isrD.append(["AREG",1])

for i in input1.split():
    
    for m in isrD:
        #print(i)
        if i in m:
            print(m)
-----------------------------------------------spcc.asm
START 200
READ A
LOOP MOVR AREG ,A
ADD AREGA ,='1'
SUB AREG ,='2'
BC GT ,LOOP
STOP
A DS 1s
LTORG
		''')
def print9():
	print('implement parse 2')
	print('''
#include<stdio.h>

#include<stdlib.h>

#include<string.h>

void main()

{

FILE *f1,*f2,*f3,*f4;

char ch[100],chp[100];

int addr=1000;

f1=fopen("input1.txt","r");

f2=fopen("optab1.txt","r");

f3=fopen("littab2.txt","w");

f4=fopen("symtab2.txt","w");

while (fscanf(f1,"%s",ch) !=EOF)

{

if(strcmp(ch,"-")==0)

{

addr++;

}

if(strcmp(ch,"db")==0)

{

fprintf(f4,"%s\t%d\n",chp,addr);

}

if(strcmp(chp,"LTORG")==0)

{

fprintf(f3,"%s\t%d\n",ch,addr);

}
 
strcpy(chp,ch);

}

fclose(f4);

fclose(f3);

fclose(f2);

fclose(f1);

}

		''')
def print10():
	print('macro parse')
	print('''
f=open("SPCC.TXT",'r')
input1=f.read()
MACROE={1:[]}
templ=[]
MDT=[]
MNT=[]
NOP=[]
IOM=[]
ALA=[]
start = "MACRO"
end = "MEND"
count=[]
i=0
j=0
m=0
a=0
n=0
MN=True
replace="NONE"
copy = False
for line in input1.split("\n"):
    if line.strip() == start:
        copy = True
        MN=True
        i=i+1
        
    elif line.strip() == end:
        copy = False
        MDT.append(i)
        MDT.append(line)
        
    elif copy:
        MDT.append(i)
        MDT.append(line)
        a=a+1
        i=i+1
    elif not copy:
        count.append(a-1)
        print(count)
        a=0
    if MN and line != "MACRO":
        MNT.append(line.split()[0])
        NOP.append(len(list(line.split()))-1)
        ALA.append(line.split())
        IOM.append(i)
        MN=False

print("MDT")   
print("Index  Statement")
for l in range(int(len(MDT)/2)) :
    print("{} | {}".format(MDT[m],MDT[m+1]))
    m=m+2
print("\nMNT")
print("Macro name | no. of parameters | MDT Index")
for name in MNT:
    print("{}       |{}                  |   {}".format(MNT[n],NOP[n]-1,IOM[n]-1))
    n=n+1


print("\nALA")
n=0
print("Formal parameter | Positional")
for name in ALA:
    del name[0]
    for naem in name :
        if naem !=",":
            print("{}               | #{} ".format(naem,n+1))
            n=n+1



def expand(str1):
    ma=0
    temp_index=0
    index=MNT.index(str1)
    temp_index=MDT.index(IOM[index])+1
    #print(index,IOM["INDEX",index])
    for  mc in range(count[index]):
        print(MDT[temp_index+ma])
        ma=ma+2
    ma=0
    
    
def expan():
    index=0
    il=0
    for string in input1.split():
        if string in MNT:
            expand(string)

expan()
cmt=True
for str2 in input1.split("\n"):
    if str2.split()[0] in MNT and str2.split()[0] !="END":
        print(MACROE[str2.split()[0]])
        cmt=False
    else:
    cmt=True
    if cmt:
        print(str2)
------------------------------------------spcc.txt
MACRO ADD1
MOV A,B
ADD C
MENU MACRO
SUB1
STORE C
MEND

MOV B,10
MOV C,20
ADD1
MUL C
SUB1
END
		''')