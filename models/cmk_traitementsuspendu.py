# -*- coding: utf-8 -*-

from odoo import models, fields

class CmkTraitementSuspendu(models.Model):
    _name = 'cmk.traitementsuspendu'
    
    traitement_suspendu = fields.Text(string='Motif de la suspension')
    date_suspension = fields.Date(string='Date de la suspension des traitements')

    patient_suspendu = fields.Many2one('cmk.patient', string="Patient") #c'est le patient