import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do modelo
grid_size = 50
beta = 0.3      # probabilidade de infecção por vizinho
gamma = 0.1     # probabilidade de recuperação
steps = 100     # número de rodadas

# Estados: 0 = Suscetível, 1 = Infectado, 2 = Recuperado
def initialize_grid():
    grid = np.zeros((grid_size, grid_size), dtype=int)
    # Inicializa uma célula infectada no centro
    grid[grid_size//2, grid_size//2] = 1
    return grid

def count_infected_neighbors(grid, x, y):
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # vizinhança de Von Neumann
    count = 0
    for dx, dy in neighbors:
        nx, ny = (x + dx) % grid_size, (y + dy) % grid_size
        if grid[nx, ny] == 1:
            count += 1
    return count

def update(grid):
    new_grid = grid.copy()
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i, j] == 0:
                infected_neighbors = count_infected_neighbors(grid, i, j)
                prob_infection = 1 - (1 - beta) ** infected_neighbors
                if infected_neighbors > 0 and np.random.rand() < prob_infection:
                    new_grid[i, j] = 1
            elif grid[i, j] == 1:
                if np.random.rand() < gamma:
                    new_grid[i, j] = 2
    return new_grid

def count_states(grid):
    unique, counts = np.unique(grid, return_counts=True)
    state_counts = dict(zip(unique, counts))
    s = state_counts.get(0, 0)
    i = state_counts.get(1, 0)
    r = state_counts.get(2, 0)
    return s, i, r

# Inicializa a grade e listas de estatísticas
grid = initialize_grid()
susceptible_counts = []
infected_counts = []
recovered_counts = []

# Simulação
for step in range(steps):
    s, i, r = count_states(grid)
    susceptible_counts.append(s)
    infected_counts.append(i)
    recovered_counts.append(r)
    grid = update(grid)

# Gráfico de evolução SIR
plt.figure(figsize=(10, 6))
plt.plot(susceptible_counts, label="Susceptíveis", linestyle='--')
plt.plot(infected_counts, label="Infectados", linestyle='-')
plt.plot(recovered_counts, label="Recuperados", linestyle='-.')
plt.xlabel("Tempo (rodadas)")
plt.ylabel("Número de indivíduos")
plt.title("Evolução dos estados (SIR) na simulação com Autômatos Celulares")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("grafico_sir_evolucao.png", dpi=300)
plt.show()

# Gráfico do pico da infecção
max_infected = max(infected_counts)
time_of_peak = infected_counts.index(max_infected)

plt.figure(figsize=(6, 4))
plt.plot(infected_counts, color="red")
plt.axvline(time_of_peak, color="black", linestyle="--", label="Pico")
plt.scatter([time_of_peak], [max_infected], color="black")
plt.xlabel("Tempo (rodadas)")
plt.ylabel("Infectados")
plt.title("Pico da infecção")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("grafico_pico_infeccao.png", dpi=300)
plt.show()

# Gráfico de pizza com o estado final
final_s = susceptible_counts[-1]
final_i = infected_counts[-1]
final_r = recovered_counts[-1]

labels = ["Susceptíveis", "Infectados", "Recuperados"]
sizes = [final_s, final_i, final_r]
colors = ['#66b3ff', '#ff9999', '#99ff99']

plt.figure(figsize=(6,6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
plt.title("Distribuição final dos estados (após 100 rodadas)")
plt.tight_layout()
plt.savefig("grafico_pizza_final.png", dpi=300)
plt.show()