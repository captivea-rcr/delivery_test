{
    'name': 'Cap BOM Line Filter',
    'version': '1.0',
    'category': 'MRP',
    'summary': 'BOM Line filter Dynamic.',
    'description': """
This module aims to manage BOM Line Filter based on Filter value selected the text is stored on the field with proper 
condition.
==================================================

This module aims to manage BOM Line Filter based on Filter value selected the text is stored on the field with proper 
condition.
       """,
    'website': 'https://www.captivea.us',
    'depends': ['mrp'],
    'data': [
        'security/ir.model.access.csv',
        'views/mrp_bom_line_view.xml',
        'views/bom_line_filter_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
