import matplotlib.pyplot as plt

# graph definition
codes = [13, 16, 17, 19, 23, 25, 27, 29, 31, 32, 37, 41, 43, 47, 49, 53,
         59, 61, 64, 67, 71, 73, 79, 81, 83, 89, 97, 101, 103, 107, 109]

# build links
links = []
for code in codes:
    # pages are 1–10 but we want 0–9
    if code < 100:
        i = code // 10 - 1
        j = code % 10 - 1
    else:
        i = code // 10 - 1
        j = code % 10 - 1
    links.append((i, j))

# 1(a) build matrix H
print("1a:")
def build_H(n, links):
    # adjacency counts
    out_counts = [0]*n
    for i, j in links:
        out_counts[i] += 1
    H = [[0.0]*n for _ in range(n)]
    for i, j in links:
        H[i][j] += 1.0 / out_counts[i]
    # dangling
    for i in range(n):
        if out_counts[i] == 0:
            for j in range(n):
                H[i][j] = 1.0 / n
    return H

n = 10
H = build_H(n, links)
print("\n\tMatrix H:")
for i, row in enumerate(H, start=1):
    print(f"\tRow {i}: {row}")
dangling = [i+1 for i in range(n) if sum(H[i]) == 0]
print("\tdangling nodes:", dangling or "none")

# 1(b) build google matrix
print("\n1b:")
def build_G(H, d):
    n = len(H)
    teleport = (1-d)/n
    return [[d*H[i][j] + teleport for j in range(n)] for i in range(n)]

G85 = build_G(H, 0.85)
print("\n\tgoogle matrix G (d=0.85):")
for i, row in enumerate(G85, 1):
    print(f"\tRow {i:2d}:", ["{0:.3f}".format(x) for x in row])

# 1(c) alternative termination criterion
print("\n1c: \n\tTerminate when the maximum change between successive PageRank vectors falls below E, max_i |v_new[i] - v_old[i]| < E, measuring convergence on specific graph and leveraging stability of the power method")

# 1(d) PageRank iteration
print("\n1d:")
def pagerank(G, v0, tol=1e-6, max_iter=10000):
    n = len(v0)
    v = v0[:]
    history_p5 = []
    history_p7 = []
    for it in range(max_iter):
        v_new = [sum(v[i]*G[i][j] for i in range(n)) for j in range(n)]
        history_p5.append(v_new[4])  
        history_p7.append(v_new[6])
        if max(abs(v_new[k]-v[k]) for k in range(n)) < tol:
            return v_new, it+1
        v = v_new
    return v, max_iter, history_p5, history_p7

v0 = [1.0/n]*n
v85, it85 = pagerank(G85, v0)
print("\n\tnumerical pagerank d=0.85:")
print(f"\tConverged in {it85} iterations")
for i, val in enumerate(v85, 1):
    print(f"\tr(P{i:2d}) = {val:.6f}")


# 1(e) Plotting the evolution of numerical values of r(P5) and r(P7) for subsequent iteration steps of the algorithm 
print("\n1e:")
def plot_history(p5, p7, title):
    plt.figure()
    plt.plot(p5, label="r(P5)")
    plt.plot(p7, label="r(P7)")
    plt.title(title)
    plt.xlabel("Iteration")
    plt.ylabel("PageRank Value")
    plt.legend()
    plt.grid(True)
    plt.show()

G55 = build_G(H, 0.55)
p5_55, p7_55 = pagerank(G55, [0.1]*n)
plot_history(p5_55, p7_55, "Evolution of r(P5) and r(P7), d=0.55")
p5_85, p7_85 = pagerank(G85, [0.1]*n)
plot_history(p5_85, p7_85, "Evolution of r(P5) and r(P7), d=0.85")


# 1(f) 
v1 = [0.1]*n
v2 = [0.55] + [0.05]*(n-1)
v3 = [0]*9 + [1.0]

v1_final, _ = pagerank(G85, v1)
v2_final, _ = pagerank(G85, v2)
v3_final, _ = pagerank(G85, v3)

print("\n1f: PageRank results with different initial vectors:")
print("\tv1_final =", [round(x, 6) for x in v1_final])
print("\tv2_final =", [round(x, 6) for x in v2_final])
print("\tv3_final =", [round(x, 6) for x in v3_final])

# 1(g)
G100 = build_G(H, 1.0)

v_100, _ = pagerank(G100, [0.1]*n)

print("\n1g: PageRank values with d=0.85 and d=1.0:")
print("\td = 0.85:", [round(x, 6) for x in v85])
print("\td = 1.00:", [round(x, 6) for x in v_100])


