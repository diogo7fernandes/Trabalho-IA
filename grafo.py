import sys
from transporte import Carro, Moto, Helicoptero, Drone
sys.path.append(".")
import math
import os
import json
import subprocess
import platform
import heapq
import networkx as nx
import matplotlib.pyplot as plt
import transporte as tr

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
            return Moto()
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
            if isinstance(transporte, Moto):  # Motos são mais afetadas pela chuva
                penalidade_clima = 1.5
        elif clima_medio <= 8:  # Tempestade
            penalidade_clima = 1.6
            if isinstance(transporte, Moto):
                penalidade_clima = 2.0
            elif isinstance(transporte, Carro):
                penalidade_clima = 1.8
        else:  # Tempestade severa
            penalidade_clima = 2.0
            if isinstance(transporte, Moto):
                return float('inf'), False  # Muito perigoso para motos
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
        elif isinstance(transporte, Moto):
            return clima < 9
        else:  # Carro
            return True  # Carros podem operar em qualquer clima, apenas mais lentamente
    
    def procura_BFS(self, inicio, transporte, objetivos):
        if inicio not in self.m_nodos:
            raise ValueError(f"Nó '{inicio}' não existe no grafo.")
        for objetivo in objetivos:
            if objetivo not in self.m_nodos:
                raise ValueError(f"Nó objetivo '{objetivo}' não existe no grafo.")

        # Verificar acessibilidade inicial
        if not transporte.transporte_pode(self.m_nodos[inicio]["acessibilidade"]):
            raise ValueError(f"Transporte {transporte.nome} não pode acessar o ponto inicial {inicio}")

        caminho_total = []
        custo_total = 0
        tempo_total = 0
        ponto_atual = inicio
        global_visitados = set()
        tentativas_alternativas = 3  # Número de tentativas para encontrar rotas alternativas

        # Process objectives one by one
        for objetivo in objetivos:
            if not self.verificar_caminho_possivel(ponto_atual, objetivo, transporte):
                print(f"Não existe caminho possível entre {ponto_atual} e {objetivo}")
                continue

            fila = [(ponto_atual, [ponto_atual])]
            visitados = set()
            caminho_encontrado = False
            tentativas = tentativas_alternativas

            while fila and not caminho_encontrado and tentativas > 0:
                atual, caminho = fila.pop(0)

                if atual == objetivo:
                    if self.verificar_caminho_completo(caminho, transporte):
                        rota_possivel = True
                        tempo_rota_total = 0
                        
                        # Verificar toda a rota antes de confirmar
                        for j in range(len(caminho) - 1):
                            atual_nodo = caminho[j]
                            proximo_nodo = caminho[j + 1]
                            
                            # Verificar condições climáticas e calcular tempo
                            tempo_viagem, seguro = self.calcular_tempo_viagem(atual_nodo, proximo_nodo, transporte)
                            
                            if tempo_viagem == float('inf'):
                                rota_possivel = False
                                break
                            
                            tempo_rota_total += tempo_viagem

                        if rota_possivel:
                            # Processar a rota confirmada
                            for j in range(len(caminho) - 1):
                                atual_nodo = caminho[j]
                                proximo_nodo = caminho[j + 1]
                                
                                if atual_nodo not in objetivos:
                                    global_visitados.add(atual_nodo)

                                distancia = self.calcular_distancia(atual_nodo, proximo_nodo)
                                if distancia > transporte.autonomia:
                                    if self.m_nodos[atual_nodo].get("reabastecimento", False):
                                        transporte.abastecer()
                                        tempo_total += 0.1  # 6 minutos para reabastecimento
                                        custo_total += 10   # Custo do reabastecimento

                                transporte.viajar(distancia)
                                custo_total += distancia
                                tempo_viagem, _ = self.calcular_tempo_viagem(atual_nodo, proximo_nodo, transporte)
                                tempo_total += tempo_viagem

                            # Atualizar caminho total
                            for nodo in caminho:
                                if not caminho_total or caminho_total[-1] != nodo:
                                    caminho_total.append(nodo)

                            # Processar entrega se houver alimentos
                            if self.m_nodos[objetivo]["alimentos"] > 0:
                                transporte.descarregar(self.m_nodos[objetivo]["alimentos"])
                                custo_total += 15  # Custo da entrega
                                tempo_total += 0.5  # 30 minutos para descarregar
                                self.m_nodos[objetivo]["alimentos"] = 0
                                self.m_nodos[objetivo]["prioridade"] = 0

                            if self.m_nodos[objetivo].get("supply_refill", False):
                                transporte.carregar()

                            ponto_atual = objetivo
                            caminho_encontrado = True
                            break
                        else:
                            tentativas -= 1
                            continue

                if atual not in visitados:
                    visitados.add(atual)
                    for vizinho, _ in self.m_grafo.get(atual, []):
                        if vizinho not in visitados and transporte.transporte_pode(self.m_nodos[vizinho]["acessibilidade"]):
                            # Verificar se é seguro viajar para o próximo nodo
                            tempo_viagem, seguro = self.calcular_tempo_viagem(atual, vizinho, transporte)
                            if tempo_viagem == float('inf'):
                                continue  # Pular este vizinho se as condições climáticas forem muito severas
                            
                            if vizinho in global_visitados and vizinho not in objetivos:
                                continue
                            novo_caminho = caminho + [vizinho]
                            if self.verificar_caminho_possivel(atual, vizinho, transporte):
                                fila.append((vizinho, novo_caminho))

            if not caminho_encontrado:
                print(f"Não foi possível encontrar um caminho seguro para {objetivo} após {tentativas_alternativas} tentativas")

        if tempo_total > 0:
            tempo_total = (tempo_total * 60) / 100  # Converter para horas
            print(f"Caminho total percorrido: {caminho_total}")
            print(f"Custo total acumulado: {custo_total:.3f}")
            print(f"Tempo total acumulado: {tempo_total:.2f} horas")
            return caminho_total, round(custo_total, 3), tempo_total
        else:
            print("Nenhum caminho válido encontrado devido às condições climáticas")
            return [], 0, 0
    
    def procura_DFS(self, inicio, transporte, objetivos):
            if inicio not in self.m_nodos:
                raise ValueError(f"Nó '{inicio}' não existe no grafo.")
            for objetivo in objetivos:
                if objetivo not in self.m_nodos:
                    raise ValueError(f"Nó objetivo '{objetivo}' não existe no grafo.")

            # Verificar acessibilidade inicial
            if not transporte.transporte_pode(self.m_nodos[inicio]["acessibilidade"]):
                raise ValueError(f"Transporte {transporte.nome} não pode acessar o ponto inicial {inicio}")

            caminho_total = []
            custo_total = 0
            tempo_total = 0
            ponto_atual = inicio
            global_visitados = set()
            tentativas_alternativas = 3  # Número de tentativas para encontrar rotas alternativas

            # Process objectives one by one
            for objetivo in objetivos:
                if not self.verificar_caminho_possivel(ponto_atual, objetivo, transporte):
                    print(f"Não existe caminho possível entre {ponto_atual} e {objetivo} para {transporte.nome}")
                    continue

                if not transporte.transporte_pode(self.m_nodos[objetivo]["acessibilidade"]):
                    print(f"Transporte {transporte.nome} não pode acessar {objetivo}. Pulando...")
                    continue

                pilha = [(ponto_atual, [ponto_atual])]
                visitados = set()
                caminho_encontrado = False
                tentativas = tentativas_alternativas

                while pilha and not caminho_encontrado and tentativas > 0:
                    atual, caminho = pilha.pop()

                    if atual == objetivo:
                        if self.verificar_caminho_completo(caminho, transporte):
                            rota_possivel = True
                            tempo_rota_total = 0
                            
                            # Verificar toda a rota antes de confirmar
                            for j in range(len(caminho) - 1):
                                atual_nodo = caminho[j]
                                proximo_nodo = caminho[j + 1]
                                
                                # Verificar condições climáticas e calcular tempo
                                tempo_viagem, seguro = self.calcular_tempo_viagem(atual_nodo, proximo_nodo, transporte)
                                
                                if not seguro or tempo_viagem == float('inf'):
                                    rota_possivel = False
                                    break
                                
                                tempo_rota_total += tempo_viagem

                            if rota_possivel:
                                # Processar a rota confirmada
                                for j in range(len(caminho) - 1):
                                    atual_nodo = caminho[j]
                                    proximo_nodo = caminho[j + 1]
                                    
                                    if atual_nodo not in objetivos:
                                        global_visitados.add(atual_nodo)

                                    distancia = self.calcular_distancia(atual_nodo, proximo_nodo)
                                    if distancia > transporte.autonomia:
                                        if self.m_nodos[atual_nodo].get("reabastecimento", False):
                                            transporte.abastecer()
                                            tempo_total += 0.1  # 6 minutos para reabastecimento
                                            custo_total += 10   # Custo do reabastecimento

                                    transporte.viajar(distancia)
                                    custo_total += distancia
                                    tempo_viagem, _ = self.calcular_tempo_viagem(atual_nodo, proximo_nodo, transporte)
                                    tempo_total += tempo_viagem

                                # Atualizar caminho total
                                for nodo in caminho:
                                    if not caminho_total or caminho_total[-1] != nodo:
                                        caminho_total.append(nodo)

                                # Processar entrega se houver alimentos
                                if self.m_nodos[objetivo]["alimentos"] > 0:
                                    transporte.descarregar(self.m_nodos[objetivo]["alimentos"])
                                    custo_total += 15  # Custo da entrega
                                    tempo_total += 0.5  # 30 minutos para descarregar
                                    self.m_nodos[objetivo]["alimentos"] = 0
                                    self.m_nodos[objetivo]["prioridade"] = 0

                                if self.m_nodos[objetivo].get("supply_refill", False):
                                    transporte.carregar()

                                ponto_atual = objetivo
                                caminho_encontrado = True
                                break
                            else:
                                tentativas -= 1
                                continue

                    if atual not in visitados:
                        visitados.add(atual)
                        for vizinho, _ in self.m_grafo.get(atual, []):
                            if vizinho not in visitados and transporte.transporte_pode(self.m_nodos[vizinho]["acessibilidade"]):
                                # Verificar se é seguro viajar para o próximo nodo
                                tempo_viagem, seguro = self.calcular_tempo_viagem(atual, vizinho, transporte)
                                if not seguro or tempo_viagem == float('inf'):
                                    continue  # Pular este vizinho se as condições climáticas forem muito severas
                                
                                if vizinho in global_visitados and vizinho not in objetivos:
                                    continue
                                novo_caminho = caminho + [vizinho]
                                if self.verificar_caminho_possivel(atual, vizinho, transporte):
                                    pilha.append((vizinho, novo_caminho))

                if not caminho_encontrado:
                    print(f"Não foi possível encontrar um caminho seguro para {objetivo} após {tentativas_alternativas} tentativas")

            if tempo_total > 0:
                tempo_total = (tempo_total * 60) / 100  # Converter para horas
                print(f"Caminho total percorrido: {caminho_total}")
                print(f"Custo total acumulado: {custo_total:.3f}")
                print(f"Tempo total acumulado: {tempo_total:.2f} horas")
                return caminho_total, round(custo_total, 3), tempo_total
            else:
                print("Nenhum caminho válido encontrado devido às condições climáticas")
                return [], 0, 0

    def a_star(self, inicio, transporte, objetivos):
        """
        A* algorithm implementation with additional safety checks and timeout mechanism
        """
        if inicio not in self.m_nodos:
            raise ValueError(f"Nó '{inicio}' não existe no grafo.")
        for objetivo in objetivos:
            if objetivo not in self.m_nodos:
                raise ValueError(f"Nó objetivo '{objetivo}' não existe no grafo.")
        if not transporte.transporte_pode(self.m_nodos[inicio]["acessibilidade"]):
            raise ValueError(f"Transporte {transporte.nome} não pode acessar o ponto inicial {inicio}")

        caminho_total = []
        custo_total = 0
        tempo_total = 0
        ponto_atual = inicio
        global_visitados = set()
        max_iterations = 1000  # Prevent infinite loops

        for objetivo in objetivos:
            if not self.verificar_caminho_possivel(ponto_atual, objetivo, transporte):
                print(f"Não existe caminho possível entre {ponto_atual} e {objetivo}")
                continue

            tentativas = 3
            caminho_encontrado = False
            iteration_count = 0

            while not caminho_encontrado and tentativas > 0 and iteration_count < max_iterations:
                fila_prioridade = []
                heapq.heappush(fila_prioridade, (0, 0, ponto_atual, [ponto_atual]))  # (f_score, g_score, node, path)
                visitados = set()
                custos_g = {ponto_atual: 0}

                while fila_prioridade and iteration_count < max_iterations:
                    iteration_count += 1
                    f_atual, g_atual, atual, caminho = heapq.heappop(fila_prioridade)

                    if atual == objetivo:
                        if self.verificar_caminho_completo(caminho, transporte):
                            rota_possivel = True
                            
                            # Verify weather conditions
                            for j in range(len(caminho) - 1):
                                atual_nodo = caminho[j]
                                proximo_nodo = caminho[j + 1]
                                tempo_viagem, seguro = self.calcular_tempo_viagem(atual_nodo, proximo_nodo, transporte)
                                
                                if not seguro or tempo_viagem == float('inf'):
                                    rota_possivel = False
                                    break

                            if rota_possivel:
                                # Process the route
                                for j in range(len(caminho) - 1):
                                    atual_nodo = caminho[j]
                                    proximo_nodo = caminho[j + 1]
                                    
                                    if atual_nodo not in objetivos:
                                        global_visitados.add(atual_nodo)

                                    distancia = self.calcular_distancia(atual_nodo, proximo_nodo)
                                    if distancia > transporte.autonomia:
                                        if self.m_nodos[atual_nodo].get("reabastecimento", False):
                                            transporte.abastecer()
                                            tempo_total += 0.1
                                            custo_total += 10

                                    transporte.viajar(distancia)
                                    custo_total += distancia
                                    tempo_viagem, _ = self.calcular_tempo_viagem(atual_nodo, proximo_nodo, transporte)
                                    tempo_total += tempo_viagem

                                for nodo in caminho:
                                    if not caminho_total or caminho_total[-1] != nodo:
                                        caminho_total.append(nodo)

                                if self.m_nodos[objetivo]["alimentos"] > 0:
                                    transporte.descarregar(self.m_nodos[objetivo]["alimentos"])
                                    custo_total += 15
                                    tempo_total += 0.5
                                    self.m_nodos[objetivo]["alimentos"] = 0
                                    self.m_nodos[objetivo]["prioridade"] = 0

                                if self.m_nodos[objetivo].get("supply_refill", False):
                                    transporte.carregar()

                                ponto_atual = objetivo
                                caminho_encontrado = True
                                break

                    if atual in visitados:
                        continue
                        
                    visitados.add(atual)

                    for vizinho, peso in self.m_grafo.get(atual, []):
                        if (vizinho not in visitados and 
                            transporte.transporte_pode(self.m_nodos[vizinho]["acessibilidade"])):
                            
                            tempo_viagem, seguro = self.calcular_tempo_viagem(atual, vizinho, transporte)
                            if not seguro or tempo_viagem == float('inf'):
                                continue

                            if vizinho in global_visitados and vizinho not in objetivos:
                                continue

                            novo_caminho = caminho + [vizinho]
                            if self.verificar_caminho_possivel(atual, vizinho, transporte):
                                novo_g = g_atual + peso
                                if vizinho not in custos_g or novo_g < custos_g[vizinho]:
                                    custos_g[vizinho] = novo_g
                                    h = self.calcular_heuristica(vizinho, objetivo)
                                    f = novo_g + h
                                    heapq.heappush(fila_prioridade, (f, novo_g, vizinho, novo_caminho))

                if not caminho_encontrado:
                    tentativas -= 1

            if iteration_count >= max_iterations:
                print(f"Limite de iterações atingido para o objetivo {objetivo}")

        if tempo_total > 0:
            tempo_total = (tempo_total * 60) / 100
            print(f"Caminho total percorrido: {caminho_total}")
            print(f"Custo total acumulado: {custo_total:.3f}")
            print(f"Tempo total acumulado: {tempo_total:.2f} horas")
            return caminho_total, round(custo_total, 3), tempo_total
        else:
            print("Nenhum caminho válido encontrado")
            return [], 0, 0

    def procura_greedy(self, inicio, transporte, objetivos):
        """
        Greedy search implementation with additional safety checks and timeout mechanism
        """
        if inicio not in self.m_nodos:
            raise ValueError(f"Nó '{inicio}' não existe no grafo.")
        for objetivo in objetivos:
            if objetivo not in self.m_nodos:
                raise ValueError(f"Nó objetivo '{objetivo}' não existe no grafo.")
        if not transporte.transporte_pode(self.m_nodos[inicio]["acessibilidade"]):
            raise ValueError(f"Transporte {transporte.nome} não pode acessar o ponto inicial {inicio}")

        caminho_total = []
        custo_total = 0
        tempo_total = 0
        ponto_atual = inicio
        global_visitados = set()
        max_iterations = 1000

        for objetivo in objetivos:
            if not self.verificar_caminho_possivel(ponto_atual, objetivo, transporte):
                print(f"Não existe caminho possível entre {ponto_atual} e {objetivo}")
                continue

            tentativas = 3
            caminho_encontrado = False
            iteration_count = 0

            while not caminho_encontrado and tentativas > 0 and iteration_count < max_iterations:
                iteration_count += 1
                fila_prioridade = []
                h_inicial = self.calcular_heuristica(ponto_atual, objetivo)
                heapq.heappush(fila_prioridade, (h_inicial, ponto_atual, [ponto_atual]))
                visitados = set()

                while fila_prioridade and iteration_count < max_iterations:
                    iteration_count += 1
                    _, atual, caminho = heapq.heappop(fila_prioridade)

                    if atual == objetivo:
                        if self.verificar_caminho_completo(caminho, transporte):
                            rota_possivel = True
                            
                            # Check weather conditions
                            for j in range(len(caminho) - 1):
                                atual_nodo = caminho[j]
                                proximo_nodo = caminho[j + 1]
                                tempo_viagem, seguro = self.calcular_tempo_viagem(atual_nodo, proximo_nodo, transporte)
                                
                                if not seguro or tempo_viagem == float('inf'):
                                    rota_possivel = False
                                    break

                            if rota_possivel:
                                # Process valid route
                                for j in range(len(caminho) - 1):
                                    atual_nodo = caminho[j]
                                    proximo_nodo = caminho[j + 1]
                                    
                                    if atual_nodo not in objetivos:
                                        global_visitados.add(atual_nodo)

                                    distancia = self.calcular_distancia(atual_nodo, proximo_nodo)
                                    if distancia > transporte.autonomia:
                                        if self.m_nodos[atual_nodo].get("reabastecimento", False):
                                            transporte.abastecer()
                                            tempo_total += 0.1
                                            custo_total += 10

                                    transporte.viajar(distancia)
                                    custo_total += distancia
                                    tempo_viagem, _ = self.calcular_tempo_viagem(atual_nodo, proximo_nodo, transporte)
                                    tempo_total += tempo_viagem

                                for nodo in caminho:
                                    if not caminho_total or caminho_total[-1] != nodo:
                                        caminho_total.append(nodo)

                                if self.m_nodos[objetivo]["alimentos"] > 0:
                                    transporte.descarregar(self.m_nodos[objetivo]["alimentos"])
                                    custo_total += 15
                                    tempo_total += 0.5
                                    self.m_nodos[objetivo]["alimentos"] = 0
                                    self.m_nodos[objetivo]["prioridade"] = 0

                                if self.m_nodos[objetivo].get("supply_refill", False):
                                    transporte.carregar()

                                ponto_atual = objetivo
                                caminho_encontrado = True
                                break

                    if atual not in visitados:
                        visitados.add(atual)
                        for vizinho, _ in self.m_grafo.get(atual, []):
                            if (vizinho not in visitados and 
                                transporte.transporte_pode(self.m_nodos[vizinho]["acessibilidade"])):
                                
                                tempo_viagem, seguro = self.calcular_tempo_viagem(atual, vizinho, transporte)
                                if not seguro or tempo_viagem == float('inf'):
                                    continue

                                if vizinho in global_visitados and vizinho not in objetivos:
                                    continue

                                novo_caminho = caminho + [vizinho]
                                if self.verificar_caminho_possivel(atual, vizinho, transporte):
                                    h = self.calcular_heuristica(vizinho, objetivo)
                                    heapq.heappush(fila_prioridade, (h, vizinho, novo_caminho))

                if not caminho_encontrado:
                    tentativas -= 1

            if iteration_count >= max_iterations:
                print(f"Limite de iterações atingido para o objetivo {objetivo}")

        if tempo_total > 0:
            tempo_total = (tempo_total * 60) / 100
            print(f"Caminho total percorrido: {caminho_total}")
            print(f"Custo total acumulado: {custo_total:.3f}")
            print(f"Tempo total acumulado: {tempo_total:.2f} horas")
            return caminho_total, round(custo_total, 3), tempo_total
        else:
            print("Nenhum caminho válido encontrado")
            return [], 0, 0
    
    def custo_uniforme(self, inicio, transporte, objetivos):
        """
        Uniform Cost Search implementation with additional safety checks and timeout mechanism
        """
        if inicio not in self.m_nodos:
            raise ValueError(f"Nó '{inicio}' não existe no grafo.")
        for objetivo in objetivos:
            if objetivo not in self.m_nodos:
                raise ValueError(f"Nó objetivo '{objetivo}' não existe no grafo.")
        if not transporte.transporte_pode(self.m_nodos[inicio]["acessibilidade"]):
            raise ValueError(f"Transporte {transporte.nome} não pode acessar o ponto inicial {inicio}")

        caminho_total = []
        custo_total = 0
        tempo_total = 0
        ponto_atual = inicio
        visitados_global = set()
        objetivos_restantes = objetivos.copy()
        max_iterations = 1000  # Prevent infinite loops

        while objetivos_restantes:
            objetivo_atual = objetivos_restantes[0]
            
            if not self.verificar_caminho_possivel(ponto_atual, objetivo_atual, transporte):
                print(f"Não existe caminho possível entre {ponto_atual} e {objetivo_atual}")
                objetivos_restantes.pop(0)
                continue

            if not transporte.transporte_pode(self.m_nodos[objetivo_atual]["acessibilidade"]):
                print(f"Transporte {transporte.nome} não pode acessar {objetivo_atual}")
                objetivos_restantes.pop(0)
                continue

            tentativas = 3
            caminho_encontrado = False
            iteration_count = 0

            while not caminho_encontrado and tentativas > 0 and iteration_count < max_iterations:
                iteration_count += 1
                fila_prioridade = [(0, ponto_atual, [ponto_atual])]  # (cost, node, path)
                visitados = set()
                custos = {ponto_atual: 0}

                while fila_prioridade and iteration_count < max_iterations:
                    iteration_count += 1
                    custo_atual, atual, caminho = heapq.heappop(fila_prioridade)

                    if atual == objetivo_atual:
                        if self.verificar_caminho_completo(caminho, transporte):
                            rota_possivel = True
                            
                            # Check weather conditions for entire route
                            for j in range(len(caminho) - 1):
                                atual_nodo = caminho[j]
                                proximo_nodo = caminho[j + 1]
                                tempo_viagem, seguro = self.calcular_tempo_viagem(atual_nodo, proximo_nodo, transporte)
                                
                                if not seguro or tempo_viagem == float('inf'):
                                    rota_possivel = False
                                    break

                            if rota_possivel:
                                # Process the confirmed route
                                for j in range(len(caminho) - 1):
                                    atual_nodo = caminho[j]
                                    proximo_nodo = caminho[j + 1]
                                    
                                    if atual_nodo not in objetivos:
                                        visitados_global.add(atual_nodo)

                                    distancia = self.calcular_distancia(atual_nodo, proximo_nodo)
                                    if distancia > transporte.autonomia:
                                        if self.m_nodos[atual_nodo].get("reabastecimento", False):
                                            transporte.abastecer()
                                            tempo_total += 0.1  # 6 minutes for refueling
                                            custo_total += 10   # Refueling cost

                                    transporte.viajar(distancia)
                                    custo_total += distancia
                                    tempo_viagem, _ = self.calcular_tempo_viagem(atual_nodo, proximo_nodo, transporte)
                                    tempo_total += tempo_viagem

                                # Update total path
                                for nodo in caminho:
                                    if not caminho_total or caminho_total[-1] != nodo:
                                        caminho_total.append(nodo)

                                # Handle delivery at objective
                                if self.m_nodos[objetivo_atual]["alimentos"] > 0:
                                    transporte.descarregar(self.m_nodos[objetivo_atual]["alimentos"])
                                    custo_total += 15  # Delivery cost
                                    tempo_total += 0.5  # 30 minutes for unloading
                                    self.m_nodos[objetivo_atual]["alimentos"] = 0
                                    self.m_nodos[objetivo_atual]["prioridade"] = 0

                                if self.m_nodos[objetivo_atual].get("supply_refill", False):
                                    transporte.carregar()

                                ponto_atual = objetivo_atual
                                objetivos_restantes.pop(0)
                                caminho_encontrado = True
                                break

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
                                
                                novo_caminho = caminho + [vizinho]
                                if self.verificar_caminho_possivel(atual, vizinho, transporte):
                                    # Calculate new cost with weather consideration
                                    tempo_base = self.calcular_distancia(atual, vizinho) / transporte.velocidade
                                    multiplicador_clima = tempo_viagem / tempo_base
                                    novo_custo = custo_atual + (peso * multiplicador_clima)
                                    
                                    if vizinho not in custos or novo_custo < custos[vizinho]:
                                        custos[vizinho] = novo_custo
                                        heapq.heappush(fila_prioridade, (novo_custo, vizinho, novo_caminho))

                if not caminho_encontrado:
                    tentativas -= 1

                if iteration_count >= max_iterations:
                    print(f"Limite de iterações atingido para o objetivo {objetivo_atual}")
                    break

            if not caminho_encontrado:
                print(f"Não foi possível encontrar um caminho seguro para {objetivo_atual} após {tentativas} tentativas")
                objetivos_restantes.pop(0)

        # Calculate final times and return results
        if tempo_total > 0:
            tempo_total = (tempo_total * 60) / 100  # Convert to hours
            print(f"Caminho total percorrido: {caminho_total}")
            print(f"Custo total acumulado: {custo_total:.3f}")
            print(f"Tempo total acumulado: {tempo_total:.2f} horas")
            return caminho_total, round(custo_total, 3), tempo_total
        else:
            print("Nenhum caminho válido encontrado")
            return [], 0, 0