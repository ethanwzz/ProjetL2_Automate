from automate import Automate


def lire_automate(nom_fichier):
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
            etat_depart = int(parts[0][0])
            symbole = parts[0][1]
            etat_arrivee = int(parts[0][2])
            transitions.append((etat_depart, symbole, etat_arrivee))
        return Automate(alphabet, list(range(etats_count)), etats_initiaux, etats_terminaux, transitions)


def main():
    while True:
        num_automate = input("Entrez le numéro de l'automate ou tapez 'exit' pour quitter: ")
        if num_automate.lower() == 'exit':
            break

        nom_fichier = f"{num_automate}.txt"
        try:
            automate = lire_automate(nom_fichier)
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {e}")
            continue

        while True:
            automate.print_automate()
            print("L'automate est-il standard ? ", automate.est_standard())
            print("L'automate est-il déterministe ? ", automate.est_deterministe())
            print("L'automate est-il complet ? ", automate.est_complet())

            print("\nChoisissez une option :")
            print("1 - Choisir un autre automate")
            print("2 - Déterminiser cet automate")
            print("3 - Standardiser cet automate")
            print("4 - Compléter cet automate")
            print("5 - Minimiser cet automate")
            print("6 - Quitter")

            choix = input("Entrez votre choix : ")

            if choix == '1':
                break  # Sortir de la boucle pour choisir un autre automate
            elif choix == '2':
                if not automate.est_deterministe():
                    automate = automate.determiniser()
                    print("Automate après déterminisation :")
                else:
                    print("Cet automate est déjà déterministe.")
            elif choix == '3':
                if not automate.est_standard():
                    automate = automate.standardiser()
                    print("Automate après standardisation :")
                else:
                    print("Cet automate est déjà standard.")
            elif choix == '4':
                if not automate.est_complet():
                    automate = automate.completer()
                    print("Automate après complétion :")
                else:
                    print("Cet automate est déjà complet.")
            elif choix == '5':
                if automate.est_deterministe() and automate.est_complet():
                    automate.minimiser()
                    print("Automate après minimisation :")
                else:
                    print("L'automate n'est pas deterministe complet, on ne peut donc pas le minimiser")
            elif choix == '6':
                return  # Quitter le programme
            else:
                print("Choix non valide. Veuillez réessayer.")




if __name__ == "__main__":
    main()