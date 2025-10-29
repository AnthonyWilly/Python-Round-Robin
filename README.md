Português / English

# Simulador de Escalonamento de CPU Round-Robin

Este repositório contém um script Python simples que simula o algoritmo **Round-Robin (RR)**, uma técnica de escalonamento de processos preemptivo usada por sistemas operacionais.

A simulação demonstra visualmente como a CPU aloca uma "fatia de tempo" (quantum) para cada processo em uma fila circular, e como o contexto de um processo (como o Program Counter e registradores) é salvo e restaurado durante a troca de contexto.

## 🚀 Como Executar

1.  Garanta que você tenha o [Python 3](https://www.python.org/) instalado.
2.  Clone este repositório ou salve o arquivo `.py` em seu computador.
3.  Abra um terminal e navegue até o diretório onde o arquivo está.
4.  Execute o script:

    ```bash
    python SimpleRoundRobinSimulator.py
    ```

## 🛠️ Como Funciona

O script é composto por três componentes principais:

* **`Classe Processo`**: Armazena o estado de um processo, incluindo seu PID, tempo de execução, tempo restante e um contexto simulado (Program Counter e registradores).
* **`Classe CPU`**: Simula a CPU, com métodos para `carregarContexto` e `salvarContexto` de um processo.
* **`Função roundRobin`**: É o escalonador principal. Ele gerencia a fila de prontos (usando `array.array` como uma fila circular FIFO) e o loop principal da simulação, decidindo quem executa e quando realizar a troca de contexto.

### ⚙️ Configuração

Você pode alterar os processos de teste e a fatia de tempo modificando as variáveis no final do script:

```python
# Quantos processos cabem na fila
quantidadeProcessosSistema = 8
# tempo máximo que cada processo usa a CPU antes de sair
timeSlice = 3

#Processos simulados
processosExemplo = [
    Processo(pid=101, tempoChegada=0, tempoExecucao=12),
    Processo(pid=102, tempoChegada=2, tempoExecucao=8),
    # ... adicione mais processos ...
]

roundRobin(processosExemplo)
```

---

# Round-Robin CPU Scheduling Simulator

This repository contains a simple Python script that simulates the **Round-Robin (RR)** algorithm, a common preemptive process scheduling technique used in operating systems.

The simulation visually demonstrates how the CPU allocates a "time slice" (quantum) to each process in a circular queue, and how a process's context (like the Program Counter and registers) is saved and restored during a context switch.

## 🚀 How to Run

1.  Ensure you have [Python 3](https://www.python.org/) installed.
2.  Clone this repository or save the `.py` file to your computer.
3.  Open a terminal and navigate to the directory where the file is located.
4.  Run the script:

    ```bash
    python SimpleRoundRobinSimulator.py
    ```

## 🛠️ How It Works

The script is composed of three main components:

* **`Processo` Class**: Stores the state of a process, including its PID, execution time, remaining time, and a simulated context (Program Counter and registers).
* **`CPU` Class**: Simulates the CPU, with methods to `carregarContexto` (load context) and `salvarContexto` (save context) for a process.
* **`roundRobin` Function**: This is the main scheduler. It manages the ready queue (using `array.array` as a circular FIFO queue) and the main simulation loop, deciding who runs and when to perform a context switch.

### ⚙️ Configuration

You can change the test processes and the quantum (time slice) by modifying the variables at the end of the script:

```python
# How many processes the system queue can hold
quantidadeProcessosSistema = 8
# The time slice (quantum) for each process
timeSlice = 3

#Simulated processes
processosExemplo = [
    Processo(pid=101, tempoChegada=0, tempoExecucao=12),
    Processo(pid=102, tempoChegada=2, tempoExecucao=8),
    # ... add more processes ...
]

roundRobin(processosExemplo)
```
