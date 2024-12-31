from datetime import datetime, date

class Joueur:
    def __init__(self, pseudo, date_arrivee, jours_restants=180, missions=None, km_mois=0, probatoire=False):
        self.pseudo = pseudo
        self.date_arrivee = date_arrivee
        self.jours_restants = jours_restants
        self.missions = missions if missions is not None else []
        self.km_mois = km_mois
        self.probatoire = probatoire
        self.derniere_mise_a_jour = datetime.now().date()

    def ajouter_mission(self, jour, mois, annee, km, note=""):
        date_mission = date(annee, mois, jour)
        self.ajouter_mission_date(date_mission, km, note)

    def ajouter_mission_date(self, date_mission, km, note=""):
        if isinstance(date_mission, datetime):
            date_mission = date_mission.date()
        
        meme_mois = next((i for i, (d, _, _) in enumerate(self.missions) 
                          if d.year == date_mission.year and d.month == date_mission.month), None)
        
        if meme_mois is not None:
            date_existante, km_existant, note_existante = self.missions[meme_mois]
            if date_mission > date_existante:
                nouvelle_date = date_mission
            else:
                nouvelle_date = date_existante
            nouveau_km = km_existant + km
            nouvelle_note = f"{note_existante}; {note}" if note else note_existante
            self.missions[meme_mois] = (nouvelle_date, nouveau_km, nouvelle_note)
        else:
            self.missions.append((date_mission, km, note))
        
        self.missions.sort(key=lambda x: x[0])
        self.update_km_mois()
        self.verifier_fin_probatoire()
        self.recalculer_jours_restants()
        
        # Ajoutez cette condition pour gérer les jours négatifs
        if self.jours_restants < 0 and km >= 1:
            jours_a_ajouter = self.calculer_jours_a_ajouter(km)
            self.jours_restants = max(1, self.jours_restants + jours_a_ajouter)

    def update_km_mois(self):
        today = datetime.now().date()
        self.km_mois = sum(km for date, km, _ in self.missions 
                           if date.year == today.year and date.month == today.month)

    @property
    def derniere_mission(self):
        if self.missions:
            return max(self.missions, key=lambda x: x[0])
        return None

    def recalculer_jours_restants(self):
        print(f"Début recalcul : jours_restants = {self.jours_restants}")  # Débogage
        today = datetime.now().date()
        
        if self.probatoire:
            total_km = sum(km for _, km, _ in self.missions)
            jours_ecoules = (today - self.date_arrivee).days
            
            if total_km >= 2500:
                self.probatoire = False
                self.jours_restants = 180
            else:
                self.jours_restants = max(0, 30 - jours_ecoules)  # Assurez-vous que ce n'est pas négatif
        else:
            if not self.missions:
                self.jours_restants = 180
                return

            date_debut = min(mission[0] for mission in self.missions)
            self.jours_restants = 180

            for date, km, _ in sorted(self.missions):
                jours_ecoules = (date - date_debut).days
                self.jours_restants -= jours_ecoules

                jours_a_ajouter = self.calculer_jours_a_ajouter(km)
                self.jours_restants += jours_a_ajouter

                self.jours_restants = min(360, self.jours_restants)
                date_debut = date

            jours_ecoules = (today - date_debut).days
            self.jours_restants -= jours_ecoules

        self.derniere_mise_a_jour = today
        self.update_km_mois()
        print(f"Fin recalcul : jours_restants = {self.jours_restants}")  # Débogage

    def calculer_jours_a_ajouter(self, km):
        if 500 <= km < 2500:
            return 30
        elif 2500 <= km < 10000:
            return 30
        elif 10000 <= km < 25000:
            return 60
        elif 25000 <= km < 35000:
            return 90
        elif 35000 <= km < 50000:
            return 120
        elif 50000 <= km < 100000:
            return 150
        elif km >= 100000:
            return 180
        return 0

    def supprimer_mission(self, index):
        if 0 <= index < len(self.missions):
            del self.missions[index]
            self.update_km_mois()
            self.recalculer_jours_restants()

    def verifier_fin_probatoire(self):
        if self.probatoire:
            total_km = sum(km for _, km, _ in self.missions)
            jours_ecoules = (datetime.now().date() - self.date_arrivee).days
            
            if total_km >= 2500 or jours_ecoules >= 30:
                self.probatoire = False
                self.jours_restants = 180