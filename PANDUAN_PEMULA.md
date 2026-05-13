# 📚 Panduan Lengkap AI Glossary - Untuk Pemula

**Tujuan:** Membuat website yang otomatis generate artikel tentang AI dalam bahasa sederhana.

**Waktu Setup:** ~30 menit  
**Kesulitan:** Mudah (tidak perlu coding)

---

## 🎯 Apa yang Akan Kita Lakukan?

1. ✅ Setup awal (5 menit)
2. ✅ Konfigurasi GitHub (10 menit)
3. ✅ Setup Telegram notifikasi (5 menit)
4. ✅ Test & jalankan (10 menit)

---

## 📋 Yang Kamu Butuhkan

- ✅ Akun GitHub (gratis)
- ✅ Akun Telegram (gratis)
- ✅ API key Groq (gratis)
- ✅ Akun Cloudflare (gratis)

**Semua gratis!** 🎉

---

## STEP 1: Setup Awal (5 menit)

### 1.1 Buka Repository

1. Go to: https://github.com/HackMyTask/AGC-WEBSITE
2. Klik tombol **"Code"** (hijau)
3. Pilih **"HTTPS"**
4. Copy link-nya

### 1.2 Clone ke Komputer (Opsional)

Kalau mau kerja lokal:
```bash
git clone https://github.com/HackMyTask/AGC-WEBSITE.git
cd AGC-WEBSITE
```

**Tapi untuk pemula, kita bisa langsung pakai GitHub Actions (otomatis).**

---

## STEP 2: Dapatkan API Keys (10 menit)

### 2.1 Groq API Key (untuk generate artikel)

1. Go to: https://console.groq.com/keys
2. Login atau buat akun (gratis)
3. Klik **"Create API Key"**
4. Copy key-nya (contoh: `gsk_abc123...`)
5. **Simpan di tempat aman** (jangan share!)

### 2.2 Cloudflare Account (untuk hosting)

1. Go to: https://dash.cloudflare.com/sign-up
2. Buat akun (gratis)
3. Verify email
4. Selesai!

### 2.3 Telegram Bot (untuk notifikasi)

1. Buka Telegram
2. Cari bot: **@BotFather**
3. Kirim: `/start`
4. Kirim: `/newbot`
5. Ikuti instruksi:
   - Nama bot: `AGC Glossary Bot`
   - Username: `agc_glossary_bot` (atau nama unik lain)
6. Copy **Bot Token** (contoh: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)
7. **Simpan bot token**

### 2.4 Telegram Chat ID

1. Buka bot yang baru dibuat
2. Kirim pesan apapun ke bot
3. Go to: `https://api.telegram.org/bot<BOT_TOKEN>/getUpdates`
   - Ganti `<BOT_TOKEN>` dengan token dari step 2.3
4. Cari `"chat":{"id":123456789}`
5. Copy angka itu (Chat ID)
6. **Simpan chat ID**

---

## STEP 3: Setup GitHub Secrets (10 menit)

**Ini adalah bagian penting!** Secrets adalah tempat aman untuk menyimpan API keys.

### 3.1 Buka Settings Repository

1. Go to: https://github.com/HackMyTask/AGC-WEBSITE
2. Klik tab **"Settings"** (atas kanan)
3. Di sidebar kiri, klik **"Secrets and variables"**
4. Klik **"Actions"**

### 3.2 Tambah Secrets

Klik **"New repository secret"** dan tambahkan satu per satu:

**Secret 1: AI_PROVIDER**
- Name: `AI_PROVIDER`
- Value: `groq`
- Klik "Add secret"

**Secret 2: GROQ_API_KEY**
- Name: `GROQ_API_KEY`
- Value: `gsk_abc123...` (dari step 2.1)
- Klik "Add secret"

**Secret 3: TELEGRAM_BOT_TOKEN**
- Name: `TELEGRAM_BOT_TOKEN`
- Value: `123456:ABC-DEF1234...` (dari step 2.3)
- Klik "Add secret"

**Secret 4: TELEGRAM_CHAT_ID**
- Name: `TELEGRAM_CHAT_ID`
- Value: `123456789` (dari step 2.4)
- Klik "Add secret"

