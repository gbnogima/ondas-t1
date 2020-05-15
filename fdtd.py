import numpy as np
from app import Application

# Variáveis globais

# Parâmetros da Linha de Transmissão
vs = 12
rs = 100
rl = 200 
l = 100 # Tamanho da linha
u = 1.0e8 # Velocidade de propagação
z0 = 50 
C = 2e-10
L = 5e-7
t = l/u # Tempo de trânsito
t_est = 10 # tempo estacionário = t_est*tempo de trânsito

# Valores de step para o tempo e distância
dt = 10e-8
dz = 10

c1 = 0
c2 = 0
array_size = 0
n_max = 0
k_max = 0
time = 1

# -----------------------------------------------------------------
# Funções auxiliares 

def init_current(v0, z0):
    return v0/z0

def init_voltage(vs, z0, rs):
    return z0*vs/(z0+rs)

def coef_refl(r, z0):
    return (r-z0)/(r+z0)

def constant(dt, X, dz):
    return dt/(X*dz)
# ----------------------------------------------------------------

def wave_propagation(i0, v0, current_matrix, voltage_matrix, current_sum, voltage_sum, bw):
    global time

    voltage = np.zeros(array_size)
    current = np.zeros(array_size)

    voltage[0] = v0
    current[0] = i0

    for n in range(1, n_max):
        for k in range(0, k_max):
            current[k+1] = current[k+1] - c1*(voltage[k+1] - voltage[k])  
            voltage[k] = voltage[k] - c2*(current[k+1] - current[k])
        if(bw):
            current_matrix[time] = current_sum - current[::-1]
            voltage_matrix[time] = voltage_sum + voltage[::-1]
        else:
            current_matrix[time] = current_sum + current
            voltage_matrix[time] = voltage_sum + voltage
        time+=1
    voltage[array_size-1] = voltage[array_size-2]
    current[array_size-1] = current[array_size-2]
    
    return current, voltage



def print_result(current, voltage):
    print("Corrente: \n")
    for i in current:
        for j in i:
            print("%.5f" % j, end = '    ')
        print("")


    print("\n\nTensão: \n")
    for i in voltage:
        for j in i:
            print("%.5f" % j, end = '    ')
        print("")

    

def main():
    global c1, c2, array_size, n_max, k_max, time

    # Cálculo das constantes das Equações do Telegrafista
    c1 = constant(dt, L, dz)
    c2 = constant(dt, C, dz)

    # Cálculo dos valores máximos de iteração sobre o tempo e distância
    k_max = int(l/dz)
    n_max = int(t/dt)

    # Cálculo dos coeficientes de reflexão do gerador e da carga
    refl_g = coef_refl(rs, z0)
    refl_c = coef_refl(rl, z0)

    # Declaração dos arrays para armazenar valores de corrente e tensão ao longo da linha de transmissão
    array_size = int(l/dz) + 1
    current_sum = np.zeros(array_size)
    voltage_sum = np.zeros(array_size)

    # Matrizes que armazenarão os valores de corrente e tensão ao longo da linha para cada intervalo
    m_size = ((n_max-1)*t_est+1, array_size)
    current_matrix = np.zeros(m_size)
    voltage_matrix = np.zeros(m_size)
    
    # Cálculo da tensão e corrente em z = -l
    v0 = init_voltage(vs, z0, rs)
    i0 = init_current(v0, z0)

    # Definindo os valores para t = 0
    current_matrix[0][0] = i0
    voltage_matrix[0][0] = v0  

    # Cada iteração corresponde a um tempo de ida + um tempo de retorno
    for i in range(0, t_est, 2):

        # Reflexão no gerador (a partir da 2a iteração)
        if i != 0:
            v0 = refl_g*v0
            i0 = refl_g*i0

        r_current, r_voltage = wave_propagation(i0, v0, current_matrix, voltage_matrix, current_sum, voltage_sum, 0)
        current_sum += r_current
        voltage_sum += r_voltage

        # Reflexão na carga
        v0 = refl_c*v0
        i0 = refl_c*i0

        r_current, r_voltage = wave_propagation(i0, v0, current_matrix, voltage_matrix, current_sum, voltage_sum, 1)
        current_sum -= r_current[::-1]
        voltage_sum += r_voltage[::-1]     

    print("n_max: {}".format(n_max))
    print("k_max: {}".format(k_max))
    print("v0: {}".format(v0))
    print("i0: {}".format(i0))
    print("c1: {}".format(c1))
    print("c2: {}".format(c2))

    # Imprime matrizes
    # Linha n corresponde ao tempo n*dt
    # Coluna k corresponde à posição k*dz
    # print_result(current_matrix, voltage_matrix)

    app = Application(current_matrix, voltage_matrix)
    app.minsize(500,500)
    app.title("Ondas Eletromagnéticas")
    app.mainloop()
    
    
    
if __name__ == '__main__':
    main()

