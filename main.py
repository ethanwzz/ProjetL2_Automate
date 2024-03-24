class Automate:
    def __init__(self, alphabet, etats, etats_initiaux, etats_terminaux, transitions):
        self.alphabet = alphabet
        self.etats = etats
        self.etats_initiaux = etats_initiaux
        self.etats_terminaux = etats_terminaux
        self.transitions = transitions

    def est_deterministe(self):
        for etat in self.etats:
            transitions_sortantes = [t for t in self.transitions if t[0] == etat]
            if len(transitions_sortantes) > len(set(t[1] for t in transitions_sortantes)):
                return False
        return True

    def est_standard(self):
        # Vérifier s'il y a exactement un seul état initial
        if len(self.etats_initiaux) != 1:
            return False

        etat_initial = self.etats_initiaux[0]

        # Vérifier si aucune transition ne mène à l'état initial, sauf les boucles sur d'autres états
        for transition in self.transitions:
            if transition[2] == etat_initial:
                if transition[0] == etat_initial:
                    return False  # Une boucle directe sur l'état initial n'est pas autorisée
                elif transition[0] in self.etats_initiaux:
                    return False  # Une transition de l'état initial vers lui-même ou un autre état initial n'est pas autorisée

        return True

    def est_complet(self):
        for etat in self.etats:
            for symbole in self.alphabet:
                transitions = [t for t in self.transitions if t[0] == etat and t[1] == symbole]
                if not transitions:
                    return False
        return True

    def afficher_tableau(self):
        # Création de la première ligne du tableau avec les symboles de l'alphabet
        header = "\t" + "\t".join(self.alphabet)

        # Création des lignes du tableau avec les transitions pour chaque état
        rows = []
        for etat in self.etats:
            row = []
            # Ajout des indicateurs d'états initiaux et terminaux en première colonne
            row.append('I' if etat in self.etats_initiaux else '')
            row.append('T' if etat in self.etats_terminaux else '')
            row.append(str(etat))  # Ajout de l'état à la première colonne
            for symbole in self.alphabet:
                # Recherche des transitions pour l'état et le symbole courants
                destinations = [t[2] for t in self.transitions if t[0] == etat and t[1] == symbole]
                row.append(",".join(map(str, destinations)) if destinations else "-")
            rows.append("\t".join(row))

        # Affichage du tableau
        print("E\tS Etat" + header)
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
    nom_fichier = "automate.txt" #input("Entrez le nom du fichier contenant l'automate : ")
    automate = lire_automate_sur_fichier(nom_fichier)
    automate.afficher_tableau()
    print("L'automate est déterministe :", automate.est_deterministe())
    print("L'automate est standard :", automate.est_standard())
    print("L'automate est complet :", automate.est_complet())

if __name__ == "__main__":
    main()
