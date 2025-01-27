#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class SceUnitPuissance(models.Model):
    _name = 'sce.unit.puissance'
    _description = 'Unit Puissance'
    _rec_name = 'unit_power'

    _sql_constraints = [
        ('unit_power_uniq', 'unique(unit_power)', _('Unit Power should be unique.')),
    ]

    unit_power = fields.Integer(string="Unit power of the panel in WC", required=True)
    is_default = fields.Boolean(string="Is default")

class SceConsoProfile(models.Model):
    _name = 'sce.conso.profile'
    _description = 'Conso Profile'
    _rec_name = 'name'

    _sql_constraints = [
        ('note_uniq', 'unique(name)', _('Name should be unique.')),
    ]

    name = fields.Char(string="Conso Profile", required=True)

class SceAutoConsumption(models.Model):
    _name = 'sce.auto.consumption'
    _description = 'Auto Consumption'
    _rec_name = 'auto_conso'

    _sql_constraints = [
        ('auto_conso_uniq', 'unique(auto_conso)', _('Auto Consumption should be unique.')),
    ]

    auto_conso = fields.Integer(string="Auto Consumption", required=True)
    is_default = fields.Boolean(string="Is default")

class SceOrientationName(models.Model):
    _name = 'sce.orientation.name'
    _description = 'Orientation'
    _rec_name = 'orientation'

    _sql_constraints = [
        ('orientation_uniq', 'unique(orientation)', _('Orientation should be unique.')),
    ]

    orientation = fields.Char(string="Orientation", required=True)

class SceOrientation(models.Model):
    _name = 'sce.orientation'
    _description = 'Orientation'
    _rec_name = 'orientation_id'

    _sql_constraints = [
        ('orientation_uniq', 'unique(orientation_id)', _('Orientation should be unique.')),
    ]

    orientation_id = fields.Many2one('sce.orientation.name', string="Orientation", required=True)
    is_multiple = fields.Boolean(string="Is multiple")
    theoretical_yield = fields.Float(string="Theoretical Yield")

class ScePurchasePrice(models.Model):
    _name = 'sce.purchase.price'
    _description = 'Purchase Price'
    _rec_name = 'purchase_price'

    _sql_constraints = [
        ('purchase_price_uniq', 'unique(purchase_price, type)', _('Auto Consumption should be unique.')),
    ]

    purchase_price = fields.Float(string="Purchase/Repurchase Price", required=True)
    type = fields.Selection([
        ('purchase', 'Purchase'),
        ('repurchase', 'Repurchase')],string="Type", required=True)
    is_default = fields.Boolean(string="Is default")

class SceMachine(models.Model):
    _name = 'sce.machine'
    _description = 'Machine'
    _rec_name = 'name'

    _sql_constraints = [
        ('name_uniq', 'unique(name)', _('Machine Type should be unique.')),
    ]

    name = fields.Char(string="Machine Type", required=True)
    puissance = fields.Float(string="Puissance", required=True)
    estimation_conso_pac = fields.Float(string="Estimation Conso PAC")

class SceInstallation(models.Model):
    _name = 'sce.installation.type'
    _description = 'Installation'
    _rec_name = 'name'

    _sql_constraints = [
        ('name_uniq', 'unique(name)', _('Installation type Type should be unique.')),
    ]

    name = fields.Char(string="Installation Type", required=True)
    val1 = fields.Float(string="Bareme Subvention 1")
    val2 = fields.Float(string="Bareme Subvention 2")

class SceTaxDeduction(models.Model):
    _name = 'sce.tax.deduction'
    _description = 'Tax Deduction'
    _rec_name = 'name_str'

    _sql_constraints = [
        ('name_uniq', 'unique(name)', _('Tax Deduction should be unique.')),
    ]

    name = fields.Float(string="Tax Deduction", required=True)
    name_str = fields.Char(string="Tax Deduction", compute='compute_name_str')
    is_default = fields.Boolean(string="Is default")

    @api.depends('name')
    def compute_name_str(self):
        for rec in self:
            rec.name_str = str(rec.name)



class SceTActualConso(models.Model):
    _name = 'sce.actual.conso'
    _description = 'Actual Conso'
    _rec_name = 'name'

    _sql_constraints = [
        ('name_uniq', 'unique(name)', _('Actual Conso should be unique.')),
    ]

    name = fields.Char(string="Actual Conso", required=True)
    type = fields.Selection([
        ('gaz', 'Gaz'),
        ('mazout', 'Mazout'),
        ('electricity', 'electricity'),
        ('pellet', 'Pellet')], string="Type", required=True)
    value = fields.Float(string="Emission Value", required=True, digits=(16, 3))
    conversion_factor = fields.Float(string="Conversion Factor", default=1)


