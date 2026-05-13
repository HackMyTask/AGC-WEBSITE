# 📚 Panduan Setup Cloudflare - Untuk Pemula

**Tujuan:** Deploy website AI Glossary ke Cloudflare Pages (gratis) dan sambungkan dengan domain kamu.

**Waktu:** ~20 menit  
**Kesulitan:** Mudah (tidak perlu coding)

---

## 🎯 Apa yang Akan Kita Lakukan?

1. ✅ Buat akun Cloudflare (5 menit)
2. ✅ Ambil API credentials (5 menit)
3. ✅ Setup Cloudflare Pages (5 menit)
4. ✅ Sambungkan dengan GitHub (3 menit)
5. ✅ Sambungkan domain (2 menit)

---

## STEP 1: Buat Akun Cloudflare (5 menit)

### 1.1 Daftar

1. Go to: https://dash.cloudflare.com/sign-up
2. Pilih: **Email address**
3. Masukkan email kamu
4. Buat password (minimal 8 karakter)
5. Klik **"Create account"**

### 1.2 Verifikasi Email

1. Buka email kamu
2. Cari email dari Cloudflare
3. Klik link **"Verify email"**
4. Selesai! ✅

### 1.3 Login

1. Go to: https://dash.cloudflare.com
2. Login dengan email & password
3. Kamu akan masuk ke dashboard

---

## STEP 2: Ambil API Credentials (5 menit)

### 2.1 Dapatkan API Token

1. Di dashboard Cloudflare, klik **"My Profile"** (atas kanan)
2. Klik **"API Tokens"** (di sidebar kiri)
3. Klik **"Create Token"** (tombol biru)

### 2.2 Pilih Template

1. Cari template: **"Edit Cloudflare Workers"**
2. Klik **"Use template"**

### 2.3 Konfigurasi Token

1. Di bagian **"Account resources"**:
   - Pilih: **"Include"**
   - Pilih akun kamu (biasanya hanya ada 1)

2. Di bagian **"Zone resources"**:
   - Pilih: **"Include"**
   - Pilih: **"All zones"**

3. Klik **"Continue to summary"**

### 2.4 Buat Token

1. Review permissions (seharusnya sudah benar)
2. Klik **"Create Token"** (hijau)
3. **COPY token** (jangan share!)
4. Simpan di tempat aman

**Contoh token:**
```
z4d90c146e1e3c3d6f8a9b0c1d2e3f4g5h
```

### 2.5 Dapatkan Account ID

1. Di dashboard Cloudflare, klik **"Home"** (atas kiri)
2. Di sidebar kanan, cari **"Account ID"**
3. **COPY Account ID**
4. Simpan di tempat aman

**Contoh Account ID:**
```
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

---

## STEP 3: Setup Cloudflare Pages (5 menit)

### 3.1 Buat Project Pages

1. Di dashboard Cloudflare, klik **"Pages"** (di sidebar kiri)
2. Klik **"Create a project"** (tombol biru)
3. Pilih: **"Connect to Git"**

### 3.2 Hubungkan GitHub

1. Klik **"GitHub"**
2. Klik **"Authorize Cloudflare"**
3. Login GitHub (jika diminta)
4. Klik **"Authorize cloudflare"** (hijau)

### 3.3 Pilih Repository

1. Cari repository: **"AGC-WEBSITE"**
2. Klik untuk select
3. Klik **"Begin setup"**

### 3.4 Konfigurasi Build

1. **Project name:** `agc-website` (atau nama lain)
2. **Production branch:** `main`
3. **Framework preset:** `Astro`
4. **Build command:** `npm run build`
5. **Build output directory:** `dist`

6. Klik **"Save and Deploy"**

### 3.5 Tunggu Deploy

1. Cloudflare akan mulai build
2. Tunggu sampai selesai (biasanya 2-3 menit)
3. Kamu akan dapat URL: `https://agc-website.pages.dev`

**Selesai!** Website sudah live! 🎉

---

## STEP 4: Sambungkan dengan GitHub Actions (3 menit)

### 4.1 Tambah Secrets ke GitHub

1. Go to: https://github.com/HackMyTask/AGC-WEBSITE/settings/secrets/actions
2. Klik **"New repository secret"**

**Tambah Secret 1: CLOUDFLARE_API_TOKEN**
- Name: `CLOUDFLARE_API_TOKEN`
- Value: (paste token dari step 2.4)
- Klik "Add secret"

**Tambah Secret 2: CLOUDFLARE_ACCOUNT_ID**
- Name: `CLOUDFLARE_ACCOUNT_ID`
- Value: (paste Account ID dari step 2.5)
- Klik "Add secret"

### 4.2 Selesai!

GitHub Actions sudah bisa deploy ke Cloudflare Pages otomatis! ✅

**Apa yang terjadi:**
- Setiap kali ada push ke `main` branch
- GitHub Actions akan build website
- Otomatis deploy ke Cloudflare Pages
- Website update dalam 2-3 menit

---

## STEP 5: Sambungkan Domain Kamu (2 menit)

### 5.1 Tambah Domain ke Cloudflare

1. Di dashboard Cloudflare, klik **"Websites"** (sidebar kiri)
2. Klik **"Add a site"** (tombol biru)
3. Masukkan domain kamu (contoh: `aiglossary.com`)
4. Klik **"Continue"**

