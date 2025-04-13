# -*- coding: utf-8 -*-
from i18n import _
import gi
gi.require_version('Gtk', '4.0')

from gi.repository import Gtk


class VideoInfoWindow(Gtk.Window):
    def __init__(self, video_info, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title(_("Video Information"))
        self.set_default_size(600, 400)

        # Main Box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_child(main_box)

        # Exibir informações básicas
        title_label = Gtk.Label(label=f"<b>Title:</b> {video_info['title']}")
        title_label.set_use_markup(True)
        main_box.append(title_label)

        duration_label = Gtk.Label(label=f"<b>Duration:</b> {video_info['duration']} seconds")
        duration_label.set_use_markup(True)
        main_box.append(duration_label)

        description_label = Gtk.Label(label=f"<b>Description:</b> {video_info.get('description', 'N/A')}")
        description_label.set_line_wrap(True)
        description_label.set_max_width_chars(50)
        main_box.append(description_label)

        # Lista de formatos
        formats_label = Gtk.Label(label="<b>Available Formats:</b>")
        formats_label.set_use_markup(True)
        main_box.append(formats_label)

        self.format_list_store = Gtk.ListStore(str, str)
        for fmt in video_info['formats']:
            self.format_list_store.append([fmt['format'], fmt['format_id']])

        tree_view = Gtk.TreeView(model=self.format_list_store)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Format", renderer, text=0)
        tree_view.append_column(column)
        main_box.append(tree_view)

        # Botão para confirmar seleção
        confirm_button = Gtk.Button(label=_("Select Format"))
        confirm_button.connect("clicked", self.on_format_selected, tree_view)
        main_box.append(confirm_button)

    def on_format_selected(self, button, tree_view):
        selection = tree_view.get_selection()
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            selected_format = model[treeiter][1]  # format_id
            print(f"Selected format: {selected_format}")
            self.destroy()
