def printall(n):
	if(n== 1):
		print('''
----------words sent---------
%option noyywrap
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
line [\\n]
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
printf("Number of Digits:%d\\n",D);
printf("Number of Characters:%d\\n",T);
printf("Number of Words:%d\\n",W);
printf("Number of Lines:%d\\n",li);
return 0;
}
-----------------------------file.txt------------
 hello
 1 2 3''')
	if(n== 2):
		print('''--------------------------------Keyword Identifier------------------
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
[\\n] {lno++;}
[\\t] {ws++;}
{sp} {printf("Special symbol=%s\\n",yytext);}
"#include" printf("Preprocersor=%s\\n",yytext);
"<stdio.h>" printf("Libary=%s\\n",yytext);
"<"|">"|"<="|">=" {printf("Relational Operator=%s\\n",yytext);}
"=" {printf("Assignment operator= %s\\n",yytext);}
"+"|"-"|"*"|"/" {printf("Arithmetic operator=%s\\n",yytext);}
"["|"]"|"("|")"|"{"|"}" {printf("Parenthesis=%s\\n",yytext);}
{keywd} {printf("Keyword=%s\\n",yytext);}
{id} {printf("Identifier=%s\\n",yytext);}
{num} {printf("Number=%s\\n",yytext);}
%%
void main()
{
yyin=fopen("file.c","r");
yylex();
}
-------------------------file.c------------------
#include<stdio.h>
void main()
{
int a=2,b=5,c;
c=a+b;
printf( ,c);
}''')
	if(n== 3):
		print('''---------------------arithamatic expression----------------------
-------------------------Prac3.1--------------------------------------

%option noyywrap
%{
	#include "y.tab.h"
	
%}

%%
[0-9]+	 {yylval=atoi(yytext);return no;}
\\n	 {return 0;}
.	 {return yytext[0];}
%%


-------------------------------------------Prac3.y---------------------------
%{
	#include<stdio.h>
	#include<stdlib.h>
%}
%token no
%left '*' '/' '+' '-'
%% 
stmt : exp {printf("\\n Answer = %d \\n",$1);}
	;
exp :exp '+' exp {$$=$1+$3;}
	| exp '-' exp {$$=$1-$3;}
	| exp '*' exp {$$=$1*$3;}
	| exp '/' exp {$$=$1/$3;}
	| no {$1=$$;}
	;
%%
int main()
{
	printf("Enter regular expression : \\t");
	yyparse();
	printf("valid expression");
	getch();
	return 0;
}

yyerror()
{
	printf("invalid");	
	exit(0);
}

int yywrap()
{
	return 1;
}
''')
	if(n== 4):
		print('''------------------------------implement ll1 parser(first and follow)--------------------
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
 ---------------------------------------input----------------
 a,b
S,A,B
ABb
a/@
b/@
''')
	if(n== 5):
		print('''-------------generate 3 address code---------------------------
import re
counter = 0
class Stack:
    def __init__(self):
        self.stack = []
        self.top=-1

    def pop(self):
        if not self.stack:
            print("Stack is empty1")
        if self.stack:
            self.top = self.top-1
            return self.stack.pop()

    def peek(self):
        if not self.stack:
            print("Stack is empty2")
        if self.stack:
            temp = self.stack[self.top]
            return temp
    def push(self,ele):
        self.stack.append(ele)
        self.top = self.top+1

    def isEmpty(self):
        if self.stack:
            return True
        else:
            return False

        
def printthis(var1,var2,op):
    global counter
    temp = str("t(%d)"%counter)
    print(op,"\\t",var1,"\\t",var2,"\\t",temp)
    counter = counter +1
    return temp
    



operators = ('/','*','+','-')
precedence ={'/':2,'*':2,'+':1,'-':1,'(':0}
expr = str(input("Enter the expression: "))
print("Op\\tVar1\\tVar2\\tTemp\\t")
valueStack= Stack()
operatorStack =Stack()
expr = re.findall(r"[A-Za-z]+|[()+\-*\/]", expr)
for x in expr:
    if x == '(':
        operatorStack.push(x)
        continue
    if x==')':
        while operatorStack.peek()!='(':
            op  = operatorStack.pop()
            var1 = valueStack.pop()
            var2 = valueStack.pop()
            val = printthis(var2,var1,op)
            valueStack.push(val)
        operatorStack.pop()
        continue
    if x in operators:
        while(True):
            if(operatorStack.isEmpty() and precedence[operatorStack.peek()]>=precedence[x]):
                op  = operatorStack.pop()
                var1 = valueStack.pop()
                var2 = valueStack.pop()
                val = printthis(var2,var1,op)
                valueStack.push(val)
            else:
                break
        operatorStack.push(x)
    if x not in operators:
        valueStack.push(x)
while operatorStack.stack:
    op  = operatorStack.pop()
    var1 = valueStack.pop()
    var2 = valueStack.pop()
    val = printthis(var2,var1,op)
    valueStack.push(val)
----------------------------input-----------------
(a+b)*(c-d)''')	
	if(n== 6):
		print('''import re
counter = 0
evallist = []
index = []
class Stack:
    def __init__(self):
        self.stack = []
        self.top=-1

    def pop(self):
        if not self.stack:
            print("Stack is empty1")
        if self.stack:
            self.top = self.top-1
            return self.stack.pop()

    def peek(self):
        if not self.stack:
            print("Stack is empty2")
        if self.stack:
            temp = self.stack[self.top]
            return temp
    def push(self,ele):
        self.stack.append(ele)
        self.top = self.top+1

    def isEmpty(self):
        if self.stack:
            return True
        else:
            return False

        
def printthis(var1,var2,op):
    t1 = str(var1+op+var2)
    if t1 not in evallist:
        global counter
        temp = str("t(%d)"%counter)
        print(op,"\\t",var1,"\\t",var2,"\\t",temp)
        evallist.append(t1)
        index.append(temp)
        counter = counter +1
        return temp
    if t1 in evallist:
        i = evallist.index(t1)
        return index[i]
    
operators = ('/','*','+','-')
precedence ={'/':2,'*':2,'+':1,'-':1,'(':0}
expr = str(input("Enter the expression: "))
print("Op\\tVar1\\tVar2\\tTemp\\t")
valueStack= Stack()
operatorStack =Stack()
expr = re.findall(r"[A-Za-z]+|[()+\-*\/]", expr)
for x in expr:
    if x == '(':
        operatorStack.push(x)
        continue
    if x==')':
        while operatorStack.peek()!='(':
            op  = operatorStack.pop()
            var1 = valueStack.pop()
            var2 = valueStack.pop()
            val = printthis(var2,var1,op)
            valueStack.push(val)
        operatorStack.pop()
        continue
    if x in operators:
        while(True):
            if(operatorStack.isEmpty() and precedence[operatorStack.peek()]>=precedence[x]):
                op  = operatorStack.pop()
                var1 = valueStack.pop()
                var2 = valueStack.pop()
                val = printthis(var2,var1,op)
                valueStack.push(val)
            else:
                break
        operatorStack.push(x)
    if x not in operators:
        valueStack.push(x)
while operatorStack.stack:
    op  = operatorStack.pop()
    var1 = valueStack.pop()
    var2 = valueStack.pop()
    val = printthis(var2,var1,op)
    valueStack.push(val)''')
	if(n== 7):
		print('''------------------------code genearation
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
            print("mov\\treg1,",st[i-1])
            if st[i]=='+':
                s='add'
            elif st[i]=='-':
                s='sub'
            elif st[i]=='*':
                s='mul'
            elif st[i]=='/':
                s='div'
            print("{}\\treg1,{}".format(s,st[i+1]))
            print("mov\\t{},reg1".format(res))
op=[]    
st=input("enter an exp : ")
str1=st.split( )
#print(str1)
print("*** code ***")
getop(str1)
ass(str1)
-----------------------input-----------
t3 = t1*t2''')
	if(n== 8):
		print('no')
	if(n== 9):
		print('no')
	if(n== 10):
		print('''--------------single macro parser--------------
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
for line in input1.split("\\n"):
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
print("\\nMNT")
print("Macro name | no. of parameters | MDT Index")
for name in MNT:
    print("{}       |{}                  |   {}".format(MNT[n],NOP[n]-1,IOM[n]-1))
    n=n+1


print("\\nALA")
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
for str2 in input1.split("\\n"):
    if str2.split()[0] in MNT and str2.split()[0] !="END":
        print(MACROE[str2.split()[0]])
        cmt=False
    else:
    cmt=True
    if cmt:
        print(str2)
---------------------------------------spcc.txt------------
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
END''')