**Secret 5: CLOUDFLARE_API_TOKEN**
- Name: `CLOUDFLARE_API_TOKEN`
- Value: (kita ambil di step 3.3)
- Klik "Add secret"

**Secret 6: CLOUDFLARE_ACCOUNT_ID**
- Name: `CLOUDFLARE_ACCOUNT_ID`
- Value: (kita ambil di step 3.3)
- Klik "Add secret"

### 3.3 Dapatkan Cloudflare Credentials

1. Go to: https://dash.cloudflare.com/profile/api-tokens
2. Klik **"Create Token"**
3. Pilih template **"Edit Cloudflare Workers"**
4. Klik **"Use template"**
5. Di bagian "Account resources", pilih akun kamu
6. Klik **"Continue to summary"**
7. Klik **"Create Token"**
8. Copy token → masukkan ke `CLOUDFLARE_API_TOKEN`

Untuk Account ID:
1. Go to: https://dash.cloudflare.com/
2. Di sidebar kanan, cari **"Account ID"**
3. Copy → masukkan ke `CLOUDFLARE_ACCOUNT_ID`

---

## STEP 4: Enable GitHub Actions (5 menit)

### 4.1 Aktifkan Workflows

1. Go to: https://github.com/HackMyTask/AGC-WEBSITE/actions
2. Klik **"I understand my workflows, go ahead and enable them"**
3. Selesai! ✅

---

## STEP 5: Test & Jalankan (10 menit)

### 5.1 Test Manual Generation

1. Go to: https://github.com/HackMyTask/AGC-WEBSITE/actions
2. Klik **"Generate Content"** (di sidebar kiri)
3. Klik **"Run workflow"** (tombol biru)
4. Isi form:
   - **batch_size:** `10` (untuk test, gunakan batch kecil)
   - **priority:** (kosongkan)
   - **random:** (kosongkan)
5. Klik **"Run workflow"** (hijau)
6. Tunggu ~2-3 menit

### 5.2 Lihat Hasil

1. Klik workflow yang sedang berjalan
2. Lihat log real-time
3. Tunggu sampai selesai (status: ✅ Success)
4. Cek Telegram - kamu akan dapat notifikasi! 📱

### 5.3 Lihat Artikel yang Dihasilkan

1. Go to: https://github.com/HackMyTask/AGC-WEBSITE
2. Buka folder **"content/glossary"**
3. Lihat file `.md` yang baru dibuat
4. Klik salah satu untuk lihat isi artikel

---

## STEP 6: Set & Forget (Otomatis Setiap Hari)

Setelah test berhasil, sistem akan otomatis:

### ✅ Apa yang Terjadi Otomatis?

**Setiap hari jam 2 pagi UTC (9 pagi WIB):**
- ✅ Generate 20 artikel baru
- ✅ Validasi kualitas
- ✅ Update link internal
- ✅ Commit ke GitHub
- ✅ Kirim notifikasi ke Telegram

**Setiap minggu (Minggu jam 3 pagi UTC):**
- ✅ Check kualitas
- ✅ Validasi data
- ✅ Generate laporan

**Setiap push ke main branch:**
- ✅ Deploy ke Cloudflare Pages
- ✅ Website live!

### 📱 Notifikasi Telegram

Kamu akan dapat notifikasi:
- ✅ Ketika generation dimulai
- ✅ Berapa artikel berhasil
- ✅ Berapa artikel gagal
- ✅ Berapa token digunakan
- ✅ Kapan API key dirotasi

---

## 🎮 Kontrol Manual (Kapan Saja)

Kalau mau generate lebih banyak atau lebih sedikit:

### Generate Batch Kecil (Testing)
1. Go to: https://github.com/HackMyTask/AGC-WEBSITE/actions
2. Klik **"Generate Content"**
3. Klik **"Run workflow"**
4. Isi: `batch_size: 10`
5. Klik "Run workflow"

### Generate Batch Besar (Cepat)
1. Go to: https://github.com/HackMyTask/AGC-WEBSITE/actions
2. Klik **"Generate Content"**
3. Klik **"Run workflow"**
4. Isi: `batch_size: 50`
5. Klik "Run workflow"

