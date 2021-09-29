from odoo import _, api, fields, models, tools


class BOMLineFilter(models.Model):
    _name = 'bom.line.filter'

    active = fields.Boolean("Active")
    name = fields.Char("Name")
    bom_line = fields.Many2one("mrp.bom.line", "BOM Line")
    possible_bom_product_template_attribute_value_ids = fields.Many2many(related="bom_line.possible_bom_product_template_attribute_value_ids")
    apply_on_variants = fields.Many2many("product.template.attribute.value", string="Apply on Variants",
                                         related="bom_line.bom_product_template_attribute_value_ids",
                                         readonly=False,
                                         domain="[('id', 'in', possible_bom_product_template_attribute_value_ids)]")
    attributes = fields.Char("Attributes", compute="_compute_attribute")
    filter = fields.Text("Filter")

    def update(self):
        bl = self.bom_line
        filter = self.filter

        bl['search_filter'] = filter

    @api.depends('bom_line')
    def _compute_attribute(self):
        for record in self:
            record['attributes'] = '\\\\\\'.join(list(
                record.bom_line.mapped('bom_product_template_attribute_value_ids').mapped('display_name')))



class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    def action_filter(self):
        self.env['bom.line.filter'].search([]).unlink()
        new = self.env['bom.line.filter'].create({'bom_line': self.id, 'active': True})
        view = self.env.ref('cap_bom_line_filter.bom_line_filter_form_view')
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'bom.line.filter',
            'res_id': new.id,
            'view_id': view.id,
            'views': [(view.id, 'form')],
            'target': 'new',
        }
