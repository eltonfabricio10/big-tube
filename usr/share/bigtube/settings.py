# -*- coding: utf-8 -*-
"""
Gerenciamento de configurações para o aplicativo
"""
import os
import json
from pathlib import Path

class Settings:
    """Gerencia as configurações do aplicativo"""

    def __init__(self):
        # Configurações padrão
        self.defaults = {
            'download_dir': str(Path.home() / "Downloads"),
            'default_format': "mp4",
            'preferred_player': "",
            'notify_sound': True,
            'max_downloads': 3,
            'keep_history': True,
            'dark_mode': True,
            'remember_window_size': True,
            'window_width': 800,
            'window_height': 600,
            'autostart_download': True,
            'preview_thumbnail': True,
            'save_location_remember': True,
            'always_ask_location': False,
            'close_to_tray': False,
            'language': "auto"
        }

        # Caminho para o arquivo de configuração
        self.config_dir = os.path.join(os.path.expanduser("~"), ".config", "bigtube")
        self.config_file = os.path.join(self.config_dir, "settings.json")

        # Configurações atuais
        self.config = self.defaults.copy()

        # Carregar configurações salvas
        self.load()

    def __getitem__(self, key):
        return self.config.get(key)

    def __setitem__(self, key, value):
        self.config[key] = value

    def load(self):
        """Carrega as configurações do arquivo"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    # Atualiza as configurações com os valores carregados
                    self.config.update(loaded_config)
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")

    def save(self):
        """Salva as configurações no arquivo"""
        try:
            # Garante que o diretório existe
            os.makedirs(self.config_dir, exist_ok=True)

            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)

            return True
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
            return False

    def get(self, key, default=None):
        """Obtém um valor de configuração"""
        return self.config.get(key, default)

    def set(self, key, value):
        """Define um valor de configuração"""
        self.config[key] = value

    def reset(self):
        """Redefine todas as configurações para os valores padrão"""
        self.config = self.defaults.copy()

    def reset_key(self, key):
        """Redefine uma configuração específica para o valor padrão"""
        if key in self.defaults:
            self.config[key] = self.defaults[key]
