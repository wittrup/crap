from urllib.parse import quote


m = [l.strip() for l in open("../ignore/sys_1_misc.txt").readlines()]

o = m[6].split()
l = ['1', '2', '3', '5', '7', '9', '13', '14', '15', '126', '105']
x = []
for i in l:
    x.append(o[int(i)-1])
print(x)

n = quote(m[7])
suffix = quote(m[8])
for p,i in enumerate(x):
    next = quote("COALESCE(%s,'Null')," % i)
    # next = quote("%s," % i)
    if len(next) + len(n) + len(suffix) + 69 < 2000:
        n += next
    else:
        z = p
        print(p, i, 'STOPPED HERE')
        break
n = n[:-3]
n += suffix
print(len(n))
print(n)