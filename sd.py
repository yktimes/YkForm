
print(''+"\n".join((i[0]+str(i[1])) for i in zip(['明天','后天','大后天'],[1,2,3])))



def ss (a,b,**c):
    print(a)
    print(b)
    print(c)


s=dict()
o=input("key")
p=input("value")
s[o]=p
ss(1,2,**s)