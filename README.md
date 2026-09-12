# EmergenceKey

I don't want to carry a keyboard.

EmergenceKey is a web interface that gives on-screen keyboard, text sending, mouse control, and media keys so your phone or laptop can
drive the target without packing a real keyboard or mouse.

This repo is the **phone / laptop web UI**. It is half of the project. The USB dongle firmware lives in [newcarp/emergencekey-firmware](https://github.com/newcarp/emergencekey-firmware).

The dongle (a [Waveshare ESP32-S3-Zero](https://www.waveshare.com/esp32-s3-zero.htm)) talks BLE to the browser and presents as a real USB HID device on the target. No drivers or extra software on the target.

Treat this as an emergency / same-room tool, not a general-purpose wireless keyboard. On some BIOS screens the chip will take keyboard but not mouse.

## What you need

**Hardware (firmware repo)**

- A Waveshare ESP32-S3-Zero flashed from [newcarp/emergencekey-firmware](https://github.com/newcarp/emergencekey-firmware) (flashing notes are there)
- The dongle plugged into the target machine, advertising as `EmergenceKey`

**This web interface**
- Use this page live on github pages - https://newcarp.github.io/emergencekey
- Or host it yourslf with a machine on the same LAN that can run Python 3 + OpenSSL. Bluetooth needs a secure context, so `serve.py` serves the page over HTTPS with a local self-signed cert if needed.
- A browser with Web Bluetooth is required:
  - **Android / desktop:** Chrome or Edge
  - **iPhone / iPad:** Safari with [Beacio](https://beacio.com) enabled (`aA` → Manage Extensions → allow Beacio)

Firefox and stock Safari have no Web Bluetooth. Opening `index.html` as a file will not work.

## Connecting

1. Open the page and hit **Connect**.
2. Pick **EmergenceKey** from the list.

If nothing happens after hitting Connect (or the light stays yellow), the OS hasn't paired with the dongle yet. The page can't always summon the pairing dialog itself — on some OSes the browser can't raise the prompt, so you have to pair manually.

- If a pairing prompt appears → tap through it once. After that, it reconnects silently.
- If no prompt appears → pair EmergenceKey manually in your OS Bluetooth settings, then come back and hit **Connect** again.

You should only have to go through the pairing step once. After that it should just work when you connect on the webpage.

**Show media** and **Show F keys** fold those rows in. Media is play/pause, next/prev, stop, rewind, FF, mute, and volume (hold Vol± / Rew / FF to repeat). Media keys need a dongle flashed from current [firmware](https://github.com/newcarp/emergencekey-firmware). Older sticks ignore them; the rest of the page still works.

## Self Hosting Quick start

```bash
cp .env.example .env
# Edit .env: set HOST to this machine's LAN IP (or hostname).
# Optional: EXTRA_SANS for Tailscale / extra IPs.

python3 serve.py
```

Then open the HTTPS URL in a Web Bluetooth browser and follow [Connecting](#connecting).

**iPhone / iPad:** Safari will not click through a self-signed cert. Open the HTTP cert page printed by the server, install `emergencekey.cer`, then enable trust under **Settings → General → About → Certificate Trust Settings**. After that, open the HTTPS URL in Safari (with Beacio).

**Android / desktop:** Chrome or Edge. Open the HTTPS URL and continue past the self-signed warning. Installing the cert is optional.

`.env` and generated certs under `.certs/` stay local (gitignored).

## License

MIT — see [LICENSE](LICENSE).
