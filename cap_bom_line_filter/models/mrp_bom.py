from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError, RedirectWarning, UserError


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    search_filter = fields.Text(string="Search", compute='_compute_search', store=True, readonly=False)
    search_eval = fields.Text(string="Search Eval", compute='_compute_search_eval', store=True, readonly=True)

    @api.depends('bom_product_template_attribute_value_ids')
    def _compute_search(self):
        for record in self:
            if not record: continue
            s = ''
            if len(record.bom_product_template_attribute_value_ids):
                for attr in record.bom_product_template_attribute_value_ids[:-1]:
                    s += attr.attribute_id.name + ': ' + attr.name + ' | '
                attr = record.bom_product_template_attribute_value_ids[-1]
                s += attr.attribute_id.name + ': ' + attr.name
            record.search_filter = s

    @api.depends('search_filter')
    def _compute_search_eval(self):
        for record in self:
            if not record: continue
            record.search_eval = ''
            if record.search_filter:
                s = record.search_filter
                for attr in record.bom_product_template_attribute_value_ids:
                    name = attr.attribute_id.name + ': ' + attr.name
                    s = s.replace(name, str(attr._origin.id))
                try:
                    eval(s)
                    record.search_eval = s
                except Exception as e:
                    raise UserError(_(str(e)))

    def _skip_bom_line(self, product):
        """ Control if a BoM line should be produced, can be inherited to add
        custom control. It currently checks that all variant values are in the
        product.

        If multiple values are encoded for the same attribute line, only one of
        them has to be found on the variant.
        """
        self.ensure_one()
        if product._name == 'product.template':
            return False
        s = self.search_eval
        if s:
            s = s.replace('|', 'or')
            s = s.replace('&', 'and')
            for id in sorted(self.bom_product_template_attribute_value_ids.ids, reverse=True):
                s = s.replace(str(id), str(id) + ' in ' + str(list(product.product_template_attribute_value_ids.ids)))

            return not bool(eval(s))

        return False
