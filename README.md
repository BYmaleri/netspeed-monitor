# 🖥️ NetSpeed Monitor

Windows 11 görev çubuğu **saatinin hemen solunda** anlık internet hızını gösteren küçük bir araç.

```
 ↓  12.4 MB/s  │  19:45
 ↑   0.8 MB/s  │  Sal 21
```

---

## ⬇️ İndirme

**[Releases](../../releases/latest)** sayfasından `NetSpeedMonitor_Setup_vX.X.X.exe` dosyasını indirin ve çalıştırın.

> Yönetici yetkisi **gerekmez**.

---

## ✨ Özellikler

- 📍 Görev çubuğu saatinin **tam soluna** yapışır
- ↓ **İndirme** hızı (yeşil) ve ↑ **Yükleme** hızı (turuncu)
- B/s · KB/s · MB/s · GB/s otomatik birim
- **Windows ile otomatik başlat** seçeneği (sağ tık menüsü)
- İstersen sürükleyerek taşı, çift tık ile tekrar yapıştır
- Yönetici yetkisi gerektirmez
- Hafif: ~8 MB RAM kullanımı

---

## 🚀 GitHub Actions — Otomatik Build

Bu repo bir tag push'landığında otomatik olarak `Setup.exe` üretir ve Releases'e yükler.

```bash
git tag v1.0.0
git push origin v1.0.0
```

Birkaç dakika içinde **Releases** sayfasında hazır!

---

## 🔨 Kendin Derle

### Gereksinimler
- Python 3.9+
- [Inno Setup 6](https://jrsoftware.org/isinfo.php) (opsiyonel — installer için)

### Adımlar

```bat
git clone https://github.com/KULLANICI_ADINIZ/netspeed-monitor
cd netspeed-monitor
build.bat
```

`installer\output\` klasöründe Setup.exe hazır olur.

---

## 📁 Proje Yapısı

```
netspeed-monitor/
├── src/
│   ├── netspeed.py        ← Ana uygulama
│   └── create_icon.py     ← İkon üretici
├── installer/
│   └── setup.iss          ← Inno Setup scripti
├── .github/workflows/
│   └── release.yml        ← Otomatik build & release
├── netspeed.spec          ← PyInstaller ayarları
├── build.bat              ← Lokal build scripti
├── requirements.txt
└── README.md
```

---

## 📄 Lisans

MIT — dilediğin gibi kullanabilirsin.
