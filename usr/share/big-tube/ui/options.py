# -*- coding: utf-8 -*-
from i18n import _
import gi
gi.require_version('Gtk', '4.0')

from gi.repository import Gtk


class OptionsWindow(Gtk.Window):
    def __init__(self, parent_window, config):
        super().__init__()
        self.set_title(_("Options"))
        self.set_default_size(400, 300)
        self.set_modal(True)
        self.set_transient_for(parent_window)

        self.config = config

        # Main Box
        main_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10
        )
        self.set_child(main_box)

        # Pasta Padrão
        folder_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=10
        )
        main_box.append(folder_box)

        folder_label = Gtk.Label(label=_("Download Directory:"))
        folder_box.append(folder_label)

        self.folder_entry = Gtk.Entry()
        self.folder_entry.set_text(self.config.get("download_dir", ""))
        folder_box.append(self.folder_entry)

        select_folder_button = Gtk.Button(label=_("Select Folder"))
        select_folder_button.connect("clicked", self.on_select_folder_clicked)
        folder_box.append(select_folder_button)

        # Formato Padrão
        format_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=10
        )
        main_box.append(format_box)

        format_label = Gtk.Label(label=_("Default Format:"))
        format_box.append(format_label)

        # Usar Gtk.DropDown com Gtk.StringList
        video_formats = ["mp4", "mkv", "avi", "mov", "flv"]
        audio_formats = ["mp3", "aac", "ogg", "wav", "flac"]
        self.all_formats = video_formats + audio_formats

        self.format_list = Gtk.StringList.new([
            fmt.upper() for fmt in self.all_formats
        ])
        self.format_dropdown = Gtk.DropDown.new(
            model=self.format_list,
            expression=None
        )
        self.format_dropdown.set_selected(
            self.all_formats.index(
                self.config.get("default_format", "mp4")
            )
        )
        format_box.append(self.format_dropdown)

        # Botões de Ação
        action_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=10
        )
        main_box.append(action_box)

        cancel_button = Gtk.Button(label=_("Cancel"))
        cancel_button.connect("clicked", lambda _: self.destroy())
        action_box.append(cancel_button)

        save_button = Gtk.Button(label=_("Save"))
        save_button.connect("clicked", self.on_save_clicked)
        action_box.append(save_button)

    def on_select_folder_clicked(self, button):
        # Criar um Gtk.FileDialog
        file_dialog = Gtk.FileDialog()
        file_dialog.set_title(_("Select a Folder"))

        # Chamar o método select_folder
        file_dialog.select_folder(
            parent=self,
            cancellable=None,
            callback=self.on_folder_selected
        )

    def on_folder_selected(self, dialog, result):
        try:
            # Obter a pasta selecionada
            selected_file = dialog.select_folder_finish(result)
            if selected_file:
                folder_path = selected_file.get_path()
                self.folder_entry.set_text(folder_path)
        except Exception as e:
            print(f"Error selecting folder: {e}")

    def on_save_clicked(self, button):
        self.config["download_dir"] = self.folder_entry.get_text()
        self.config["default_format"] = self.all_formats[
            self.format_dropdown.get_selected()
        ]
        save_config(self.config)
        self.destroy()
