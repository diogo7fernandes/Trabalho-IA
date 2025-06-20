
class Transporte:
    def __init__(self, nome, capacidade, alimentos, velocidade, autonomia, deposito):
        self.nome = nome
        self.capacidade = capacidade
        self.alimentos = alimentos
        self.velocidade = velocidade
        self.autonomia = autonomia
        self.deposito = deposito
    
    def get_capacidade (self):
        return self.capacidade

    def __str__(self):
        return f"{self.nome} (Capacidade: {self.capacidade} kg, Velocidade: {self.velocidade} km/h, Autonomia: {self.autonomia} km)"
    
    def carregar(self):
        self.alimentos = self.capacidade

    def descarregar(self, quantidade):
        if (quantidade >= self.alimentos):
            quantidade = quantidade - self.alimentos
            self.alimentos = 0
        else:
            quantidade = 0
            self.alimentos = self.alimentos - quantidade

    def abastecer(self):
        self.autonomia = self.deposito
    
    def viajar(self, distancia):
        self.autonomia -= distancia

    def __lt__(self, other):
        return self.nome < other.nome
    
    def transporte_pode(self,acessibilidade):
        if isinstance(self, Carro) and (0 <= acessibilidade <= 5):
            return True
        elif isinstance(self, Mota) and (0 <= acessibilidade <= 7):
            return True
        elif isinstance(self, Helicoptero) and (0 <= acessibilidade <= 10):
            return True
        elif isinstance(self, Drone) and  (0 <= acessibilidade <= 10):
            return True
        else:
            return False

class Carro(Transporte):
    def __init__(self):
        super().__init__(
            nome="Carro",
            capacidade = 500,
            alimentos = 500,
            velocidade = 80,
            autonomia = 700,
            deposito = 700
        )

class Mota(Transporte):
    def __init__(self):
        super().__init__(
            nome="Mota",
            capacidade = 100,
            alimentos = 100,
            velocidade = 60,
            autonomia = 300,
            deposito = 300
        )

class Helicoptero(Transporte):
    def __init__(self):
        super().__init__(
            nome="Helicóptero",
            capacidade = 1000,
            alimentos = 1000,
            velocidade = 200,
            autonomia = 600,
            deposito = 600
        )

class Drone(Transporte):
    def __init__(self):
        super().__init__(
            nome="Drone",
            capacidade = 50,
            alimentos = 50,
            velocidade = 40,
            autonomia = 50,
            deposito = 50
        )

