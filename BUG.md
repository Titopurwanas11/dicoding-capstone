# Dokumentasi Bug - Fine-Tuning & NLP System

## Status: UNRESOLVED (Current Bugs / Improvements)

Tidak ada bug unresolved saat ini. Semua sudah diselesaikan.

---

## Status: RESOLVED

Semua bug di bawah ini sudah diperbaiki di branch `feat/bi-encoder-only` (atau main).

---

## 8. Deskripsi Pekerjaan (JD) Tidak Dibersihkan saat Scraping & Ranking HR (RESOLVED)

* **Lokasi**: 
  * `backend/app/services/linkedin_scraper.py` (line 106)
  * `backend/app/api/hr_endpoints.py` (line 21)
* **Gejala / Masalah**: 
  * Pada saat scraping LinkedIn (`linkedin_scraper.py`), teks deskripsi pekerjaan disimpan ke MongoDB dan langsung di-encode (`description_embedding`) **tanpa dibersihkan**. JD mentah sering kali mengandung tag HTML, URL lowongan, email kontak, dan noise lainnya yang mengotori hasil embedding.
  * Pada pencarian semantik (`/jobs/semantic-search`), teks CV yang bersih dibandingkan dengan embedding JD yang kotor, sehingga menurunkan akurasi pencarian.
  * Pada endpoint HR (`/hr/rank`), `job_description` dikirim langsung ke `get_similarity_score` tanpa dibersihkan terlebih dahulu.
* **Solusi**: 
  1. Import `clean_text` dari `parser.py` dan bersihkan deskripsi pekerjaan sebelum melakukan embedding di scraper.
  2. Bersihkan juga `job_description` di `hr_endpoints.py` sebelum masuk ke fungsi scoring.

---

## 9. Bug Eksekusi Script dari Jupyter Notebook (RESOLVED)

* **Lokasi**: `training/notebooks/finetuning-model.ipynb`
* **Gejala / Masalah**: 
  * Menggunakan string `'python'` langsung pada `subprocess.run()`. Hal ini memicu *interpreter default sistem*, bukan *virtual environment* (conda/venv) aktif milik Jupyter Kernel. Akibatnya muncul error `ModuleNotFoundError`.
  * Menggunakan `subprocess.run(capture_output=True)` yang menahan output stdout ke memori. Log training (loss, progress bar) tidak tercetak secara real-time sehingga Jupyter terlihat hang/freeze berjam-jam selama proses training.
* **Solusi**: 
  1. Ganti `'python'` dengan `sys.executable` agar menggunakan interpreter yang sama dengan kernel.
  2. Ganti `subprocess.run()` dengan `subprocess.Popen()` untuk men-stream log training (loss, progress bar) secara real-time ke output cell notebook.

---

## 1. Cross-Encoder Predictions Collapse ke ~78% (RESOLVED)

* **Lokasi**: `backend/app/services/nlp.py` (sebelumnya)
* **Penyebab**: Fungsi `get_similarity_score()` menggunakan Cross-Encoder tetapi tidak menerapkan fungsi sigmoid pada output logit. Logit mentah (bisa <0 atau >1) dipaksa ke rentang 0-1 menggunakan `max(0.0, min(1.0, val))` sehingga semua prediksi menumpuk di angka yang sama.
* **Solusi**:
  1. Menambahkan fungsi sigmoid: `prob = 1.0 / (1.0 + math.exp(-val))`
  2. Switching ke Bi-Encoder (Cosine Similarity) untuk scoring utama

---

## 2. Ekstraksi Skill Noise (Kata Umum dianggap Skill) (RESOLVED)

* **Lokasi**: `backend/app/services/nlp.py` (`extract_phrases`), `backend/app/services/parser.py` (`STOPWORDS`)
* **Gejala**: Kata-kata seperti "Have", "Skills", "Work", "Indonesia", "Solusi", "Medan" muncul di daftar matched/missing skills.
* **Penyebab**:
  - Fungsi `extract_phrases()` mengekstrak semua kata berawalan huruf kapital sebagai skill
  - `clean_text()` mengonversi seluruh teks ke lowercase, sehingga deteksi ALL CAPS (SQL, AWS) tidak berfungsi
  - Daftar `STOPWORDS` terlalu sedikit
