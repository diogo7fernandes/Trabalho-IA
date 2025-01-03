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

        # Process objectives one by one
        for objetivo in objetivos:
            if not self.verificar_caminho_possivel(ponto_atual, objetivo, transporte):
                print(f"Não existe caminho possível entre {ponto_atual} e {objetivo} para {transporte.nome}")
                continue

            if not transporte.transporte_pode(self.m_nodos[objetivo]["acessibilidade"]):
                print(f"Transporte {transporte.nome} não pode acessar {objetivo}. Pulando...")
                continue

            fila = [(ponto_atual, [ponto_atual])]
            visitados = set()
            caminho_encontrado = False

            while fila and not caminho_encontrado:
                atual, caminho = fila.pop(0)

                if atual == objetivo:
                    if self.verificar_caminho_completo(caminho, transporte):
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
                            tempo_viagem = distancia / transporte.velocidade
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

                        if self.m_nodos[objetivo]["supply_refill"] == True:
                            transporte.carregar()

                        ponto_atual = objetivo
                        caminho_encontrado = True
                        break

                for vizinho, _ in self.m_grafo.get(atual, []):
                    if vizinho not in visitados and transporte.transporte_pode(self.m_nodos[vizinho]["acessibilidade"]):
                        if vizinho in global_visitados and vizinho not in objetivos:
                            continue
                        novo_caminho = caminho + [vizinho]
                        if self.verificar_caminho_possivel(atual, vizinho, transporte):
                            visitados.add(vizinho)
                            fila.append((vizinho, novo_caminho))

        tempo_total = (tempo_total * 60) / 100
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
        if not transporte.transporte_pode(self.m_nodos[inicio]["acessibilidade"]):
            raise ValueError(f"Transporte {transporte.nome} não pode acessar o ponto inicial {inicio}")

        caminho_total = []
        custo_total = 0
        tempo_total = 0
        ponto_atual = inicio
        global_visitados = set()

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

            while pilha and not caminho_encontrado:
                atual, caminho = pilha.pop()

                if atual == objetivo:
                    if self.verificar_caminho_completo(caminho, transporte):
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
                            tempo_viagem = distancia / transporte.velocidade
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

                        if self.m_nodos[objetivo]["supply_refill"] == True:
                            transporte.carregar()

                        ponto_atual = objetivo
                        caminho_encontrado = True
                        break

                if atual not in visitados:
                    visitados.add(atual)
                    for vizinho, _ in self.m_grafo.get(atual, []):
                        if vizinho not in visitados and transporte.transporte_pode(self.m_nodos[vizinho]["acessibilidade"]):
                            if vizinho in global_visitados and vizinho not in objetivos:
                                continue
                            novo_caminho = caminho + [vizinho]
                            if self.verificar_caminho_possivel(atual, vizinho, transporte):
                                pilha.append((vizinho, novo_caminho))

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
        if not transporte.transporte_pode(self.m_nodos[inicio]["acessibilidade"]):
            raise ValueError(f"Transporte {transporte.nome} não pode acessar o ponto inicial {inicio}")

        caminho_total = []
        custo_total = 0
        tempo_total = 0
        ponto_atual = inicio  # Keep track of current position
        global_visitados = set()

        # Process objectives one by one
        for objetivo in objetivos:
            if not self.verificar_caminho_possivel(ponto_atual, objetivo, transporte):
                print(f"Não existe caminho possível entre {ponto_atual} e {objetivo} para {transporte.nome}")
                continue

            if not transporte.transporte_pode(self.m_nodos[objetivo]["acessibilidade"]):
                print(f"Transporte {transporte.nome} não pode acessar {objetivo}. Pulando...")
                continue

            fila_prioridade = []
            heapq.heappush(fila_prioridade, (0, ponto_atual, [ponto_atual], 0))
            visitados = set()
            caminho_encontrado = False

            while fila_prioridade and not caminho_encontrado:
                f_atual, atual, caminho, g_atual = heapq.heappop(fila_prioridade)

                if atual in visitados:
                    continue
                visitados.add(atual)

                if atual == objetivo:
                    if self.verificar_caminho_completo(caminho, transporte):
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
                            tempo_viagem = distancia / transporte.velocidade
                            tempo_total += tempo_viagem

                        # Update path and current position
                        for nodo in caminho:
                            if not caminho_total or caminho_total[-1] != nodo:
                                caminho_total.append(nodo)
                        ponto_atual = objetivo
                        
                        if self.m_nodos[objetivo]["alimentos"] > 0:
                            transporte.descarregar(self.m_nodos[objetivo]["alimentos"])
                            custo_total += 15
                            tempo_total += 0.5
                            self.m_nodos[objetivo]["alimentos"] = 0
                            self.m_nodos[objetivo]["prioridade"] = 0

                        if self.m_nodos[objetivo]["supply_refill"] == True:
                            transporte.carregar()
                            
                        caminho_encontrado = True
                        break

                for vizinho, peso in self.m_grafo.get(atual, []):
                    if vizinho not in visitados and transporte.transporte_pode(self.m_nodos[vizinho]["acessibilidade"]):
                        if vizinho in global_visitados and vizinho not in objetivos:
                            continue
                            
                        novo_caminho = caminho + [vizinho]
                        if self.verificar_caminho_possivel(atual, vizinho, transporte):
                            g_vizinho = g_atual + peso
                            h_vizinho = self.calcular_heuristica(vizinho, objetivo)
                            f_vizinho = g_vizinho + h_vizinho
                            heapq.heappush(fila_prioridade, (f_vizinho, vizinho, novo_caminho, g_vizinho))

        tempo_total = (tempo_total * 60) / 100
        print(f"Caminho total percorrido: {caminho_total}")
        print(f"Custo total acumulado: {custo_total:.3f}")
        print(f"Tempo total acumulado: {tempo_total:.2f} horas")
        return caminho_total, round(custo_total, 3), tempo_total

    def procura_greedy(self, inicio, transporte, objetivos):
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

        # Process objectives one by one
        for objetivo in objetivos:
            if not self.verificar_caminho_possivel(ponto_atual, objetivo, transporte):
                print(f"Não existe caminho possível entre {ponto_atual} e {objetivo} para {transporte.nome}")
                continue

            if not transporte.transporte_pode(self.m_nodos[objetivo]["acessibilidade"]):
                print(f"Transporte {transporte.nome} não pode acessar {objetivo}. Pulando...")
                continue

            fila_prioridade = [(0, ponto_atual, [ponto_atual])]
            visitados = set()
            caminho_encontrado = False

            while fila_prioridade and not caminho_encontrado:
                _, atual, caminho = heapq.heappop(fila_prioridade)

                if atual == objetivo:
                    if self.verificar_caminho_completo(caminho, transporte):
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
                            tempo_viagem = distancia / transporte.velocidade
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

                        if self.m_nodos[objetivo]["supply_refill"] == True:
                            transporte.carregar()

                        ponto_atual = objetivo
                        caminho_encontrado = True
                        break

                if atual not in visitados:
                    visitados.add(atual)
                    for vizinho, _ in self.m_grafo.get(atual, []):
                        if vizinho not in visitados and transporte.transporte_pode(self.m_nodos[vizinho]["acessibilidade"]):
                            if vizinho in global_visitados and vizinho not in objetivos:
                                continue
                            novo_caminho = caminho + [vizinho]
                            if self.verificar_caminho_possivel(atual, vizinho, transporte):
                                h_custo = self.calcular_heuristica(vizinho, objetivo)
                                heapq.heappush(fila_prioridade, (h_custo, vizinho, novo_caminho))

        tempo_total = (tempo_total * 60) / 100
        print(f"Caminho total percorrido: {caminho_total}")
        print(f"Custo total acumulado: {custo_total:.3f}")
        print(f"Tempo total acumulado: {tempo_total:.2f} horas")
        return caminho_total, round(custo_total, 3), tempo_total
    
    def custo_uniforme(self, inicio, transporte, objetivos):
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
        visitados_global = set()
        objetivos_restantes = objetivos.copy()

        while objetivos_restantes:
            objetivo_atual = objetivos_restantes[0]
            
            # Verificar se existe caminho possível para o próximo objetivo
            if not self.verificar_caminho_possivel(ponto_atual, objetivo_atual, transporte):
                print(f"Não existe caminho possível entre {ponto_atual} e {objetivo_atual}")
                objetivos_restantes.pop(0)
                continue

            # Verificar acessibilidade do objetivo
            if not transporte.transporte_pode(self.m_nodos[objetivo_atual]["acessibilidade"]):
                print(f"Transporte {transporte.nome} não pode acessar {objetivo_atual}")
                objetivos_restantes.pop(0)
                continue

            fila_prioridade = [(0, ponto_atual, [ponto_atual])]
            visitados = set()
            caminho_encontrado = False

            while fila_prioridade and not caminho_encontrado:
                custo_atual, atual, caminho = heapq.heappop(fila_prioridade)

                if atual == objetivo_atual:
                    # Verificar se o caminho é válido considerando autonomia
                    caminho_valido = True
                    autonomia_atual = transporte.autonomia
                    
                    for i in range(len(caminho) - 1):
                        atual_nodo = caminho[i]
                        proximo_nodo = caminho[i + 1]
                        distancia = self.calcular_distancia(atual_nodo, proximo_nodo)
                        
                        if distancia > autonomia_atual:
                            if not self.m_nodos[atual_nodo].get("reabastecimento", False):
                                caminho_valido = False
                                break
                            autonomia_atual = transporte.deposito
                        
                        autonomia_atual -= distancia

                    if caminho_valido:
                        # Processar o caminho encontrado
                        for i in range(len(caminho) - 1):
                            atual_nodo = caminho[i]
                            proximo_nodo = caminho[i + 1]

                            if atual_nodo not in objetivos:
                                visitados_global.add(atual_nodo)

                            distancia = self.calcular_distancia(atual_nodo, proximo_nodo)
                            if distancia > transporte.autonomia:
                                if self.m_nodos[atual_nodo].get("reabastecimento", False):
                                    transporte.abastecer()
                                    tempo_total += 0.1  # 6 minutos para reabastecer
                                    custo_total += 10   # Custo do reabastecimento

                            transporte.viajar(distancia)
                            custo_total += distancia
                            tempo_viagem = distancia / transporte.velocidade
                            tempo_total += tempo_viagem

                        # Atualizar caminho total
                        for nodo in caminho:
                            if not caminho_total or caminho_total[-1] != nodo:
                                caminho_total.append(nodo)

                        # Processar entrega de alimentos
                        if self.m_nodos[objetivo_atual]["alimentos"] > 0:
                            transporte.descarregar(self.m_nodos[objetivo_atual]["alimentos"])
                            custo_total += 15  # Custo da entrega
                            tempo_total += 0.5  # 30 minutos para descarregar
                            self.m_nodos[objetivo_atual]["alimentos"] = 0
                            self.m_nodos[objetivo_atual]["prioridade"] = 0

                        # Atualizar posição atual e remover objetivo completado
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
                            novo_caminho = caminho + [vizinho]
                            novo_custo = custo_atual + peso
                            heapq.heappush(fila_prioridade, (novo_custo, vizinho, novo_caminho))

            if not caminho_encontrado:
                print(f"Não foi possível encontrar caminho para {objetivo_atual}")
                objetivos_restantes.pop(0)

        tempo_total = (tempo_total * 60) / 100  # Converter para horas
        return caminho_total, round(custo_total, 3), tempo_total