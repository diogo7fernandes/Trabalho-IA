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
		pos = nx.spring_layout(g, seed = 1)

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
		print(f"A distância entre {origem} e {destino} é aproximadamente {distancia:.2f} km.")
	
	def procura_BFS(self, inicio, transporte, objetivos):
		if inicio not in self.m_nodos:
			raise ValueError(f"Nó '{inicio}' não existe no grafo.")
		for objetivo in objetivos:
			if objetivo not in self.m_nodos:
				raise ValueError(f"Nó objetivo '{objetivo}' não existe no grafo.")

		caminho_total = []
		custo_total = 0
		tempo_total = 0  # Inicializa o tempo total

		pontos = [inicio] + objetivos  # Cria uma lista que começa no início e inclui os objetivos
		i = 0  # Índice para iterar sobre a lista de pontos
		while i < len(pontos) - 1:
			ponto_atual = pontos[i]
			ponto_objetivo = pontos[i + 1]

			if ponto_atual not in objetivos and ponto_atual != inicio:
				i += 1
				continue

			if ponto_objetivo not in objetivos:
				i += 1
				continue

			# Encontrar o caminho entre os dois pontos
			caminho_otimo = self.encontrar_caminho(ponto_atual, ponto_objetivo)
			if not caminho_otimo:
				break

			# Percorrer o caminho encontrado
			for j in range(len(caminho_otimo) - 1):
				atual = caminho_otimo[j]
				proximo = caminho_otimo[j + 1]

				# Reduz o TTL e atualiza o custo
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
				tempo_viagem = distancia / transporte.velocidade  # Calcula o tempo da viagem
				tempo_total += tempo_viagem  # Acumula o tempo total


			# Adiciona o caminho ao caminho total sem duplicações consecutivas
			for nodo in caminho_otimo:
				if not caminho_total or caminho_total[-1] != nodo:
					caminho_total.append(nodo)

			# Atender o objetivo
			if ponto_objetivo in self.m_nodos and self.m_nodos[ponto_objetivo]["alimentos"] > 0:
				tr.Transporte.descarregar(transporte, self.m_nodos[ponto_objetivo]["alimentos"])
				custo_total += 15
				tempo_total += 0.5
				self.m_nodos[ponto_objetivo]["alimentos"] = 0
				self.m_nodos[ponto_objetivo]["prioridade"] = 0
			
			if self.m_nodos[ponto_objetivo]["supply_refill"] == True:
				tr.Transporte.carregar(transporte)


			# Avança para o próximo ponto
			i += 1
		tempo_total = (tempo_total*60)/100
		print(f"Caminho total percorrido: {caminho_total}")
		print(f"Custo total acumulado: {custo_total:.3f}")
		print(f"Tempo total acumulado: {tempo_total:.2f} horas")
		return caminho_total, round(custo_total, 3), tempo_total


	def encontrar_caminho(self, inicio, objetivo):
		"""
		Encontra o caminho mais curto entre dois nós usando BFS.
		Retorna o caminho como uma lista de nós ou None se não houver caminho.
		"""
		visitados = set()
		fila = [(inicio, [inicio])]  # Fila com (nó atual, caminho percorrido)

		while fila:
			atual, caminho = fila.pop(0)

			if atual == objetivo:
				return caminho

			if atual not in visitados:
				visitados.add(atual)

				for vizinho, peso in self.m_grafo.get(atual, []):  # Apenas vizinhos conectados
					if vizinho not in visitados:
						fila.append((vizinho, caminho + [vizinho]))

		return None  # Caminho não encontrado





	def procura_DFS_prioritario(self, inicio, transporte):
   
		if inicio not in self.m_nodos:
			raise ValueError(f"Nó '{inicio}' não existe no grafo.")

		# Criar lista de nodos ordenados por prioridade decrescente
		objetivos = sorted(
			[(nodo, atributos["prioridade"]) for nodo, atributos in self.m_nodos.items() if atributos["prioridade"] > 0],
			key=lambda x: x[1],
			reverse=True
		)
		objetivos = [nodo for nodo, _ in objetivos]

		print(f"Lista inicial de objetivos ordenados por prioridade: {objetivos}")

		visitados = set()
		caminho_total = []
		custo_total = 0

		def dfs_recursivo(atual):
			nonlocal custo_total

			# Verificar se há objetivos restantes
			if not objetivos:
				print("Todos os objetivos foram visitados.")
				return

			# Atualizar o objetivo atual
			objetivo_atual = objetivos[0]

			print(f"Iniciando DFS de '{atual}' para '{objetivo_atual}'...")

			pilha = [(atual, 0)]  # Pilha com (nó, custo acumulado)

			while pilha:
				nodo_atual, custo_atual = pilha.pop()

				if nodo_atual not in visitados:
					visitados.add(nodo_atual)
					caminho_total.append(nodo_atual)
					print(f"Visitando nó: {nodo_atual}, custo acumulado: {custo_atual}")

					# Processar vizinhos
					vizinhos = self.m_grafo.get(nodo_atual, [])
					vizinho_prioritario = max(
						[viz for viz in vizinhos if viz[0] not in visitados],
						key=lambda x: self.m_nodos[x[0]]["prioridade"],
						default=None
					)

					if vizinho_prioritario is None:
						print(f"Sem vizinhos prioritários disponíveis para o nó '{nodo_atual}'.")
						continue

					vizinho, peso = vizinho_prioritario
					distancia = self.calcular_distancia(nodo_atual, vizinho)

					# Verificar autonomia e reabastecimento
					if distancia > transporte.autonomia:
						if self.m_nodos[nodo_atual].get("reabastecimento", False):
							print(f"Reabastecendo transporte no nó '{nodo_atual}'.")
							transporte.abastecer()
						else:
							print(f"Nó '{nodo_atual}' não permite reabastecimento. Nó ignorado.")
							continue

					# Usar o transporte para o próximo nó
					transporte.viajar(distancia)
					custo_total += distancia
					pilha.append((vizinho, custo_atual + distancia))

				# Se alcançamos o objetivo atual, remove-o da lista e reinicia
				if nodo_atual == objetivo_atual:
					print(f"Objetivo '{objetivo_atual}' alcançado!")
					objetivos.pop(0)  # Remove o objetivo alcançado
					print(f"Objetivos restantes: {objetivos}")
					print(f"Nodos visitados até agora: {list(visitados)}")
					dfs_recursivo(nodo_atual)  # Chamada recursiva para o próximo objetivo
					break

		dfs_recursivo(inicio)

		print(f"\nCaminho total percorrido pelo transporte '{transporte.nome}': {caminho_total}")
		print(f"Custo total pelo transporte '{transporte.nome}': {custo_total}")

		return caminho_total, custo_total

			

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
						if self.m_nodos[atual].get("reabastecimento", False):
							print(f"Reabastecendo transporte {transporte.nome} no nó '{atual}'.")
							transporte.reabastecer()
						else:
							print(f"Nó '{atual}' não permite reabastecimento. Ignorando o vizinho '{vizinho}'.")
							continue

			transporte.autonomia = autonomia_inicial
						

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
		"""
		Salva as estatísticas dos nós em um arquivo JSON e tenta abri-lo de forma multiplataforma.
		:param filename: Nome do arquivo JSON onde os dados serão salvos.
		"""
		# Salvar os dados em um arquivo JSON
		with open(filename, "w") as file:
			json.dump(self.m_nodos, file, indent=4)
		print(f"Estatísticas dos nós foram salvas em '{filename}'")
		
		# Abrir o arquivo de forma compatível com diferentes sistemas operacionais
		sistema = platform.system()
		try:
			if sistema == "Windows":
				os.startfile(filename)  # Windows
			elif sistema == "Darwin":  # macOS
				subprocess.run(["open", filename], check=True)
			elif sistema == "Linux":  # Linux
				subprocess.run(["xdg-open", filename], check=True)
			else:
				print(f"Não foi possível abrir o arquivo automaticamente no sistema {sistema}.")
		except Exception as e:
			print(f"Erro ao tentar abrir o arquivo: {e}")
   
	def procura_greedy(self, inicio, transporte):
		if inicio not in self.m_nodos:
			raise ValueError(f"Nó '{inicio}' não existe no grafo.")

		visitados = set()
		fila_prioridade = [(0, inicio)]  # (heurística, nó)
		caminho = []
		custo_total = 0

		while fila_prioridade:
			# Expandir o nó com menor valor de heurística
			_, atual = heapq.heappop(fila_prioridade)

			if atual in visitados:
				continue

			visitados.add(atual)
			caminho.append(atual)
			print(f"Visitando nó: {atual}")

			# Processar vizinhos
			for vizinho, peso in self.m_grafo.get(atual, []):
				if vizinho not in visitados:
					distancia = self.calcular_distancia(atual, vizinho)

					# Verificar autonomia do transporte
					if distancia > transporte.autonomia:
						atributos = self.m_nodos[atual]
						if atributos["reabastecimento"]:
							transporte.abastecer()
							custo_total += 1  # Custo para reabastecer
							print(f"Reabastecendo em '{atual}' para continuar.")
						else:
							continue

					transporte.viajar(distancia)
					custo_total += distancia

					# Calcular heurística e adicionar à fila
					h_custo = self.calcular_heuristica(vizinho, inicio)
					print(f"Heurística para nó '{vizinho}': {h_custo}")
					heapq.heappush(fila_prioridade, (h_custo, vizinho))

		print(f"Caminho percorrido: {caminho}")
		print(f"Custo total: {custo_total}")
		return caminho, custo_total
