import matplotlib.pyplot as plt

def compute_recurrence(max_num):

    #store T(1) to T(max_n+1) and avoids out of range errors
    T = [0] * (max_num + 2)

    #initial condition T(1) = 4
    T[1] = 4.0 
   
    #T(n+1) = T(n) * (((n^2+4n)/(n^2+4n+3))^n) * ((n+4)/(n+1))
    for n in range(1, max_num + 1):
        first_parenthesis = (n**2 + 4*n) / (n**2 + 4*n + 3)
        second_parenthesis = (first_parenthesis ** n) * ((n + 4) / (n + 1))
        T[n + 1] = T[n] * second_parenthesis
    return T

#set the maximum n value for the simulation
max_num = 1000
T_values = compute_recurrence(max_num)

#prepare x values: n from 1 to max_n
n_values = list(range(1, max_num + 1))

#plot T(n) vs n
plt.plot(n_values, T_values[1:max_num+1], marker='.', linestyle='-')
plt.xlabel('n')
plt.ylabel('T(n)')
plt.title('Graph of T(n) for the Recurrence')
plt.show()
#print values from 990 to max number
for i in range(990, max_num + 1):
    print("T(",i,") = ",T_values[i])