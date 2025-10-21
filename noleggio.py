class Noleggio:
    contatore = 1

    def __init__(self, data, id_automobile, cognome_cliente):
        self.codice = f"N{Noleggio.contatore}"
        Noleggio.contatore += 1
        self.data = data
        self.id_automobile = id_automobile
        self.cognome_cliente = cognome_cliente

    def __str__(self):
        return f"{self.codice} | avvenuto il: {self.data} | ID auto: {self.id_automobile} | {self.cognome_cliente}"

    def __repr__(self):
        return f"{self.codice} | avvenuto il: {self.data} | ID auto: {self.id_automobile} | {self.cognome_cliente}"
