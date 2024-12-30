import sys
from transporte import Carro, Moto, Helicoptero, Drone
sys.path.append(".")
import math
import os
import json
import transporte as tr
import heapq
import networkx as nx  # biblioteca de tratamento de grafos necessária para desnhar graficamente o grafo
import matplotlib.pyplot as plt  # idem


class Grafo:

	def __init__(self, direcionado=True):
		self.m_nodos = {}
		self.m_direcionado = direcionado
		self.m_grafo = {}  # dicionario para armazenar os nodos e arestas
		self.m_h = (
			{}
		)  # dicionario para posterirmente armazenar as heuristicas para cada nodo -> pesquisa informad

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

		c_total = (
			0.3 * distancia - 0.4 * prioridade + 0.2 * acessibilidade + 0.1 * clima
		)

		return round(c_total, 2)

	def calcular_distancia(self, nodo1, nodo2):

		coordenadas1 = self.m_nodos[nodo1].get("coordenadas")
		coordenadas2 = self.m_nodos[nodo2].get("coordenadas")

		if not coordenadas1 or not coordenadas2:
			raise ValueError(f"Faltam coordenadas para os nós {nodo1} ou {nodo2}.")

		lat1, lon1 = map(math.radians, coordenadas1)
		lat2, lon2 = map(math.radians, coordenadas2)

		# Fórmula de Haversine
		dlat = lat2 - lat1
		dlon = lon2 - lon1
		a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
		R = 6371  # Raio da Terra em km

		return R * c  # Retorna a distância em quilômetros


	def desenha(self):

		# Criar um grafo do NetworkX como direcionado ou não, baseado em self.m_direcionado
		g = nx.DiGraph() if self.m_direcionado else nx.Graph()

		# Adicionar os nós ao grafo
		for nodo, atributos in self.m_nodos.items():
			g.add_node(nodo, **atributos)

		# Adicionar as arestas ao grafo
		for origem, conexoes in self.m_grafo.items():
			for destino, peso in conexoes:
				g.add_edge(origem, destino, weight=peso)

		# Definir o layout para os nós
		pos = nx.spring_layout(g)

		# Desenhar os nós e arestas
		nx.draw_networkx(
			g,
			pos,
			with_labels=True,
			font_weight="bold",
			node_size=700,
			node_color="lightblue",
			arrows=True,
		)

		# Mostrar o grafo
		plt.title(
			"Representação do Grafo Direcionado"
			if self.m_direcionado
			else "Representação do Grafo Não Direcionado"
		)
		plt.show()

	def atualizar_atributos(self, nodo, prioridade, clima=None, acessibilidade=None, alimentos=None):

		if nodo not in self.m_nodos:
			raise ValueError(f"Localidade '{nodo}' não existe no grafo.")

		# Atualizar os atributos especificados
		if prioridade is not None:
			self.m_nodos[nodo]["prioridade"] = prioridade
		if clima is not None:
			self.m_nodos[nodo]["clima"] = clima
		if acessibilidade is not None:
			self.m_nodos[nodo]["acessibilidade"] = acessibilidade
		if alimentos is not None:
			self.m_nodos[nodo]["alimentos"] = alimentos

		import heapq  # Biblioteca para usar a fila de prioridade

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

		# Obter as coordenadas dos nós
		coordenadas_origem = self.m_nodos[origem].get("coordenadas")
		coordenadas_destino = self.m_nodos[destino].get("coordenadas")

		if not coordenadas_origem or not coordenadas_destino:
			raise ValueError(
				f"Coordenadas ausentes para calcular a distância entre '{origem}' e '{destino}'."
			)

		# Extrair latitudes e longitudes
		lat1, lon1 = coordenadas_origem
		lat2, lon2 = coordenadas_destino

		# Calcular a distância usando a fórmula de Haversine
		distancia = Grafo.calcular_distancia(lat1, lon1, lat2, lon2)
		print(
			f"A distância entre {origem} e {destino} é aproximadamente {distancia:.2f} km."
		)
	
	
	def procura_BFS(self, inicio):
		if inicio not in self.m_nodos:
			raise ValueError(f"Nó '{inicio}' não existe no grafo.")

		from transporte import Carro, Moto, Helicoptero, Drone

		transportes = [Carro(), Moto(), Helicoptero(), Drone()]
		resultados = []

		for transporte in transportes:
			visitados = set()
			caminho = []
			fila = [(inicio, 0)]  # Fila com (nó, custo acumulado)

			custo_total = 0
			tempo_total = 0

			while fila:
				atual, custo_atual = fila.pop(0)

				if atual not in visitados:
					visitados.add(atual)
					caminho.append(atual)

					# Calcular tempo de viagem para o nó
					for vizinho, peso in self.m_grafo.get(atual, []):
						distancia = self.calcular_distancia(atual, vizinho)

						if vizinho not in visitados:
							if transporte.autonomia >= distancia:
								fila.append((vizinho, custo_atual + distancia))
								transporte.autonomia -= distancia
								tempo_total += distancia / transporte.velocidade
							else:
								print(f"Autonomia insuficiente para {transporte.nome} alcançar {vizinho}. Reabastecimento necessário.")
								transporte.abastecer()

					# Atualizar o custo total com o custo acumulado atual
					custo_total = max(custo_total, custo_atual)

			resultados.append((transporte.nome, caminho, custo_total, tempo_total))

		# Output organizado
		for transporte_nome, caminho, custo, tempo in resultados:
			print(f"\n--- Resultados para {transporte_nome} ---")
			print(f"Caminho: {caminho}")
			print(f"Custo Total: {custo}")
			print(f"Tempo Total: {tempo:.2f} horas")



	
	def procura_DFS(self, inicio):
    
		if inicio not in self.m_nodos:
			raise ValueError(f"Nó '{inicio}' não existe no grafo.")

		from transporte import Carro, Moto, Helicoptero, Drone

		transportes = [Carro(), Moto(), Helicoptero(), Drone()]
		resultados = []

		for transporte in transportes:
			visitados = set()
			caminho = []
			pilha = [(inicio, 0)]  # Pilha com (nó, custo acumulado)

			custo_total = 0
			tempo_total = 0

			while pilha:
				atual, custo_atual = pilha.pop()

				if atual not in visitados:
					visitados.add(atual)
					caminho.append(atual)

					# Calcular tempo de viagem para o nó
					for vizinho, peso in self.m_grafo.get(atual, []):
						if vizinho not in visitados:
							if transporte.autonomia >= peso:  # Verifica se o transporte pode alcançar o próximo nó
								pilha.append((vizinho, custo_atual + peso))
								transporte.autonomia -= peso
								tempo_total += peso / transporte.velocidade
							else:
								print(f"Autonomia insuficiente para {transporte.nome} alcançar {vizinho}. Reabastecimento necessário.")
								transporte.abastecer()

					custo_total = custo_atual

			resultados.append((transporte.nome, caminho, custo_total, tempo_total))

		# Output organizado
		for transporte_nome, caminho, custo, tempo in resultados:
			print(f"\n--- Resultados para {transporte_nome} ---")
			print(f"Caminho: {caminho}")
			print(f"Custo Total: {custo}")
			print(f"Tempo Total: {tempo:.2f} horas")

	def heuristica_grafo(self):
		"""
		Retorna uma lista de localidades ordenadas pela prioridade (maior para menor).
		"""
		if not self.m_nodos:
			raise ValueError("O grafo não possui nós para serem organizados.")

		# Criar uma lista de tuplas (localidade, prioridade)
		prioridades = [
			(nodo, atributos.get("prioridade", 0)) for nodo, atributos in self.m_nodos.items()
		]

		# Ordenar pela prioridade (decrescente)
		prioridades_ordenadas = sorted(prioridades, key=lambda x: x[1], reverse=True)

		# Retornar a lista de localidades ordenadas
		return [localidade for localidade, _ in prioridades_ordenadas]



	def a_star(self):
		"""
		Implementação do algoritmo A* considerando transportes com diferentes autonomias.
		"""
		inicio = 'Centro'
		loc = self.heuristica_grafo()
		objetivo = loc[1]  # Objetivo é o segundo nó com maior prioridade
		
		if inicio not in self.m_nodos or objetivo not in self.m_nodos:
			raise ValueError("Nó inicial ou objetivo não existe no grafo.")

		# Lista de transportes disponíveis
		transportes = [Carro(), Moto(), Helicoptero(), Drone()]
		resultados = []

		for transporte in transportes:
			fila_prioridade = []
			heapq.heappush(fila_prioridade, (0, inicio, [inicio]))  # (f_custo, nó atual, caminho percorrido)
			custos = {inicio: 0}
			tempo_total = 0
			autonomia_inicial = transporte.autonomia  # Salva a autonomia inicial do transporte

			while fila_prioridade:
				f_atual, atual, caminho = heapq.heappop(fila_prioridade)

				if atual == objetivo:
					custo_total = custos[atual]
					resultados.append((transporte.nome, caminho, custo_total, tempo_total))
					break

				for vizinho, peso in self.m_grafo.get(atual, []):
					if transporte.autonomia >= peso:  # Verifica se o transporte pode alcançar o próximo nó
						# Inicializa o custo para o vizinho, se necessário
						if vizinho not in custos:
							custos[vizinho] = float('inf')

						g_custo = custos[atual] + peso  # Custo acumulado
						h_custo = self.calcular_heuristica(vizinho, objetivo)
						f_custo = g_custo + h_custo

						# Atualizar custos se o caminho for melhor ou se o vizinho ainda não tiver sido visitado
						if g_custo < custos[vizinho]:
							custos[vizinho] = g_custo
							heapq.heappush(fila_prioridade, (f_custo, vizinho, caminho + [vizinho]))
							transporte.autonomia -= peso
							tempo_total += peso / transporte.velocidade
					else:
						print(f"Autonomia insuficiente para {transporte.nome} alcançar {vizinho}. Reabastecendo...")
						transporte.abastecer()
						

		# Exibir resultados
		for transporte_nome, caminho, custo, tempo in resultados:
			print(f"\n--- Resultados para {transporte_nome} ---")
			print(f"Caminho: {caminho}")
			print(f"Custo Total: {custo}")
			print(f"Tempo Total: {tempo:.2f} horas")


	def calcular_heuristica(self, nodo, objetivo):
   
		coordenadas_nodo = self.m_nodos[nodo].get("coordenadas")
		coordenadas_objetivo = self.m_nodos[objetivo].get("coordenadas")

		if not coordenadas_nodo or not coordenadas_objetivo:
			return float('inf')  # Retorna infinito se não houver coordenadas

		# Coordenadas (latitude, longitude) em graus
		lat1, lon1 = coordenadas_nodo
		lat2, lon2 = coordenadas_objetivo

		# Converter para radianos
		lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

		# Fórmula de Haversine
		dlat = lat2 - lat1
		dlon = lon2 - lon1
		a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
		R = 6371  # Raio da Terra em km
		return R * c



	def imprimir_stats_nodos(self, filename="stats_nodos.json"):
        
		with open(filename, "w") as file:
			json.dump(self.m_nodos, file, indent=4)
		print(f"Estatísticas dos nós foram salvas em '{filename}'")
		os.startfile(filename)