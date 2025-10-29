import array
import time

class Processo:
    def __init__(self, pid, tempoChegada, tempoExecucao, pcInicial=0):
        self.pid = pid
        self.tempoEspera = 0
        self.tempoChegada = tempoChegada
        self.tempoExecucao = tempoExecucao
        self.tempoRestante = tempoExecucao
        
        # Coisas que a CPU precisa salvar/ler (apenas pra simular)
        self.programCounter = pcInicial
        self.registradores = {'R1': 0, 'R2': 0, 'R3': 0}

class CPU:
    """ Simula a CPU """
    def __init__(self):
        self.pidExecutando = -1 # -1 = CPU ociosa
        self.pcAtual = 0
        self.registradoresCpu = {'R1': 0, 'R2': 0, 'R3': 0}
        
    def carregarContexto(self, processo):
        # "Coloca" o processo na CPU
        self.pidExecutando = processo.pid
        self.pcAtual = processo.programCounter
        self.registradoresCpu = processo.registradores.copy()
        
    def salvarContexto(self, processo):
        # "Tira" o processo da CPU e salva o estado dele
        processo.programCounter = self.pcAtual
        processo.registradores = self.registradoresCpu.copy()
        
    def executarInstrucao(self):
        # Finge que está fazendo algo útil
        self.pcAtual += 1
        self.registradoresCpu['R1'] += 1 # Mexe num registrador

def roundRobin(processos):
    # A fila de processos prontos (FIFO)
    queueSchedule = array.array('i', [0] * quantidadeProcessosSistema)
    head = 0  # De onde sai
    tail = -1 # Onde entra
    
    cpuSimulada = CPU()

    # Prepara o início da simulação
    if processos:
        # O primeiro processo já começa rodando
        cpuSimulada.carregarContexto(processos[0])
        # Um "mapa" pra achar o processo pelo PID
        processosAtivos = {p.pid: p for p in processos}
        
        # Coloca o resto na fila de espera
        for i in range(1, len(processos)):
            tail = (tail + 1) % quantidadeProcessosSistema
            queueSchedule[tail] = processos[i].pid
    else:
        print("Nenhum processo para rodar.")
        return

    def encontrarProcessoPorPid(pid):
        # Acha o objeto do processo na lista
        return processosAtivos.get(pid)

    def trocaDeContexto():
        # Função que faz a troca de contexto, e salva o contexto anterior
        nonlocal head, tail
        
        processoAntigo = encontrarProcessoPorPid(cpuSimulada.pidExecutando)
        
        # 1. Salva quem estava rodando
        if processoAntigo:
            cpuSimulada.salvarContexto(processoAntigo)
        
        # 2. Se ele não terminou, bota ele no fim da fila
        if processoAntigo and processoAntigo.tempoRestante > 0:
            tail = (tail + 1) % quantidadeProcessosSistema
            queueSchedule[tail] = cpuSimulada.pidExecutando
        
        # 3. Puxa o próximo da fila (se tiver alguém)
        if head != (tail + 1) % quantidadeProcessosSistema: # Fila não está vazia?
            
            pidProximo = queueSchedule[head]
            queueSchedule[head] = -1 # Limpa o slot
            head = (head + 1) % quantidadeProcessosSistema # Anda a fila
            
            processoNovo = encontrarProcessoPorPid(pidProximo)
            
            # 4. Carrega o novo processo
            if processoNovo:
                cpuSimulada.carregarContexto(processoNovo)
            else:
                # Deixa a cpu ociosa se o próximo a entrar já tiver terminado
                cpuSimulada.pidExecutando = -1
                
        else:
            # Fila vazia, CPU ociosa.
            cpuSimulada.pidExecutando = -1
            
    # Loop principal da simulação
    while True:
        cpu = cpuSimulada.pidExecutando
        processoAtual = encontrarProcessoPorPid(cpu)
        
        # Se a CPU está livre
        if not processoAtual:
            if not processosAtivos:
                # Ninguém na CPU e ninguém mais na lista = FIM
                print("Todos os processos concluídos.")
            else:
                # Ninguém na CPU, mas ainda tem gente pra rodar
                print("CPU ociosa. Aguardando processos.")
                
            time.sleep(1)
            
            # Tenta puxar o próximo da fila
            if head != (tail + 1) % quantidadeProcessosSistema:
                trocaDeContexto()
            if not processosAtivos:
                # Se tentou puxar e mesmo assim não tem mais ninguém, finaliza
                break
            continue # Volta pro começo do loop

        # Mostra o status atual
        print(f"PID: {processoAtual.pid} | Tempo Restante: {processoAtual.tempoRestante} | PC: {cpuSimulada.pcAtual} | R1: {cpuSimulada.registradoresCpu['R1']}")
        
        # Vê quanto tempo ele vai rodar (o timeSlice ou o que falta)
        tempoExecutado = min(timeSlice, processoAtual.tempoRestante)
        
        # Simula a execução (o "trabalho" em si)
        for _ in range(tempoExecutado):
            cpuSimulada.executarInstrucao()
            time.sleep(1) # 1 segundo por unidade de tempo
            
        processoAtual.tempoRestante -= tempoExecutado
        
        # Se o processo terminou
        if processoAtual.tempoRestante <= 0:
            print(f"Processo {processoAtual.pid} CONCLUÍDO.")
            
            # Tira ele da lista de ativos
            del processosAtivos[processoAtual.pid]
            
            # Puxa o próximo da fila (sem salvar contexto, já que esse acabou)
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
                # Fila vazia
                cpuSimulada.pidExecutando = -1
                
        else:
            # Tempo acabou, mas o processo não.
            trocaDeContexto()

        # Se não tem mais ninguém pra rodar, para o loop
        if not processosAtivos:
            print("FIM DA SIMULAÇÃO.")
            break

#TESTE

# Quantos processos cabem na fila ao mesmo tempo (o tanto que de processos que o sistema tem)
quantidadeProcessosSistema = 8
# tempo máximo que cada processo usa a CPU antes de sair
timeSlice = 3

#Processos simulados
processosExemplo = [
    Processo(pid=101, tempoChegada=0, tempoExecucao=12, pcInicial=1000),
    Processo(pid=102, tempoChegada=2, tempoExecucao=8, pcInicial=2000),
    Processo(pid=103, tempoChegada=3, tempoExecucao=15, pcInicial=3000),
    Processo(pid=104, tempoChegada=5, tempoExecucao=6, pcInicial=4000),
    Processo(pid=105, tempoChegada=8, tempoExecucao=10, pcInicial=5000),
    Processo(pid=106, tempoChegada=10, tempoExecucao=7, pcInicial=6000),
    Processo(pid=107, tempoChegada=12, tempoExecucao=9, pcInicial=7000),
]

roundRobin(processosExemplo)
