# -*- coding: utf-8 -*-

from ast import literal_eval
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _

CHAMPS_ADRESSES = ('adresse_rue', 'adresse_ville', 'adresse_pays', 'adresse_postal')

class CmkPatient(models.Model):
    _name = 'cmk.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    #_inherit = 'res.partner'
    #_rec_name = 'patient'
    _description = 'Patient'

    #formulaire
    patient_name = fields.Many2one(
        'res.partner', string='Nom du Patient', required=True)
        #code patient (identifiant) généré automatiquement pour le patient
    id_patient = fields.Char(string='Numéro d\'identification', size=16, readonly=True,
        help="Code patient (identifiant) généré automatiquement", default=lambda *a: 'PATXXXX')
    #name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    photo_patient = fields.Binary(string='Photo')
    name = fields.Char(string='Prénom', required=True)#prenom
    state = fields.Selection( [
        ('nouveau_client', 'Nouveau client'),
        ('prescriptionV', 'Prescription validée'),
        ('patient_en_traitement', 'Patient en cours de traitement'),
        ('patient_terminé', 'Patient ayant terminé')
    ], string='Statut du patient', default='nouveau_client', readonly=True, copy=False, index=True, track_visibility='onchange')
    state_annule = fields.Selection( [
        ('annuler_prescription', 'Annuler prescription'),
        ('annuler_traitement', 'Annuler traitement')
    ], string='Annuler boutons', readonly=True, copy=False, index=True, track_visibility='onchange')
    titre = fields.Selection([
         ('M.', 'Monsieur'), ('Mme', 'Madame'),
         ('Mlle', 'Mademoiselle'), ('Vve', 'Veuve'),
    ], string='Titre', required=True)
    genre = fields.Selection( [
        ('H', 'Homme'), ('F', 'Femme')
    ], string='Genre', required=True)
    date_naissance = fields.Date(string='Date de naissance', required=True)
    age = fields.Char(string='Age', compute='compute_age')
    date = fields.Datetime(string='Date Requested', default=lambda s: fields.Datetime.now(), invisible=True)
    kine_assigne = fields.Many2one('hr.employee', string='Kiné traitant')
    # pathologie = fields.Many2many('cmk.pathologie', string='Pathologies')
    product_id = fields.Many2many('product.product', string='Pathologies', index=True)
    suivi_traitement = fields.One2many('cmk.traitement', 'patient_traitement')
    traitement_suspendu_tree = fields.One2many('cmk.traitementsuspendu', 'patient_suspendu')
    traitement_suspendu_radio = fields.Selection([
        ('actif', 'Patient actif'), ('suspendu', 'Patient suspendu')
    ], string='Etat du patient', default='actif')
    #Fin formulaire

    #Notebook
    adresse_rue = fields.Char(string='Rue', size=128)
    adresse_ville = fields.Char(String='Ville', size=128, required=True)
    adresse_pays = fields.Many2one('res.country', string='Pays', ondelete='restrict')
    adresse_postal = fields.Char(string='Code postal')
    telephone = fields.Char(string='Téléphone', required=True)
    email = fields.Char(string='Email', required=True)
    note = fields.Text(string='Diagnostic')
    company_name = fields.Char('Company Name')
    note_kine = fields.Char()
    note_docteur = fields.Text()
    note_administration = fields.Text()
    societe_patient = fields.Many2one('res.partner', string='Société', index=True)
    # type_societe = fields.Selection([
    #     ('IPM', 'IPM'), ('Assurance', 'Assurance')
    # ], string='Type de la société')

    fichier_prescription = fields.Many2many('ir.attachment',string='Ajouter prescription')
    fichier_assurance = fields.Many2many('ir.attachment',string='Ajouter assurance')
    fichier_rapport = fields.Many2many('ir.attachment',string='Ajouter rapport')
    #Fin notebook

    #api pour créer de manière automatique le code patient : "PATXXX"
    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('cmk.patient')
        vals['id_patient'] = sequence or '/'
        return super(CmkPatient, self).create(vals)

    #api pour calculer l'age à partir de la date de naissance et de la date actuelle
    @api.multi
    def compute_age(self):
        for data in self:
            if data.date_naissance:
                date_naissance = fields.Datetime.from_string(data.date_naissance)
                date = fields.Datetime.from_string(data.date)
                delta = relativedelta(date, date_naissance)
            data.age = str(delta.years) + ' ans'

    #api pour le formatage de l'adresse en un groupe : adresse_rue, adresse_ville, adresse_pays, adresse_postal
    @api.model
    def _get_default_address_formatage(self):
        return "%(adresse_rue)s\n%(adresse_ville)s\n%(adresse_pays)s %(adresse_postal)s"

    # #Fonctions du status bar
    # @api.multi
    # def valide_prescription_progressbar(self):
    #     return self.write({'state': 'prescriptionV'})

    # @api.multi
    # def traitement_en_cours_progressbar(self):
    #     return self.write({'state': 'patient_en_traitement'})

    # @api.multi
    # def termine_progressbar(self):
    #     return self.write({'state': 'patient_terminé'})

    # @api.multi
    # def annuler_prescription_progessbar(self):
    #     return self.write({'state': 'nouveau_client'})

    # @api.multi
    # def annuler_traitement_progessbar(self):
    #     return self.write({'state': 'prescriptionV'})
    # #Fin Fonctions du status bar