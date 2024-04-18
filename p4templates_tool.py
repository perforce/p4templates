import os
from argparse import ArgumentParser

from PyQt6.QtWidgets import QApplication

from p4templates.ui.p4_template_loader_gui import P4TemplateLoaderDialog
from p4templates.kernel.utils import load_server_config

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
    