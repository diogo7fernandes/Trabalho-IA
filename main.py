import sys
from grafo import Grafo
import random
from transporte import Carro, Moto, Helicoptero, Drone
import os
import copy

sys.path.append(".")  # Adiciona o diretório atual ao PYTHONPATH

def guardar_resultados(algoritmo, caminho, custo_total):
    """
    Salva os resultados de um algoritmo num ficheiro externo.

    :param algoritmo: Nome do algoritmo.
    :param caminho: Caminho percorrido.
    :param custo_total: Custo total.
    """
    nome_ficheiro = f"resultados_{algoritmo}.txt"

    with open(nome_ficheiro, "a") as ficheiro:
        ficheiro.write(f"\nAlgoritmo: {algoritmo}\n")
        ficheiro.write(f"Caminho percorrido: {caminho}\n")
        ficheiro.write(f"Custo total: {custo_total}\n")
        ficheiro.write("-" * 40 + "\n")

def main():

    g = Grafo()


# Função para gerar valores aleatórios
    def gerar_atributos_aleatorios():
        return {
            "prioridade": random.randint(0, 10),  # Valores de 0 a 10
            "acessibilidade": random.randint(0, 10),  # Valores de 0 a 10
            # valores de acessibilidade para carros:0-2, mota:3-5, helicoptero:6-8, drone:9-10
            "clima": random.randint(0, 10),  # Valores de 0 a 10
            "alimentos": random.randint(0, 100),  # Quantidade de alimentos necessarios na loc de 0 a 100
            "reabastecimento": random.choice([True, False]),  # Verdadeiro se der para rewabastecer
            "supply_refill": random.choice([True, False]),
            "TTL": random.randint(0, 100)

        }

    # Adicionando os nós com valores aleatórios
    g.adicionar_nodo("Centro", {"coordenadas": (41.4679, -8.4120), "prioridade" : 0, "acessibilidade":0, "clima":0, "alimentos":0,"reabastecimento":True,"supply_refill":True,"TTL":10000})
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

    def organizar_prioridade(self):
        # Criar uma lista de tuplas (nó, prioridade) a partir do grafo, excluindo prioridades zero
        prioridades = [(nodo, atributos["prioridade"]) for nodo, atributos in self.m_nodos.items() if atributos["alimentos"] > 0]

        # Ordenar a lista pela prioridade de forma decrescente
        prioridades_ordenadas = sorted(prioridades, key=lambda x: x[1], reverse=True)

        # Retornar apenas os nomes dos nós, mantendo a ordem
        return [nodo for nodo, _ in prioridades_ordenadas]

    lista_prioridades = organizar_prioridade(g)

    def copiar_grafo(grafo_original):
        """
        Faz uma cópia profunda do grafo, garantindo que alterações na cópia 
        não afetem o grafo original.

        Args:
            grafo_original (Grafo): O grafo original a ser copiado.

        Returns:
            Grafo: Uma nova instância do grafo copiada.
        """
            # Criar uma nova instância da classe Grafo
        grafo_copiado = Grafo()

        # Copiar os nós e as arestas de forma independente
        grafo_copiado.m_nodos = copy.deepcopy(grafo_original.m_nodos)
        grafo_copiado.m_grafo = copy.deepcopy(grafo_original.m_grafo)

        return grafo_copiado

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
        print("(1) Imprimir Grafo")
        print("(2) Desenhar Grafo")
        print("(3) Imprimir  nodos de Grafo")
        print("(4) DFS")
        print("(5) BFS")
        print("(6) A*")
        print("(7) Custo uniforme")
        print("(8) Greedy")
        print("(9) Modificar situação de localidade")
        print("(0) Sair")

        gg = copiar_grafo(g)

        try:
            user_input = input("Introduza a sua opcao -> ")
            if user_input.strip() == "":
                print("Por favor, introduza um número entre 0 e 9")
                input("Pressione Enter para continuar...")
                continue
            saida = int(user_input)
            if saida < 0 or saida > 9:
                print("Por favor, introduza um número entre 0 e 9")
                input("Pressione Enter para continuar...")
                continue
        except ValueError:
            print("Por favor, introduza um número válido entre 0 e 9")
            input("Pressione Enter para continuar...")
            continue
        
        if saida == 0:
            print("Saindo.......")
        elif saida == 1:
            print(g.m_grafo)
            l = input("Pressione Enter para continuar...")
        elif saida == 2:
            g.desenha()
        elif saida == 3:
            print(gg.imprimir_stats_nodos())
            l = input("Pressione Enter para continuar...")
        elif saida == 4:
            # Instanciar os transportes
            transportes = [
                Carro(),
                Moto(),
                Helicoptero(),
                Drone()
            ]

            caminhos_totais = {}
            custos_totais = {}

            for transporte in transportes:
                print(f"\nExecutando DFS para o transporte '{transporte.nome}'...")
                try:
                    inicio = "Centro"  # Define o nó inicial para cada transporte

                    # Executar o método de busca DFS
                    caminho, custo_total = gg.procura_DFS_prioritario(inicio, transporte)

                    # Salvar resultados
                    caminhos_totais[transporte.nome] = caminho
                    custos_totais[transporte.nome] = custo_total

                    # Salvar resultados no ficheiro
                    guardar_resultados(f"DFS_{transporte.nome}", caminho, custo_total)

                    # Exibir resultados intermediários
                    print(f"\nResultados parciais para o transporte '{transporte.nome}':")
                    print(f"Caminho percorrido: {caminho}")
                    print(f"Custo total acumulado: {custo_total}")

                except ValueError as e:
                    print(f"Erro ao processar transporte '{transporte.nome}': {e}")

            # Imprimir resultados finais para todos os transportes
            print("\nResultados Finais:")
            for transporte in transportes:
                print(f"\nTransporte: {transporte.nome}")
                print(f"Caminho percorrido: {caminhos_totais.get(transporte.nome, [])}")
                print(f"Custo total: {custos_totais.get(transporte.nome, 0)}")
            
            input("Pressione Enter para continuar...")
        elif saida == 5:
            inicio = "Centro"
            transportes = [
                Carro(),
                Moto(),
                Helicoptero(),
                Drone()
            ]
            for transporte in transportes:
                try:
                    caminho, custo_total = gg.procura_BFS(inicio, transporte, lista_prioridades)
                    # Salvar resultados no ficheiro
                    guardar_resultados(f"BFS_{transporte.nome}", caminho, custo_total)
                except ValueError as e:
                    print(e)
            input("Pressione Enter para continuar...")

        elif saida == 6:
            try:
                caminho, custo_total = gg.a_star()
                # Salvar resultados no ficheiro
                guardar_resultados("A*", caminho, custo_total)
            except ValueError as e:
                print(e)
            input("Pressione Enter para continuar...")
        elif saida == 7:
            caminho, custo_total = gg.custo_uniforme()
            print(caminho)
            print(custo_total)
            # Salvar resultados no ficheiro
            guardar_resultados("Custo_Uniforme", caminho, custo_total)
            l = input("prima enter para continuar")
        elif saida == 8:
            inicio = "Centro"  # Nó inicial
            transportes = [Carro(), Moto(), Helicoptero(), Drone()]
            for transporte in transportes:
                try:
                    print(f"Executando Greedy para o transporte '{transporte.nome}'...")
                    caminho, custo_total = g.procura_greedy(inicio, transporte)
                    print(f"Caminho: {caminho}")
                    print(f"Custo Total: {custo_total}")
                    # Salvar resultados no ficheiro
                    guardar_resultados(f"Greedy_{transporte.nome}", caminho, custo_total)
                except ValueError as e:
                    print(e)
            input("Pressione Enter para continuar...")
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

            l = input("Pressione Enter para continuar...")


        else:
            print("you didn't add anything")
            l = input("Pressione Enter para continuar...")


if __name__ == "__main__":
    main()
