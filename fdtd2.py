import numpy as np
import math

# Variáveis globais

# Parâmetros da Linha de Transmissão
vs = 1
rs = 75
rl = 0
l = 100 # Tamanho da linha
u = 2.7e8 # Velocidade de propagação
z0 = 50 
C = 7.40740741e-11
L = 1.85185185e-7
t = l/u # Tempo de trânsito
t_est = 10 # tempo estacionário = t_est*tempo de trânsito

# Valores de step para o tempo e distância
dt = 3e-8
dz = 8.1

c1 = 0
c2 = 0

array_size = 0
n_max = 0
k_max = 0
time = 0

# -----------------------------------------------------------------
# Funções auxiliares 

def init_current(v0):
    return v0/z0

def init_voltage(vs, z0, rs):
    return z0*vs/(z0+rs)

def coef_refl(r, z0):
    if r == float(math.inf):
        return 1
    else:
        return (r-z0)/(r+z0)

def constant(X):
    return dt/(X*dz)

def input_voltage(n, v):
    if n*dt > l/(2*u):
        return 0
    else:
        return v
# ----------------------------------------------------------------

def update_matrix(current_matrix, voltage_matrix, current, voltage, bw, t):
    if(bw):
        current_matrix[t] -= current[::-1]
        voltage_matrix[t] += voltage[::-1]
    else:
        current_matrix[t] += current
        voltage_matrix[t] += voltage
    



def wave_propagation(i0, v0, current_matrix, voltage_matrix, bw):
    global time
    tx = 0

    voltage = np.zeros(array_size)
    current = np.zeros(array_size)

    voltage[0] = v0
    current[0] = i0
    
    # Tempo 0
    update_matrix(current_matrix, voltage_matrix, current, voltage, bw, time+tx)
    tx+=1


    for n in range(1, n_max):
        voltage[0] = input_voltage(n, v0)
        current[0] = init_current(voltage[0])
        for k in range(0, k_max):
            current[k+1] = current[k+1] - c1*(voltage[k+1] - voltage[k])  
            voltage[k] = voltage[k] - c2*(current[k+1] - current[k])

        update_matrix(current_matrix, voltage_matrix, current, voltage, bw, time+tx)
        tx+=1

    
    # Onda atinge a carga
    voltage[array_size-1] = voltage[array_size-2]
    current[array_size-1] = current[array_size-2]

    update_matrix(current_matrix, voltage_matrix, current, voltage, bw, time+tx)
    tx+=1
    t_aux = time + tx

    if(t_aux >= t_est*(n_max+1)):
        time = t_aux
        return

    

    
    for n in range(1, int(0.5*t/dt)+1):
        for k in range(0, k_max):
            current[k+1] = current[k+1] - c1*(voltage[k+1] - voltage[k])  
            voltage[k] = voltage[k] - c2*(current[k+1] - current[k])

        update_matrix(current_matrix, voltage_matrix, current, voltage, bw, time+tx)
        tx+=1
    
    time = t_aux

class FDTD2:
    def calculate(rl):
        global c1, c2, array_size, n_max, k_max, time

        c1 = 0
        c2 = 0

        array_size = 0
        n_max = 0
        k_max = 0
        time = 0

        # Cálculo das constantes das Equações do Telegrafista
        c1 = constant(L)
        c2 = constant(C)

        # Cálculo dos valores máximos de iteração sobre o tempo e distância
        k_max = int(l/dz)
        n_max = int(t/dt)
        
        # Declaração dos arrays para armazenar valores de corrente e tensão ao longo da linha de transmissão
        array_size = int(l/dz) + 1
        current_sum = np.zeros(array_size)
        voltage_sum = np.zeros(array_size)

        # Matrizes que armazenarão os valores de corrente e tensão ao longo da linha para cada intervalo
        m_size = ((n_max+1)*t_est, array_size)
        current_matrix = np.zeros(m_size)
        voltage_matrix = np.zeros(m_size)
        
        # Cálculo da tensão e corrente em z = -l
        v0 = init_voltage(vs, z0, rs)
        i0 = init_current(v0)

        # Cálculo dos coeficientes de reflexão do gerador e da carga
        refl_g = coef_refl(rs, z0)
        refl_c = coef_refl(rl, z0)

        # Definindo os valores para t = 0
        # current_matrix[0][0] = i0
        # voltage_matrix[0][0] = v0  

        for i in range(0, t_est, 2):
            if i != 0:
                v0 = refl_g*v0
                i0 = refl_g*i0

            wave_propagation(i0, v0, current_matrix, voltage_matrix, 0)
            
            v0 = refl_c*v0
            i0 = refl_c*i0

            wave_propagation(i0, v0, current_matrix, voltage_matrix, 1)

        return(current_matrix, voltage_matrix, dz, dt)