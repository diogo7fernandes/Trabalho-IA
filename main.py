import sys
sys.path.append(".")  # Adiciona o diretório atual ao PYTHONPATH
from grafo import Grafo
import random
from transporte import Carro, Moto, Helicoptero, Drone


def main():

	g = Grafo()
	


# Função para gerar valores aleatórios
	def gerar_atributos_aleatorios():
		return {
			"prioridade": random.randint(0, 10),  # Valores de 0 a 10
			"acessibilidade": random.randint(0, 10),  # Valores de 0 a 10
			#valores de acessibilidade para carros:0-2, mota:3-5, helicoptero:6-8, drone:9-10
			"clima": random.randint(0, 10),  # Valores de 0 a 10
			"alimentos": random.randint(0, 100),  # Quantidade de alimentos necessarios na loc de 0 a 100
			"reabastecimento": random.choice([True, False]),  # Verdadeiro se der para rewabastecer
			"supply_refill": random.choice([True, False])

		}

	# Adicionando os nós com valores aleatórios
	g.adicionar_nodo("Centro", {"coordenadas": (41.4679, -8.4120), **gerar_atributos_aleatorios()})
	g.adicionar_nodo("Braga", {"coordenadas": (41.5503, -8.4201), **gerar_atributos_aleatorios()})
	g.adicionar_nodo("Esposende", {"coordenadas": (41.5320, -8.7832), **gerar_atributos_aleatorios()})
	g.adicionar_nodo("Barcelos", {"coordenadas": (41.5388, -8.6151), **gerar_atributos_aleatorios()})
	g.adicionar_nodo("Vila Nova de Famalicao", {"coordenadas": (41.4091, -8.5198), **gerar_atributos_aleatorios()})
	g.adicionar_nodo("Guimaraes", {"coordenadas": (41.4444, -8.2962), **gerar_atributos_aleatorios()})
	g.adicionar_nodo("Vizela", {"coordenadas": (41.3890, -8.2926), **gerar_atributos_aleatorios()})
	g.adicionar_nodo("Fafe", {"coordenadas": (41.4541, -8.1706), **gerar_atributos_aleatorios()})
	g.adicionar_nodo("Povoa de Lanhoso", {"coordenadas": (41.5769, -8.2697), **gerar_atributos_aleatorios()})
	g.adicionar_nodo("Amares", {"coordenadas": (41.6308, -8.3514), **gerar_atributos_aleatorios()})
	g.adicionar_nodo("Vila Verde", {"coordenadas": (41.6480, -8.4367), **gerar_atributos_aleatorios()})
	g.adicionar_nodo("Terras de Bouro", {"coordenadas": (41.7323, -8.3088), **gerar_atributos_aleatorios()})
	g.adicionar_nodo("Vieira do Minho", {"coordenadas": (41.6325, -8.1461), **gerar_atributos_aleatorios()})
	g.adicionar_nodo("Celourico de Basto", {"coordenadas": (41.3899, -8.0058), **gerar_atributos_aleatorios()})
	g.adicionar_nodo("Cabeceiras de Basto", {"coordenadas": (41.5151, -7.9889), **gerar_atributos_aleatorios()})


	g.adicionar_aresta("Esposende", "Barcelos")
	g.adicionar_aresta("Barcelos", "Esposende")

	g.adicionar_aresta("Barcelos", "Vila Nova de Famalicao")
	g.adicionar_aresta("Vila Nova de Famalicao", "Barcelos")

	g.adicionar_aresta("Barcelos", "Vila Verde")
	g.adicionar_aresta("Vila Verde", "Barcelos")

	g.adicionar_aresta("Barcelos", "Braga")
	g.adicionar_aresta("Braga", "Barcelos")

	g.adicionar_aresta("Vila Verde", "Braga")
	g.adicionar_aresta("Braga", "Vila Verde")

	g.adicionar_aresta("Vila Verde", "Terras de Bouro")
	g.adicionar_aresta("Terras de Bouro", "Vila Verde")

	g.adicionar_aresta("Vila Verde", "Amares")
	g.adicionar_aresta("Amares", "Vila Verde")

	g.adicionar_aresta("Braga", "Centro")
	g.adicionar_aresta("Centro", "Braga")

	g.adicionar_aresta("Braga", "Vila Nova de Famalicao")
	g.adicionar_aresta("Vila Nova de Famalicao", "Braga")

	g.adicionar_aresta("Braga", "Amares")
	g.adicionar_aresta("Amares", "Braga")

	g.adicionar_aresta("Braga", "Guimaraes")
	g.adicionar_aresta("Guimaraes", "Braga")

	g.adicionar_aresta("Braga", "Povoa de Lanhoso")
	g.adicionar_aresta("Povoa de Lanhoso", "Braga")

	g.adicionar_aresta("Guimaraes", "Vila Nova de Famalicao")
	g.adicionar_aresta("Vila Nova de Famalicao", "Guimaraes")

	g.adicionar_aresta("Guimaraes", "Vizela")
	g.adicionar_aresta("Vizela", "Guimaraes")

	g.adicionar_aresta("Guimaraes", "Fafe")
	g.adicionar_aresta("Fafe", "Guimaraes")

	g.adicionar_aresta("Guimaraes", "Povoa de Lanhoso")
	g.adicionar_aresta("Povoa de Lanhoso", "Guimaraes")

	g.adicionar_aresta("Guimaraes", "Centro")
	g.adicionar_aresta("Centro", "Guimaraes")

	g.adicionar_aresta("Vila Nova de Famalicao", "Centro")
	g.adicionar_aresta("Centro", "Vila Nova de Famalicao")

	g.adicionar_aresta("Fafe", "Povoa de Lanhoso")
	g.adicionar_aresta("Povoa de Lanhoso", "Fafe")

	g.adicionar_aresta("Fafe", "Vieira do Minho")
	g.adicionar_aresta("Vieira do Minho", "Fafe")

	g.adicionar_aresta("Fafe", "Celourico de Basto")
	g.adicionar_aresta("Celourico de Basto", "Fafe")

	g.adicionar_aresta("Fafe", "Cabeceiras de Basto")
	g.adicionar_aresta("Cabeceiras de Basto", "Fafe")

	g.adicionar_aresta("Cabeceiras de Basto", "Celourico de Basto")
	g.adicionar_aresta("Celourico de Basto", "Cabeceiras de Basto")

	g.adicionar_aresta("Cabeceiras de Basto", "Vieira do Minho")
	g.adicionar_aresta("Vieira do Minho", "Cabeceiras de Basto")

	g.adicionar_aresta("Vieira do Minho", "Terras de Bouro")
	g.adicionar_aresta("Terras de Bouro", "Vieira do Minho")

	g.adicionar_aresta("Vieira do Minho", "Povoa de Lanhoso")
	g.adicionar_aresta("Povoa de Lanhoso", "Vieira do Minho")

	g.adicionar_aresta("Terras de Bouro", "Amares")
	g.adicionar_aresta("Amares", "Terras de Bouro")

	g.adicionar_aresta("Amares", "Povoa de Lanhoso")
	g.adicionar_aresta("Povoa de Lanhoso", "Amares")
	


	saida = -1
	while saida != 0:
		print("1-Imprimir Grafo")
		print("2-Desenhar Grafo")
		print("3-Imprimir  nodos de Grafo")
		print("4-Imprimir arestas de Grafo")
		print("5-DFS")
		print("6-BFS")
		print("7-A*")
		print("8-Custo uniforme")
		print("9-Modificar situação de localidade")
		print("0-Saír")

		saida = int(input("introduza a sua opcao-> "))
		if saida == 0:
			print("saindo.......")
		elif saida == 1:
			print(g.m_grafo)
			l = input("prima enter para continuar")
		elif saida == 2:
			g.desenha()
		elif saida == 3:
			print(g.imprimir_stats_nodos())
			l = input("prima enter para continuar")
		elif saida == 4:
			origem ="Esposende"
			destino="Guimarães"
			print(g.imprimir_distancia(origem,destino))
			l = input("prima enter para continuar")
		elif saida == 5:
			inicio = "Centro"
			try:
				g.procura_DFS(inicio)
			except ValueError as e:
				print(e)
			input("Pressione Enter para continuar...")
		elif saida == 6:
			inicio = "Centro"
			transportes = [Carro(), Moto(), Helicoptero(), Drone()]
			try:
				caminho = g.procura_BFS(inicio)
				g.simular_transporte(caminho,Carro())
				
			except ValueError as e:
				print(e)
			input("Pressione Enter para continuar...")

		elif saida == 7:
			try:
				g.a_star()
			except ValueError as e:
				print(e)
			input("Pressione Enter para continuar...")
		elif saida == 8:
			print(g.custo_uniforme())
			l = input("prima enter para continuar")
		elif saida == 9:
			nodo = input ("Localidade a alterar: ")
			prioridade = input("Novo valor para prioridade (ou pressione Enter para ignorar): ")
			acessibilidade = input("Novo valor para acessibilidade do terreno (ou pressione Enter para ignorar): ")
			clima = input("Novo valor para condiçoes de clima (ou pressione Enter para ignorar): ")
			alimentos = input("Novo valor para kg de alimentos que são necessários (ou pressione Enter para ignorar): ")

			prioridade = int(prioridade) if prioridade else None
			acessibilidade = int(acessibilidade) if acessibilidade else None
			clima = int(clima) if clima else None
			alimentos = int(alimentos) if alimentos else None

			try:
				g.atualizar_atributos(nodo, prioridade=prioridade, clima=clima, acessibilidade=acessibilidade, alimentos=alimentos)
				print(f"Atributos da localidade '{nodo}' atualizados com sucesso.")
			except ValueError as e:
				print(e)

			l = input("prima enter para continuar")
	   

		else:
			print("you didn't add anything")
			l = input("prima enter para continuar")


if __name__ == "__main__":
	main()
