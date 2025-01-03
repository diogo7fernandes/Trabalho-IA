import sys
from transporte import Carro, Mota, Helicoptero, Drone
sys.path.append(".")
import math
import os
import json
import subprocess
import platform
import heapq
import networkx as nx
import matplotlib.pyplot as plt

class Grafo:
    
    def __init__(self, direcionado=True):
        self.m_nodos = {}
        self.m_direcionado = direcionado
        self.m_grafo = {}
        self.m_h = {}

    def adicionar_nodo(self, nodo, atributos=None):
        if nodo not in self.m_nodos:
            self.m_nodos[nodo] = atributos if atributos else {}
            self.m_grafo[nodo] = []

    def adicionar_aresta(self, origem, destino, peso=None):
        if origem not in self.m_nodos:
            raise ValueError(f"Nó '{origem}' não existe no grafo.")

        if destino not in self.m_nodos:
            raise ValueError(f"Nó '{destino}' não existe no grafo.")

        if peso is None:
            peso = self.calcular_peso(origem, destino)

        self.m_grafo[origem].append((destino, peso))

    def calcular_peso(self, origem, destino):
        atributos_destino = self.m_nodos.get(destino)
        distancia = self.calcular_distancia(origem, destino)
        prioridade = atributos_destino.get("prioridade", 1)
        acessibilidade = atributos_destino.get("acessibilidade", 1)
        clima = atributos_destino.get("clima", 1)

        c_total = (0.3 * distancia - 0.4 * prioridade + 0.2 * acessibilidade + 0.1 * clima)
        return round(c_total, 2)

    def calcular_distancia(self, nodo1, nodo2):
        coordenadas1 = self.m_nodos[nodo1].get("coordenadas")
        coordenadas2 = self.m_nodos[nodo2].get("coordenadas")

        if not coordenadas1 or not coordenadas2:
            raise ValueError(f"Faltam coordenadas para os nós {nodo1} ou {nodo2}.")

        lat1, lon1 = map(math.radians, coordenadas1)
        lat2, lon2 = map(math.radians, coordenadas2)

        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        R = 6371

        return R * c

    def desenha(self):
        g = nx.DiGraph() if self.m_direcionado else nx.Graph()

        for nodo, atributos in self.m_nodos.items():
            g.add_node(nodo, **atributos)

        for origem, conexoes in self.m_grafo.items():
            for destino, peso in conexoes:
                g.add_edge(origem, destino, weight=peso)

        pos = nx.spring_layout(g, seed=1)

        nx.draw_networkx(
            g,
            pos,
            with_labels=True,
            font_weight="bold",
            node_size=700,
            node_color="lightblue",
            arrows=True,
        )

        plt.title(
            "Representação do Grafo Direcionado"
            if self.m_direcionado
            else "Representação do Grafo Não Direcionado"
        )
        plt.show()

    def atualizar_atributos(self, nodo, prioridade, clima=None, acessibilidade=None, alimentos=None):
        if nodo not in self.m_nodos:
            raise ValueError(f"Localidade '{nodo}' não existe no grafo.")

        if prioridade is not None:
            self.m_nodos[nodo]["prioridade"] = prioridade
        if clima is not None:
            self.m_nodos[nodo]["clima"] = clima
        if acessibilidade is not None:
            self.m_nodos[nodo]["acessibilidade"] = acessibilidade
        if alimentos is not None:
            self.m_nodos[nodo]["alimentos"] = alimentos

    @staticmethod
    def escolher_transporte(acessibilidade):
        if (0 <= acessibilidade <= 5):
            return Carro()
        elif (3 <= acessibilidade <= 7):
            return Mota()
        elif (6 <= acessibilidade <= 10):
            return Helicoptero()
        elif (0 <= acessibilidade <= 10):
            return Drone()
        return None

    def imprimir_distancia(self, origem, destino):
        if origem not in self.m_nodos or destino not in self.m_nodos:
            raise ValueError(f"Nó '{origem}' ou '{destino}' não existe no grafo.")

        coordenadas_origem = self.m_nodos[origem].get("coordenadas")
        coordenadas_destino = self.m_nodos[destino].get("coordenadas")

        if not coordenadas_origem or not coordenadas_destino:
            raise ValueError(
                f"Coordenadas ausentes para calcular a distância entre '{origem}' e '{destino}'."
            )

        lat1, lon1 = coordenadas_origem
        lat2, lon2 = coordenadas_destino

        distancia = Grafo.calcular_distancia(lat1, lon1, lat2, lon2)
        print(f"A distância entre {origem} e {destino} é aproximadamente {distancia:.2f} km.")

    def heuristica_grafo(self):
        if not self.m_nodos:
            raise ValueError("O grafo não possui nós para serem organizados.")

        prioridades = [
            (nodo, atributos.get("prioridade", 0)) 
            for nodo, atributos in self.m_nodos.items()
        ]

        prioridades_ordenadas = sorted(prioridades, key=lambda x: x[1], reverse=True)
        return [localidade for localidade, _ in prioridades_ordenadas]

    def calcular_heuristica(self, nodo, objetivo):
        coordenadas_nodo = self.m_nodos[nodo].get("coordenadas")
        coordenadas_objetivo = self.m_nodos[objetivo].get("coordenadas")

        if not coordenadas_nodo or not coordenadas_objetivo:
            return float('inf')

        lat1, lon1 = coordenadas_nodo
        lat2, lon2 = coordenadas_objetivo

        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        R = 6371
        return R * c

    def imprimir_stats_nodos(self, filename="stats_nodos.json"):
        with open(filename, "w") as file:
            json.dump(self.m_nodos, file, indent=4)
        print(f"Estatísticas dos nós foram salvas em '{filename}'")
        
        sistema = platform.system()
        try:
            if sistema == "Windows":
                os.startfile(filename)
            elif sistema == "Darwin":
                subprocess.run(["open", filename], check=True)
            elif sistema == "Linux":
                subprocess.run(["xdg-open", filename], check=True)
            else:
                print(f"Não foi possível abrir o arquivo automaticamente no sistema {sistema}.")
        except Exception as e:
            print(f"Erro ao tentar abrir o arquivo: {e}")
            
    def encontrar_caminho(self, inicio, objetivo):
        visitados = set()
        fila = [(inicio, [inicio])]

        while fila:
            atual, caminho = fila.pop(0)

            if atual == objetivo:
                return caminho

            if atual not in visitados:
                visitados.add(atual)

                for vizinho, peso in self.m_grafo.get(atual, []):
                    if vizinho not in visitados:
                        fila.append((vizinho, caminho + [vizinho]))

        return None
    
    def encontrar_caminho_DFS(self, inicio, objetivo):
        visitados = set()
        pilha = [(inicio, [inicio])]

        while pilha:
            atual, caminho = pilha.pop()

            if atual == objetivo:
                return caminho

            if atual not in visitados:
                visitados.add(atual)

                for vizinho, peso in self.m_grafo.get(atual, []):
                    if vizinho not in visitados:
                        pilha.append((vizinho, caminho + [vizinho]))

        return None
    
    def verificar_caminho_possivel(self, origem, destino, transporte):
        """
        Verifica se existe um caminho possível entre origem e destino para o transporte dado,
        considerando acessibilidade e autonomia.
        """
        if origem not in self.m_nodos or destino not in self.m_nodos:
            return False
            
        visitados = set()
        fila = [(origem, transporte.autonomia)]
        
        while fila:
            atual, autonomia_restante = fila.pop(0)
            
            if atual == destino:
                return True
                
            if atual not in visitados:
                visitados.add(atual)
                
                for vizinho, _ in self.m_grafo.get(atual, []):
                    if vizinho not in visitados:
                        # Verifica acessibilidade
                        if not transporte.transporte_pode(self.m_nodos[vizinho]["acessibilidade"]):
                            continue
                            
                        # Calcula autonomia necessária
                        distancia = self.calcular_distancia(atual, vizinho)
                        nova_autonomia = autonomia_restante - distancia
                        
                        # Verifica se pode alcançar com a autonomia atual ou se há ponto de reabastecimento
                        if nova_autonomia >= 0 or self.m_nodos[atual].get("reabastecimento", False):
                            # Se há reabastecimento, restaura autonomia total
                            if self.m_nodos[atual].get("reabastecimento", False):
                                nova_autonomia = transporte.deposito
                            fila.append((vizinho, nova_autonomia))
                            
        return False

    def verificar_caminho_completo(self, caminho, transporte):
        """
        Verifica se um caminho completo é possível para o transporte dado.
        """
        if not caminho or len(caminho) < 2:
            return False
            
        for i in range(len(caminho) - 1):
            if not self.verificar_caminho_possivel(caminho[i], caminho[i+1], transporte):
                return False
        return True

    def atualizar_clima(self, nodo, novo_clima):
        """
        Atualiza as condições climáticas de um nodo.
        Clima é representado em uma escala de 0 a 10:
        0-3: Tempo bom
        4-6: Chuva moderada
        7-8: Tempestade
        9-10: Tempestade severa
        """
        if nodo not in self.m_nodos:
            raise ValueError(f"Nó '{nodo}' não existe no grafo.")
        if not (0 <= novo_clima <= 10):
            raise ValueError("Valor do clima deve estar entre 0 e 10")
        
        self.m_nodos[nodo]["clima"] = novo_clima

    def calcular_tempo_viagem(self, origem, destino, transporte):
        """
        Calcula o tempo de viagem entre dois pontos considerando o clima.
        Retorna o tempo em horas e um booleano indicando se é seguro viajar.
        """
        if origem not in self.m_nodos or destino not in self.m_nodos:
            raise ValueError("Origem ou destino não existem no grafo")

        clima_origem = self.m_nodos[origem].get("clima", 0)
        clima_destino = self.m_nodos[destino].get("clima", 0)
        clima_medio = (clima_origem + clima_destino) / 2
        
        # Verificar condições de segurança baseadas no tipo de transporte
        if isinstance(transporte, Helicoptero):
            if clima_medio >= 8:  # Helicoptero não voa em tempestades severas
                return float('inf'), False
        elif isinstance(transporte, Drone):
            if clima_medio >= 7:  # Drone não voa em qualquer tempestade
                return float('inf'), False
        
        # Calcular penalidade de tempo baseada no clima
        penalidade_clima = 1.0  # fator multiplicador base
        
        if clima_medio <= 3:  # Tempo bom
            penalidade_clima = 1.0
        elif clima_medio <= 6:  # Chuva moderada
            penalidade_clima = 1.3
            if isinstance(transporte, Mota):  # Motas são mais afetadas pela chuva
                penalidade_clima = 1.5
        elif clima_medio <= 8:  # Tempestade
            penalidade_clima = 1.6
            if isinstance(transporte, Mota):
                penalidade_clima = 2.0
            elif isinstance(transporte, Carro):
                penalidade_clima = 1.8
        else:  # Tempestade severa
            penalidade_clima = 2.0
            if isinstance(transporte, Mota):
                return float('inf'), False  # Muito perigoso para Motas
            elif isinstance(transporte, Carro):
                penalidade_clima = 2.5
        
        distancia = self.calcular_distancia(origem, destino)
        tempo_base = distancia / transporte.velocidade
        tempo_final = tempo_base * penalidade_clima
        
        return tempo_final, True

    def verificar_seguranca_clima(self, nodo, transporte):
        """
        Verifica se é seguro para o transporte operar no nodo dado as condições climáticas.
        """
        clima = self.m_nodos[nodo].get("clima", 0)
        
        if isinstance(transporte, Helicoptero):
            return clima < 8
        elif isinstance(transporte, Drone):
            return clima < 7
        elif isinstance(transporte, Mota):
            return clima < 9
        else:  # Carro
            return True  # Carros podem operar em qualquer clima, apenas mais lentamente
        
    def verificar_tempo_critico(self, nodo, tempo_atual):
        """
        Verifica se um nodo ainda está acessível baseado em seu tempo crítico.
        
        Args:
            nodo: Nome do nodo
            tempo_atual: Tempo atual da missão em horas
            
        Returns:
            bool: True se o nodo ainda está acessível, False caso contrário
        """
        ttl = self.m_nodos[nodo].get("TTL", float('inf'))
        return tempo_atual <= ttl

    def verificar_caminho_tempo_critico(self, caminho, transporte, tempo_inicial=0):
        """
        Verifica se um caminho completo é viável considerando as janelas de tempo críticas.
        
        Args:
            caminho: Lista de nodos representando o caminho
            transporte: Objeto do tipo Transporte
            tempo_inicial: Tempo inicial da missão em horas
            
        Returns:
            tuple: (bool, float) - (viabilidade do caminho, tempo total)
        """
        if not caminho or len(caminho) < 2:
            return False, 0

        tempo_atual = tempo_inicial
        
        for i in range(len(caminho) - 1):
            atual = caminho[i]
            proximo = caminho[i + 1]
            
            # Verifica se o nodo atual ainda está acessível
            if not self.verificar_tempo_critico(atual, tempo_atual):
                return False, tempo_atual
            
            # Calcula tempo de viagem entre os nodos
            tempo_viagem, seguro = self.calcular_tempo_viagem(atual, proximo, transporte)
            if not seguro or tempo_viagem == float('inf'):
                return False, tempo_atual
            
            # Adiciona tempo de viagem
            tempo_atual += tempo_viagem
            
            # Adiciona tempo de operações se necessário
            if self.m_nodos[proximo].get("alimentos", 0) > 0:
                tempo_atual += 0.5  # 30 minutos para descarregar
            
            if self.m_nodos[atual].get("reabastecimento", False):
                tempo_atual += 0.1  # 6 minutos para reabastecimento
            
            # Verifica se o próximo nodo estará acessível quando chegarmos lá
            if not self.verificar_tempo_critico(proximo, tempo_atual):
                return False, tempo_atual

        return True, tempo_atual

    def verificar_viabilidade_transporte(self, transporte, inicio, objetivo):
        """
        Verifica detalhadamente se um transporte pode completar uma rota entre dois pontos.
        Retorna (bool, str) - (é viável, motivo da inviabilidade)
        """
        # Verificar capacidade de carga
        alimentos_necessarios = self.m_nodos[objetivo].get("alimentos", 0)
        if alimentos_necessarios > transporte.capacidade:
            return False, f"Capacidade insuficiente: necessário {alimentos_necessarios}kg, capacidade {transporte.capacidade}kg"

        # Verificar distância vs autonomia
        distancia = self.calcular_distancia(inicio, objetivo)
        if distancia > transporte.autonomia:
            # Verificar se há ponto de reabastecimento no caminho
            if not self.m_nodos[inicio].get("reabastecimento", False):
                return False, f"Autonomia insuficiente: necessário {distancia}km, autonomia {transporte.autonomia}km"

        # Verificar clima
        clima_inicio = self.m_nodos[inicio].get("clima", 0)
        clima_objetivo = self.m_nodos[objetivo].get("clima", 0)
        clima_medio = (clima_inicio + clima_objetivo) / 2

        if isinstance(transporte, Drone) and clima_medio >= 7:
            return False, f"Clima inadequado para Drone: {clima_medio}"
        elif isinstance(transporte, Mota) and clima_medio >= 9:
            return False, f"Clima muito severo para Moto: {clima_medio}"
        elif isinstance(transporte, Helicoptero) and clima_medio >= 8:
            return False, f"Clima inadequado para Helicóptero: {clima_medio}"

        # Verificar acessibilidade
        acessibilidade = self.m_nodos[objetivo].get("acessibilidade", 0)
        if not transporte.transporte_pode(acessibilidade):
            return False, f"Terreno inacessível: nível {acessibilidade}"

        return True, "OK"
    
    def procura_BFS(self, inicio, transporte, objetivos):
        """
        Implementação atualizada do algoritmo BFS com validações melhoradas.
        """
        # Basic input validation
        if not objetivos:
            print("Lista de objetivos está vazia")
            return [], 0, 0
            
        # Filter for locations that need deliveries
        locais_entrega = [obj for obj in objetivos if self.m_nodos[obj]["alimentos"] > 0]
        if not locais_entrega:
            print("Não há locais que necessitem de entrega")
            return [], 0, 0

        # Validate starting point
        if inicio not in self.m_nodos:
            raise ValueError(f"Nó '{inicio}' não existe no grafo.")
            
        # Validate all objectives exist in graph
        for objetivo in objetivos:
            if objetivo not in self.m_nodos:
                raise ValueError(f"Nó objetivo '{objetivo}' não existe no grafo.")
                
        # Validate starting point accessibility
        if not transporte.transporte_pode(self.m_nodos[inicio]["acessibilidade"]):
            raise ValueError(f"Transporte {transporte.nome} não pode acessar o ponto inicial {inicio}")

        # Check initial vehicle capacity
        maior_carga = max(self.m_nodos[obj]["alimentos"] for obj in locais_entrega)
        if maior_carga > transporte.capacidade:
            print(f"Aviso: Alguns destinos requerem {maior_carga}kg, mas {transporte.nome} só suporta {transporte.capacidade}kg")

        # Initialize variables
        caminho_total = []
        custo_total = 0
        tempo_total = 0
        ponto_atual = inicio
        global_visitados = set()
        tentativas_alternativas = 3

        # Process each delivery location
        for objetivo in locais_entrega:
            # Verify if path is possible considering vehicle limitations
            viavel, motivo = self.verificar_viabilidade_transporte(transporte, ponto_atual, objetivo)
            if not viavel:
                print(f"Destino {objetivo} não é viável: {motivo}")
                continue

            if not self.verificar_caminho_possivel(ponto_atual, objetivo, transporte):
                print(f"Não existe caminho possível entre {ponto_atual} e {objetivo}")
                continue

            fila = [(ponto_atual, [ponto_atual])]
            visitados = set()
            caminho_encontrado = False
            tentativas = tentativas_alternativas
            tempos = {ponto_atual: tempo_total}

            while fila and not caminho_encontrado and tentativas > 0:
                atual, caminho = fila.pop(0)

                if atual == objetivo:
                    viavel, tempo_rota = self.verificar_caminho_tempo_critico(caminho, transporte, tempo_total)
                    if viavel and self.verificar_caminho_completo(caminho, transporte):
                        rota_possivel = True
                        
                        # Verify weather conditions for entire route
                        for j in range(len(caminho) - 1):
                            atual_nodo = caminho[j]
                            proximo_nodo = caminho[j + 1]
                            tempo_viagem, seguro = self.calcular_tempo_viagem(atual_nodo, proximo_nodo, transporte)
                            
                            if not seguro or tempo_viagem == float('inf'):
                                rota_possivel = False
                                print(f"Condições climáticas impedem viagem de {atual_nodo} para {proximo_nodo}")
                                break

                        if rota_possivel:
                            # Process confirmed route
                            for j in range(len(caminho) - 1):
                                atual_nodo = caminho[j]
                                proximo_nodo = caminho[j + 1]
                                
                                if atual_nodo not in objetivos:
                                    global_visitados.add(atual_nodo)

                                distancia = self.calcular_distancia(atual_nodo, proximo_nodo)
                                
                                # Check if refueling is needed
                                if distancia > transporte.autonomia:
                                    if self.m_nodos[atual_nodo].get("reabastecimento", False):
                                        transporte.abastecer()
                                        tempo_total += 0.1  # 6 minutes for refueling
                                        custo_total += 10   # Refueling cost
                                    else:
                                        print(f"Sem ponto de reabastecimento em {atual_nodo}")
                                        rota_possivel = False
                                        break

                                transporte.viajar(distancia)
                                custo_total += distancia
                                tempo_viagem, _ = self.calcular_tempo_viagem(atual_nodo, proximo_nodo, transporte)
                                tempo_total += tempo_viagem

                            if rota_possivel:
                                # Add nodes to total path
                                for nodo in caminho:
                                    if not caminho_total or caminho_total[-1] != nodo:
                                        caminho_total.append(nodo)

                                # Process delivery at destination
                                if self.m_nodos[objetivo]["alimentos"] > 0:
                                    carga = self.m_nodos[objetivo]["alimentos"]
                                    if carga <= transporte.capacidade:
                                        transporte.descarregar(carga)
                                        custo_total += 15  # Delivery cost
                                        tempo_total += 0.5  # 30 minutes for unloading
                                        self.m_nodos[objetivo]["alimentos"] = 0
                                        self.m_nodos[objetivo]["prioridade"] = 0
                                    else:
                                        print(f"Capacidade insuficiente para entrega em {objetivo}")
                                        continue

                                # Resupply if available
                                if self.m_nodos[objetivo].get("supply_refill", False):
                                    transporte.carregar()

                                ponto_atual = objetivo
                                caminho_encontrado = True
                                tempo_total = tempo_rota
                                break
                        
                        if not rota_possivel:
                            tentativas -= 1
                            continue

                if atual not in visitados:
                    visitados.add(atual)
                    for vizinho, _ in self.m_grafo.get(atual, []):
                        if (vizinho not in visitados and 
                            transporte.transporte_pode(self.m_nodos[vizinho]["acessibilidade"])):
                            
                            # Check weather conditions for next step
                            tempo_viagem, seguro = self.calcular_tempo_viagem(atual, vizinho, transporte)
                            if not seguro or tempo_viagem == float('inf'):
                                continue

                            # Verify critical time window
                            tempo_estimado = tempos[atual] + tempo_viagem
                            if not self.verificar_tempo_critico(vizinho, tempo_estimado):
                                continue
                                
                            # Skip already visited nodes unless they're objectives
                            if vizinho in global_visitados and vizinho not in objetivos:
                                continue

                            novo_caminho = caminho + [vizinho]
                            if self.verificar_caminho_possivel(atual, vizinho, transporte):
                                tempos[vizinho] = tempo_estimado
                                fila.append((vizinho, novo_caminho))

            if not caminho_encontrado:
                print(f"Não foi possível encontrar um caminho seguro para {objetivo}")

        # Return results
        if tempo_total > 0:
            tempo_total = (tempo_total * 60) / 100  # Convert to hours
            print(f"Caminho total percorrido: {' -> '.join(caminho_total)}")
            print(f"Custo total acumulado: {custo_total:.3f}")
            print(f"Tempo total acumulado: {tempo_total:.2f} horas")
            return caminho_total, round(custo_total, 3), tempo_total
        else:
            print("Nenhum caminho válido encontrado")
            return [], 0, 0

    def procura_DFS(self, inicio, transporte, objetivos):
        """
        Implementação atualizada do algoritmo DFS com validações melhoradas.
        """
        # Basic input validation
        if not objetivos:
            print("Lista de objetivos está vazia")
            return [], 0, 0
            
        # Filter for locations that need deliveries
        locais_entrega = [obj for obj in objetivos if self.m_nodos[obj]["alimentos"] > 0]
        if not locais_entrega:
            print("Não há locais que necessitem de entrega")
            return [], 0, 0

        # Validate starting point
        if inicio not in self.m_nodos:
            raise ValueError(f"Nó '{inicio}' não existe no grafo.")
            
        # Validate all objectives exist in graph
        for objetivo in objetivos:
            if objetivo not in self.m_nodos:
                raise ValueError(f"Nó objetivo '{objetivo}' não existe no grafo.")
                
        # Validate starting point accessibility
        if not transporte.transporte_pode(self.m_nodos[inicio]["acessibilidade"]):
            raise ValueError(f"Transporte {transporte.nome} não pode acessar o ponto inicial {inicio}")

        # Check initial vehicle capacity
        maior_carga = max(self.m_nodos[obj]["alimentos"] for obj in locais_entrega)
        if maior_carga > transporte.capacidade:
            print(f"Aviso: Alguns destinos requerem {maior_carga}kg, mas {transporte.nome} só suporta {transporte.capacidade}kg")

        # Initialize variables
        caminho_total = []
        custo_total = 0
        tempo_total = 0
        ponto_atual = inicio
        global_visitados = set()
        tentativas_alternativas = 3

        # Process each delivery location
        for objetivo in locais_entrega:
            # Verify if path is possible considering vehicle limitations
            viavel, motivo = self.verificar_viabilidade_transporte(transporte, ponto_atual, objetivo)
            if not viavel:
                print(f"Destino {objetivo} não é viável: {motivo}")
                continue

            if not self.verificar_caminho_possivel(ponto_atual, objetivo, transporte):
                print(f"Não existe caminho possível entre {ponto_atual} e {objetivo}")
                continue

            pilha = [(ponto_atual, [ponto_atual])]
            visitados = set()
            caminho_encontrado = False
            tentativas = tentativas_alternativas

            while pilha and not caminho_encontrado and tentativas > 0:
                atual, caminho = pilha.pop()

                if atual == objetivo:
                    # Check time-critical constraints and path completeness
                    viavel, tempo_rota = self.verificar_caminho_tempo_critico(caminho, transporte, tempo_total)
                    if viavel and self.verificar_caminho_completo(caminho, transporte):
                        rota_possivel = True
                        
                        # Verify weather conditions for entire route
                        for j in range(len(caminho) - 1):
                            atual_nodo = caminho[j]
                            proximo_nodo = caminho[j + 1]
                            tempo_viagem, seguro = self.calcular_tempo_viagem(atual_nodo, proximo_nodo, transporte)
                            
                            if not seguro or tempo_viagem == float('inf'):
                                rota_possivel = False
                                print(f"Condições climáticas impedem viagem de {atual_nodo} para {proximo_nodo}")
                                break

                        if rota_possivel:
                            # Process the confirmed route
                            for j in range(len(caminho) - 1):
                                atual_nodo = caminho[j]
                                proximo_nodo = caminho[j + 1]
                                
                                if atual_nodo not in objetivos:
                                    global_visitados.add(atual_nodo)

                                distancia = self.calcular_distancia(atual_nodo, proximo_nodo)
                                
                                # Check if refueling is needed
                                if distancia > transporte.autonomia:
                                    if self.m_nodos[atual_nodo].get("reabastecimento", False):
                                        transporte.abastecer()
                                        tempo_total += 0.1  # 6 minutes for refueling
                                        custo_total += 10   # Refueling cost
                                    else:
                                        print(f"Sem ponto de reabastecimento em {atual_nodo}")
                                        rota_possivel = False
                                        break

                                # Update vehicle state and costs
                                transporte.viajar(distancia)
                                custo_total += distancia
                                tempo_viagem, _ = self.calcular_tempo_viagem(atual_nodo, proximo_nodo, transporte)
                                tempo_total += tempo_viagem

                            if rota_possivel:
                                # Update total path
                                for nodo in caminho:
                                    if not caminho_total or caminho_total[-1] != nodo:
                                        caminho_total.append(nodo)

                                # Process delivery at destination
                                if self.m_nodos[objetivo]["alimentos"] > 0:
                                    carga = self.m_nodos[objetivo]["alimentos"]
                                    if carga <= transporte.capacidade:
                                        transporte.descarregar(carga)
                                        custo_total += 15  # Delivery cost
                                        tempo_total += 0.5  # 30 minutes for unloading
                                        self.m_nodos[objetivo]["alimentos"] = 0
                                        self.m_nodos[objetivo]["prioridade"] = 0
                                    else:
                                        print(f"Capacidade insuficiente para entrega em {objetivo}")
                                        continue

                                # Resupply if available
                                if self.m_nodos[objetivo].get("supply_refill", False):
                                    transporte.carregar()

                                ponto_atual = objetivo
                                caminho_encontrado = True
                                tempo_total = tempo_rota
                                break

                        if not rota_possivel:
                            tentativas -= 1
                            continue

                if atual not in visitados:
                    visitados.add(atual)
                    # Get neighbors in reverse order for DFS (to maintain depth-first property)
                    vizinhos = [(vizinho, peso) for vizinho, peso in self.m_grafo.get(atual, [])]
                    vizinhos.reverse()  # Process neighbors in reverse order
                    
                    for vizinho, _ in vizinhos:
                        if (vizinho not in visitados and 
                            transporte.transporte_pode(self.m_nodos[vizinho]["acessibilidade"])):
                            
                            # Check weather conditions for next step
                            tempo_viagem, seguro = self.calcular_tempo_viagem(atual, vizinho, transporte)
                            if not seguro or tempo_viagem == float('inf'):
                                continue
                            
                            # Skip already visited nodes unless they're objectives
                            if vizinho in global_visitados and vizinho not in objetivos:
                                continue

                            novo_caminho = caminho + [vizinho]
                            if self.verificar_caminho_possivel(atual, vizinho, transporte):
                                pilha.append((vizinho, novo_caminho))

            if not caminho_encontrado:
                print(f"Não foi possível encontrar um caminho seguro para {objetivo} após {tentativas_alternativas - tentativas} tentativas")

        # Return results
        if tempo_total > 0:
            tempo_total = (tempo_total * 60) / 100  # Convert to hours
            print(f"Caminho total percorrido: {' -> '.join(caminho_total)}")
            print(f"Custo total acumulado: {custo_total:.3f}")
            print(f"Tempo total acumulado: {tempo_total:.2f} horas")
            return caminho_total, round(custo_total, 3), tempo_total
        else:
            print("Nenhum caminho válido encontrado")
            return [], 0, 0

    def a_star(self, inicio, transporte, objetivos):
        """
        Implementação atualizada do algoritmo A* com validações melhoradas.
        """
        # Basic input validation
        if not objetivos:
            print("Lista de objetivos está vazia")
            return [], 0, 0
            
        # Filter for locations that need deliveries
        locais_entrega = [obj for obj in objetivos if self.m_nodos[obj]["alimentos"] > 0]
        if not locais_entrega:
            print("Não há locais que necessitem de entrega")
            return [], 0, 0

        # Validate starting point and objectives
        if inicio not in self.m_nodos:
            raise ValueError(f"Nó '{inicio}' não existe no grafo.")
        for objetivo in objetivos:
            if objetivo not in self.m_nodos:
                raise ValueError(f"Nó objetivo '{objetivo}' não existe no grafo.")
                
        # Validate starting point accessibility
        if not transporte.transporte_pode(self.m_nodos[inicio]["acessibilidade"]):
            raise ValueError(f"Transporte {transporte.nome} não pode acessar o ponto inicial {inicio}")

        # Check initial vehicle capacity
        maior_carga = max(self.m_nodos[obj]["alimentos"] for obj in locais_entrega)
        if maior_carga > transporte.capacidade:
            print(f"Aviso: Alguns destinos requerem {maior_carga}kg, mas {transporte.nome} só suporta {transporte.capacidade}kg")

        # Initialize variables
        caminho_total = []
        custo_total = 0
        tempo_total = 0
        ponto_atual = inicio
        global_visitados = set()
        max_iterations = 1000

        # Process each delivery location
        for objetivo in locais_entrega:
            # Verify if path is possible considering vehicle limitations
            viavel, motivo = self.verificar_viabilidade_transporte(transporte, ponto_atual, objetivo)
            if not viavel:
                print(f"Destino {objetivo} não é viável: {motivo}")
                continue

            if not self.verificar_caminho_possivel(ponto_atual, objetivo, transporte):
                print(f"Não existe caminho possível entre {ponto_atual} e {objetivo}")
                continue

            # A* specific initialization
            tentativas = 3
            caminho_encontrado = False
            iteration_count = 0

            while not caminho_encontrado and tentativas > 0 and iteration_count < max_iterations:
                iteration_count += 1
                fila_prioridade = []
                heapq.heappush(fila_prioridade, (0, 0, ponto_atual, [ponto_atual]))
                visitados = set()
                custos_g = {ponto_atual: 0}
                tempos = {ponto_atual: tempo_total}

                while fila_prioridade and iteration_count < max_iterations:
                    iteration_count += 1
                    f_atual, g_atual, atual, caminho = heapq.heappop(fila_prioridade)

                    if atual == objetivo:
                        viavel, tempo_rota = self.verificar_caminho_tempo_critico(caminho, transporte, tempo_total)
                        if viavel and self.verificar_caminho_completo(caminho, transporte):
                            rota_possivel = True
                            
                            # Verify weather conditions for entire route
                            for j in range(len(caminho) - 1):
                                atual_nodo = caminho[j]
                                proximo_nodo = caminho[j + 1]
                                tempo_viagem, seguro = self.calcular_tempo_viagem(atual_nodo, proximo_nodo, transporte)
                                
                                if not seguro or tempo_viagem == float('inf'):
                                    rota_possivel = False
                                    print(f"Condições climáticas impedem viagem de {atual_nodo} para {proximo_nodo}")
                                    break

                            if rota_possivel:
                                # Process the confirmed route
                                for j in range(len(caminho) - 1):
                                    atual_nodo = caminho[j]
                                    proximo_nodo = caminho[j + 1]
                                    
                                    if atual_nodo not in objetivos:
                                        global_visitados.add(atual_nodo)

                                    distancia = self.calcular_distancia(atual_nodo, proximo_nodo)
                                    
                                    # Check and handle refueling
                                    if distancia > transporte.autonomia:
                                        if self.m_nodos[atual_nodo].get("reabastecimento", False):
                                            transporte.abastecer()
                                            tempo_total += 0.1  # 6 minutes for refueling
                                            custo_total += 10   # Refueling cost
                                        else:
                                            print(f"Sem ponto de reabastecimento em {atual_nodo}")
                                            rota_possivel = False
                                            break

                                    transporte.viajar(distancia)
                                    custo_total += distancia
                                    tempo_viagem, _ = self.calcular_tempo_viagem(atual_nodo, proximo_nodo, transporte)
                                    tempo_total += tempo_viagem

                                if rota_possivel:
                                    # Add nodes to total path
                                    for nodo in caminho:
                                        if not caminho_total or caminho_total[-1] != nodo:
                                            caminho_total.append(nodo)

                                    # Handle delivery at destination
                                    if self.m_nodos[objetivo]["alimentos"] > 0:
                                        carga = self.m_nodos[objetivo]["alimentos"]
                                        if carga <= transporte.capacidade:
                                            transporte.descarregar(carga)
                                            custo_total += 15  # Delivery cost
                                            tempo_total += 0.5  # 30 minutes for unloading
                                            self.m_nodos[objetivo]["alimentos"] = 0
                                            self.m_nodos[objetivo]["prioridade"] = 0
                                        else:
                                            print(f"Capacidade insuficiente para entrega em {objetivo}")
                                            continue

                                    # Resupply if available
                                    if self.m_nodos[objetivo].get("supply_refill", False):
                                        transporte.carregar()

                                    ponto_atual = objetivo
                                    caminho_encontrado = True
                                    tempo_total = tempo_rota
                                    break

                            if not rota_possivel:
                                tentativas -= 1
                                continue

                    if atual in visitados:
                        continue

                    visitados.add(atual)

                    # Process neighbors with A* specific calculations
                    for vizinho, peso in self.m_grafo.get(atual, []):
                        if (vizinho not in visitados and 
                            transporte.transporte_pode(self.m_nodos[vizinho]["acessibilidade"])):
                            
                            # Verify weather conditions
                            tempo_viagem, seguro = self.calcular_tempo_viagem(atual, vizinho, transporte)
                            if not seguro or tempo_viagem == float('inf'):
                                continue

                            # Check time constraints
                            tempo_estimado = tempos[atual] + tempo_viagem
                            if not self.verificar_tempo_critico(vizinho, tempo_estimado):
                                continue

                            # Skip already visited nodes unless they're objectives
                            if vizinho in global_visitados and vizinho not in objetivos:
                                continue

                            # Calculate new path and costs
                            novo_caminho = caminho + [vizinho]
                            if self.verificar_caminho_possivel(atual, vizinho, transporte):
                                novo_g = g_atual + peso
                                if vizinho not in custos_g or novo_g < custos_g[vizinho]:
                                    custos_g[vizinho] = novo_g
                                    tempos[vizinho] = tempo_estimado
                                    h = self.calcular_heuristica(vizinho, objetivo)
                                    f = novo_g + h
                                    heapq.heappush(fila_prioridade, (f, novo_g, vizinho, novo_caminho))

                if iteration_count >= max_iterations:
                    print(f"Limite de iterações atingido para o objetivo {objetivo}")

        # Return results
        if tempo_total > 0:
            tempo_total = (tempo_total * 60) / 100  # Convert to hours
            print(f"Caminho total percorrido: {' -> '.join(caminho_total)}")
            print(f"Custo total acumulado: {custo_total:.3f}")
            print(f"Tempo total acumulado: {tempo_total:.2f} horas")
            return caminho_total, round(custo_total, 3), tempo_total
        else:
            print("Nenhum caminho válido encontrado")
            return [], 0, 0

    def procura_greedy(self, inicio, transporte, objetivos):
        """
        Implementação atualizada do algoritmo Greedy com validações melhoradas.
        """
        # Basic input validation
        if not objetivos:
            print("Lista de objetivos está vazia")
            return [], 0, 0
            
        # Filter for locations that need deliveries
        locais_entrega = [obj for obj in objetivos if self.m_nodos[obj]["alimentos"] > 0]
        if not locais_entrega:
            print("Não há locais que necessitem de entrega")
            return [], 0, 0

        # Validate starting point and objectives
        if inicio not in self.m_nodos:
            raise ValueError(f"Nó '{inicio}' não existe no grafo.")
        for objetivo in objetivos:
            if objetivo not in self.m_nodos:
                raise ValueError(f"Nó objetivo '{objetivo}' não existe no grafo.")
                
        # Validate starting point accessibility
        if not transporte.transporte_pode(self.m_nodos[inicio]["acessibilidade"]):
            raise ValueError(f"Transporte {transporte.nome} não pode acessar o ponto inicial {inicio}")

        # Check initial vehicle capacity against requirements
        maior_carga = max(self.m_nodos[obj]["alimentos"] for obj in locais_entrega)
        if maior_carga > transporte.capacidade:
            print(f"Aviso: Alguns destinos requerem {maior_carga}kg, mas {transporte.nome} só suporta {transporte.capacidade}kg")

        # Initialize variables
        caminho_total = []
        custo_total = 0
        tempo_total = 0
        ponto_atual = inicio
        global_visitados = set()
        max_iterations = 1000

        # Process each delivery location
        for objetivo in locais_entrega:
            # Check viability for current destination
            viavel, motivo = self.verificar_viabilidade_transporte(transporte, ponto_atual, objetivo)
            if not viavel:
                print(f"Destino {objetivo} não é viável: {motivo}")
                continue

            if not self.verificar_caminho_possivel(ponto_atual, objetivo, transporte):
                print(f"Não existe caminho possível entre {ponto_atual} e {objetivo}")
                continue

            # Greedy search initialization
            tentativas = 3
            caminho_encontrado = False
            iteration_count = 0

            while not caminho_encontrado and tentativas > 0 and iteration_count < max_iterations:
                iteration_count += 1
                fila_prioridade = []
                h_inicial = self.calcular_heuristica(ponto_atual, objetivo)
                heapq.heappush(fila_prioridade, (h_inicial, ponto_atual, [ponto_atual]))
                visitados = set()
                tempos = {ponto_atual: tempo_total}

                while fila_prioridade and iteration_count < max_iterations:
                    iteration_count += 1
                    _, atual, caminho = heapq.heappop(fila_prioridade)

                    if atual == objetivo:
                        # Verify time constraints and path completeness
                        viavel, tempo_rota = self.verificar_caminho_tempo_critico(caminho, transporte, tempo_total)
                        if viavel and self.verificar_caminho_completo(caminho, transporte):
                            rota_possivel = True
                            
                            # Check weather conditions for entire route
                            for j in range(len(caminho) - 1):
                                atual_nodo = caminho[j]
                                proximo_nodo = caminho[j + 1]
                                tempo_viagem, seguro = self.calcular_tempo_viagem(atual_nodo, proximo_nodo, transporte)
                                
                                if not seguro or tempo_viagem == float('inf'):
                                    rota_possivel = False
                                    print(f"Condições climáticas impedem viagem de {atual_nodo} para {proximo_nodo}")
                                    break

                            if rota_possivel:
                                # Process the confirmed route
                                for j in range(len(caminho) - 1):
                                    atual_nodo = caminho[j]
                                    proximo_nodo = caminho[j + 1]
                                    
                                    if atual_nodo not in objetivos:
                                        global_visitados.add(atual_nodo)

                                    distancia = self.calcular_distancia(atual_nodo, proximo_nodo)
                                    
                                    # Handle refueling if needed
                                    if distancia > transporte.autonomia:
                                        if self.m_nodos[atual_nodo].get("reabastecimento", False):
                                            transporte.abastecer()
                                            tempo_total += 0.1  # 6 minutes for refueling
                                            custo_total += 10   # Refueling cost
                                        else:
                                            print(f"Sem ponto de reabastecimento em {atual_nodo}")
                                            rota_possivel = False
                                            break

                                    # Update vehicle state and costs
                                    transporte.viajar(distancia)
                                    custo_total += distancia
                                    tempo_viagem, _ = self.calcular_tempo_viagem(atual_nodo, proximo_nodo, transporte)
                                    tempo_total += tempo_viagem

                                if rota_possivel:
                                    # Update total path
                                    for nodo in caminho:
                                        if not caminho_total or caminho_total[-1] != nodo:
                                            caminho_total.append(nodo)

                                    # Handle delivery at destination
                                    if self.m_nodos[objetivo]["alimentos"] > 0:
                                        carga = self.m_nodos[objetivo]["alimentos"]
                                        if carga <= transporte.capacidade:
                                            transporte.descarregar(carga)
                                            custo_total += 15  # Delivery cost
                                            tempo_total += 0.5  # 30 minutes for unloading
                                            self.m_nodos[objetivo]["alimentos"] = 0
                                            self.m_nodos[objetivo]["prioridade"] = 0
                                        else:
                                            print(f"Capacidade insuficiente para entrega em {objetivo}")
                                            continue

                                    # Resupply if available
                                    if self.m_nodos[objetivo].get("supply_refill", False):
                                        transporte.carregar()

                                    ponto_atual = objetivo
                                    caminho_encontrado = True
                                    tempo_total = tempo_rota
                                    break

                            if not rota_possivel:
                                tentativas -= 1
                                continue

                    if atual not in visitados:
                        visitados.add(atual)
                        for vizinho, _ in self.m_grafo.get(atual, []):
                            if (vizinho not in visitados and 
                                transporte.transporte_pode(self.m_nodos[vizinho]["acessibilidade"])):
                                
                                # Check weather conditions
                                tempo_viagem, seguro = self.calcular_tempo_viagem(atual, vizinho, transporte)
                                if not seguro or tempo_viagem == float('inf'):
                                    continue

                                # Check time constraints
                                tempo_estimado = tempos[atual] + tempo_viagem
                                if not self.verificar_tempo_critico(vizinho, tempo_estimado):
                                    continue

                                # Skip already visited nodes unless they're objectives
                                if vizinho in global_visitados and vizinho not in objetivos:
                                    continue

                                novo_caminho = caminho + [vizinho]
                                if self.verificar_caminho_possivel(atual, vizinho, transporte):
                                    # Calculate heuristic for greedy decision
                                    h = self.calcular_heuristica(vizinho, objetivo)
                                    tempos[vizinho] = tempo_estimado
                                    heapq.heappush(fila_prioridade, (h, vizinho, novo_caminho))

                if iteration_count >= max_iterations:
                    print(f"Limite de iterações atingido para o objetivo {objetivo}")

        # Return results
        if tempo_total > 0:
            tempo_total = (tempo_total * 60) / 100  # Convert to hours
            print(f"Caminho total percorrido: {' -> '.join(caminho_total)}")
            print(f"Custo total acumulado: {custo_total:.3f}")
            print(f"Tempo total acumulado: {tempo_total:.2f} horas")
            return caminho_total, round(custo_total, 3), tempo_total
        else:
            print("Nenhum caminho válido encontrado")
            return [], 0, 0
        
    def custo_uniforme(self, inicio, transporte, objetivos):
        """
        Implementação atualizada do algoritmo de Custo Uniforme com validações melhoradas.
        """
        # Basic input validation
        if not objetivos:
            print("Lista de objetivos está vazia")
            return [], 0, 0
            
        # Filter for locations that need deliveries
        locais_entrega = [obj for obj in objetivos if self.m_nodos[obj]["alimentos"] > 0]
        if not locais_entrega:
            print("Não há locais que necessitem de entrega")
            return [], 0, 0

        # Validate starting point
        if inicio not in self.m_nodos:
            raise ValueError(f"Nó '{inicio}' não existe no grafo.")
            
        # Validate all objectives exist in graph
        for objetivo in objetivos:
            if objetivo not in self.m_nodos:
                raise ValueError(f"Nó objetivo '{objetivo}' não existe no grafo.")
                
        # Validate starting point accessibility
        if not transporte.transporte_pode(self.m_nodos[inicio]["acessibilidade"]):
            raise ValueError(f"Transporte {transporte.nome} não pode acessar o ponto inicial {inicio}")

        # Check initial vehicle capacity
        maior_carga = max(self.m_nodos[obj]["alimentos"] for obj in locais_entrega)
        if maior_carga > transporte.capacidade:
            print(f"Aviso: Alguns destinos requerem {maior_carga}kg, mas {transporte.nome} só suporta {transporte.capacidade}kg")

        # Initialize variables
        caminho_total = []
        custo_total = 0
        tempo_total = 0
        ponto_atual = inicio
        visitados_global = set()
        objetivos_restantes = locais_entrega.copy()
        max_iterations = 1000

        # Process remaining objectives
        while objetivos_restantes:
            objetivo_atual = objetivos_restantes[0]
            
            # Verify if path is possible
            viavel, motivo = self.verificar_viabilidade_transporte(transporte, ponto_atual, objetivo_atual)
            if not viavel:
                print(f"Destino {objetivo_atual} não é viável: {motivo}")
                objetivos_restantes.pop(0)
                continue

            if not self.verificar_caminho_possivel(ponto_atual, objetivo_atual, transporte):
                print(f"Não existe caminho possível entre {ponto_atual} e {objetivo_atual}")
                objetivos_restantes.pop(0)
                continue

            if not transporte.transporte_pode(self.m_nodos[objetivo_atual]["acessibilidade"]):
                print(f"Transporte {transporte.nome} não pode acessar {objetivo_atual}")
                objetivos_restantes.pop(0)
                continue

            # Search initialization
            tentativas = 3
            caminho_encontrado = False
            iteration_count = 0

            while not caminho_encontrado and tentativas > 0 and iteration_count < max_iterations:
                iteration_count += 1
                fila_prioridade = [(0, ponto_atual, [ponto_atual])]
                visitados = set()
                custos = {ponto_atual: 0}
                tempos = {ponto_atual: tempo_total}

                while fila_prioridade and iteration_count < max_iterations:
                    iteration_count += 1
                    custo_atual, atual, caminho = heapq.heappop(fila_prioridade)

                    if atual == objetivo_atual:
                        # Verify time constraints and path completeness
                        viavel, tempo_rota = self.verificar_caminho_tempo_critico(caminho, transporte, tempo_total)
                        if viavel and self.verificar_caminho_completo(caminho, transporte):
                            rota_possivel = True
                            
                            # Check weather conditions for entire route
                            for j in range(len(caminho) - 1):
                                atual_nodo = caminho[j]
                                proximo_nodo = caminho[j + 1]
                                tempo_viagem, seguro = self.calcular_tempo_viagem(atual_nodo, proximo_nodo, transporte)
                                
                                if not seguro or tempo_viagem == float('inf'):
                                    rota_possivel = False
                                    print(f"Condições climáticas impedem viagem de {atual_nodo} para {proximo_nodo}")
                                    break

                            if rota_possivel:
                                # Process the confirmed route
                                for j in range(len(caminho) - 1):
                                    atual_nodo = caminho[j]
                                    proximo_nodo = caminho[j + 1]
                                    
                                    if atual_nodo not in objetivos:
                                        visitados_global.add(atual_nodo)

                                    distancia = self.calcular_distancia(atual_nodo, proximo_nodo)
                                    
                                    # Handle refueling if needed
                                    if distancia > transporte.autonomia:
                                        if self.m_nodos[atual_nodo].get("reabastecimento", False):
                                            transporte.abastecer()
                                            tempo_total += 0.1  # 6 minutes for refueling
                                            custo_total += 10   # Refueling cost
                                        else:
                                            print(f"Sem ponto de reabastecimento em {atual_nodo}")
                                            rota_possivel = False
                                            break

                                    transporte.viajar(distancia)
                                    custo_total += distancia
                                    tempo_viagem, _ = self.calcular_tempo_viagem(atual_nodo, proximo_nodo, transporte)
                                    tempo_total += tempo_viagem

                                if rota_possivel:
                                    # Update total path
                                    for nodo in caminho:
                                        if not caminho_total or caminho_total[-1] != nodo:
                                            caminho_total.append(nodo)

                                    # Handle delivery at destination
                                    if self.m_nodos[objetivo_atual]["alimentos"] > 0:
                                        carga = self.m_nodos[objetivo_atual]["alimentos"]
                                        if carga <= transporte.capacidade:
                                            transporte.descarregar(carga)
                                            custo_total += 15  # Delivery cost
                                            tempo_total += 0.5  # 30 minutes for unloading
                                            self.m_nodos[objetivo_atual]["alimentos"] = 0
                                            self.m_nodos[objetivo_atual]["prioridade"] = 0
                                        else:
                                            print(f"Capacidade insuficiente para entrega em {objetivo_atual}")
                                            continue

                                    # Resupply if available
                                    if self.m_nodos[objetivo_atual].get("supply_refill", False):
                                        transporte.carregar()

                                    ponto_atual = objetivo_atual
                                    objetivos_restantes.pop(0)
                                    caminho_encontrado = True
                                    tempo_total = tempo_rota
                                    break

                            if not rota_possivel:
                                tentativas -= 1
                                continue

                    if atual not in visitados:
                        visitados.add(atual)
                        for vizinho, peso in self.m_grafo.get(atual, []):
                            if (vizinho not in visitados and 
                                transporte.transporte_pode(self.m_nodos[vizinho]["acessibilidade"]) and
                                (vizinho not in visitados_global or vizinho in objetivos)):
                                
                                # Check weather safety for next step
                                tempo_viagem, seguro = self.calcular_tempo_viagem(atual, vizinho, transporte)
                                if not seguro or tempo_viagem == float('inf'):
                                    continue
                                
                                # Check critical time window
                                tempo_estimado = tempos[atual] + tempo_viagem
                                if not self.verificar_tempo_critico(vizinho, tempo_estimado):
                                    continue
                                
                                novo_caminho = caminho + [vizinho]
                                if self.verificar_caminho_possivel(atual, vizinho, transporte):
                                    # Calculate new cost considering weather
                                    tempo_base = self.calcular_distancia(atual, vizinho) / transporte.velocidade
                                    multiplicador_clima = tempo_viagem / tempo_base
                                    novo_custo = custo_atual + (peso * multiplicador_clima)
                                    
                                    if vizinho not in custos or novo_custo < custos[vizinho]:
                                        custos[vizinho] = novo_custo
                                        tempos[vizinho] = tempo_estimado
                                        heapq.heappush(fila_prioridade, (novo_custo, vizinho, novo_caminho))

                if iteration_count >= max_iterations:
                    print(f"Limite de iterações atingido para o objetivo {objetivo_atual}")
                    break

            if not caminho_encontrado:
                print(f"Não foi possível encontrar um caminho seguro para {objetivo_atual} após {tentativas} tentativas")
                objetivos_restantes.pop(0)

        # Return results
        if tempo_total > 0:
            tempo_total = (tempo_total * 60) / 100  # Convert to hours
            print(f"Caminho total percorrido: {' -> '.join(caminho_total)}")
            print(f"Custo total acumulado: {custo_total:.3f}")
            print(f"Tempo total acumulado: {tempo_total:.2f} horas")
            return caminho_total, round(custo_total, 3), tempo_total
        else:
            print("Nenhum caminho válido encontrado")
            return [], 0, 0