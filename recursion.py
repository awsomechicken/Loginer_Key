def fn(a, b, i):
    a=a+b
    print(a, b)
    if i < 10:
        i=i+1
        fn(a, b, i)

    else:
        return 0

if __name__=='__main__':
    fn(1, 2, 0)
