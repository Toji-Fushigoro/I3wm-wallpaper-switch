# i3wm-wallpaper-switch

A lightweight Python GTK 3 application to easily switch and scale wallpapers on i3wm (or any X11-based window manager). It uses `feh` as the backend to ensure compatibility with multi-monitor setups.

## Features

- **GUI Image Selection**: Browse and select `.jpg`, `.jpeg`, and `.png` files.
- **Image Preview**: View a scaled preview of the selected wallpaper before applying.
- **Scaling Modes**:
  - **Fill Screen (Crop)**: Fills the entire screen, cropping edges if aspect ratios differ.
  - **Fit Screen (Borders)**: Fits the whole image with black bars to preserve aspect ratio.
  - **Stretch (Distort)**: Stretches the image to fit the screen exactly.
  - **Center**: Places the image in the center at its original size.
- **Multi-Monitor Support**: Automatically applies the selected wallpaper to all connected monitors identically.
- **Error Handling**: Robust exception handling and subprocess timeouts to prevent system hangs.

## Requirements

- **Python 3**
- **PyGObject** (`python3-gi`)
- **GTK 3**
- **feh** (The standard X11 wallpaper utility)

### Installing Dependencies (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3-gi gir1.2-gtk-3.0 feh
```

### Installing Dependencies (Arch Linux)

```bash
sudo pacman -S python-gobject gtk3 feh
```

## Usage

1. **Run the Application**:
   ```bash
   python3 wallpaper_switcher.py
   ```
2. **Select an Image**: Click "Select Image" and choose your file.
3. **Choose Scaling**: Pick your preferred scaling mode from the dropdown.
4. **Apply**: Click "Apply Wallpaper".

## Persistence (Keep wallpaper after reboot)

The application updates the standard `~/.fehbg` file. To ensure your wallpaper is restored when you log into i3wm, add the following line to your `~/.config/i3/config` file:

```text
exec_always --no-startup-id ~/.fehbg
```

## Troubleshooting

- If the "Apply" button is disabled, ensure `feh` is installed and available in your `$PATH`.
- If the preview doesn't load, check if the image file is corrupted or if you have the necessary `gdk-pixbuf` loaders for your image format.

## License

MIT License - Feel free to modify and distribute.
