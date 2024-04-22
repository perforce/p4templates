#    p4templates - custom tooling to quickly create Helix Core depot/stream/group/permission setups.
#    Copyright (C) 2024 Perforce Software, Inc.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
from argparse import ArgumentParser

from PyQt6.QtWidgets import QApplication

from p4_templates.ui.p4_template_loader_gui import P4TemplateLoaderDialog
from p4_templates.kernel.utils import load_server_config

def main():
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", default="./config.json")
    parser.add_argument("-t", "--template_dir", default="./templates")
    parsed_args = parser.parse_args()

    config_path = parsed_args.config

    if not os.path.exists(config_path):
        print('A valid server configuration file is required')
    else:
        config_path = os.path.abspath(config_path)

    config = load_server_config(config_path)

    if config.get('template_dir', ''):
        template_dir = config.get('template_dir')
    else:
        template_dir = parsed_args.template_dir

    if not os.path.exists(template_dir):
        print('Template directory not found')
    else:
        template_dir = os.path.abspath(template_dir)

    script_dir = os.path.dirname(__file__)
    os.chdir(script_dir)

    app = QApplication([])
    P4TemplateLoaderDialog(
        config_path=config_path,
        template_dir=template_dir
    )


if __name__ == "__main__":
    main()
