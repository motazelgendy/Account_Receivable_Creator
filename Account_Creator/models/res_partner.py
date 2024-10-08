from odoo import models, fields, api


class partner_account_mapper(models.Model):
    _inherit = 'res.partner'

    def _compute_account_code(self, account_type):
        max_code = self.env['account.account'].search(
            [('account_type', '=', account_type)],
            order='code desc',
            limit=1
        ).mapped('code')

        if max_code[0] in self.env['account.account'].search([('id','!=',False)]).mapped('code'):
            arr = list(str(max_code[0]))
            for num in range(2):
                arr.insert(2,'0')
                account_code = ''.join(arr)
        else:
            account_code = str(int(max_code[0])+1)
        return account_code

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
