--- ROLES ---
INSERT INTO role (libelle) VALUES
('Administrateur'),
('employé'),
('Client');

--- THEMES ---
INSERT INTO theme (libelle) VALUES
('Mariage'),
('Anniversaire'),
('Baptême'),
('Communion'),
('Fête familiale'),
('Réunion professionnelle'),
('Séminaire'),
('Cocktail d''entreprise'),
('Inauguration'),
('Soirée privée'),
('Buffet créole'),
('Barbecue'),
('Repas de fin d''année'),
('Saint-Valentin'),
('Noël'),
('Nouvel An');

--- REGIMES---
INSERT INTO regime (libelle) VALUES
('Standard'),
('Végétarien'),
('Végétalien'),
('Sans gluten'),
('Sans lactose'),
('Halal');

--- TYPES DE PLATS ---
INSERT INTO type_plat (libelle) VALUES
('Entrée'),
('Plat principal'),
('Accompagnement'),
('Dessert'),
('Boisson');

--- ALLERGENES ---
INSERT INTO allergene (libelle) VALUES
('Gluten'),
('Crustacés'),
('Œufs'),
('Poissons'),
('Arachides'),
('Soja'),
('Lait'),
('Fruits à coque'),
('Céleri'),
('Moutarde'),
('Graines de sésame'),
('Sulfites'),
('Lupin'),
('Mollusques');

--- HORAIRES D'OUVERTURE ---
INSERT INTO horaire (
    jour,
    heure_ouverture,
    heure_fermeture,
    ferme
) VALUES
('Lundi', '08:00', '18:00', FALSE),
('Mardi', '08:00', '18:00', FALSE),
('Mercredi', '08:00', '18:00', FALSE),
('Jeudi', '08:00', '18:00', FALSE),
('Vendredi', '08:00', '18:00', FALSE),
('Samedi', '08:00', '16:00', FALSE),
('Dimanche', NULL, NULL, TRUE);

--- COMPTE ADMINISTRATEUR ---
INSERT INTO utilisateur (
    email,
    mot_de_passe,
    nom,
    prenom,
    telephone,
    adresse_postale,
    actif,
    created_at,
    role_id
) VALUES (
    'admin@traiteur.re',
    '$2b$12$fwmnutzd2PjlcxeF0E5lOupy1Om4CN.c2OHgLcnCs8crLCePMbGLy',
    'Admin',
    'Super',
    '0692000000',
    'Saint-Denis',
    TRUE,
    CURRENT_TIMESTAMP,
    1
);