### 5.2 Pilih Plan

1. Pilih: **"Free"** (gratis)
2. Klik **"Continue"**

### 5.3 Update Nameserver

Cloudflare akan kasih 2 nameserver:
```
ns1.cloudflare.com
ns2.cloudflare.com
```

**Kamu perlu update di registrar domain kamu:**

1. Go ke registrar domain kamu (contoh: Niagahoster, Namecheap, dll)
2. Login ke akun kamu
3. Cari domain kamu
4. Cari **"Nameserver"** atau **"DNS"**
5. Ganti dengan nameserver Cloudflare:
   - `ns1.cloudflare.com`
   - `ns2.cloudflare.com`
6. Save/Update

**Tunggu 24 jam** untuk propagasi DNS.

### 5.4 Sambungkan Pages ke Domain

1. Di Cloudflare, buka project **"agc-website"**
2. Klik **"Custom domains"** (tab atas)
3. Klik **"Set up a custom domain"**
4. Masukkan domain kamu (contoh: `aiglossary.com`)
5. Klik **"Continue"**
6. Klik **"Activate domain"**

### 5.5 Selesai!

Website kamu sekarang live di domain sendiri! 🎉

**Contoh:**
- Sebelum: `https://agc-website.pages.dev`
- Sesudah: `https://aiglossary.com`

---

## 📊 Ringkasan Setup

| Step | Apa | Waktu |
|------|-----|-------|
| 1 | Buat akun Cloudflare | 5 min |
| 2 | Ambil API credentials | 5 min |
| 3 | Setup Cloudflare Pages | 5 min |
| 4 | Sambungkan GitHub Actions | 3 min |
| 5 | Sambungkan domain | 2 min |
| **Total** | | **20 min** |

---

## ✅ Checklist Setup

- [ ] Buat akun Cloudflare
- [ ] Ambil API Token
- [ ] Ambil Account ID
- [ ] Setup Cloudflare Pages
- [ ] Sambungkan GitHub
- [ ] Deploy pertama kali (tunggu 2-3 min)
- [ ] Tambah GitHub Secrets (CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID)
- [ ] Tambah domain ke Cloudflare
- [ ] Update nameserver di registrar
- [ ] Sambungkan Pages ke domain
- [ ] Tunggu 24 jam DNS propagasi
- [ ] Test website di domain kamu

---

## 🎯 Apa yang Terjadi Sekarang?

### Workflow Otomatis:

```
1. GitHub Actions generate artikel (2 AM UTC)
   ↓
2. Push ke GitHub
   ↓
3. Cloudflare Pages detect push
   ↓
4. Build website otomatis
   ↓
5. Deploy ke Cloudflare Pages
   ↓
6. Website live di domain kamu!
```

### Timeline:
- **2:00 AM UTC:** Generation dimulai
- **2:10 AM UTC:** Artikel selesai, push ke GitHub
- **2:12 AM UTC:** Cloudflare detect push
- **2:15 AM UTC:** Build selesai
- **2:16 AM UTC:** Deploy selesai
- **2:17 AM UTC:** Website update live! ✅

---

## 📱 Monitoring

### Lihat Deploy Status

1. Go to: https://github.com/HackMyTask/AGC-WEBSITE/actions
2. Klik workflow yang sedang berjalan
3. Lihat status deploy

### Lihat Website Live

1. Go to: `https://aiglossary.com` (atau domain kamu)
2. Lihat artikel terbaru
3. Selesai! 🎉

---

## ❓ FAQ

### Q: Berapa biaya Cloudflare?
**A:** Gratis! Plan free Cloudflare cukup untuk website kamu.

### Q: Berapa lama DNS propagasi?
**A:** Biasanya 5-30 menit, tapi bisa sampai 24 jam.

### Q: Bisa ganti domain nanti?
**A:** Ya! Tinggal tambah domain baru di Cloudflare.

### Q: Gimana kalau domain sudah punya DNS?
**A:** Ganti nameserver ke Cloudflare (step 5.3).

### Q: Bisa pakai subdomain?
**A:** Ya! Contoh: `glossary.domain.com`

### Q: Gimana kalau deploy gagal?
**A:** Cek GitHub Actions log untuk error message.

---

## 🚀 Selesai!

Kamu sekarang punya:
- ✅ Website live di Cloudflare Pages
- ✅ Domain sendiri
- ✅ Auto-deploy dari GitHub
- ✅ Gratis selamanya

**Tinggal tunggu artikel generate otomatis setiap hari!** ☕

---

## 📞 Troubleshooting

### Website tidak muncul di domain
- ✅ Tunggu 24 jam DNS propagasi
- ✅ Cek nameserver sudah update
- ✅ Cek domain sudah ditambah di Cloudflare

### Deploy gagal
- ✅ Cek GitHub Actions log
- ✅ Cek build command benar
- ✅ Cek output directory benar

### Artikel tidak update
- ✅ Cek GitHub Actions workflow jalan
- ✅ Cek Telegram notification
- ✅ Cek logs di GitHub

---

**Selamat setup! Kalau ada pertanyaan, baca FAQ atau troubleshooting section.** 😊
