from models import Employe, Budget, Depense
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine("sqlite:///daaf.db")
Session = sessionmaker(bind=engine)

# Ajouter (Add)
def ajouter_employe(data):
    session = Session()
    e = Employe(**data)
    session.add(e)
    session.commit()
    session.close()

def ajouter_budget(data):
    session = Session()
    b = Budget(**data)
    session.add(b)
    session.commit()
    session.close()

def ajouter_depense(data):
    session = Session()
    d = Depense(**data)
    session.add(d)
    session.commit()
    session.close()

# Get all records
def get_employes():
    session = Session()
    emps = session.query(Employe).all()
    session.close()
    return emps

def get_budgets():
    session = Session()
    bs = session.query(Budget).all()
    session.close()
    return bs

def get_depenses():
    session = Session()
    ds = session.query(Depense).all()
    session.close()
    return ds

# Modifier (Update)
def modifier_employe(emp_id, data):
    session = Session()
    emp = session.query(Employe).get(emp_id)
    if emp:
        for key, value in data.items():
            setattr(emp, key, value)
        session.commit()
    session.close()

def modifier_budget(budget_id, data):
    session = Session()
    budget = session.query(Budget).get(budget_id)
    if budget:
        for key, value in data.items():
            setattr(budget, key, value)
        session.commit()
    session.close()

def modifier_depense(depense_id, data):
    session = Session()
    depense = session.query(Depense).get(depense_id)
    if depense:
        for key, value in data.items():
            setattr(depense, key, value)
        session.commit()
    session.close()

# Supprimer (Delete)
def supprimer_employe(emp_id):
    session = Session()
    emp = session.query(Employe).get(emp_id)
    if emp:
        session.delete(emp)
        session.commit()
    session.close()

def supprimer_budget(budget_id):
    session = Session()
    budget = session.query(Budget).get(budget_id)
    if budget:
        session.delete(budget)
        session.commit()
    session.close()

def supprimer_depense(depense_id):
    session = Session()
    depense = session.query(Depense).get(depense_id)
    if depense:
        session.delete(depense)
        session.commit()
    session.close()