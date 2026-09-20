EmergenceKey came about when I couldn't find the dongle for my Bluetooth keyboard, and remembered a few other times where I could have used an emergency keyboard. Hence EmergenceKey.

EmergenceKey combines cheap hardware and a self-hostable web interface that gives an on-screen keyboard, text sending, mouse control, media keys, and (on desktop) fullscreen keyboard-and-mouse capture so your phone or laptop can control a device just like a real keyboard/mouse.

## What you need to get started

This is the web UI only; you also need the hardware component for it to connect to. For hardware I've used a [Waveshare ESP32-S3-Zero](https://www.waveshare.com/esp32-s3-zero.htm) that connects over BLE to the browser and presents as a USB HID device on the target.

The USB dongle firmware is available at [newcarp/emergencekey-firmware](https://github.com/newcarp/emergencekey-firmware). Flash that to the device and you're ready to connect via the web interface.

There is no need to self-host; you can use EmergenceKey via [GitHub Pages](https://newcarp.github.io/emergencekey).

Or host it yourself with a machine with a Bluetooth adapter that can run Python 3 + OpenSSL. Bluetooth needs a secure context, so `serve.py` serves the page over HTTPS with a local self-signed cert if needed.

- A browser with Web Bluetooth is required:
  - **Android / desktop:** Chrome or Edge
  - **iPhone / iPad:** Safari with [Beacio](https://beacio.com) enabled

Firefox has no Web Bluetooth, so EmergenceKey will not function with it.

## Connecting

1. Open the page and hit **Connect**.
2. Pick **EmergenceKey** (or if you set a custom name, choose that) from the list.

Current [firmware](https://github.com/newcarp/emergencekey-firmware) can store an optional PIN on the EmergenceKey. A fresh EmergenceKey has none, so the page offers **Set a PIN**. You can skip this if you would rather not use one, but this lets anyone in range connect to the device when it's available for pairing, so it's strongly recommended to add one. If you skipped and want to add one later, or want to change or remove the PIN, you can do so through the settings menu.

After a PIN is stored, connecting in the future unlocks automatically and the browser remembers the code so it can reconnect. Wrong guesses will lock the connection out. You can wait, or power cycle the EmergenceKey.

## Features

**Capture** (desktop Chrome/Edge) is the closest thing to plugging in a real keyboard and mouse. Hit **Capture** and the trackpad goes fullscreen, locks the pointer, and every key and mouse movement on this machine is sent to the target similar to a VM console. Press Esc to release. If the target itself needs Esc, use the on-screen Esc key before you capture, or after you release.

The top bar also lets you show or hide the pieces you actually need:

- **Trackpad** — move, click, two-finger scroll / right-click, and double-tap-hold to drag. Mouse speed is in Settings.
- **Keys** — on-screen QWERTY, modifiers, arrows, and a text box. Type or paste, then **Send**. Enter in that box sends the text and a Return on the target. Hold **Fn** with the arrows for Home / End / Page Up / Page Down.
- **Media keys** — play, pause, skip, rewind, fast forward, volume, and mute.
- **F keys** — Esc and F1–F12.

## Settings

Open the gear in the top-left.

- **Mouse speed** — how fast the trackpad moves the pointer (0.25×–4×).
- **PIN** — set, change, or clear the PIN on the connected EmergenceKey. **Forget saved PIN** only drops the code this browser stored; it does not remove the PIN from the dongle.
- **Auto-reconnect** — after the screen locks or the Bluetooth link drops, reconnect to the last EmergenceKey. It does not run when you first open the page, and it stops if the EmergenceKey is off.
- **Keep screen on** — on phones that support it, stops the screen from sleeping while connected so the Bluetooth link stays up. Uses more battery. You can still lock with the power button.
- **Previous devices** — EmergenceKeys you have connected show up here. Tap one to connect, or **Forget** to remove it from the list (that also drops a saved PIN for it).
- **Scan all devices** — same as holding / right-clicking **Connect**: pick from every nearby Bluetooth device instead of only named EmergenceKeys.

## Troubleshooting

If nothing happens after hitting Connect (or the light on the device stays yellow), it's likely the OS hasn't paired with the dongle yet. The page can't always summon the pairing dialog itself, and on some OSes the browser can't raise the prompt, so you have to pair manually.

- If a pairing prompt appears → tap through it once. After that, it reconnects silently.
- If no prompt appears → pair EmergenceKey manually in your OS Bluetooth settings, then come back and hit **Connect** again.

You should only have to go through the pairing step once. After that it should just work when you connect on the webpage.

On Linux, tap **Disconnect** before you close the tab. Closing Chrome while still connected can leave the EmergenceKey attached; another device will not see it until you unplug or run `bluetoothctl disconnect`. Windows, Mac, iPhone, and Android drop the link on their own.

## Self-hosting quick start

```bash
cp .env.example .env
# Edit .env: set HOST to this machine's IP or hostname.
python3 serve.py
```

Then open the HTTPS URL in a Web Bluetooth browser and follow [Connecting](#connecting).

**iPhone / iPad:** Safari will not click through a self-signed cert. Open the HTTP cert page printed by the server, install `emergencekey.cer`, then enable trust under **Settings → General → About → Certificate Trust Settings**. After that, open the HTTPS URL in Safari (with Beacio).

**Android / desktop:** Chrome or Edge. Open the HTTPS URL and continue past the self-signed warning. Installing the cert is optional.

`.env` and generated certs under `.certs/` stay local (gitignored).
