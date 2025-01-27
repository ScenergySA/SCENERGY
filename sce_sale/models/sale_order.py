# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import json


class SceSaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_default_deduction_tax(self):
        return self.env['sce.tax.deduction'].sudo().search([('is_default', '=', True)], limit=1)

    def _get_default_repurchase_price_id(self):
        return self.env['sce.purchase.price'].sudo().search([('is_default', '=', True), ('type', '=', 'repurchase')],
                                                            limit=1)

    def _get_default_purchase_price_id(self):
        return self.env['sce.purchase.price'].sudo().search([('is_default', '=', True), ('type', '=', 'purchase')],
                                                            limit=1)

    def _get_default_auto_conso_id(self):
        return self.env['sce.auto.consumption'].sudo().search([('is_default', '=', True)], limit=1)

    def _get_default_unit_power_id(self):
        return self.env['sce.unit.puissance'].sudo().search([('is_default', '=', True)], limit=1)

    order_lines = fields.One2many('sale.order.line', 'order_id', string='Order Lines')
    unit_power_id = fields.Many2one('sce.unit.puissance', string="Unit power of the panel in WC",
                                    default=_get_default_unit_power_id)
    nb_panels = fields.Integer(string="Number of pannels")
    total_puissance = fields.Float(string="Total Puissance KWC", compute="compute_total_puissance", store=True)
    orientation_id = fields.Many2one('sce.orientation', string="Orientation")
    theoretical_yield = fields.Float(string="Theoretical Yield", store=True)
    is_multiple = fields.Boolean(string="Is multiple", related="orientation_id.is_multiple", store=True)
    theoretical_yield_2 = fields.Float(string="Theoretical Yield 2")
    annual_production = fields.Float(string="Annual Production Kw/h", compute="compute_annual_production", store=True)
    conso_profile_id = fields.Many2one('sce.conso.profile', string="Conso Profile")
    client_elect_conso = fields.Integer(string="Client Electric Conso Kw/h")
    auto_conso_id = fields.Many2one('sce.auto.consumption', string="Auto Consumption Kw/h",
                                    default=_get_default_auto_conso_id)
    purchase_price_id = fields.Many2one('sce.purchase.price', string="Purchase Price",
                                        domain=[('type', '=', 'purchase')], default=_get_default_purchase_price_id)
    repurchase_price_id = fields.Many2one('sce.purchase.price', string="Repurchase Price",
                                          domain=[('type', '=', 'repurchase')],
                                          default=_get_default_repurchase_price_id)
    auto_consumed = fields.Float(string="Auto Consumed Kw/h", compute="compute_auto_consumed", store=True)
    auto_reinjected = fields.Float(string="Auto Reinjected Kw/h", compute="compute_auto_reinjected", store=True)
    electrical_vehicle = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], string="Electrical Vehicle")
    storage_battery = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], string="Storage Battery")
    pac_piscine = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], string="PAC Piscine")
    climatisation = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], string="Climatisation")
    eco_n1_chf = fields.Float(string="Economie N+1 CHF", compute="compute_eco_n1_chf", store=True)
    installation_cost = fields.Float(string="Installation Cost")
    installation_type_id = fields.Many2one('sce.installation.type', string="Installation Type")
    subvention_pronovo = fields.Float(string="Subvention Pronovo", compute="compute_subvention_pronovo", store=True)
    subvention_communal = fields.Float(string="Subvention Communal")
    deduction_tax_id = fields.Many2one('sce.tax.deduction', string="Deduction Tax", default=_get_default_deduction_tax)
    deduction_tax_amount = fields.Float(string="Deduction Tax Amount", compute="compute_deduction_tax_amount",
                                        store=True)
    deduction_tax_amount_pac = fields.Float(string="Deduction Tax Amount PAC", compute="compute_deduction_tax_amount")
    real_cost = fields.Float(string="Real Cost", compute="compute_real_cost", store=True)
    depreciation_projection_years = fields.Float(string="Depreciation Projection in Years",
                                                 compute="compute_depreciation_projection_years", store=True)
    categ_id = fields.Many2one('product.category', string="Product Category")
    machine_id = fields.Many2one('product.product', string="Machine Type", domain=[('categ_id', '=', categ_id)])
    product_domain = fields.Char(compute="_get_product_domain")
    puissance = fields.Float(string="Puissance", related="machine_id.puissance")
    actual_conso = fields.Integer(string="Actual Consomation Kwh")
    actual_conso_id = fields.Many2one('sce.actual.conso', string="Actual Consomation")
    actual_annual_cost = fields.Float(string="Actual Annual Cost")
    # estimation_conso_pac = fields.Integer(string="Estimation Conso PAC", related="machine_id.estimation_conso_pac")
    estimation_conso_pac = fields.Float(string="Estimation Conso PAC", compute="compute_estimation_conso_pac")
    annual_cost_pac = fields.Float(string="Annual Cost energ. PAC", compute="compute_annual_cost_pac", store=True)
    annual_eco = fields.Float(string="Annual Economie", compute="compute_annual_eco", store=True)
    installation_cost_pac = fields.Float(string="Installation Cost PAC")
    subvention_cantonal_pac = fields.Float(string="Subvention Cantona PAC")
    others_subvention = fields.Float(string="Others Subvention")
    deduction_tax_2 = fields.Many2one('sce.tax.deduction', string="Deduction Tax")
    real_investment_n1 = fields.Float(string="Real Investment N+1", compute="compute_real_investment_n1")
    emission_co2_tonne = fields.Float(string="Emission CO2 Tonnes", compute="compute_emission_co2_tonne", store=True)
    emission_co2_pac = fields.Float(string="Emission CO2 Tonnes", store=True, compute="compute_emission_co2_pac")
    co2_eco_tonne = fields.Float(string="CO2 Eco Annual tonne", compute="compute_co2_eco_tonne", store=True)
    co2_eco_vehicle = fields.Integer(string="CO2 Eco", compute="compute_co2_eco_vehicle", store=True)
    co2_eco_tree = fields.Integer(string="CO2 Eco Tree", compute="compute_co2_eco_tree", store=True)

    # Ajout des champs
    independance_wished = fields.Float(string="Independance Wished", compute="compute_independance_wished")
    distribution_network_group_id = fields.Many2one('distribution.network.group', string="GRD")
    cop_fpa = fields.Float(string="COP / FPA", digits=(12, 2))
    fuel_oil_correspondence = fields.Float(string="Fuel Oil Correspondence", compute="compute_fuel_oil_correspondence")

    current_heating_conso_distribution = fields.Float(string="Current heating consumption distribution",
                                                      compute="compute_current_heating_conso_distribution")
    current_conso_distribution_ecs = fields.Float(string="Current consumption distribution ECS",
                                                  compute="compute_current_conso_distribution_ecs")

    pac_heating_conso_distribution = fields.Float(string="Current heating consumption distribution",
                                                  compute="compute_pac_heating_conso_distribution")
    pac_conso_distribution_ecs = fields.Float(string="Current consumption distribution ECS",
                                              compute="compute_pac_conso_distribution_ecs")

    area = fields.Float("Area", compute="compute_area")
    type_calcul_co2 = fields.Selection([
        ('calcul_pv', 'Calcul selon PV'),
        ('calcul_pac', 'Calcul selon PAC')], string="Type de calcul CO2")

    purchased_electrical = fields.Float(string="Kwh purchased on the electrical network",
                                        compute='compute_independance_wished')

    def _compute_purchased_electrical(self):
        for rec in self:
            rec.purchased_electrical = rec.client_elect_conso - rec.auto_consumed

    @api.depends("auto_consumed", "client_elect_conso")
    def compute_independance_wished(self):
        for r in self:
            r.purchased_electrical = r.client_elect_conso - r.auto_consumed
            r.independance_wished = (r.auto_consumed * 100 / r.client_elect_conso) if r.client_elect_conso \
                                                                                      and r.client_elect_conso > 0 and r.auto_consumed else 0.0

    @api.depends('actual_conso', 'estimation_conso_pac')
    def compute_area(self):
        for r in self:
            r.area = r.actual_conso - r.estimation_conso_pac

    @api.depends('actual_conso', 'actual_conso_id')
    def compute_fuel_oil_correspondence(self):
        for r in self:
            r.fuel_oil_correspondence = (r.actual_conso * 98.73) / 1000 if r.actual_conso and r.actual_conso_id and r.actual_conso_id.type == "mazout" else 0.0

    @api.depends('actual_conso', 'cop_fpa')
    def compute_estimation_conso_pac(self):
        for r in self:
            if r.cop_fpa == 0:
                r.estimation_conso_pac = 0  # set the value to zero
            else:
                r.estimation_conso_pac = r.actual_conso / r.cop_fpa

    @api.depends('actual_conso')
    def compute_current_heating_conso_distribution(self):
        for r in self:
            r.current_heating_conso_distribution = (r.actual_conso * 80) / 100 if r.actual_conso else 0

    @api.depends('actual_conso')
    def compute_current_conso_distribution_ecs(self):
        for r in self:
            r.current_conso_distribution_ecs = (r.actual_conso * 20) / 100 if r.actual_conso else 0

    @api.depends('estimation_conso_pac')
    def compute_pac_heating_conso_distribution(self):
        for r in self:
            r.pac_heating_conso_distribution = (r.estimation_conso_pac * 80) / 100 if r.estimation_conso_pac else 0

    @api.depends('estimation_conso_pac')
    def compute_pac_conso_distribution_ecs(self):
        for r in self:
            r.pac_conso_distribution_ecs = (r.estimation_conso_pac * 20) / 100 if r.estimation_conso_pac else 0

    # End modif added
    @api.depends('estimation_conso_pac', 'actual_conso_id', 'actual_conso_id.value', 'type_calcul_co2')
    def compute_emission_co2_pac(self):
        for rec in self:
            rec.emission_co2_pac = (rec.estimation_conso_pac * 0.133) / 1000

    @api.depends('installation_cost_pac', 'subvention_cantonal_pac', 'others_subvention', 'deduction_tax_2',
                 'deduction_tax_amount_pac')
    def compute_real_investment_n1(self):
        for rec in self:
            rec.real_investment_n1 = (
                rec.installation_cost_pac - rec.subvention_cantonal_pac - rec.others_subvention - rec.deduction_tax_amount_pac)

    @api.depends('co2_eco_tonne')
    def compute_co2_eco_tree(self):
        for rec in self:
            # rec.co2_eco_tree = rec.co2_eco_tonne / 0.0125
            rec.co2_eco_tree = rec.co2_eco_tonne / 0.025

    @api.constrains('is_multiple', 'orientation_id.is_multiple', 'orientation_id', 'orientation_id.theoretical_yield')
    def _check_is_multiple(self):
        for rec in self:
            rec.theoretical_yield = 0
            if not rec.orientation_id.is_multiple:
                rec.theoretical_yield = rec.orientation_id.theoretical_yield

    @api.onchange('is_multiple', 'orientation_id.is_multiple', 'orientation_id', 'orientation_id.theoretical_yield')
    def _onchange_is_multiple(self):
        for rec in self:
            rec.theoretical_yield = 0
            if not rec.is_multiple:
                rec.theoretical_yield = rec.orientation_id.theoretical_yield

    @api.depends('co2_eco_tonne', 'emission_co2_pac')
    def compute_co2_eco_tonne(self):
        for rec in self:
            rec.co2_eco_tonne = rec.emission_co2_tonne - rec.emission_co2_pac

    @api.depends('estimation_conso_pac', 'purchase_price_id', 'purchase_price_id.purchase_price')
    def compute_annual_cost_pac(self):
        for rec in self:
            rec.annual_cost_pac = rec.estimation_conso_pac * rec.purchase_price_id.purchase_price

    @api.depends('annual_cost_pac', 'actual_annual_cost')
    def compute_annual_eco(self):
        for rec in self:
            rec.annual_eco = rec.actual_annual_cost - rec.annual_cost_pac

    @api.onchange('theoretical_yield', 'orientation_id', 'orientation_id.theoretical_yield')
    def onchange_theorical(self):
        for rec in self:
            rec.theoretical_yield_2 = rec.theoretical_yield

    @api.depends('installation_type_id', 'installation_type_id.val1', 'installation_type_id.val2', 'total_puissance')
    def compute_subvention_pronovo(self):
        for rec in self:
            rec.subvention_pronovo = rec.total_puissance * rec.installation_type_id.val1 + rec.installation_type_id.val2

    @api.depends('categ_id')
    def _get_product_domain(self):
        products = self.env['product.template'].search([('categ_id', '=', self.categ_id.id)])
        products = products.product_variant_ids
        self.product_domain = json.dumps([('id', 'in', products.ids)])

    @api.depends('actual_conso', 'actual_conso_id.value', 'actual_conso_id', 'type_calcul_co2',
                 'actual_conso_id.conversion_factor')
    def compute_emission_co2_tonne(self):
        for rec in self:
            if rec.type_calcul_co2 == 'calcul_pv':
                rec.emission_co2_tonne = ((rec.annual_production * 0.443) / 1000)
            else:
                rec.emission_co2_tonne = (rec.actual_conso / (
                    rec.actual_conso_id.conversion_factor if rec.actual_conso_id.conversion_factor != 0.0 else 1) * rec.actual_conso_id.value) / 1000

    @api.depends('co2_eco_tonne')
    def compute_co2_eco_vehicle(self):
        for rec in self:
            rec.co2_eco_vehicle = (rec.co2_eco_tonne * 1000) / 0.15

    # @api.depends('estimation_conso_pac', 'actual_conso_id.value', 'actual_conso_id')
    # def compute_emission_co2_pac(self):
    #     for rec in self:
    #         rec.emission_co2_pac = (rec.estimation_conso_pac * rec.actual_conso_id.value) / 1000

    @api.depends('unit_power_id', 'unit_power_id.unit_power', 'nb_panels')
    def compute_total_puissance(self):
        for rec in self:
            rec.total_puissance = (rec.unit_power_id.unit_power * rec.nb_panels) / 1000

    @api.depends('total_puissance', 'theoretical_yield_2')
    def compute_annual_production(self):
        for rec in self:
            rec.annual_production = rec.total_puissance * rec.theoretical_yield_2

    @api.depends('auto_conso_id', 'auto_conso_id.auto_conso', 'annual_production')
    def compute_auto_consumed(self):
        for rec in self:
            rec.auto_consumed = (int(rec.auto_conso_id.auto_conso) * rec.annual_production) / 100

    @api.depends('deduction_tax_id', 'deduction_tax_id.name', 'subvention_pronovo', 'installation_cost',
                 'subvention_cantonal_pac', 'installation_cost_pac', 'others_subvention', 'deduction_tax_2')
    def compute_deduction_tax_amount(self):
        for rec in self:
            rec.deduction_tax_amount_pac = (
                                                   rec.installation_cost_pac - rec.subvention_cantonal_pac - rec.others_subvention) * rec.deduction_tax_2.name / 100
            rec.deduction_tax_amount = ((
                                                rec.installation_cost - rec.subvention_pronovo) * rec.deduction_tax_id.name) / 100

    @api.depends('auto_consumed', 'annual_production')
    def compute_auto_reinjected(self):
        for rec in self:
            rec.auto_reinjected = rec.annual_production - rec.auto_consumed

    @api.depends('real_cost', 'eco_n1_chf')
    def compute_depreciation_projection_years(self):
        for rec in self:
            depreciation_projection_years = 0
            if rec.eco_n1_chf != 0:
                depreciation_projection_years = (rec.real_cost / rec.eco_n1_chf) - (
                    rec.real_cost / rec.eco_n1_chf * 30 / 100)
            rec.depreciation_projection_years = depreciation_projection_years

    @api.depends('installation_cost', 'subvention_pronovo', 'subvention_communal', 'deduction_tax_amount')
    def compute_real_cost(self):
        for rec in self:
            rec.real_cost = rec.installation_cost - rec.subvention_pronovo - rec.subvention_communal - rec.deduction_tax_amount

    @api.depends('purchase_price_id', 'purchase_price_id.purchase_price', 'auto_consumed', 'repurchase_price_id',
                 'repurchase_price_id.purchase_price', 'auto_reinjected')
    def compute_eco_n1_chf(self):
        for rec in self:
            rec.eco_n1_chf = (rec.purchase_price_id.purchase_price * rec.auto_consumed) + (
                rec.repurchase_price_id.purchase_price * rec.auto_reinjected)
