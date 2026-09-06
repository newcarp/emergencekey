# EmergenceKey

I don't want to carry a keyboard.

EmergenceKey is a web interface that gives on-screen keyboard, text sending, and mouse control so your phone or laptop can 
drive the target without packing a real keyboard or mouse.

This repo is the **phone / laptop web UI**. It is half of the project. The USB dongle firmware lives in [newcarp/emergencekey-firmware](https://github.com/newcarp/emergencekey-firmware).

The dongle (a [Waveshare ESP32-S3-Zero](https://www.waveshare.com/esp32-s3-zero.htm)) talks BLE to the browser and presents as a real USB HID device on the target. No drivers or extra software on the target.

**BLE is open (no pairing).** Treat this as an emergency / same-room tool, not a general-purpose wireless keyboard. On some BIOS screens the chip will take keyboard but not mouse.

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

## Quick start

```bash
cp .env.example .env
# Edit .env: set HOST to this machine's LAN IP (or hostname).
# Optional: EXTRA_SANS for Tailscale / extra IPs.

python3 serve.py
```

Then:

1. On iPhone, open the HTTP cert page printed by the server, install `emergencekey.cer`, and enable trust under **Settings → General → About → Certificate Trust Settings**.
2. Open the HTTPS URL in Safari (or another Web Bluetooth browser).
3. Tap **Connect**, pick the EmergenceKey device, and type / pointer away.

`.env` and generated certs under `.certs/` stay local (gitignored).

## License

MIT — see [LICENSE](LICENSE).
