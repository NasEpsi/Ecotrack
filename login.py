import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

class GestionComptesUtilisateurs(QWidget):
    def __init__(self):
        super().__init__()

        self.comptes_utilisateurs = {}

        self.setWindowTitle("Gestion des Comptes Utilisateurs")
        self.setGeometry(300, 300, 400, 300)

        self.label_nom_utilisateur = QLabel("Nom d'utilisateur:")
        self.edit_nom_utilisateur = QLineEdit(self)

        self.label_mot_de_passe = QLabel("Mot de passe:")
        self.edit_mot_de_passe = QLineEdit(self)
        self.edit_mot_de_passe.setEchoMode(QLineEdit.Password)

        self.label_nom = QLabel("Nom:")
        self.edit_nom = QLineEdit(self)

        self.label_prenom = QLabel("Prénom:")
        self.edit_prenom = QLineEdit(self)

        self.label_age = QLabel("Âge:")
        self.edit_age = QLineEdit(self)

        self.label_email = QLabel("Email:")
        self.edit_email = QLineEdit(self)

        self.bouton_creer_compte = QPushButton("Créer un compte", self)
        self.bouton_afficher_profil = QPushButton("Afficher le profil", self)

        self.bouton_creer_compte.clicked.connect(self.creer_compte)
        self.bouton_afficher_profil.clicked.connect(self.afficher_profil)

        layout = QVBoxLayout()
        layout.addWidget(self.label_nom_utilisateur)
        layout.addWidget(self.edit_nom_utilisateur)
        layout.addWidget(self.label_mot_de_passe)
        layout.addWidget(self.edit_mot_de_passe)
        layout.addWidget(self.label_nom)
        layout.addWidget(self.edit_nom)
        layout.addWidget(self.label_prenom)
        layout.addWidget(self.edit_prenom)
        layout.addWidget(self.label_age)
        layout.addWidget(self.edit_age)
        layout.addWidget(self.label_email)
        layout.addWidget(self.edit_email)
        layout.addWidget(self.bouton_creer_compte)
        layout.addWidget(self.bouton_afficher_profil)

        self.setLayout(layout)

    def creer_compte(self):
        nom_utilisateur = self.edit_nom_utilisateur.text()
        mot_de_passe = self.edit_mot_de_passe.text()
        profil_utilisateur = {
            'Nom': self.edit_nom.text(),
            'Prénom': self.edit_prenom.text(),
            'Âge': self.edit_age.text(),
            'Email': self.edit_email.text(),
        }
        self.comptes_utilisateurs[nom_utilisateur] = {'Mot de passe': mot_de_passe, 'Profil': profil_utilisateur}
        QMessageBox.information(self, 'Succès', f'Le compte utilisateur {nom_utilisateur} a été créé avec succès.')

    def afficher_profil(self):
        nom_utilisateur = self.edit_nom_utilisateur.text()
        if nom_utilisateur in self.comptes_utilisateurs:
            profil_utilisateur = self.comptes_utilisateurs[nom_utilisateur]['Profil']
            profil_texte = f"\nProfil de {nom_utilisateur}:\n"
            for cle, valeur in profil_utilisateur.items():
                profil_texte += f"{cle}: {valeur}\n"
            QMessageBox.information(self, 'Profil Utilisateur', profil_texte)
        else:
            QMessageBox.warning(self, 'Erreur', f'Le compte utilisateur {nom_utilisateur} n\'existe pas.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fenetre = GestionComptesUtilisateurs()
    fenetre.show()
    sys.exit(app.exec_())
