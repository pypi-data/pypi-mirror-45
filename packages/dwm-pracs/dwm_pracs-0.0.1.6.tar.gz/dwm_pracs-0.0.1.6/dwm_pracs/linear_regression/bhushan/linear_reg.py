X = [69, 63, 66, 64, 67, 64, 70, 66, 68, 67, 65, 71]
y = [70, 65, 68, 65, 69, 66, 68, 65, 71, 67, 64, 72]

n = len(X)
sum_X = sum(X)
sum_y = sum(y)
sum_Xsquare = sum([x**2 for x in X])
sum_Xy = sum([x*y for x, y in zip(X, y)])

print("Sum X = ", sum_X)
print("Sum Y = ", sum_y)
print("Sum X square = ", sum_Xsquare)
print("Sum XY = ", sum_Xy)


b1 = ((n*sum_Xy) - (sum_X * sum_y)) / ((n*sum_Xsquare) - (sum_X ** 2))
b0 = (sum_y - (b1 * sum_X)) / n

print("b0 = ", b0)
print("b1 = ", b1)

print("Equation: y = {}x + {}".format(b1, b0))

'''
Sum X =  800
Sum Y =  810
Sum X square =  53402
Sum XY =  54059
b0 =  10.218446601941755
b1 =  0.8592233009708737
Equation: y = 0.8592233009708737x + 10.218446601941755
'''