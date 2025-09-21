import sys,math
import random
input=sys.stdin.readline

pr=[2,325,9375,28178,450775,9780504,1795265022]

# https://github.com/kth-competitive-programming/kactl/blob/main/content/number-theory/MillerRabin.h
def isp(n):
    if n<2:
        return False
    if n&1==0:
        return n==2
    d=n-1
    s=0
    while d&1==0:
        d>>=1
        s+=1
    for a in pr:
        if a%n==0:
            continue
        x = pow(a,d,n)
        if x==1 or x==n-1:
            continue
        for _ in range(s-1):
            x=x*x%n
            if x==n-1:
                break
        else:
            return False
    return True

def pol(n):
    if n % 2 == 0:
        return 2
    if isp(n):
        return n
    def f(x,c):
        return (x*x+c)%n
    while True:
        x=random.randrange(2,n-1)
        y=x
        c=random.randrange(1,n-1)
        d=1
        while d==1:
            x=f(x,c)
            y=f(f(y,c),c)
            d=math.gcd(abs(x-y),n)
        if d!=n:
            return d

def factor(n):
    if n == 1:
        return []
    if isp(n):
        return [n]
    d=pol(n)
    return factor(d)+factor(n//d)
