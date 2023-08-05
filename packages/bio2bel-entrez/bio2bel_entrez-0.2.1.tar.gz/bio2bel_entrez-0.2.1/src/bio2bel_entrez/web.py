# -*- coding: utf-8 -*-

"""Build a WSGI application for Bio2BEL Entrez.

This module builds a :mod:`Flask` application for interacting with the underlying database. When installing,
use the web extra like:

.. source-code:: sh

    pip install bio2bel_entrez[web]
"""

from .manager import Manager

manager = Manager()
app = manager.get_flask_admin_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
