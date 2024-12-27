import sys
sys.path.append(".")  # Adiciona o diretório atual ao PYTHONPATH
from grafo import Grafo




def main():

	g = Grafo()
	
	#lat, longitude
	g.adicionar_nodo("Centro", {"coordenadas": (41.4679, -8.4120), "prioridade":0, "acessibilidade":0, "clima":0, "alimentos":0})
	g.adicionar_nodo("Braga", {"coordenadas": (41.5503, -8.4201), "prioridade":1, "acessibilidade":1, "clima":1, "alimentos":0})
	g.adicionar_nodo("Esposende", {"coordenadas": (41.5320, -8.7832), "prioridade":2, "acessibilidade":2, "clima":2, "alimentos":0})
	g.adicionar_nodo("Barcelos", {"coordenadas": (41.5388, -8.6151), "prioridade":3, "acessibilidade":3, "clima":3, "alimentos":0})
	g.adicionar_nodo("Vila Nova de Famalicão", {"coordenadas": (41.4091, -8.5198), "prioridade":3, "acessibilidade":1, "clima":3, "alimentos":0})
	g.adicionar_nodo("Guimarães", {"coordenadas": (41.4444, -8.2962), "prioridade":5, "acessibilidade":1, "clima":4, "alimentos":0})
	g.adicionar_nodo("Vizela", {"coordenadas": (41.3890, -8.2926), "prioridade":5, "acessibilidade":10, "clima":2, "alimentos":0})
	g.adicionar_nodo("Fafe", {"coordenadas": (41.4541, -8.1706), "prioridade":1, "acessibilidade":0, "clima":2, "alimentos":0})
	g.adicionar_nodo("Póvoa de Lanhoso", {"coordenadas": (41.5769, -8.2697), "prioridade":1, "acessibilidade":10, "clima":2, "alimentos":0})
	g.adicionar_nodo("Amares", {"coordenadas": (41.6308, -8.3514), "prioridade":1, "acessibilidade":5, "clima":6, "alimentos":0})
	g.adicionar_nodo("Vila Verde", {"coordenadas": (41.6480, -8.4367), "prioridade":1, "acessibilidade":2, "clima":5, "alimentos":0})
	g.adicionar_nodo("Terras de Bouro", {"coordenadas": (41.7323, -8.3088), "prioridade":8, "acessibilidade":2, "clima":6, "alimentos":0})
	g.adicionar_nodo("Vieira do Minho", {"coordenadas": (41.6325, -8.1461), "prioridade":4, "acessibilidade":7, "clima":4, "alimentos":0})
	g.adicionar_nodo("Celourico de Basto", {"coordenadas": (41.3899, -8.0058), "prioridade":5, "acessibilidade":5, "clima":7, "alimentos":0})
	g.adicionar_nodo("Cabeceiras de Basto", {"coordenadas": (41.5151, -7.9889), "prioridade":5, "acessibilidade":5, "clima":6, "alimentos":0})

	g.adicionar_aresta("Esposende", "Barcelos")
	g.adicionar_aresta("Barcelos", "Esposende")

	g.adicionar_aresta("Barcelos", "Vila Nova de Famalicão")
	g.adicionar_aresta("Vila Nova de Famalicão", "Barcelos")

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

	g.adicionar_aresta("Braga", "Vila Nova de Famalicão")
	g.adicionar_aresta("Vila Nova de Famalicão", "Braga")

	g.adicionar_aresta("Braga", "Amares")
	g.adicionar_aresta("Amares", "Braga")

	g.adicionar_aresta("Braga", "Guimarães")
	g.adicionar_aresta("Guimarães", "Braga")

	g.adicionar_aresta("Braga", "Póvoa de Lanhoso")
	g.adicionar_aresta("Póvoa de Lanhoso", "Braga")

	g.adicionar_aresta("Guimarães", "Vila Nova de Famalicão")
	g.adicionar_aresta("Vila Nova de Famalicão", "Guimarães")

	g.adicionar_aresta("Guimarães", "Vizela")
	g.adicionar_aresta("Vizela", "Guimarães")

	g.adicionar_aresta("Guimarães", "Fafe")
	g.adicionar_aresta("Fafe", "Guimarães")

	g.adicionar_aresta("Guimarães", "Póvoa de Lanhoso")
	g.adicionar_aresta("Póvoa de Lanhoso", "Guimarães")

	g.adicionar_aresta("Guimarães", "Centro")
	g.adicionar_aresta("Centro", "Guimarães")

	g.adicionar_aresta("Vila Nova de Famalicão", "Centro")
	g.adicionar_aresta("Centro", "Vila Nova de Famalicão")

	g.adicionar_aresta("Fafe", "Póvoa de Lanhoso")
	g.adicionar_aresta("Póvoa de Lanhoso", "Fafe")

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

	g.adicionar_aresta("Vieira do Minho", "Póvoa de Lanhoso")
	g.adicionar_aresta("Póvoa de Lanhoso", "Vieira do Minho")

	g.adicionar_aresta("Terras de Bouro", "Amares")
	g.adicionar_aresta("Amares", "Terras de Bouro")

	g.adicionar_aresta("Amares", "Póvoa de Lanhoso")
	g.adicionar_aresta("Póvoa de Lanhoso", "Amares")
	


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
			print(g.m_grafo.keys())
			l = input("prima enter para continuar")
		elif saida == 4:
			origem ="Esposende"
			destino="Guimarães"
			print(g.imprimir_distancia(origem,destino))
			l = input("prima enter para continuar")
		elif saida == 5:
			inicio = "Centro"
			try:
				ordem_visita = g.procura_DFS(inicio) 
				print(f"Ordem dos nós visitados (DFS): {ordem_visita}")
			except ValueError as e:
				print(e)
			input("Pressione Enter para continuar...")
		elif saida == 6:
			inicio = "Centro"
			try:
				ordem_visita = g.procura_BFS(inicio)
				print(f"Ordem dos nós visitados (BFS): {ordem_visita}")
			except ValueError as e:
				print(e)
			input("Pressione Enter para continuar...")       
		elif saida == 7:
			inicio = input("Digite o nó inicial: ")
			objetivo = input("Digite o nó objetivo: ")
			try:
				caminho, custo = g.a_star(inicio, objetivo)
				if caminho:
					print(f"Caminho encontrado: {caminho}")
					print(f"Custo total: {custo:.2f}")
				else:
					print("Nenhum caminho encontrado.")
			except ValueError as e:
				print(e)
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
