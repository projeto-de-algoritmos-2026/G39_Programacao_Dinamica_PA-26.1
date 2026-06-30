"""
Algoritmo de Weighted Interval Scheduling
Resolve o problema de agendar intervalos com pesos maximizando o valor total
"""

class Aula:
    """Representa uma aula com horários e prioridade"""
    def __init__(self, id, nome, inicio, fim, prioridade, sala=None):
        self.id = id
        self.nome = nome
        self.inicio = inicio  # em minutos desde 00:00
        self.fim = fim        # em minutos desde 00:00
        self.prioridade = prioridade
        self.sala = sala
    
    def __repr__(self):
        h_ini = self.inicio // 60
        m_ini = self.inicio % 60
        h_fim = self.fim // 60
        m_fim = self.fim % 60
        return f"{self.nome} ({h_ini:02d}:{m_ini:02d}-{h_fim:02d}:{m_fim:02d}) P:{self.prioridade}"


def converter_hora_para_minutos(hora_str):
    """Converte string 'HH:MM' para minutos desde 00:00"""
    h, m = map(int, hora_str.split(':'))
    return h * 60 + m


def encontrar_ultima_aula_compativel(aulas, indice):
    """
    Encontra a última aula que não conflita com aulas[indice]
    
    Uma aula j é compatível se seu fim <= início da aula i
    """
    aula_atual = aulas[indice]
    
    # Procura de trás pra frente a última aula que termina antes desta começar
    for j in range(indice - 1, -1, -1):
        if aulas[j].fim <= aula_atual.inicio:
            return j
    
    return -1  # Nenhuma aula compatível


def weighted_interval_scheduling(aulas_lista):
    """
    Resolve o problema de Weighted Interval Scheduling
    
    Args:
        aulas_lista: Lista de objetos Aula
    
    Returns:
        tuple: (aulas_selecionadas, prioridade_total)
    """
    
    # 1. Ordena aulas por horário de término
    aulas = sorted(aulas_lista, key=lambda a: a.fim)
    n = len(aulas)
    
    if n == 0:
        return [], 0
    
    # 2. Cria array de programação dinâmica
    # dp[i] = máxima prioridade usando aulas 0..i
    dp = [0] * n
    compativel = [-1] * n  # índice da última aula compatível
    
    # 3. Base: primeira aula sempre é considerada
    dp[0] = aulas[0].prioridade
    compativel[0] = -1
    
    # 4. Preenche a tabela DP
    for i in range(1, n):
        # Opção 1: Incluir a aula i
        # Valor = prioridade da aula i + máximo que conseguimos com aulas compatíveis
        ultima_compativel = encontrar_ultima_aula_compativel(aulas, i)
        compativel[i] = ultima_compativel
        
        valor_incluindo = aulas[i].prioridade
        if ultima_compativel != -1:
            valor_incluindo += dp[ultima_compativel]
        
        # Opção 2: NÃO incluir a aula i
        valor_nao_incluindo = dp[i - 1]
        
        # Escolhe o melhor
        dp[i] = max(valor_incluindo, valor_nao_incluindo)
    
    # 5. Reconstrói a solução (backtracking)
    aulas_selecionadas = []
    i = n - 1
    
    while i >= 0:
        # Verifica se a aula i foi incluída
        valor_incluindo = aulas[i].prioridade
        if compativel[i] != -1:
            valor_incluindo += dp[compativel[i]]
        else:
            valor_incluindo = aulas[i].prioridade
        
        valor_nao_incluindo = dp[i - 1] if i > 0 else 0
        
        # Se incluir é melhor, aula i foi selecionada
        if valor_incluindo > valor_nao_incluindo:
            aulas_selecionadas.append(aulas[i])
            i = compativel[i]
        else:
            i -= 1
    
    # Inverte para ordem crescente
    aulas_selecionadas.reverse()
    
    return aulas_selecionadas, dp[n - 1]


def alocar_aulas_em_salas(aulas_selecionadas, num_salas):
    """
    Aloca as aulas selecionadas nas salas disponíveis
    MELHORADO: Distribui balanceadamente entre as salas
    Escolhe a sala com MENOS aulas (e sem conflitos)
    
    Args:
        aulas_selecionadas: Lista de aulas já filtradas pelo scheduling
        num_salas: Número total de salas
    
    Returns:
        dict: {num_sala: [aulas alocadas naquela sala]}
    """
    salas = {i: [] for i in range(1, num_salas + 1)}
    
    for aula in aulas_selecionadas:
        melhor_sala = -1
        menor_aulas = float('inf')
        
        # Procura a sala com MENOS aulas e sem conflito
        for sala_num in range(1, num_salas + 1):
            pode_alocar = True
            
            # Verifica se há conflito nesta sala
            for aula_existente in salas[sala_num]:
                if not (aula.fim <= aula_existente.inicio or 
                        aula.inicio >= aula_existente.fim):
                    pode_alocar = False
                    break
            
            # Se não há conflito, compara com melhor opção
            if pode_alocar:
                num_aulas = len(salas[sala_num])
                if num_aulas < menor_aulas:
                    menor_aulas = num_aulas
                    melhor_sala = sala_num
        
        # Aloca na sala com menos aulas
        if melhor_sala != -1:
            aula.sala = melhor_sala
            salas[melhor_sala].append(aula)
        else:
            print(f"AVISO: Não foi possível alocar {aula.nome} em nenhuma sala sem conflito")
    
    return salas


# Exemplo de uso
if __name__ == "__main__":
    # Cria aulas de exemplo
    aulas_teste = [
        Aula(1, "Python I", converter_hora_para_minutos("08:00"), 
             converter_hora_para_minutos("09:00"), 5),
        Aula(2, "Python II", converter_hora_para_minutos("08:30"), 
             converter_hora_para_minutos("09:30"), 3),
        Aula(3, "Java", converter_hora_para_minutos("09:00"), 
             converter_hora_para_minutos("10:00"), 4),
        Aula(4, "C++", converter_hora_para_minutos("10:00"), 
             converter_hora_para_minutos("11:00"), 2),
    ]
    
    # Executa o algoritmo
    selecionadas, total = weighted_interval_scheduling(aulas_teste)
    
    print("=== WEIGHTED INTERVAL SCHEDULING ===\n")
    print("Aulas Selecionadas:")
    for aula in selecionadas:
        print(f"  {aula}")
    
    print(f"\nPrioridade Total: {total}")
    
    # Aloca em salas
    agendamento = alocar_aulas_em_salas(selecionadas, num_salas=2)
    
    print("\n=== AGENDAMENTO POR SALA ===")
    for sala, aulas_da_sala in agendamento.items():
        print(f"\nSala {sala}:")
        for aula in sorted(aulas_da_sala, key=lambda a: a.inicio):
            h_ini = aula.inicio // 60
            m_ini = aula.inicio % 60
            h_fim = aula.fim // 60
            m_fim = aula.fim % 60
            print(f"  {aula.nome}: {h_ini:02d}:{m_ini:02d}-{h_fim:02d}:{m_fim:02d}")