### Generate Random (Testing Kualitas)
1. Go to: https://github.com/HackMyTask/AGC-WEBSITE/actions
2. Klik **"Generate Content"**
3. Klik **"Run workflow"**
4. Isi: `random: 30`
5. Klik "Run workflow"

---

## 📊 Monitoring & Laporan

### Lihat Progress

1. Go to: https://github.com/HackMyTask/AGC-WEBSITE/actions
2. Klik workflow yang sedang berjalan
3. Lihat log real-time
4. Lihat summary di bawah

### Lihat Artikel yang Dihasilkan

1. Go to: https://github.com/HackMyTask/AGC-WEBSITE
2. Buka folder **"content/glossary"**
3. Lihat semua artikel `.md`

### Lihat Laporan Kualitas

1. Go to: https://github.com/HackMyTask/AGC-WEBSITE
2. Buka folder **"logs"**
3. Lihat file:
   - `usage.log` - Token yang digunakan
   - `quality_failures.log` - Artikel yang gagal
   - `api_rotation.log` - Kapan API key dirotasi

---

## 🚀 Kapasitas & Scaling

### Dengan 1 API Key (Groq)
- **Per hari:** 20 artikel (default)
- **Per minggu:** 140 artikel
- **Per bulan:** 600 artikel

### Kalau Mau Lebih Cepat

**Tambah API Keys:**
1. Buat 2-3 akun Groq gratis
2. Dapatkan 3 API keys
3. Di GitHub Secrets, ubah `GROQ_API_KEY`:
   ```
   gsk_key1,gsk_key2,gsk_key3
   ```
4. Sistem otomatis rotate antar keys
5. **Kapasitas jadi 3x lipat!**

---

## ❓ FAQ (Pertanyaan Umum)

### Q: Berapa biaya?
**A:** Gratis! Semua tools yang digunakan punya tier gratis.

### Q: Berapa lama generate 1 artikel?
**A:** ~30 detik per artikel. Jadi 20 artikel = ~10 menit.

### Q: Bisa generate lebih dari 50 artikel?
**A:** Bisa, tapi maksimal 50 per run. Bisa jalankan berkali-kali.

### Q: Gimana kalau API key habis quota?
**A:** Sistem otomatis rotate ke API key berikutnya. Tidak ada downtime.

### Q: Bisa customize artikel?
**A:** Ya! Edit file `prompts/article.txt` di repository.

### Q: Bisa deploy ke domain sendiri?
**A:** Ya! Setup Cloudflare Pages dengan domain kamu.

### Q: Gimana kalau ada error?
**A:** Cek Telegram notifikasi atau lihat log di GitHub Actions.

---

## 📞 Troubleshooting

### Workflow tidak jalan
- ✅ Cek apakah secrets sudah ditambah
- ✅ Cek apakah workflows sudah di-enable
- ✅ Cek apakah API key valid

### Tidak dapat notifikasi Telegram
- ✅ Cek apakah bot token benar
- ✅ Cek apakah chat ID benar
- ✅ Kirim pesan ke bot dulu

### Artikel gagal quality gate
- ✅ Cek `logs/quality_failures.log`
- ✅ Lihat alasan gagal
- ✅ Adjust prompt di `prompts/article.txt`

---

## 🎉 Selesai!

Kamu sekarang punya:
- ✅ Website AI Glossary otomatis
- ✅ Generate artikel setiap hari
- ✅ Notifikasi real-time
- ✅ Hosting gratis di Cloudflare
- ✅ Tidak perlu maintenance

**Tinggal duduk santai dan biarkan sistem bekerja!** 🚀

---

## 📚 Referensi Cepat

| Kebutuhan | Link |
|-----------|------|
| Repository | https://github.com/HackMyTask/AGC-WEBSITE |
| GitHub Actions | https://github.com/HackMyTask/AGC-WEBSITE/actions |
| GitHub Secrets | https://github.com/HackMyTask/AGC-WEBSITE/settings/secrets/actions |
| Groq API | https://console.groq.com/keys |
| Cloudflare | https://dash.cloudflare.com |
| Telegram Bot | https://t.me/BotFather |

---

**Selamat! Sistem kamu sudah siap! 🎊**
