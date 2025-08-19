def build():
    size=1
    while size<n:
        size<<=1
    tree=[0]*2*size
    for i in range(size,size+n):
        tree[i]=a[i-size]
    for i in range(size-1,0,-1):
        tree[i]=tree[i<<1]+tree[i<<1|1]
    return tree,size

def query(s,f):
    s+=size
    f+=size+1
    t=0
    while s<f:
        if s&1:
            t+=tree[s]
            s+=1
        if f&1:
            f-=1
            t+=tree[f]
        s>>=1
        f>>=1
    return t

def upd(i,c):
    i+=size
    tree[i]=c
    i>>=1
    while i:
        tree[i]=tree[i<<1]+tree[i<<1|1]
        i>>=1
        
n=int(input())
a=list(map(int,input().split()))
tree,size=build()
m=int(input())
for _ in range(m):
    print()

    
