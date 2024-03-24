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
        etats_accessibles = set(self.etats_initiaux)
        etats_finaux = set(self.etats_terminaux)
        etats_vus = set()
        while etats_accessibles:
            etat = etats_accessibles.pop()
            etats_vus.add(etat)
            transitions_sortantes = [t for t in self.transitions if t[0] == etat]
            for transition in transitions_sortantes:
                etat_arrivee = transition[2]
                if etat_arrivee not in etats_vus:
                    etats_accessibles.add(etat_arrivee)
                if etat_arrivee in etats_finaux and etat not in self.etats_initiaux:
                    return False
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
