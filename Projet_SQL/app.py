import os
from flask import Flask, render_template, request, url_for, redirect # Ils nous permettent de rediriger l'utilisateur après un POST
import sqlite3

app = Flask(__name__)

def envoie_requete(req):
    conn = sqlite3.connect(r"C:\Users\mbowm\OneDrive\Dokumente\projet\NSI\Projet\ProjetNSI/SF.db")
    cur = conn.cursor()
    cur.execute(req) 
    result = cur.fetchall()  
    conn.commit()  
    cur.close()  
    conn.close()  
    return result

@app.route('/ajouter_pilote', methods=['GET', 'POST'])
def ajouter_pilote():
    """
    Route pour ajouter un nouveau pilote.
    - Affiche le formulaire pour ajouter un pilote si la méthode est GET.
    - Ajoute le pilote à la base de données si la méthode est POST.
    """
    if request.method == 'GET':
        return render_template('ajouter_pilote.html') 
    elif request.method == 'POST':
        # Récupération des données du formulaire
        nom = request.form['nom']
        prénom = request.form['prénom']
        nationalite = request.form['nationalite']
        date_naissance = request.form['date_naissance']  
        
        # Requête SQL pour insérer un nouveau pilote
        requete_sql = f"""INSERT INTO pilote (nom, prénom, nationalite, date_naissance)
                          VALUES ('{nom}', '{prénom}', '{nationalite}', '{date_naissance}')"""
        envoie_requete(requete_sql)
        return redirect(url_for('pilote'))  # Redirection vers la page des pilotes pour voir si la pilote a été ajouté

@app.route('/ajouter_gp', methods=['GET', 'POST'])
def ajouter_gp():
    """
    Route pour ajouter un nouveau grand prix.
    - Affiche le formulaire pour ajouter un gp si la méthode est GET.
    - Ajoute le gp à la base de données si la méthode est POST.
    """
    if request.method == 'GET':
        return render_template('ajouter_gp.html') 
    elif request.method == 'POST':
        # Récupération des données du formulaire
        nom = request.form['nom']
        date = request.form['date']
        CIRCUIT = request.form['CIRCUIT']  
        
        # Requête SQL pour insérer un nouveau pilote
        requete_sql = f"""INSERT INTO gp (nom, date, id_circuit)
                          VALUES ('{nom}',  '{date}', '{CIRCUIT}')"""
        envoie_requete(requete_sql)
        return redirect(url_for('grand_prix'))  # Redirection vers la page des gp pour voir si la gp a été ajouté



@app.route('/modifier_ecurie', methods=['GET', 'POST'])
def modifier_ecurie():
    """
    Route pour modifier les informations d'une écurie.
    - Affiche le formulaire de modification si la méthode est GET.
    - Met à jour les informations de l'écurie dans la base de données si la méthode est POST.
    """
    if request.method == 'GET':
        requete_sql = 'SELECT * FROM écurie'
        result = envoie_requete(requete_sql)  # Récupération des données des écuries pour choisir laquelle modifier
        return render_template('modifier_ecurie.html', data=result)
    elif request.method == 'POST':
        # Récupération des données modifiées du formulaire
        id_écurie = request.form['id_écurie']
        nom = request.form['nom']
        nationalité = request.form['nationalité']
        date_creation = request.form['date_creation']
        
        # Requête SQL pour mettre à jour l'écurie
        requete_sql = f"""UPDATE écurie SET nom = '{nom}', nationalité = '{nationalité}', date_création = '{date_creation}' WHERE id_ecurie = '{id_écurie}'"""
        envoie_requete(requete_sql)
        
        return redirect(url_for('ecurie'))  # Redirection vers la page des écuries pour voir la modification

