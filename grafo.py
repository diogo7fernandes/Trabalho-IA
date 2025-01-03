import sys
from transporte import Carro, Moto, Helicoptero, Drone
sys.path.append(".")
import math
import os
import json
import subprocess
import platform
import transporte as tr
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
    
    def procura_BFS(self, inicio, transporte, objetivos):
        if inicio not in self.m_nodos:
            raise ValueError(f"Nó '{inicio}' não existe no grafo.")
        for objetivo in objetivos:
            if objetivo not in self.m_nodos:
                raise ValueError(f"Nó objetivo '{objetivo}' não existe no grafo.")

        caminho_total = []
        custo_total = 0
        tempo_total = 0

        pontos = [inicio] + objetivos
        i = 0
        while i < len(pontos) - 1:
            ponto_atual = pontos[i]
            ponto_objetivo = pontos[i + 1]

            if ponto_atual not in objetivos and ponto_atual != inicio:
                i += 1
                continue

            if ponto_objetivo not in objetivos:
                i += 1
                continue

            # Verificar acessibilidade do ponto objetivo
            if not tr.Transporte.transporte_pode(transporte, self.m_nodos[ponto_objetivo]["acessibilidade"]):
                print(f"Transporte {transporte.nome} não pode acessar {ponto_objetivo}. Pulando...")
                i += 1
                continue

            caminho_otimo = self.encontrar_caminho(ponto_atual, ponto_objetivo)
            if not caminho_otimo:
                break

            # Verificar acessibilidade para cada ponto no caminho
            caminho_acessivel = True
            for j in range(len(caminho_otimo)):
                if not tr.Transporte.transporte_pode(transporte, self.m_nodos[caminho_otimo[j]]["acessibilidade"]):
                    print(f"Caminho bloqueado: {transporte.nome} não pode acessar {caminho_otimo[j]}")
                    caminho_acessivel = False
                    break

            if not caminho_acessivel:
                i += 1
                continue

            for j in range(len(caminho_otimo) - 1):
                atual = caminho_otimo[j]
                proximo = caminho_otimo[j + 1]

                self.m_nodos[atual]["TTL"] -= 1
                if self.m_nodos[atual]["TTL"] <= 0:
                    continue

                distancia = self.calcular_distancia(atual, proximo)
                if distancia > transporte.autonomia:
                    if self.m_nodos[atual].get("reabastecimento", False):
                        tr.Transporte.abastecer(transporte)
                        tempo_total += 0.1
                        custo_total += 10
                    else:
                        break

                tr.Transporte.viajar(transporte, distancia)
                custo_total += distancia
                tempo_viagem = distancia / transporte.velocidade
                tempo_total += tempo_viagem

            for nodo in caminho_otimo:
                if not caminho_total or caminho_total[-1] != nodo:
                    caminho_total.append(nodo)

            if ponto_objetivo in self.m_nodos and self.m_nodos[ponto_objetivo]["alimentos"] > 0:
                tr.Transporte.descarregar(transporte, self.m_nodos[ponto_objetivo]["alimentos"])
                custo_total += 15
                tempo_total += 0.5
                self.m_nodos[ponto_objetivo]["alimentos"] = 0
                self.m_nodos[ponto_objetivo]["prioridade"] = 0
            
            if self.m_nodos[ponto_objetivo]["supply_refill"] == True:
                tr.Transporte.carregar(transporte)

            i += 1
        
        tempo_total = (tempo_total*60)/100
        print(f"Caminho total percorrido: {caminho_total}")
        print(f"Custo total acumulado: {custo_total:.3f}")
        print(f"Tempo total acumulado: {tempo_total:.2f} horas")
        return caminho_total, round(custo_total, 3), tempo_total
    
    def procura_DFS(self, inicio, transporte, objetivos):
        if inicio not in self.m_nodos:
            raise ValueError(f"Nó '{inicio}' não existe no grafo.")
        for objetivo in objetivos:
            if objetivo not in self.m_nodos:
                raise ValueError(f"Nó objetivo '{objetivo}' não existe no grafo.")

        # Verificar acessibilidade inicial
        if not tr.Transporte.transporte_pode(transporte, self.m_nodos[inicio]["acessibilidade"]):
            raise ValueError(f"Transporte {transporte.nome} não pode acessar o ponto inicial {inicio}")

        caminho_total = []
        custo_total = 0
        tempo_total = 0

        pontos = [inicio] + objetivos
        i = 0
        while i < len(pontos) - 1:
            ponto_atual = pontos[i]
            ponto_objetivo = pontos[i + 1]

            # Verificar acessibilidade do ponto objetivo
            if not tr.Transporte.transporte_pode(transporte, self.m_nodos[ponto_objetivo]["acessibilidade"]):
                print(f"Transporte {transporte.nome} não pode acessar {ponto_objetivo}. Pulando...")
                i += 1
                continue

            if ponto_atual not in objetivos and ponto_atual != inicio:
                i += 1
                continue

            if ponto_objetivo not in objetivos:
                i += 1
                continue

            caminho_otimo = self.encontrar_caminho_DFS(ponto_atual, ponto_objetivo)
            if not caminho_otimo:
                break

            # Verificar acessibilidade para cada ponto no caminho
            caminho_acessivel = True
            for j in range(len(caminho_otimo)):
                if not tr.Transporte.transporte_pode(transporte, self.m_nodos[caminho_otimo[j]]["acessibilidade"]):
                    print(f"Caminho bloqueado: {transporte.nome} não pode acessar {caminho_otimo[j]}")
                    caminho_acessivel = False
                    break

            if not caminho_acessivel:
                i += 1
                continue

            for j in range(len(caminho_otimo) - 1):
                atual = caminho_otimo[j]
                proximo = caminho_otimo[j + 1]

                self.m_nodos[atual]["TTL"] -= 1
                if self.m_nodos[atual]["TTL"] <= 0:
                    continue

                distancia = self.calcular_distancia(atual, proximo)
                if distancia > transporte.autonomia:
                    if self.m_nodos[atual].get("reabastecimento", False):
                        tr.Transporte.abastecer(transporte)
                        tempo_total += 0.1
                        custo_total += 10
                    else:
                        break

                tr.Transporte.viajar(transporte, distancia)
                custo_total += distancia
                tempo_viagem = distancia / transporte.velocidade
                tempo_total += tempo_viagem

            for nodo in caminho_otimo:
                if not caminho_total or caminho_total[-1] != nodo:
                    caminho_total.append(nodo)

            if ponto_objetivo in self.m_nodos and self.m_nodos[ponto_objetivo]["alimentos"] > 0:
                tr.Transporte.descarregar(transporte, self.m_nodos[ponto_objetivo]["alimentos"])
                custo_total += 15
                tempo_total += 0.5
                self.m_nodos[ponto_objetivo]["alimentos"] = 0
                self.m_nodos[ponto_objetivo]["prioridade"] = 0
            
            if self.m_nodos[ponto_objetivo]["supply_refill"] == True:
                tr.Transporte.carregar(transporte)

            i += 1

        tempo_total = (tempo_total * 60) / 100
        print(f"Caminho total percorrido: {caminho_total}")
        print(f"Custo total acumulado: {custo_total:.3f}")
        print(f"Tempo total acumulado: {tempo_total:.2f} horas")
        return caminho_total, round(custo_total, 3), tempo_total
    
    def a_star(self, inicio, transporte, objetivos):
        if inicio not in self.m_nodos:
            raise ValueError(f"Nó '{inicio}' não existe no grafo.")
        for objetivo in objetivos:
            if objetivo not in self.m_nodos:
                raise ValueError(f"Nó objetivo '{objetivo}' não existe no grafo.")

        # Verificar acessibilidade inicial
        if not tr.Transporte.transporte_pode(transporte, self.m_nodos[inicio]["acessibilidade"]):
            raise ValueError(f"Transporte {transporte.nome} não pode acessar o ponto inicial {inicio}")

        caminho_total = []
        custo_total = 0
        tempo_total = 0

        pontos = [inicio] + objetivos
        i = 0
        while i < len(pontos) - 1:
            ponto_atual = pontos[i]
            ponto_objetivo = pontos[i + 1]

            if not tr.Transporte.transporte_pode(transporte, self.m_nodos[ponto_objetivo]["acessibilidade"]):
                print(f"Transporte {transporte.nome} não pode acessar {ponto_objetivo}. Pulando...")
                i += 1
                continue

            if ponto_atual not in objetivos and ponto_atual != inicio:
                i += 1
                continue

            if ponto_objetivo not in objetivos:
                i += 1
                continue

            fila_prioridade = []
            heapq.heappush(fila_prioridade, (0, ponto_atual, [ponto_atual], 0))
            visitados = set()

            while fila_prioridade:
                f_atual, atual, caminho, g_atual = heapq.heappop(fila_prioridade)

                if atual in visitados:
                    continue
                visitados.add(atual)

                if atual == ponto_objetivo:
                    # Verificar acessibilidade do caminho completo
                    caminho_acessivel = True
                    for nodo in caminho:
                        if not tr.Transporte.transporte_pode(transporte, self.m_nodos[nodo]["acessibilidade"]):
                            caminho_acessivel = False
                            break
                    
                    if caminho_acessivel:
                        for j in range(len(caminho) - 1):
                            atual = caminho[j]
                            proximo = caminho[j + 1]

                            distancia = self.calcular_distancia(atual, proximo)
                            custo_total += distancia
                            tempo_viagem = distancia / transporte.velocidade
                            tempo_total += tempo_viagem

                        for nodo in caminho:
                            if not caminho_total or caminho_total[-1] != nodo:
                                caminho_total.append(nodo)
                        break

                for vizinho, peso in self.m_grafo.get(atual, []):
                    if vizinho not in visitados and tr.Transporte.transporte_pode(transporte, self.m_nodos[vizinho]["acessibilidade"]):
                        g_vizinho = g_atual + peso
                        h_vizinho = self.calcular_heuristica(vizinho, ponto_objetivo)
                        f_vizinho = g_vizinho + h_vizinho
                        heapq.heappush(fila_prioridade, (f_vizinho, vizinho, caminho + [vizinho], g_vizinho))

            i += 1

        tempo_total = (tempo_total * 60) / 100
        print(f"Caminho total percorrido: {caminho_total}")
        print(f"Custo total acumulado: {custo_total:.3f}")
        print(f"Tempo total acumulado: {tempo_total:.2f} horas")
        return caminho_total, round(custo_total, 3), tempo_total
            
    def procura_greedy(self, inicio, transporte, lista_prioridades):
        
        if inicio not in self.m_nodos:
            raise ValueError(f"Nó '{inicio}' não existe no grafo.")
        for objetivo in lista_prioridades:
            if objetivo not in self.m_nodos:
                raise ValueError(f"Nó objetivo '{objetivo}' não existe no grafo.")

        caminho_total = []
        custo_total = 0
        tempo_total = 0
        lista_prioridades = lista_prioridades[:]  # Criação de uma cópia da lista de prioridades

        while lista_prioridades:
            objetivo_atual = lista_prioridades[0]  # Primeiro objetivo da lista
            print(f"\nIniciando busca de '{inicio}' para '{objetivo_atual}'.")

            fila_prioridade = [(0, inicio)]
            visitados = set()
            objetivo_alcancavel = False

            while fila_prioridade:
                _, atual = heapq.heappop(fila_prioridade)

                if atual in visitados:
                    continue

                visitados.add(atual)

                # Adicionar ao caminho, evitando repetições consecutivas
                if not caminho_total or caminho_total[-1] != atual:
                    caminho_total.append(atual)

                print(f"Visitando nó: {atual}")

                # Suprimir necessidades de nós intermediários
                if self.m_nodos[atual]["alimentos"] > 0:
                    alimentos_necessarios = self.m_nodos[atual]["alimentos"]
                    self.m_nodos[atual]["alimentos"] = tr.Transporte.descarregar(transporte, alimentos_necessarios)
                    custo_total += 15  # Incrementa o custo para descarregar alimentos
                    tempo_total += 0.5

                # Recarregar alimentos no transporte, se permitido no nó
                if transporte.alimentos < transporte.capacidade and self.m_nodos[atual]["supply_refill"] is True:
                    tr.Transporte.carregar(transporte)
                    custo_total += 10
                    tempo_total += 0.3
                    print(f"Reabastecimento de alimentos realizado no nó '{atual}'.")

                # Se o objetivo atual for alcançado
                if atual == objetivo_atual:
                    objetivo_alcancavel = True
                    print(f"Objetivo '{objetivo_atual}' alcançado!")
                    # Satisfazendo as necessidades de alimentos do objetivo antes de removê-lo
                    if self.m_nodos[atual]["alimentos"] > 0:
                        alimentos_necessarios = self.m_nodos[atual]["alimentos"]
                        self.m_nodos[atual]["alimentos"] = tr.Transporte.descarregar(transporte, alimentos_necessarios)
                        custo_total += 15
                        tempo_total += 0.5
                        print(f"Necessidades de alimentos satisfeitas no objetivo '{objetivo_atual}'.")
                    lista_prioridades.pop(0)  # Remove o objetivo atual da lista
                    inicio = atual  # Atualiza o início para o próximo ciclo
                    break

                # Explorar vizinhos conectados com validação de caminho possível
                for vizinho, peso in self.m_grafo.get(atual, []):
                    # Verificar se existe um caminho válido utilizando o método encontrar_caminho
                    caminho_possivel = self.encontrar_caminho(atual, vizinho)
                    if not caminho_possivel:
                        print(f"Nó '{vizinho}' não é acessível a partir de '{atual}'. Ignorando.")
                        continue

                    # Certificar que o vizinho está conectado diretamente ao atual
                    if vizinho not in [nodo for nodo, _ in self.m_grafo.get(atual, [])]:
                        print(f"Nó '{vizinho}' não está conectado a '{atual}'. Ignorando.")
                        continue

                    if vizinho not in visitados:
                        distancia = self.calcular_distancia(atual, vizinho)

                        # Verificar se o transporte pode acessar o vizinho
                        acessibilidade = self.m_nodos[vizinho]["acessibilidade"]
                        if not tr.Transporte.transporte_pode(transporte, acessibilidade):
                            print(f"Transporte '{transporte.nome}' não pode acessar o nó '{vizinho}'.")
                            continue

                        # Verificar autonomia e reabastecer, se permitido no nó
                        if distancia > transporte.autonomia:
                            if self.m_nodos[atual]["reabastecimento"] is True:
                                tr.Transporte.abastecer(transporte)
                                tempo_total += 0.1
                                custo_total += 10
                                print(f"Reabastecimento de combustível realizado no nó '{atual}'.")
                            else:
                                print(f"Nó '{atual}' não permite reabastecimento. Ignorando '{vizinho}'.")
                                continue

                        tr.Transporte.viajar(transporte, distancia)
                        custo_total += distancia
                        tempo_viagem = distancia / transporte.velocidade
                        tempo_total += tempo_viagem

                        # Calcular heurística e adicionar à fila
                        h_custo = self.calcular_heuristica(vizinho, objetivo_atual)
                        heapq.heappush(fila_prioridade, (h_custo, vizinho))

            # Caso o objetivo não seja alcançável, removê-lo da lista
            if not objetivo_alcancavel:
                print(f"Objetivo '{objetivo_atual}' não é alcançável. Removendo da lista de prioridades.")
                lista_prioridades.pop(0)

            tempo_total = (tempo_total * 60) / 100
            print(f"\nCaminho total percorrido: {caminho_total}")
            print(f"Custo total acumulado: {custo_total:.3f}")
            print(f"Tempo total acumulado: {tempo_total:.2f} horas")
        return caminho_total, round(custo_total, 3), tempo_total
    
    def custo_uniforme(self, inicio, transporte, lista_prioridades):
        if inicio not in self.m_nodos:
            raise ValueError(f"Nó '{inicio}' não existe no grafo.")
        for objetivo in lista_prioridades:
            if objetivo not in self.m_nodos:
                raise ValueError(f"Nó objetivo '{objetivo}' não existe no grafo.")

        # Verificar acessibilidade inicial
        if not tr.Transporte.transporte_pode(transporte, self.m_nodos[inicio]["acessibilidade"]):
            raise ValueError(f"Transporte {transporte.nome} não pode acessar o ponto inicial {inicio}")

        caminho_total = []
        custo_total = 0
        tempo_total = 0
        lista_prioridades = lista_prioridades[:]

        while lista_prioridades:
            objetivo_atual = lista_prioridades[0]

            # Verificar acessibilidade do objetivo atual
            if not tr.Transporte.transporte_pode(transporte, self.m_nodos[objetivo_atual]["acessibilidade"]):
                print(f"Transporte {transporte.nome} não pode acessar {objetivo_atual}. Pulando para o próximo objetivo...")
                lista_prioridades.pop(0)
                continue

            fila_prioridade = [(0, inicio, [])]
            visitados = set()
            caminho_encontrado = False

            while fila_prioridade:
                custo_atual, atual, caminho = heapq.heappop(fila_prioridade)

                if atual in visitados:
                    continue

                visitados.add(atual)
                novo_caminho = caminho + [atual]

                if atual == objetivo_atual:
                    # Verificar acessibilidade de todo o caminho
                    caminho_acessivel = True
                    for nodo in novo_caminho:
                        if not tr.Transporte.transporte_pode(transporte, self.m_nodos[nodo]["acessibilidade"]):
                            caminho_acessivel = False
                            break

                    if caminho_acessivel:
                        # Processar o caminho encontrado
                        for i in range(len(novo_caminho) - 1):
                            atual_nodo = novo_caminho[i]
                            proximo_nodo = novo_caminho[i + 1]
                            distancia = self.calcular_distancia(atual_nodo, proximo_nodo)
                            
                            if distancia > transporte.autonomia:
                                if self.m_nodos[atual_nodo].get("reabastecimento", False):
                                    tr.Transporte.abastecer(transporte)
                                    tempo_total += 0.1
                                    custo_total += 10
                                else:
                                    caminho_acessivel = False
                                    break

                            custo_total += distancia
                            tempo_viagem = distancia / transporte.velocidade
                            tempo_total += tempo_viagem

                        if caminho_acessivel:
                            caminho_total.extend(nodo for nodo in novo_caminho if not caminho_total or caminho_total[-1] != nodo)
                            caminho_encontrado = True
                            inicio = atual
                            break

                for vizinho, peso in self.m_grafo.get(atual, []):
                    if vizinho not in visitados and tr.Transporte.transporte_pode(transporte, self.m_nodos[vizinho]["acessibilidade"]):
                        distancia = self.calcular_distancia(atual, vizinho)
                        if distancia <= transporte.autonomia:
                            novo_custo = custo_atual + peso
                            heapq.heappush(fila_prioridade, (novo_custo, vizinho, novo_caminho))

            if caminho_encontrado:
                if self.m_nodos[objetivo_atual]["alimentos"] > 0:
                    tr.Transporte.descarregar(transporte, self.m_nodos[objetivo_atual]["alimentos"])
                    custo_total += 15
                    tempo_total += 0.5
                    self.m_nodos[objetivo_atual]["alimentos"] = 0
                lista_prioridades.pop(0)
            else:
                print(f"Não foi possível encontrar um caminho acessível para {objetivo_atual}. Pulando para o próximo objetivo...")
                lista_prioridades.pop(0)

        tempo_total = (tempo_total * 60) / 100
        print(f"Caminho total percorrido: {caminho_total}")
        print(f"Custo total acumulado: {custo_total:.3f}")
        print(f"Tempo total acumulado: {tempo_total:.2f} horas")
        return caminho_total, round(custo_total, 3), tempo_total