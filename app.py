import streamlit as st
from Database import init_db
from utils import *
from datetime import date
import datetime
import hashlib

# Password protection
def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hashlib.sha256(st.session_state["password"].encode()).hexdigest() == st.secrets["password_hash"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if not check_password():
    st.stop()  # Do not continue if check_password is not True.

st.set_page_config(layout="wide")
# Create two columns, one for the image and one for the title
header_col1, header_col2 = st.columns([1,3])
# Display the logo 
with header_col1:
    st.image('logo.png', width=100)
# display the title in the second column
with header_col2:
    st.title('MDHFCRIR')
    
init_db()

st.title("📊 Direction des Affaires Administrative et Financière")

st.write("🧪 Application chargée avec succès.")

menu = st.sidebar.radio("📁 Menu", ["👥 Employés", "💰 Budgets", "🧾 Dépenses"])

# Sidebar
st.sidebar.title('Home')
home_button = st.sidebar.button('Accueil', key='home')
about_us_link = st.sidebar.button('A Propos de Nous', key='about')
contact_us_link = st.sidebar.button('Contactez Nous', key='contact')

# Main content
if contact_us_link:
    st.write("<span style='color:#6F4E37;'>https://droitsdelhomme.gouv.tg/</span><br>"
        "<span style='color:#FAFAFA;'>B.P. 1325 Lomé-TOGO, Tel: +228 22 51 83 85, mindhrir@gmail.com</span>", unsafe_allow_html=True)
elif about_us_link:
    st.write("<span style='color:#FAFAFA;'>Ministère des Droits de l'Homme, de la Formation à la Citoyenneté, des Relations avec les Institutions de la République.</span>", unsafe_allow_html=True)
else:
    st.write("<div style='text-align: center;'><span style='color:#FAFAFA'></span></div>", unsafe_allow_html=True)

# === Employés ===
if menu == "👥 Employés":
    st.header("👥 Gestion des Employés")

    with st.form("form_employe"):
        col1, col2 = st.columns(2)
        data = {
            "numero_matricule": col1.text_input("1. Numéro matricule"),
            "nom": col1.text_input("2. Nom"),
            "prenom": col2.text_input("3. Prénom"),
            "date_naissance": col1.date_input(
                "4. Date de naissance",
                min_value=datetime.date(1800, 1, 1),
                max_value=datetime.date.today()
            ),
            "sexe": col2.selectbox("5. Sexe", ["M", "F"]),
            "diplome": col1.text_input("6. Diplôme"),
            "date_recrutement": col2.date_input("7. Date de recrutement"),
            "poste": col1.text_input("8. Poste"),
            "statut": col2.selectbox("9. Statut", ["Permanent", "Contractuel"]),
            "categorie": col1.text_input("10. Catégorie"),
            "grade": col2.text_input("11. Grade"),
            "duree_experience": col1.number_input("12. Durée d'expérience (années)", min_value=0, step=1),
            "direction": col2.text_input("13. Direction"),
            "date_depart_retraite": col1.date_input(
                "14. Date de départ à la retraite",
                max_value=datetime.date(2100, 12, 31)
            ),
            "personne_prevenir": col2.text_input("15. Personne à prévenir en cas de besoin")
        }
        submit = st.form_submit_button("Ajouter Employé")
        if submit:
            ajouter_employe(data)
            st.success("✅ Employé ajouté.")

    st.subheader("Liste des Employés")
    emps = get_employes()
    emp_map = {f"{e.numero_matricule} - {e.nom} {e.prenom}": e.id for e in emps}

    if emps:
        selected_emp = st.selectbox("Sélectionner un Employé", list(emp_map.keys()))

        # Modifier Employé
        if st.button("Modifier Employé"):
            emp_id = emp_map[selected_emp]
            selected_emp_data = next(e for e in emps if e.id == emp_id)
            data = {
                "numero_matricule": st.text_input("1. Numéro matricule", value=selected_emp_data.numero_matricule),
                "nom": st.text_input("2. Nom", value=selected_emp_data.nom),
                "prenom": st.text_input("3. Prénom", value=selected_emp_data.prenom),
                "date_naissance": st.date_input("4. Date de naissance", value=selected_emp_data.date_naissance),
                "sexe": st.selectbox("5. Sexe", ["M", "F"], index=["M", "F"].index(selected_emp_data.sexe)),
                "diplome": st.text_input("6. Diplôme", value=selected_emp_data.diplome),
                "date_recrutement": st.date_input("7. Date de recrutement", value=selected_emp_data.date_recrutement),
                "poste": st.text_input("8. Poste", value=selected_emp_data.poste),
                "statut": st.selectbox("9. Statut", ["Permanent", "Contractuel"], index=["Permanent", "Contractuel"].index(selected_emp_data.statut)),
                "categorie": st.text_input("10. Catégorie", value=selected_emp_data.categorie),
                "grade": st.text_input("11. Grade", value=selected_emp_data.grade),
                "duree_experience": st.number_input("12. Durée d'expérience (années)", min_value=0, step=1, value=selected_emp_data.duree_experience),
                "direction": st.text_input("13. Direction", value=selected_emp_data.direction),
                "date_depart_retraite": st.date_input(
                    "14. Date de départ à la retraite", 
                    value=selected_emp_data.date_depart_retraite,
                    max_value=datetime.date(2100, 12, 31)
                ),
                "personne_prevenir": st.text_input("15. Personne à prévenir en cas de besoin", value=selected_emp_data.personne_prevenir)
            }

            if st.button("Enregistrer Modifications"):
                modifier_employe(emp_id, data)
                st.success("✅ Employé modifié.")

        # Supprimer Employé
        if st.button("Supprimer Employé"):
            emp_id = emp_map[selected_emp]
            supprimer_employe(emp_id)
            st.success("✅ Employé supprimé.")

        st.dataframe([vars(e) for e in emps])

    else:
        st.warning("Tout est Supprimé, Enregistrez un Nouveau Employé.")

# === Budgets ===
elif menu == "💰 Budgets":
    st.header("💰 Gestion des Budgets")

    with st.form("form_budget"):
        exercice = st.number_input("Exercice", step=1, value=date.today().year)
        montant = st.number_input("Montant total", step=1000.0)
        type_budget = st.selectbox("Type", ["Fonctionnement", "Investissement"])
        date_val = st.date_input("Date de validation")

        submit = st.form_submit_button("Ajouter Budget")
        if submit:
            ajouter_budget({
                "exercice": exercice,
                "montant_total": montant,
                "type_budget": type_budget,
                "date_validation": date_val
            })
            st.success("✅ Budget ajouté.")

    st.subheader("Liste des Budgets")
    budgets = get_budgets()
    budget_map = {f"Budget {b.id} – {b.exercice}": b.id for b in budgets}

    if budgets:
        selected_budget = st.selectbox("Sélectionner un Budget", list(budget_map.keys()))

        # Modifier Budget
        if st.button("Modifier Budget"):
            budget_id = budget_map[selected_budget]
            data = {
                "exercice": st.number_input("Exercice", step=1, value=budgets[budget_id - 1].exercice),
                "montant_total": st.number_input("Montant total", step=1000.0, value=budgets[budget_id - 1].montant_total),
                "type_budget": st.selectbox("Type", ["Fonctionnement", "Investissement"], index=["Fonctionnement", "Investissement"].index(budgets[budget_id - 1].type_budget)),
                "date_validation": st.date_input("Date de validation", value=budgets[budget_id - 1].date_validation)
            }

            if st.button("Enregistrer Modifications"):
                modifier_budget(budget_id, data)
                st.success("✅ Budget modifié.")

        # Supprimer Budget
        if st.button("Supprimer Budget"):
            budget_id = budget_map[selected_budget]
            supprimer_budget(budget_id)
            st.success("✅ Budget supprimé.")

        st.dataframe([vars(b) for b in budgets])

    else:
        st.warning("Tout est Supprimé, Enregistrez un Nouveau Budget.")

# === Dépenses ===
elif menu == "🧾 Dépenses":
    st.header("🧾 Suivi des Dépenses")

    budgets = get_budgets()
    budget_map = {f"Budget {b.id} – {b.exercice}": b.id for b in budgets}

    with st.form("form_depense"):
        description = st.text_input("Description")
        montant = st.number_input("Montant", step=100.0)
        date_depense = st.date_input("Date de la dépense")
        responsable = st.text_input("Responsable")
        code = st.text_input("Code imputation")
        budget_libelle = st.selectbox("Budget", list(budget_map.keys()))

        submit = st.form_submit_button("Ajouter Dépense")
        if submit:
            ajouter_depense({
                "description": description,
                "montant": montant,
                "date_depense": date_depense,
                "responsable": responsable,
                "code_imputation": code,
                "budget_id": budget_map[budget_libelle]
            })
            st.success("✅ Dépense ajoutée.")

    st.subheader("Liste des Dépenses")
    depenses = get_depenses()
    depense_map = {f"{d.description} ({d.montant}€)": d.id for d in depenses}

    if depenses:
        selected_depense = st.selectbox("Sélectionner une Dépense", list(depense_map.keys()))

        # Modifier Dépense
        if st.button("Modifier Dépense"):
            depense_id = depense_map[selected_depense]
            data = {
                "description": st.text_input("Description", value=depenses[depense_id - 1].description),
                "montant": st.number_input("Montant", step=100.0, value=depenses[depense_id - 1].montant),
                "date_depense": st.date_input("Date de la dépense", value=depenses[depense_id - 1].date_depense),
                "responsable": st.text_input("Responsable", value=depenses[depense_id - 1].responsable),
                "code_imputation": st.text_input("Code imputation", value=depenses[depense_id - 1].code_imputation),
                "budget_id": st.selectbox("Budget", list(budget_map.keys()), index=list(budget_map.keys()).index(f"Budget {depenses[depense_id - 1].budget_id} – {depenses[depense_id - 1].exercice}"))
            }

            if st.button("Enregistrer Modifications"):
                modifier_depense(depense_id, data)
                st.success("✅ Dépense modifiée.")

        # Supprimer Dépense
        if st.button("Supprimer Dépense"):
            depense_id = depense_map[selected_depense]
            supprimer_depense(depense_id)
            st.success("✅ Dépense supprimée.")

        st.dataframe([vars(d) for d in depenses])

    else:
        st.warning("Tout est Supprimé, Enregistrez une Nouvelle Dépense.")

# Footer
st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #262730;
            text-align: center;
            padding: 10px;
        }
        .footer a {
            margin: 0 10px;
        }
    </style>
    <div class="footer">
        <p>Trademark © MDHFCRIR. All rights reserved.</p>
        <p>Suivez-nous sur <a href="https://x.com/memppc" target="_blank">Twitter</a>, 
        <a href="https://web.facebook.com/MEMPPC/?_rdc=1&_rdr#" target="_blank">Facebook</a>, and 
        <a href="https://www.linkedin.com/company/memppc1" target="_blank">LinkedIn</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
