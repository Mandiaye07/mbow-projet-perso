from position import Position


class Player:
    """
    Classe représentant un joueur humain.

    Attributs:
        _name (str): nom du joueur
        _color (int): couleur du joueur (0 = blanc, 1 = noir)
    """

    def __init__(self, name, color):
        """
        Initialise un joueur.

        Args:
            name (str): nom du joueur
            color (int): 0 pour blanc, 1 pour noir
        """
        self._name = name
        self._color = color

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._color

    def askMove(self):
        """
        Demande au joueur de saisir son coup.

        Returns:
            str: coup saisi ex: 'Nb1 Nc3'
        """
        return input(f"{self._name} ({'Blanc' if self._color == 0 else 'Noir'}), entrez votre coup (ex: Nb1 Nc3) : ")


if __name__ == "__main__":
    print("Test Player :")
    p = Player("Alice", 0)
    print(f"Joueur : {p.name}, couleur : {p.color}")
    print("Tests Player OK !")