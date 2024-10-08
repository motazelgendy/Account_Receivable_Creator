from odoo import models, fields, api


class partner_account_mapper(models.Model):
    _inherit = 'res.partner'

    def _compute_account_code(self, account_type):
       chart_code = self.env['account.account'].search([('account_type','=',account_type)]).mapped('code')
       account_code = max([eval(code) for code in chart_code]) + 1
       print(account_code)
       if str(account_code) in self.env['account.account'].search([('id','!=',False)]).mapped('code'):
            arr = list(str(account_code))
            for i in range(1):
                 arr.insert(5,'0')
            account_code = ''.join(arr)
       return  str(account_code)

    @api.model
    def create(self, vals):
        account_type = 'liability_payable' if 'supplier_rank' in vals.keys() else 'asset_receivable'
        account_code = self._compute_account_code(account_type)

        account_id = self.env['account.account'].create(
            {'code': account_code, 'name': vals['name'], 'account_type': account_type}
        )

        if account_type == 'liability_payable':
            vals['property_account_payable_id'] = account_id
        else:
            vals['property_account_receivable_id'] = account_id

        return super().create(vals)
