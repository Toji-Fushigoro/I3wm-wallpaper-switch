#!/usr/bin/env /usr/bin/python3
import gi
import os
import subprocess
import shutil

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gdk


class WallpaperSwitcher(Gtk.Window):
    def __init__(self):
        super().__init__(title="i3 Wallpaper Switcher")
        self.set_border_width(10)
        self.set_default_size(400, 500)
        self.set_resizable(False)

        # Main Layout
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.vbox)

        # Image Preview Area
        self.preview_image = Gtk.Image()
        self.preview_image.set_from_icon_name("image-missing", Gtk.IconSize.DIALOG)
        self.preview_frame = Gtk.Frame(label="Preview")
        self.preview_frame.set_size_request(350, 250)
        self.preview_frame.add(self.preview_image)
        self.vbox.pack_start(self.preview_frame, True, True, 0)

        # Selected Path Label
        self.path_label = Gtk.Label(label="No image selected")
        self.path_label.set_ellipsize(3)  # PANGO_ELLIPSIZE_MIDDLE
        self.vbox.pack_start(self.path_label, False, False, 0)

        # File Selection Button
        self.btn_select = Gtk.Button(label="Select Image")
        self.btn_select.connect("clicked", self.on_select_clicked)
        self.vbox.pack_start(self.btn_select, False, False, 0)

        # Scaling Mode Dropdown
        scaling_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        scaling_label = Gtk.Label(label="Scaling Mode:")
        self.scaling_combo = Gtk.ComboBoxText()
        # feh mapping: (Display Name, feh flag)
        self.modes = [
            ("Fill Screen (Crop)", "--bg-fill"),
            ("Fit Screen (Borders)", "--bg-max"),
            ("Stretch (Distort)", "--bg-scale"),
            ("Center (Original Size)", "--bg-center"),
        ]
        for name, flag in self.modes:
            self.scaling_combo.append_text(name)
        self.scaling_combo.set_active(0)

        scaling_box.pack_start(scaling_label, False, False, 0)
        scaling_box.pack_start(self.scaling_combo, True, True, 0)
        self.vbox.pack_start(scaling_box, False, False, 0)

        # Apply Button
        self.btn_apply = Gtk.Button(label="Apply Wallpaper")
        self.btn_apply.get_style_context().add_class("suggested-action")
        self.btn_apply.connect("clicked", self.on_apply_clicked)
        self.vbox.pack_start(self.btn_apply, False, False, 0)

        # Status Label
        self.status_label = Gtk.Label(label="")
        self.vbox.pack_start(self.status_label, False, False, 0)

        self.selected_file = None

        # Check if feh is installed
        self.feh_path = shutil.which("feh")
        if not self.feh_path:
            self.show_error(
                "Dependency Error", "The 'feh' tool is not found. Please install it."
            )
            self.btn_apply.set_sensitive(False)

    def on_select_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Select an image", parent=self, action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )

        filter_img = Gtk.FileFilter()
        filter_img.set_name("Images")
        filter_img.add_mime_type("image/jpeg")
        filter_img.add_mime_type("image/png")
        filter_img.add_pattern("*.jpg")
        filter_img.add_pattern("*.jpeg")
        filter_img.add_pattern("*.png")
        dialog.add_filter(filter_img)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.selected_file = dialog.get_filename()
            self.path_label.set_text(os.path.basename(self.selected_file))
            self.update_preview(self.selected_file)
            self.status_label.set_text("")

        dialog.destroy()

    def update_preview(self, filepath):
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                filepath, width=340, height=240, preserve_aspect_ratio=True
            )
            self.preview_image.set_from_pixbuf(pixbuf)
        except Exception as e:
            self.status_label.set_text(f"Error loading preview: {str(e)}")

    def on_apply_clicked(self, widget):
        if not self.selected_file:
            self.status_label.set_text("Please select an image first.")
            return

        idx = self.scaling_combo.get_active()
        mode_flag = self.modes[idx][1]

        try:
            # Command to set wallpaper on all monitors identically
            command = [self.feh_path, mode_flag, self.selected_file]

            # Use subprocess to run feh
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5,
            )

            if result.returncode == 0:
                self.status_label.set_text("Wallpaper applied successfully!")
            else:
                self.status_label.set_text(
                    f"feh error: {result.stderr.splitlines()[0]}"
                )

        except subprocess.TimeoutExpired:
            self.status_label.set_text("Error: feh operation timed out.")
        except Exception as e:
            self.status_label.set_text(f"Critical error: {str(e)}")

    def show_error(self, title, message):
        dialog = Gtk.MessageDialog(
            parent=self,
            modal=True,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=title,
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()


if __name__ == "__main__":
    win = WallpaperSwitcher()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
