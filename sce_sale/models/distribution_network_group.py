#-*- coding: utf-8 -*-

from odoo import models, fields, api, _


class DistributionNetworkGroup(models.Model):
    _name = "distribution.network.group"

    name = fields.Char('Name', required=True)

