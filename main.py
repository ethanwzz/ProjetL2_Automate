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
            print("5 - Faire le complémentaire cet automate")
            print("6 - Supprimer les etats inatteignables")
            print("7 - Quitter")

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
                    automate = automate.complementaire()
                    print("Automate après complémentarisation")
                else:
                    print("Il faut que l'automate soit deterministe complet pour pouvoir faire son complémentaire")
            elif choix == '6':
                automate.supprimer_etat_inatteignable()
                print("Les etats inatteignables ont ete supprime")
            elif choix == '7':
                return  # Quitter le programme
            else:
                print("Choix non valide. Veuillez réessayer.")

#Main permettant de faire l'entiereté des tests
"""def main():
    for i in range(1, 45):  # De E1-1 à E1-30
        filename = f"E1-{i}.txt"
        try:
            print(f"Chargement de l'automate depuis le fichier : {filename}")
            automate = lire_automate(filename)  # Assurez-vous que lire_automate est défini correctement
            print(f"Automate chargé : {filename}")
            automate.print_automate()  # Assurez-vous que print_automate est défini correctement
            print("L'automate est-il standard ? ", automate.est_standard())
            print("L'automate est-il déterministe ? ", automate.est_deterministe())
            print("L'automate est-il complet ?", automate.est_complet())
            print("")
            automate = automate.standardiser()
            automate.print_automate()
            print("L'automate est-il standard ? ", automate.est_standard())
            print("L'automate est-il déterministe ? ", automate.est_deterministe())
            print("L'automate est-il complet ?", automate.est_complet())
            print("")
            automate = automate.determiniser()
            automate.print_automate()
            print("L'automate est-il standard ? ", automate.est_standard())
            print("L'automate est-il déterministe ? ", automate.est_deterministe())
            print("L'automate est-il complet ?", automate.est_complet())
            print("")
            automate = automate.completer()
            automate.print_automate()
            print("L'automate est-il standard ? ", automate.est_standard())
            print("L'automate est-il déterministe ? ", automate.est_deterministe())
            print("L'automate est-il complet ? ", automate.est_complet())
            print("")
            print("Voici l'automate complementaire : ")
            automate = automate.complementaire()
            automate.print_automate()





            # Ici, ajoutez les opérations que vous voulez effectuer sur l'automate,
            # comme éliminer les transitions epsilon, déterminiser, etc.
            # Par exemple:
            # automate.eliminate_epsilon_transitions()
            # automate.determiniser()
            # automate.print_automate()

        except FileNotFoundError:
            print(f"Le fichier {filename} n'a pas été trouvé.")
        except Exception as e:
            print(f"Une erreur est survenue lors du traitement de l'automate : {e}")

        print("-" * 40)  # Séparateur pour chaque automate"""


if __name__ == "__main__":
    main()