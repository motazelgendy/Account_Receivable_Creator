# -*- coding: utf-8 -*-

from odoo import models, fields, api


class account_creator(models.Model):
    _inherit = 'res.partner'

    def _compute_account_code(self,account_type):
       chart_code = self.env['account.account'].search([('account_type','=',account_type)]).mapped('code')
       account_code = max([eval(code) for code in chart_code]) + 1
       print(account_code)
       if str(account_code) in self.env['account.account'].search([('id','!=',False)]).mapped('code'):
            arr = list(str(account_code))
            for i in range(2):
                 arr.insert(2,'0')
            account_code = ''.join(arr)
       return  str(account_code)
              
                        
    @api.model
    def create(self, vals):
         if 'supplier_rank' in vals.keys():
               account_id = self.env['account.account'].create(
                   {'code':self._compute_account_code('liability_payable'),'name':vals['name'],'account_type': 'liability_payable'})
               vals['property_account_payable_id'] = account_id
         else:
                account_id = self.env['account.account'].create(
                     {'code':self._compute_account_code('asset_receivable'),'name':vals['name'],'account_type': 'asset_receivable'})
                vals['property_account_receivable_id'] = account_id

         partner_id = super().create(vals)
         return partner_id




        