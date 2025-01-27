#-*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SceProduct(models.Model):
    _inherit = "product.template"

    puissance = fields.Float(string="Puissance")
    estimation_conso_pac = fields.Integer(string="Estimation Conso PAC")
