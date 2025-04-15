# -*- coding: utf-8 -*-
import os
import sys
from utils.config_handler import load_config, save_config
from utils.downloader import download_subtitles, download_video
from ui.options import OptionsWindow
from ui.info import VideoInfoWindow
from i18n import _

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib


class MainWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(
            title=_("BigTube"),
            default_width=800,
            default_height=650,
            **kwargs
        )

        # Carregar configurações
        self.config = load_config()

        # HeaderBar
        header = Adw.HeaderBar()

        # App icon on the left
        app_icon = Gtk.Image.new_from_icon_name("big-webapps")
        app_icon.set_pixel_size(24)
        header.pack_start(app_icon)

        # Botão de Opções
        options_button = Gtk.Button(label=_("Options"))
        options_button.connect("clicked", self.on_options_clicked)
        header.pack_end(options_button)

        # Main Box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        main_box.append(header)

        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content_box.set_margin_start(20)
        content_box.set_margin_end(20)

        # URL TextView
        url_label = Gtk.Label(label=_("Enter Video URLs (one per line):"))
        content_box.append(url_label)

        self.url_textview = Gtk.TextView()
        self.url_textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.url_textview.set_size_request(-1, 100)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_child(self.url_textview)
        content_box.append(scrolled_window)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        button_box.set_halign(Gtk.Align(3))

        # Download Button
        download_button = Gtk.Button(label=_("Download"))
        download_button.connect("clicked", self.on_download_clicked)
        download_button.add_css_class("suggested-action")
        button_box.append(download_button)
        content_box.append(button_box)

        self.spinner = Gtk.Spinner()
        content_box.append(self.spinner)
        main_box.append(content_box)

        self.set_content(main_box)

    def on_options_clicked(self, button):
        options_window = OptionsWindow(parent_window=self, config=self.config)
        options_window.present()

    def on_download_clicked(self, button):
        # Obter URLs do TextView
        buffer = self.url_textview.get_buffer()
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_end_iter()
        text = buffer.get_text(start_iter, end_iter, False)

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
            # Reset status and start spinner
            # self.spinner.start()

            # Execute download in a separate thread to avoid blocking the UI
            # download_video(url, download_dir, default_format)
            VideoInfoWindow(url)


class BigTubeApp(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="org.biglinux.BigTube",
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        win = MainWindow(application=app)
        win.present()


if __name__ == "__main__":
    app = BigTubeApp()
    app.run(sys.argv)
