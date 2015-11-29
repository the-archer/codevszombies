limit = 30

fib = []
fib.append(0)
fib.append(1)
for i in range(2, limit+1):
	fib.append(fib[i-1] + fib[i-2])
print(fib)

fibsum = []

cur = 0
f1 = open("output.txt", "w")
f1.write("fib = [")
for no in fib:
	cur += no
	fibsum.append(cur)
	f1.write(str(cur) + ',')
f1.write("]")
f1.close()
