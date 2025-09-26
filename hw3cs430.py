import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# part a compute P100 and P200

pd.set_option('display.float_format', '{:.10f}'.format) # 10 decimal places for displays

def compute_dp(N, start, K):
    P = np.zeros((N, N))
    P[start] = 1.0
    for _ in range(K):
        Q = np.zeros_like(P)
        for i in range(N):      # loop over all cells
            for j in range(N):
                p = P[i,j]
                if p == 0.0:
                    continue
                for di,dj in [(-1,0),(1,0),(0,-1),(0,1)]:       # prob for neighbors
                    ni, nj = i+di, j+dj
                    if 0 <= ni < N and 0 <= nj < N:
                        Q[ni,nj] += 0.25 * p
        P = Q
    return P

N = 10
P100 = compute_dp(N, start=(0,0), K=100)
P200 = compute_dp(N, start=(4,4), K=200)

df_P100 = pd.DataFrame(P100, index=range(1,N+1), columns=range(1,N+1))
df_P200 = pd.DataFrame(P200, index=range(1,N+1), columns=range(1,N+1))

print("P after 100 steps from (1,1):")  # prob for 100 steps
print(df_P100, "\n")
print("P after 200 steps from (5,5):")  # prob for 200 steps
print(df_P200, "\n")


# part b evolution of p(4,7)

def evolution(N, start, K, target):
    P = np.zeros((N, N))
    P[start] = 1.0
    evo = []        # record prob of target cell at each step
    for _ in range(K):
        Q = np.zeros_like(P)
        for i in range(N):
            for j in range(N):
                p = P[i, j]
                if p == 0.0:
                    continue
                for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < N and 0 <= nj < N:
                        Q[ni, nj] += 0.25 * p
        P = Q
        evo.append(P[target])       # record prob of target cell
    return evo

target = (3, 6)  # (4,7)
evo1 = evolution(N, start=(0,0), K=100, target=target)
evo2 = evolution(N, start=(4,4), K=200, target=target)

plt.figure(figsize=(8,5))
plt.plot(range(1,101), evo1, label='Start (1,1), K=100')
plt.plot(range(1,201), evo2, label='Start (5,5), K=200')
plt.xlabel('Step k')
plt.ylabel('Probability at (4,7)')
plt.title('Evolution of p(4,7)')
plt.legend()
plt.grid(True)
plt.show()      #plot

# EXIT OUT OF THE PLOT IN ORDER TO SEE PART C !!!!


# part c exit probabilities

def boundary_exit(N, start, K):
    P_prev = compute_dp(N, start, K-1) # get P at step K-1
    rows, total = [], 0.0
    for i in range(N):
        for j in range(N):      # consider only the boundary cells
            if i in (0,N-1) or j in (0,N-1):
                off = sum(      # count num of moves that go outside the grid
                    1 for di,dj in [(-1,0),(1,0),(0,-1),(0,1)]
                    if not (0 <= i+di < N and 0 <= j+dj < N)
                )
                prob = P_prev[i,j] * off/4.0       # exit prob
                rows.append((i+1,j+1,prob))
                total += prob
    df = pd.DataFrame(rows, columns=['i','j','exit_prob'])
    return df, total

df_exit100, tot100 = boundary_exit(N, start=(0,0), K=100)
df_exit200, tot200 = boundary_exit(N, start=(4,4), K=200)

print("Boundary exit prob at step 100:")        # total prob of exit at step 100
print(df_exit100, "\n")
print(f"Total exit prob at step 100: {tot100:.10f}\n")
print("Boundary exit prob at step 200:")
print(df_exit200, "\n")
print(f"Total exit prob at step 200: {tot200:.10f}")        # total prob of exit at step 200
