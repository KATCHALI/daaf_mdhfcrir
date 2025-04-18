# models.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime

Base = declarative_base()

# ------------------ Modèles ------------------

class Employe(Base):
    __tablename__ = 'employes'
    id = Column(Integer, primary_key=True)
    numero_matricule = Column(String, unique=True)
    nom = Column(String)
    prenom = Column(String)
    date_naissance = Column(Date)
    sexe = Column(String)
    diplome = Column(String)
    date_recrutement = Column(Date)
    poste = Column(String)
    statut = Column(String)
    categorie = Column(String)
    grade = Column(String)
    duree_experience = Column(Integer)  # en années
    direction = Column(String)
    date_depart_retraite = Column(Date)
    personne_prevenir = Column(String)

class Budget(Base):
    __tablename__ = 'budgets'
    id = Column(Integer, primary_key=True)
    exercice = Column(Integer)
    montant_total = Column(Float)
    type_budget = Column(String)
    date_validation = Column(Date)

class Depense(Base):
    __tablename__ = 'depenses'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    montant = Column(Float)
    date_depense = Column(Date)
    responsable = Column(String)
    code_imputation = Column(String)
    budget_id = Column(Integer, ForeignKey('budgets.id'))

# ------------------ Connexion à la BD ------------------

engine = create_engine('sqlite:///daaf.db')
Session = sessionmaker(bind=engine)
session = Session()

# ------------------ Fonctions ------------------

def ajouter_employe():
    try:
        numero_matricule = input("1. Numéro matricule : ")
        nom = input("2. Nom : ")
        prenom = input("3. Prénom : ")
        date_naissance_str = input("4. Date de naissance (YYYY-MM-DD) : ")
        date_naissance = datetime.strptime(date_naissance_str, "%Y-%m-%d").date()
        if date_naissance < date(1900, 1, 1) or date_naissance > date.today():
            print("⚠️ Date de naissance invalide. Doit être entre 1900 et aujourd'hui.")
            return

        sexe = input("5. Sexe (M/F) : ")
        diplome = input("6. Diplôme : ")
        date_recrutement_str = input("7. Date de recrutement (YYYY-MM-DD) : ")
        date_recrutement = datetime.strptime(date_recrutement_str, "%Y-%m-%d").date()
        poste = input("8. Poste : ")
        statut = input("9. Statut : ")
        categorie = input("10. Catégorie : ")
        grade = input("11. Grade : ")
        duree_experience = int(input("12. Durée d'expérience (en années) : "))
        direction = input("13. Direction : ")
        date_depart_retraite_str = input("14. Date de départ à la retraite (YYYY-MM-DD) : ")
        date_depart_retraite = datetime.strptime(date_depart_retraite_str, "%Y-%m-%d").date()
        if date_depart_retraite > date(2100, 12, 31):
            print("⚠️ Date de départ à la retraite invalide. Doit être avant 2101.")
            return
        personne_prevenir = input("15. Personne à prévenir en cas de besoin : ")

        nouvel_employe = Employe(
            numero_matricule=numero_matricule,
            nom=nom,
            prenom=prenom,
            date_naissance=date_naissance,
            sexe=sexe,
            diplome=diplome,
            date_recrutement=date_recrutement,
            poste=poste,
            statut=statut,
            categorie=categorie,
            grade=grade,
            duree_experience=duree_experience,
            direction=direction,
            date_depart_retraite=date_depart_retraite,
            personne_prevenir=personne_prevenir
        )
        session.add(nouvel_employe)
        session.commit()
        print("✅ Employé ajouté avec succès.")
    except Exception as e:
        print("❌ Erreur lors de l'ajout :", e)

# ... (rest of the CLI functions remain the same, just update field order where needed)

def supprimer_employe():
    try:
        employe_id = int(input("ID de l'employé à supprimer : "))
        employe = session.query(Employe).filter(Employe.id == employe_id).first()
        if employe:
            session.delete(employe)
            session.commit()
            print(f"🗑️ Employé avec l'ID {employe_id} supprimé.")
        else:
            print("❌ Aucun employé trouvé avec cet ID.")
    except ValueError:
        print("❌ ID invalide.")
    except Exception as e:
        print("❌ Erreur :", e)

