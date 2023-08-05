# -*- coding: utf-8 -*-

"""Command line interface for Bio2BEL InterPro.

Run this script with :code:`python3 -m bio2bel_interpro`.
"""

from .manager import Manager

main = Manager.get_cli()

if __name__ == '__main__':
    main()
