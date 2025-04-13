# -*- coding: utf-8 -*-
import os
from utils.config_handler import load_config, save_config
from utils.downloader import download_subtitles, download_video
from ui.options import OptionsWindow
from i18n import _

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title(_("BigTube"))
        self.set_default_size(800, 600)

        # Carregar configurações
        self.config = load_config()

        # HeaderBar
        header = Adw.HeaderBar()
        self.set_titlebar(header)

        # Botão de Opções
        options_button = Gtk.Button(label=_("Options"))
        options_button.connect("clicked", self.on_options_clicked)
        header.pack_start(options_button)

        # Main Box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_child(main_box)

        # URL TextView
        url_label = Gtk.Label(label=_("Enter Video URLs (one per line):"))
        main_box.append(url_label)

        self.url_textview = Gtk.TextView()
        self.url_textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.url_textview.set_size_request(-1, 100)
        main_box.append(self.url_textview)

        # Download Button
        download_button = Gtk.Button(label=_("Download"))
        download_button.connect("clicked", self.on_download_clicked)
        main_box.append(download_button)

    def on_options_clicked(self, button):
        options_window = OptionsWindow(parent_window=self, config=self.config)
        options_window.present()

    def on_download_clicked(self, button):
        # Obter URLs do TextView
        buffer = self.url_textview.get_buffer()
        text = buffer.get_text(
            buffer.get_start_iter(),
            buffer.get_end_iter(),
            False
        )
        urls = [url.strip() for url in text.splitlines() if url.strip()]

        if not urls:
            print(_("Please enter at least one valid URL."))
            return

        download_dir = self.config.get("download_dir", ".")
        default_format = self.config.get("default_format", "mp4")

        for url in urls:
            print(f"Processing URL: {url}")
            print(f"Destination folder: {download_dir}")
            print(f"Selected format: {default_format}")

            # Simular download (substitua isso pela lógica real de download)
            print(f"Downloading video from: {url}")
            download_video(url, download_dir, default_format)


class BigTubeApp(Adw.Application):
    def __init__(self, app_id):
        super().__init__(application_id=app_id)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        win = MainWindow(app)
        win.present()


if __name__ == "__main__":
    app = BigTubeApp("org.biglinux.tube")
    app.run(None)