* **Solusi**:
  1. `clean_text()` tidak lagi lowercase teks (mempertahankan casing)
  2. Penambahan 100+ STOPWORDS (action verbs, lokasi, kata generik, e.g./dll)
  3. `extract_phrases()` hanya mengekstrak kata yang ALL CAPS atau mengandung karakter teknologi (+, #, ., -)

---

## 3. Frasa Gabungan Tidak Terpecah (RESOLVED)

* **Lokasi**: `backend/app/services/nlp.py` (`extract_phrases`)
* **Gejala**: "js and database SQL" diekstrak sebagai satu frasa utuh, bukan terpecah menjadi skill individual.
* **Penyebab**: Fungsi split hanya memecah berdasarkan `,` `;` `\n` tanpa memperhatikan kata hubung tengah (`and`, `or`, `dan`, `atau`).
* **Solusi**:
  1. Menambahkan split berdasarkan `:` dan `()[]`
  2. Jika frasa mengandung kata hubung tengah, dipecah menjadi sub-frasa
  3. Stopwords di awal/akhir frasa di-strip secara iteratif (contoh: "database SQL" → strip "database" → "SQL")

---

## 4. Tanda Kurung dan Konten Noise Masih Lolos (RESOLVED)

* **Lokasi**: `backend/app/services/parser.py` (`clean_text`)
* **Gejala**: Teks seperti "(e.g., Python, Java)", "(WFO)", "(Teknik Informatika)" masih muncul di output.
* **Penyebab**: `clean_text()` mempertahankan karakter `()` di regex.
* **Solusi**:
  1. Regex baru menghapus isi dalam kurung: `re.sub(r'\([^)]*\)', ' ', text)`
  2. Tambah kata `e.g.`, `eg`, `i.e.`, `etc`, `dll`, `dsb` ke STOPWORDS

---

## 5. JD Tidak Dibersihkan sebelum Matching (RESOLVED)

* **Lokasi**: `backend/app/api/endpoints.py`, `backend/app/api/hr_endpoints.py`
* **Gejala**: `job_description` dari form input dikirim langsung ke `get_similarity_score()` tanpa pembersihan, menyebabkan noise HTML/URL/email mengganggu cosine similarity.
* **Solusi**: Menambahkan `jd_clean = clean_text(job_description)` sebelum dikirim ke fungsi matching.

---

## 6. Template Placeholder `{skill1}` / `{skill2}` Tidak Ter-replace (RESOLVED)

* **Lokasi**: `training/scripts/generate_dataset.py` (`_fill_template`)
* **Penyebab**: Logic penggantian menggunakan AND condition, sehingga jika hanya ada `{skill1}` saja, replace tidak tereksekusi.
* **Solusi**: Mengganti `and` dengan `or` pada pengecekan placeholder.

---

## 7. Training Warmup Steps Terlalu Agresif (RESOLVED)

* **Lokasi**: `training/scripts/train_cross_encoder.py`
* **Penyebab**: `warmup_steps` default 100, tetapi dengan 2000 data dan batch 16, total training hanya ~375 steps. Warmup 27% dari total training membuat model hampir tidak belajar.
* **Solusi**: Warmup steps otomatis dihitung sebagai 10% dari total training steps.

---

## Known Limitations (Future Work)

1. **Deduksi skill CI/CD**: `CI` dan `CD` muncul terpisah dari `CI/CD`. Bisa diatasi dengan deduplikasi post-processing.
2. **"WFO" masih muncul**: Sudah ditambahkan ke STOPWORDS tetapi mungkin perlu verifikasi lebih lanjut.
3. **JD scraping tanpa cleaning**: `linkedin_scraper.py` belum menerapkan `clean_text()` ke deskripsi pekerjaan sebelum embedding. Sebaiknya ditambahkan untuk konsistensi.
