import sys

sys.path.append(".")
import math
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

		atributos_origem = self.m_nodos.get(origem)
		atributos_destino = self.m_nodos.get(destino)

		coordenadas_origem = atributos_origem.get("coordenadas")
		coordenadas_destino = atributos_destino.get("coordenadas")

		if not coordenadas_origem or not coordenadas_destino:
			raise ValueError(
				"Coordenadas ausentes para calcular o peso entre '{}' e '{}'.".format(
					origem, destino
				)
			)

		x1, y1 = coordenadas_origem
		x2, y2 = coordenadas_destino
		distancia = Grafo.calcular_distancia(x1, y1, x2, y2)

		prioridade = atributos_destino.get("prioridade", 1)
		acessibilidade = atributos_destino.get("acessibilidade", 1)
		clima = atributos_destino.get("clima", 1)

		c_total = (
			0.3 * distancia - 0.4 * prioridade + 0.2 * acessibilidade + 0.1 * clima
		)

		return round(c_total, 2)

	def calcular_distancia(lat1, lon1, lat2, lon2):

		# Converter graus para radianos
		lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

		# Diferenças
		delta_lat = lat2 - lat1
		delta_lon = lon2 - lon1

		# Fórmula Haversine
		a = (
			math.sin(delta_lat / 2) ** 2
			+ math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2
		)
		c = 2 * math.asin(math.sqrt(a))
		R = 6371  # Raio da Terra em km
		return R * c

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

	def atualizar_atributos(
		self, nodo, prioridade, clima=None, acessibilidade=None, alimentos=None
	):

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

	def custo_uniforme(self):

		# Inicializar os veículos
		frota = [tr.Carro(), tr.Moto(), tr.Helicoptero(), tr.Drone()]
		grafo = Grafo()

		inicio = "Centro"
		if inicio not in self.m_nodos:
			raise ValueError("Nó 'Centro' não existe no grafo.")

		# Fila de prioridade: (custo acumulado, nó atual, veículo, kms restantes, caminho percorrido, tempo total)
		fila_prioridade = [(0, inicio, veiculo, [inicio], 0) for veiculo in frota]
		visitados = set()
		custo_total = 0
		tempo_total = 0

		while fila_prioridade:
			# Extrair o nó com o menor custo acumulado
			custo_atual, atual, veiculo, caminho, tempo = heapq.heappop(fila_prioridade)
			atributos = self.m_nodos[atual]

			# Marcar o nó como visitado por este veículo
			visitados.add((atual, veiculo.nome))

			if atributos["alimentos"] > 0:
				# Entregar suprimentos até o limite do veículo
				tr.Transporte.descarregar(veiculo, atributos["alimentos"])
				if atributos["alimentos"] == 0:
					atributos["prioridade"] = (
						0  # Zerar a prioridade se a entrega for concluída
					)

			# Atualizar o custo total e o tempo total
			custo_total += custo_atual
			tempo_total += tempo

			# Adicionar os vizinhos não visitados à fila de prioridade
			for vizinho, peso in self.m_grafo.get(atual, []):
				if (vizinho, veiculo.nome) not in visitados:

					coordenadas_atual = self.m_nodos[atual].get("coordenadas")
					coordenadas_vizinho = self.m_nodos[vizinho].get("coordenadas")
					lat1, lon1 = coordenadas_atual
					lat2, lon2 = coordenadas_vizinho

					# Calcular a distância usando a fórmula de Haversine
					distancia = Grafo.calcular_distancia(lat1, lon1, lat2, lon2)
					tempo_gasto = distancia / veiculo.velocidade

					# ver o caminho

					if veiculo.autonomia >= distancia:

						tr.Transporte.viajar(veiculo, distancia)
						print(vizinho)

						# Veículo pode alcançar o vizinho
						heapq.heappush(
							fila_prioridade,
							(
								custo_atual + distancia,
								vizinho,
								veiculo,
								caminho + [vizinho],
								tempo + tempo_gasto,
							),
						)
					elif veiculo.nome == "Helicóptero" or veiculo.autonomia < distancia:
						tr.Transporte.abastecer(veiculo)
						# Reabastecer combustível (mantém a posição)
						heapq.heappush(
							fila_prioridade,
							(
								custo_atual + distancia,
								atual,
								veiculo,
								caminho,
								tempo + 1,
							),  # Adiciona 1h para reabastecer
						)
					if vizinho == inicio:
						# Reabastecer suprimentos (voltar ao centro)
						tr.Transporte.carregar(veiculo)

		return caminho, custo_total, tempo_total
	
	
	def procura_BFS(self, inicio):
	
		if inicio not in self.m_nodos:
			raise ValueError(f"Nó '{inicio}' não existe no grafo.")
		
		visitados = set()  # Conjunto de nós visitados
		fila = [inicio]  # Fila para a BFS
		ordem_visita = []  # Lista para registrar a ordem de visita dos nós

		while fila:
			atual = fila.pop(0)  # Retira o primeiro elemento da fila

			if atual not in visitados:
				visitados.add(atual)  # Marca o nó como visitado
				ordem_visita.append(atual)  # Adiciona à ordem de visita

			# Adiciona os vizinhos a fila na ordem inversa para manter a logica DFS
			for vizinho, _ in reversed(self.m_grafo.get(atual, [])):
				if vizinho not in visitados:
					fila.append(vizinho)

		return ordem_visita

	
	def procura_DFS(self, inicio):
	
		if inicio not in self.m_nodos:
			raise ValueError(f"Nó '{inicio}' não existe no grafo.")

		visitados = set()  # Conjunto de nós visitados
		pilha = [inicio]  # Pilha para a DFS
		ordem_visita = []  # Lista para registar a ordem de visita dos nós

		while pilha:
			atual = pilha.pop()  # Retira o último elemento da pilha

			if atual not in visitados:
				visitados.add(atual)  # Marca o nó como visitado
				ordem_visita.append(atual)  # Adiciona à ordem de visita

			# Adiciona os vizinhos do nó atual à pilha (inverso da ordem para manter DFS)
			for vizinho, _ in reversed(self.m_grafo.get(atual, [])):
				if vizinho not in visitados:
					pilha.append(vizinho)

		return ordem_visita
	

	def a_star(self, inicio, objetivo):
	
		if inicio not in self.m_nodos or objetivo not in self.m_nodos:
			raise ValueError("Nó inicial ou objetivo não existe no grafo.")

		# Inicializar a fila de prioridade
		fila_prioridade = []
		heapq.heappush(fila_prioridade, (0, inicio, [inicio]))  # (f(n), nó atual, caminho percorrido)

		# Custos acumulados para chegar a cada nó
		custos = {inicio: 0}

		while fila_prioridade:
			f_atual, atual, caminho = heapq.heappop(fila_prioridade)

			# Se alcançamos o objetivo, retornamos o caminho e o custo
			if atual == objetivo:
				return caminho, custos[atual]

			# Expandir os vizinhos do nó atual
			for vizinho, peso in self.m_grafo.get(atual, []):
				g_custo = custos[atual] + peso
				h_custo = self.calcular_heuristica(vizinho, objetivo)
				f_custo = g_custo + h_custo

				# Se encontramos um caminho melhor para o vizinho, atualizamos
				if vizinho not in custos or g_custo < custos[vizinho]:
					custos[vizinho] = g_custo
					heapq.heappush(fila_prioridade, (f_custo, vizinho, caminho + [vizinho]))

		# Se nenhum caminho for encontrado
		return None, float('inf')


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



