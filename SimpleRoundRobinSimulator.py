from array import array
import time
import random  # Para simular operações nos registradores

# Mask para registradores de 16 bits
REGISTER_MASK = 0xFFFF

class Processo:
    def __init__(self, pid, tempoChegada, totalLinhas, pcInicial=0):
        self.pid = pid
        self.tempoEspera = 0
        self.tempoChegada = tempoChegada
        self.totalLinhas = totalLinhas
        self.pcInicial = pcInicial
        self.programCounter = pcInicial

        # Registradores do processo
        self.registradores = {
            'R1': random.randint(0, REGISTER_MASK),
            'R2': random.randint(0, REGISTER_MASK),
            'R3': random.randint(0, REGISTER_MASK)
        }


class CPU:
    def __init__(self):
        self.pidExecutando = -1  # -1 = CPU ociosa
        self.pcAtual = 0

        self.registradoresCpu = {'R1': 0, 'R2': 0, 'R3': 0}

    def carregarContexto(self, processo):
        self.pidExecutando = processo.pid
        self.pcAtual = processo.programCounter
        self.registradoresCpu = processo.registradores.copy()

    def salvarContexto(self, processo):
        processo.programCounter = self.pcAtual
        processo.registradores = self.registradoresCpu.copy()

    def executarInstrucao(self):
        self.pcAtual += 1

        # mexe num registrador aleatório
        reg = random.choice(['R1', 'R2', 'R3'])
        valor_op = (self.pcAtual % 5) + 1
        novo_valor = (self.registradoresCpu[reg] + valor_op) & REGISTER_MASK
        self.registradoresCpu[reg] = novo_valor


def roundRobin(processos):

    queueSchedule = array('i', [-1] * quantidadeProcessosSistema)
    head = 0
    tail = -1

    cpuSimulada = CPU()

    if processos:
        cpuSimulada.carregarContexto(processos[0])
        processosAtivos = {p.pid: p for p in processos}

        for i in range(1, len(processos)):
            tail = (tail + 1) % quantidadeProcessosSistema
            queueSchedule[tail] = processos[i].pid
    else:
        print("Nenhum processo para rodar.")
        return

    def encontrarProcessoPorPid(pid):
        return processosAtivos.get(pid)

    def trocaDeContexto():
        nonlocal head, tail

        processoAntigo = encontrarProcessoPorPid(cpuSimulada.pidExecutando)

        if processoAntigo:
            cpuSimulada.salvarContexto(processoAntigo)

        # recoloca se não terminou
        if processoAntigo and processoAntigo.programCounter < (processoAntigo.pcInicial + processoAntigo.totalLinhas):
            tail = (tail + 1) % quantidadeProcessosSistema
            queueSchedule[tail] = cpuSimulada.pidExecutando

        # pega próximo
        if head != (tail + 1) % quantidadeProcessosSistema:
            pidProximo = queueSchedule[head]
            queueSchedule[head] = -1
            head = (head + 1) % quantidadeProcessosSistema

            processoNovo = encontrarProcessoPorPid(pidProximo)
            if processoNovo:
                cpuSimulada.carregarContexto(processoNovo)
            else:
                cpuSimulada.pidExecutando = -1
        else:
            cpuSimulada.pidExecutando = -1

    #loop cpu
    while True:
        cpu = cpuSimulada.pidExecutando
        processoAtual = encontrarProcessoPorPid(cpu)

        # CPU ociosa + fila vazia,  acabou
        if not processoAtual and head == (tail + 1) % quantidadeProcessosSistema:
            print("Todos os processos concluídos.")
            break

        # CPU ociosa mas há alguém na fila troca de contexto
        if not processoAtual:
            trocaDeContexto()
            continue

        linhasExecutadas = processoAtual.programCounter - processoAtual.pcInicial
        linhasRestantes = (processoAtual.pcInicial + processoAtual.totalLinhas) - processoAtual.programCounter

        r1 = cpuSimulada.registradoresCpu['R1']
        r2 = cpuSimulada.registradoresCpu['R2']
        r3 = cpuSimulada.registradoresCpu['R3']

        #Formatação dos hexa aleatórios para simular ação nos registradores
        regs_str = f"R1: {r1:#06x} | R2: {r2:#06x} | R3: {r3:#06x}"

        print(f"PID: {processoAtual.pid} | Linhas Executadas/Total de linhas: {linhasExecutadas}/{processoAtual.totalLinhas} | PC: {cpuSimulada.pcAtual:04X} | {regs_str}")

        tempoExecutado = min(timeSlice, linhasRestantes)

        for _ in range(tempoExecutado):
            cpuSimulada.executarInstrucao()
            time.sleep(0.5)

        # terminou
        if processoAtual.programCounter >= (processoAtual.pcInicial + processoAtual.totalLinhas):
            print(f"Processo {processoAtual.pid} CONCLUÍDO (PC: {processoAtual.programCounter:04X}).")
            del processosAtivos[processoAtual.pid]

            if head != (tail + 1) % quantidadeProcessosSistema:
                pidProximo = queueSchedule[head]
                queueSchedule[head] = -1
                head = (head + 1) % quantidadeProcessosSistema

                processoNovo = encontrarProcessoPorPid(pidProximo)
                if processoNovo:
                    cpuSimulada.carregarContexto(processoNovo)
                else:
                    cpuSimulada.pidExecutando = -1
            else:
                cpuSimulada.pidExecutando = -1

        else:
            # timeSlice acabou
            trocaDeContexto()

        if not processosAtivos:
            print("FIM DA SIMULAÇÃO.")
            break


#teste
quantidadeProcessosSistema = 8
timeSlice = 3

processosExemplo = [
    Processo(pid=101, tempoChegada=0, totalLinhas=12, pcInicial=1000),
    Processo(pid=102, tempoChegada=2, totalLinhas=8, pcInicial=2000),
    Processo(pid=103, tempoChegada=3, totalLinhas=15, pcInicial=3000),
    Processo(pid=104, tempoChegada=5, totalLinhas=6, pcInicial=4000),
    Processo(pid=105, tempoChegada=8, totalLinhas=10, pcInicial=5000),
    Processo(pid=106, tempoChegada=10, totalLinhas=7, pcInicial=6000),
    Processo(pid=107, tempoChegada=12, totalLinhas=9, pcInicial=7000),
]

roundRobin(processosExemplo)