@app.route('/modifier_participation', methods=['GET', 'POST'])
def modifier_participation():
    """
    Route pour modifier les informations de participation d'un pilote à un Grand Prix.
    - Affiche le formulaire pour modifier les participations si la méthode est GET.
    - Met à jour les informations de participation dans la base de données si la méthode est POST.
    """
    if request.method == 'GET':
        # Requête pour récupérer les participations existantes
        participations = envoie_requete("""
            SELECT participe.id, pilote.nom, pilote.prénom, gp.nom, participe.temps, participe.position
            FROM participe
            JOIN pilote ON participe.id_pilote = pilote.id_pilote
            JOIN gp ON participe.id_gp = gp.id_gp
        """)    
        pilotes = envoie_requete("SELECT id_pilote, nom, prénom FROM pilote")
        gps = envoie_requete("SELECT id_gp, nom FROM gp")
        
        # Affichage du formulaire avec les données existantes
        return render_template('modifier_participation.html', participations=participations, pilotes=pilotes, gps=gps)
    elif request.method == 'POST':
        # Récupération des données du formulaire pour la mise à jour
        participation_id = request.form['participation_id']
        id_pilote = request.form['id_pilote']
        id_gp = request.form['id_gp']
        temps = request.form['temps']
        position = request.form['position']

        # Requête SQL pour mettre à jour la participation
        requete_sql = f"""
            UPDATE participe 
            SET id_pilote = '{id_pilote}', id_gp = '{id_gp}', temps = '{temps}', position = '{position}' 
            WHERE id = '{participation_id}'
        """
        envoie_requete(requete_sql)

        return redirect(url_for('participe'))  # Redirection vers la page des participations

@app.route('/')
def index():
    """Route pour la page d'accueil."""
    return render_template('index.html')

@app.route('/pilote')
def pilote():
    """Route pour afficher la liste des pilotes."""
    requete_sql = 'SELECT * FROM pilote'
    result = envoie_requete(requete_sql)
    return render_template('pilote.html', data=result)

@app.route('/ecurie')
def ecurie():
    """Route pour afficher la liste des écuries."""
    requete_sql = 'SELECT * FROM écurie'
    result = envoie_requete(requete_sql)
    return render_template('ecurie.html', data=result)

@app.route('/circuit')
def circuit():
    """Route pour afficher la liste des circuits."""
    requete_sql = 'SELECT * FROM circuit'
    result = envoie_requete(requete_sql)
    return render_template('circuit.html', data=result)

@app.route('/gp')
def grand_prix():
    """Route pour afficher la liste des Grands Prix."""
    requete_sql = 'SELECT circuit.nom, gp.*'
    requete_sql += 'FROM gp '
    requete_sql += 'JOIN circuit ON circuit.id_circuit = gp.id_circuit'
    result = envoie_requete(requete_sql)
    return render_template('gp.html', data=result)

@app.route('/fait_partie')
def fait_partie():
    """Route pour afficher la liste des faits parties (relation entre pilotes et écuries selon les saisons)."""
    requete_sql = 'SELECT pilote.nom, pilote.prénom, écurie.nom, fait_partie.saison ' 
    requete_sql += 'FROM fait_partie '
    requete_sql += 'JOIN pilote ON pilote.id_pilote = fait_partie.id_pilote ' 
    requete_sql += 'JOIN écurie ON écurie.id_écurie = fait_partie.id_écurie'
    result = envoie_requete(requete_sql)
    return render_template('fait_partie.html', data=result)

@app.route('/participe')
def participe():
    """Route pour afficher la liste des participations des pilotes aux Grands Prix."""
    requete_sql = 'SELECT pilote.nom, pilote.prénom, gp.nom, participe.position, participe.temps '
    requete_sql += 'FROM participe '
    requete_sql += 'JOIN pilote ON pilote.id_pilote = participe.id_pilote ' 
    requete_sql += 'JOIN gp ON gp.id_gp = participe.id_gp'
    result = envoie_requete(requete_sql)
    return render_template('participe.html', data=result)

@app.route('/gagnant')
def resultats():
    """
    Route pour afficher les résultats des pilotes qui ont gagné des Grands Prix.
    Affiche les informations des pilotes, les temps de course, le nom et la date du GP.
    """
    requete_sql = """
        SELECT pilote.nom, pilote.prénom, participe.temps, gp.nom, gp.date 
        FROM pilote 
        JOIN participe ON pilote.id_pilote = participe.id_pilote
        JOIN gp ON participe.id_gp = gp.id_gp
        WHERE participe.position = 1;
    """
    resultats = envoie_requete(requete_sql)
    return render_template('gagnant.html', data=resultats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