def afficher_employes():
    employes = session.query(Employe).all()
    if not employes:
        print("📭 Aucun employé trouvé.")
        return
    print("\n📋 Liste des employés :")
    for emp in employes:
        print(f"[{emp.id}] {emp.numero_matricule} - {emp.nom} {emp.prenom} - {emp.poste} ({emp.direction})")

def modifier_employe():
    try:
        employe_id = int(input("ID de l'employé à modifier : "))
        employe = session.query(Employe).filter(Employe.id == employe_id).first()
        if employe:
            print("Laissez vide pour ne pas modifier un champ.")
            numero_matricule = input(f"Numéro matricule ({employe.numero_matricule}) : ") or employe.numero_matricule
            nom = input(f"Nom ({employe.nom}) : ") or employe.nom
            prenom = input(f"Prénom ({employe.prenom}) : ") or employe.prenom
            dn_str = input(f"Date de naissance ({employe.date_naissance}) [YYYY-MM-DD] : ")
            date_naissance = datetime.strptime(dn_str, "%Y-%m-%d").date() if dn_str else employe.date_naissance

            if date_naissance < date(1900, 1, 1) or date_naissance > date.today():
                print("⚠️ Date de naissance invalide.")
                return

            sexe = input(f"Sexe ({employe.sexe}) : ") or employe.sexe
            poste = input(f"Poste ({employe.poste}) : ") or employe.poste
            direction = input(f"Direction ({employe.direction}) : ") or employe.direction
            statut = input(f"Statut ({employe.statut}) : ") or employe.statut
            dr_str = input(f"Date de recrutement ({employe.date_recrutement}) [YYYY-MM-DD] : ")
            date_recrutement = datetime.strptime(dr_str, "%Y-%m-%d").date() if dr_str else employe.date_recrutement
            diplome = input(f"Diplôme ({employe.diplome}) : ") or employe.diplome
            categorie = input(f"Catégorie ({employe.categorie}) : ") or employe.categorie
            duree_experience = input(f"Durée d'expérience ({employe.duree_experience}) : ") or employe.duree_experience
            ddr_str = input(f"Date de départ à la retraite ({employe.date_depart_retraite}) [YYYY-MM-DD] : ")
            date_depart_retraite = datetime.strptime(ddr_str, "%Y-%m-%d").date() if ddr_str else employe.date_depart_retraite
            grade = input(f"Grade ({employe.grade}) : ") or employe.grade
            personne_prevenir = input(f"Personne à prévenir ({employe.personne_prevenir}) : ") or employe.personne_prevenir

            # Mise à jour
            employe.numero_matricule = numero_matricule
            employe.nom = nom
            employe.prenom = prenom
            employe.date_naissance = date_naissance
            employe.sexe = sexe
            employe.poste = poste
            employe.direction = direction
            employe.statut = statut
            employe.date_recrutement = date_recrutement
            employe.diplome = diplome
            employe.categorie = categorie
            employe.duree_experience = duree_experience
            employe.date_depart_retraite = date_depart_retraite
            employe.grade = grade
            employe.personne_prevenir = personne_prevenir

            session.commit()
            print("✏️ Employé mis à jour avec succès.")
        else:
            print("❌ Aucun employé trouvé avec cet ID.")
    except Exception as e:
        print("❌ Erreur :", e)

# ------------------ Menu CLI ------------------

def menu():
    while True:
        print("\n=== MENU EMPLOYE ===")
        print("1. Ajouter un employé")
        print("2. Supprimer un employé")
        print("3. Afficher tous les employés")
        print("4. Modifier un employé")
        print("5. Quitter")
        choix = input("Votre choix : ")

        if choix == "1":
            ajouter_employe()
        elif choix == "2":
            supprimer_employe()
        elif choix == "3":
            afficher_employes()
        elif choix == "4":
            modifier_employe()
        elif choix == "5":
            print("👋 Au revoir !")
            break
        else:
            print("❌ Choix invalide.")

# ------------------ Initialisation ------------------

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    menu()
