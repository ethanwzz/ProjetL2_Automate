class Automate:
    def __init__(self, alphabet, states, initial_states, final_states, transitions_list):
        self.alphabet = alphabet
        self.states = states
        self.initial_states = initial_states
        self.final_states = final_states
        self.transitions = {}
        for (start_state, symbol, end_state) in transitions_list:
            if (start_state, symbol) not in self.transitions:
                self.transitions[(start_state, symbol)] = []
            self.transitions[(start_state, symbol)].append(end_state)

    def est_deterministe(self):
        if len(self.initial_states) != 1:
            return False
        for state in self.states:
            seen = set()
            for symbol in self.alphabet:
                if (state, symbol) in self.transitions and len(self.transitions[(state, symbol)]) > 1:
                    return False
                if (state, symbol) in self.transitions:
                    if symbol in seen:
                        return False
                    seen.add(symbol)
        return True

    def est_standard(self):
        # Vérifier s'il y a exactement un seul état initial
        if len(self.initial_states) != 1:
            return False

        etat_initial = self.initial_states[0]

        # Vérifier si aucune transition ne mène à l'état initial, y compris les boucles sur l'état initial
        for (source_state, symbol), target_states in self.transitions.items():
            # Si l'état initial est dans les états cibles d'une transition, et cette transition part de l'état initial, retourner False
            if etat_initial in target_states:
                return False  # Aucune transition n'est autorisée à mener à l'état initial

        return True

    def est_complet(self):
        for state in self.states:
            for symbol in self.alphabet:
                # Si une transition manque pour un symbole à partir de cet état, l'automate n'est pas complet
                if (state, symbol) not in self.transitions or not self.transitions[(state, symbol)]:
                    return False
        return True

    def determiniser(self):
        if self.est_deterministe():
            print("L'automate est déjà déterministe.")
            return self

        # Un dictionnaire pour suivre les nouveaux états de l'automate déterministe
        # La clé est un frozenset d'états de l'automate original et la valeur est le nouvel état dans l'automate déterministe
        new_states_map = {frozenset(self.initial_states): 0}
        new_initial_states = [0]
        new_transitions_list = []
        new_final_states = []
        checked_states = set()  # Garde une trace des états déjà vérifiés

        # Une file pour vérifier les états de l'automate de manière itérative
        states_to_check = [frozenset(self.initial_states)]

        while states_to_check:
            current_states = states_to_check.pop(0)
            current_state_id = new_states_map[current_states]

            # Si l'un des états actuels est un état final dans l'automate original, ajouter à la liste des états finaux
            if any(state in self.final_states for state in current_states) and current_state_id not in new_final_states:
                new_final_states.append(current_state_id)

            # Pour chaque symbole de l'alphabet, trouver le nouvel état après la transition
            for symbol in self.alphabet:
                # Trouver toutes les transitions pour ce symbole pour tous les états courants
                next_states = frozenset(
                    end_state for start_state in current_states
                    if (start_state, symbol) in self.transitions
                    for end_state in self.transitions[(start_state, symbol)]
                )

                if not next_states:
                    continue

                # Ajouter les nouveaux états à la file d'attente si ce n'est pas déjà fait
                if next_states not in new_states_map:
                    new_state_id = len(new_states_map)
                    new_states_map[next_states] = new_state_id
                    states_to_check.append(next_states)
                else:
                    new_state_id = new_states_map[next_states]

                # Ajouter la transition au nouvel automate
                new_transitions_list.append((current_state_id, symbol, new_state_id))

        # Construire le nouvel automate déterministe
        new_states_count = len(new_states_map)
        return Automate(
            self.alphabet,
            list(range(new_states_count)),
            new_initial_states,
            new_final_states,
            new_transitions_list
        )

    def standardiser(self):
        # Si l'automate est déjà standard, ne rien faire
        if self.est_standard():
            return self

        # Créer un nouvel état qui sera le seul état initial
        new_initial_state = max(self.states) + 1
        self.states.append(new_initial_state)
        new_transitions_list = [(new_initial_state, symbol, target) for symbol in self.alphabet for target in
                                self.initial_states]

        # Ajouter les nouvelles transitions dans la liste des transitions
        for transition in new_transitions_list:
            self.transitions[transition[:2]] = transition[2:]

        # Mettre à jour les états initiaux
        self.initial_states = [new_initial_state]

        # Retirer les anciennes transitions qui arrivaient à l'état initial
        for (source_state, symbol), target_states in list(self.transitions.items()):
            if self.initial_states[0] in target_states and source_state != self.initial_states[0]:
                self.transitions[(source_state, symbol)].remove(self.initial_states[0])

        return self

    def completer(self):
        if self.est_complet():
            print("L'automate est déjà complet.")
            return self

        # Utiliser -1 pour l'état poubelle
        etat_poubelle = -1
        if etat_poubelle not in self.states:
            self.states.append(etat_poubelle)

        # Ajoutez les transitions manquantes vers l'état poubelle
        for state in self.states:
            for symbol in self.alphabet:
                if (state, symbol) not in self.transitions:
                    self.transitions[(state, symbol)] = [etat_poubelle]

        # Ajoutez des transitions de l'état poubelle à lui-même pour chaque symbole
        for symbol in self.alphabet:
            self.transitions[(etat_poubelle, symbol)] = [etat_poubelle]

        return self

    def remove_unreachable_states(self):
        accessible_states = set()
        states_to_check = [self.initial_states[0]]  # Partir de l'état initial

        while states_to_check:
            state = states_to_check.pop()
            accessible_states.add(state)
            for symbol in self.alphabet:
                if (state, symbol) in self.transitions:
                    for target in self.transitions[(state, symbol)]:
                        if target not in accessible_states:
                            states_to_check.append(target)

        # Filtrer les transitions pour ne garder que celles qui concernent des états accessibles
        self.transitions = {(s, sy): t for (s, sy), t in self.transitions.items() if
                            s in accessible_states and all(ti in accessible_states for ti in t)}
        self.states = list(accessible_states)  # Mettre à jour la liste des états

        # Mettre à jour les états initiaux et les états finaux
        self.initial_states = [s for s in self.initial_states if s in accessible_states]
        self.final_states = [s for s in self.final_states if s in accessible_states]

    def minimiser(self):
        self.remove_unreachable_states()

        # Initialisation des partitions
        P = [set(self.final_states), {state for state in self.states if state not in self.final_states}]
        new_P = []

        # Processus d'affinement des partitions
        while P != new_P:
            if new_P:
                P = new_P.copy()
            new_P = []

            for A in P:
                partitions = {}
                for state in A:
                    transitions = tuple((symbol, frozenset(self.transitions.get((state, symbol), []))) for symbol in self.alphabet)
                    if transitions not in partitions:
                        partitions[transitions] = []
                    partitions[transitions].append(state)

                new_P.extend([set(partition) for partition in partitions.values()])

        # Reconstruire l'automate avec les partitions finales
        new_transitions = {}
        state_mapping = {state: i for i, part in enumerate(new_P) for state in part}
        for (state, symbol), targets in self.transitions.items():
            new_state = state_mapping[state]
            new_target = state_mapping[next(iter(targets))]  # Assume une cible pour simplifier
            if (new_state, symbol) not in new_transitions:
                new_transitions[(new_state, symbol)] = new_target

        # Mettre à jour les états, transitions, états initiaux et finaux
        self.states = list(range(len(new_P)))
        self.transitions = new_transitions
        self.initial_states = [state_mapping[init] for init in self.initial_states if init in state_mapping]
        self.final_states = [state_mapping[fin] for fin in self.final_states if fin in state_mapping]

        return self

    def complementaire(self):
        # Déterminiser l'automate si ce n'est pas déjà fait
        if not self.est_deterministe():
            self = self.determiniser()

        # Compléter l'automate si ce n'est pas déjà fait
        if not self.est_complet():
            self = self.completer()

        # Inverser les états terminaux et non terminaux
        for state in self.states:
            if state in self.final_states:
                self.final_states.remove(state)  # Retirer les états terminaux
            else:
                self.final_states.append(state)  # Rendre les états non terminaux terminaux

        # Marquer l'état poubelle comme terminal
        if -1 not in self.final_states:
            self.final_states.append(-1)

        return self

    def print_automate(self):
        # Calculer la largeur des colonnes pour l'affichage
        max_state = max([state for state in self.states if state != -1], default=0, key=abs)
        state_width = max(len(str(max_state)), 5) + 2
        cell_width = max(max(len(str(s)) for s in self.states if s != -1), 3, key=abs) + 2
        type_width = 4  # Largeur pour la colonne de type

        # En-tête du tableau
        header = f"{'Type':^{type_width}}" + f"{'Etat':^{state_width}}" + "".join(
            f"{sym:^{cell_width}}" for sym in self.alphabet)
        print(header)
        print('-' * len(header))

        # Lignes du tableau
        for state in self.states:
            # Remplacer l'affichage de l'état poubelle par 'P'
            state_display = 'P' if state == -1 else state

            # Indiquer si l'état est initial, terminal ou les deux
            state_type = ''
            if state in self.initial_states:
                state_type += 'I'
            if state in self.final_states:
                state_type += 'T'

            row = f"{state_type:^{type_width}}" + f"{state_display:^{state_width}}"

            for symbol in self.alphabet:
                transition_states = self.transitions.get((state, symbol), [])
                cell = ','.join('P' if s == -1 else str(s) for s in transition_states)
                row += f"{cell:^{cell_width}}"
            print(row)