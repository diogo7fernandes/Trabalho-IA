import grafo as Grafo   

class Transporte:
    def __init__(self, nome, capacidade, alimentos, velocidade, autonomia, deposito):
        self.nome = nome  # Nome do transporte
        self.capacidade = capacidade  # Capacidade de carga maxima (kg)
        self.alimentos = alimentos  # Carga atual
        self.velocidade = velocidade  # Velocidade média (km/h)
        self.autonomia = autonomia # distancia restante que pode ser percorrida
        self.deposito = deposito  # Autonomia máxima (km)
        
    def __str__(self):
        return f"{self.nome} (Capacidade: {self.capacidade} kg, Velocidade: {self.velocidade} km/h, Autonomia: {self.autonomia} km)"
    
    def carregar(self):
        self.alimentos = self.capacidade

    def descarregar(self, quantidade):
        
        if (quantidade>=self.alimentos):
            quantidade = quantidade - self.alimentos
            self.alimentos = 0
        else:
            quantidade = 0
            self.alimentos = self.alimentos - quantidade
            
    def abastecer(self):
        self.autonomia = self.deposito
    
    def viajar(self, distancia):        
        # Atualizar a autonomia
        self.autonomia -= distancia
        print(f"Viagem concluída. Autonomia restante: {self.autonomia:.2f} km. Com o {self.nome}")


        # Retornar a distância percorrida
        return distancia




    def __lt__(self, other):
            # Comparar pelo nome para garantir a ordenação no heap
            return self.nome < other.nome

class Carro(Transporte):
    def __init__(self):
        super().__init__(nome="Carro", capacidade=500, alimentos=500, velocidade=80, autonomia=700, deposito=700)

class Moto(Transporte):
    def __init__(self):
        super().__init__(nome="Moto", capacidade=100, alimentos=100, velocidade=60, autonomia=300, deposito=300)

class Helicoptero(Transporte):
    def __init__(self):
        super().__init__(nome="Helicóptero", capacidade=1000, alimentos=1000, velocidade=200, autonomia=600, deposito=600)

class Drone(Transporte):
    def __init__(self):
        super().__init__(nome="Drone", capacidade=50, alimentos=50, velocidade=40, autonomia=50, deposito=50)

    