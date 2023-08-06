
def main():
	print("hi")
	
def sum(*args):
    sum = 0
    for i in args:
        sum = sum+i
    print(sum)
        


def sub(a,b):
    sub = a-b
    print(sub)
        


def mul(*args):
    mul = 1
    for i in args:
        mul = mul*i
    print(mul)
        


def div(a,b):
    div = a/b
    print(div)
        


def mod(a,b):
    mod = a%b
    print(mod)
        


def sqr(a,b):
    print(a**b)
    


def sqrt(a):
    print(a**0.5)
    


def avg(*args):
    sum = 0
    for i in args:
        sum = sum + i
    average= sum/len(args) 
    print(average)
     

def isprime(n):
    for i in range(2,int(n**0.5)+1):
        if n%i==0:
            print("not prime")
        else:
            print("prime")


def iseven(n):
    if (n % 2) == 0:
        print("{0} is Even".format(n))
    else:
        print("{0} is Odd".format(n))
        

	
if __name__ == "__main__":
	main()