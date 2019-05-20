from odoo import models, fields

class CmkContacts(models.Model):
    _inherit = 'res.partner'

    est_patient = fields.Boolean(string='Est un patient')