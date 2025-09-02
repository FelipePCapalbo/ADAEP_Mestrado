# Exercício 2.14

X = 1
Y = 2
Z = 3

# A)
A = X + 3
print(A)

# B)
B = X ** 3
print(B)

# C)
C = (X * 5)**(1/3)
print(C)

# D)
D = X + (Y * 3)
print(D)

# E)
E = X ** Y
print(E)

# F)
F = (X ** Y)+ (3/Z)
print(F)

# Exercício 2.15

# Nome
Nome = "Felipe Papa Capalbo"

# Contador de vogais
dicionario_Vogais = {"aA": 0, "eE": 0, "iI": 0, "oO": 0, "uU": 0}

for cont_letra in Nome:
    for cont_i in dicionario_Vogais:
        if cont_letra in cont_i:
            dicionario_Vogais[cont_i] += 1

print(f"aA: {dicionario_Vogais["aA"]}, eE: {dicionario_Vogais["eE"]}, iI: {dicionario_Vogais["iI"]}, oO: {dicionario_Vogais["oO"]}, uU: {dicionario_Vogais["uU"]}.")

# Exercício 3.4

X = 3
Y = 4
Z = 5

if X > 0 and Y > 0 and Z > 0:
    if (X < Y + Z) and (Y < X + Z) and (Z < X + Y):
        if X == Y and Y == Z:
            print("Triangulo Equilátero.")
        elif X == Y or Y == Z or X == Z:
            print("Triangulo Isósceles.")
        else:
            print("Triangulo Escaleno.")
    else:
        print("Não é triangulo.")

# Exercício 3.5

delta_Bhaskara = (Y**2) - (4 * X * Z)
x_Bhaskara = (-Y + (delta_Bhaskara**(1/2))) / (2 * X)

print(x_Bhaskara)