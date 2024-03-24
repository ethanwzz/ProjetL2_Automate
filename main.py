class Automate:
    def __init__(self, alphabet, etats, etats_initiaux, etats_terminaux, transitions):
        self.alphabet = alphabet
        self.etats = etats
        self.etats_initiaux = etats_initiaux
        self.etats_terminaux = etats_terminaux
        self.transitions = transitions

    def afficher_tableau(self):
        # Création de la première ligne du tableau avec les symboles de l'alphabet
        header = "\t" + "\t".join(self.alphabet)

        # Création des lignes du tableau avec les transitions pour chaque état
        rows = []
        for etat in self.etats:
            row = [str(etat)]
            for symbole in self.alphabet:
                # Recherche des transitions pour l'état et le symbole courants
                destinations = [t[2] for t in self.transitions if t[0] == etat and t[1] == symbole]
                row.append(",".join(map(str, destinations)) if destinations else "-")
            rows.append("\t".join(row))

        # Affichage du tableau
        print(header)
        for row in rows:
            print(row)

def lire_automate_sur_fichier(nom_fichier):
    with open(nom_fichier, 'r') as file:
        lines = file.readlines()
        alphabet_size = int(lines[0].split('#')[0].strip())
        alphabet = [chr(ord('a') + i) for i in range(alphabet_size)]
        etats_count = int(lines[1].split('#')[0].strip())
        etats_initiaux = list(map(int, lines[2].split('#')[0].split()[1:]))
        etats_terminaux = list(map(int, lines[3].split('#')[0].split()[1:]))
        transitions = []
        for line in lines[5:]:
            parts = line.strip().split()
            etat_depart = int(parts[0][0])  # Premier caractère de la première partie de la transition
            symbole = parts[0][1]           # Deuxième caractère de la première partie de la transition
            etat_arrivee = int(parts[0][2]) # Troisième caractère de la première partie de la transition
            transitions.append((etat_depart, symbole, etat_arrivee))
        return Automate(alphabet, list(range(etats_count)), etats_initiaux, etats_terminaux, transitions)

def main():
    nom_fichier = input("Entrez le nom du fichier contenant l'automate : ")
    automate = lire_automate_sur_fichier(nom_fichier)
    automate.afficher_tableau()

if __name__ == "__main__":
    main()
