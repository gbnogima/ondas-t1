import numpy as np
import inquirer
from app import Application

# Variáveis globais

# Parâmetros da Linha de Transmissão
vs = 2
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
dt = 1e-8
dz = 2.7

c1 = 0
c2 = 0
array_size = 0
n_max = 0
k_max = 0
time = 1

# Solicita o valor da carga
def rl_choice_menu():
    questions = [
        inquirer.List('R',
                    message="Valor da carga",
                    choices=[('∞ (carga em aberto)', 1), ('0 (carga em curto-circuito)', 2), ('100', 3)],
                ),
        ]
    answer = inquirer.prompt(questions)
    if answer['R'] == 1:
        return 'inf'
        
    elif answer['R'] == 2:
        return 0

    elif answer['R'] == 3:
        return 100

# -----------------------------------------------------------------
# Funções auxiliares 

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

def init_current(v0, z0):
    return v0/z0

def init_voltage(vs, z0, rs):
    return z0*vs/(z0+rs)

def coef_refl(r, z0):
    if r == 'inf':
        return 1
    else:
        return (r-z0)/(r+z0)

def constant(dt, X, dz):
    return dt/(X*dz)
# ----------------------------------------------------------------

# Atualiza as matrizes de tensão e corrente a cada incremento no tempo
def update_matrix(current_matrix, voltage_matrix, current_sum, voltage_sum, bw, current, voltage):
    if(bw):
        current_matrix[time] = current_sum - current[::-1]
        voltage_matrix[time] = voltage_sum + voltage[::-1]
    else:
        current_matrix[time] = current_sum + current
        voltage_matrix[time] = voltage_sum + voltage
    

# Simula a propagação da onda a cada tempo t
def wave_propagation(i0, v0, current_matrix, voltage_matrix, current_sum, voltage_sum, bw):
    global time

    voltage = np.zeros(array_size)
    current = np.zeros(array_size)

    voltage[0] = v0
    current[0] = i0

    update_matrix(current_matrix, voltage_matrix, current_sum, voltage_sum, bw, current, voltage)
    time+=1

    for n in range(1, n_max):
        for k in range(0, k_max):
            current[k+1] = current[k+1] - c1*(voltage[k+1] - voltage[k])  
            voltage[k] = voltage[k] - c2*(current[k+1] - current[k])

        update_matrix(current_matrix, voltage_matrix, current_sum, voltage_sum, bw, current, voltage)
        time+=1
    voltage[array_size-1] = voltage[array_size-2]
    current[array_size-1] = current[array_size-2]
    
    return current, voltage

def calculate(rl):
    global c1, c2, array_size, n_max, k_max, time

    # Cálculo das constantes das Equações do Telegrafista
    c1 = constant(dt, L, dz)
    c2 = constant(dt, C, dz)


    # Cálculo dos valores máximos de iteração sobre o tempo e distância
    k_max = int(l/dz)
    n_max = int(t/dt)


    # Declaração dos arrays para armazenar valores de corrente e tensão ao longo da linha de transmissão
    array_size = int(l/dz) + 1
    current_sum = np.zeros(array_size)
    voltage_sum = np.zeros(array_size)


    # Matrizes que armazenarão os valores de corrente e tensão ao longo da linha para cada intervalo
    m_size = ((n_max)*t_est+1, array_size)
    current_matrix = np.zeros(m_size)
    voltage_matrix = np.zeros(m_size)


    # Cálculo da tensão e corrente em z = -l
    v0 = init_voltage(vs, z0, rs)
    i0 = init_current(v0, z0)


    # Definindo os valores para t = 0
    current_matrix[0][0] = i0
    voltage_matrix[0][0] = v0  


    # Solicita do usuário o valor da carga
    # rl = rl_choice_menu()


    # Cálculo dos coeficientes de reflexão do gerador e da carga
    refl_g = coef_refl(rs, z0)
    refl_c = coef_refl(rl, z0)


    # A cada iteração considera-se um tempo de ida+retorno, uma reflexão na carga e uma reflexão no gerador
    for i in range(0, t_est, 2):
        if i != 0:
            v0 = refl_g*v0
            i0 = refl_g*i0

        r_current, r_voltage = wave_propagation(i0, v0, current_matrix, voltage_matrix, current_sum, voltage_sum, 0)
        current_sum += r_current
        voltage_sum += r_voltage

        v0 = refl_c*v0
        i0 = refl_c*i0

        r_current, r_voltage = wave_propagation(i0, v0, current_matrix, voltage_matrix, current_sum, voltage_sum, 1)
        current_sum -= r_current[::-1]
        voltage_sum += r_voltage[::-1]     

    print_result(current_matrix, voltage_matrix)
    
    print("n_max: {}".format(n_max))
    print("k_max: {}".format(k_max))
    print("c1: {}".format(c1))
    print("c2: {}".format(c2))

    app = Application(current_matrix, voltage_matrix)
    app.minsize(500,500)
    app.title("Ondas Eletromagnéticas")
    app.mainloop()

def main():
    rl = rl_choice_menu()
    calculate(rl)

    
if __name__ == '__main__':
    main()