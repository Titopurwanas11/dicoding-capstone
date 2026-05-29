
# perubahan dan optimalisasi
ubah agar system sesuai dengan permintaan dibwah

## fitur jobseeker
- 1. **scrapt & find matches**:
    - sekarang dia tidak lagi perlu mengupload file pdf/docs
    - sekarang dia akan menampilkan data pada mongo db hasil dari scraping data cukup data pentingnya saja. seperti company, location, title, dan url
    - saat ini hanya ada 1 tombol filter yaitu time range setelah update akan ada tambahan tombol input yang nantinya isi dari parameter pertama dari fungsi scrape_linkedin_jobs di linkedin_scraper.py,
    - flow user akan menentukan berapa waktu kebelakang seperti opstion sekarang lalu menginput lokasi dengan input text dan input keyword dengan input text dan ketika disubmit maka akan scraping data
- 2. **semantic job search**:
    - sekarang dia menggunakan text input. saya ingin agar disana adalah upload file dan text yang sudah diconvert oleh python adalah inputanya. jadi user cukup upload file
    - flow sudah sama bedanya pada inputan yaitu menjadi pdf/docs dan akan diproses oleh python sampai menhasilkan text baru dilempar kefungsi semantic

## fitu hr
- 1. **cv bulk rangking**:
    - perbaiki tampilan inputnya coba cari apakah ada library agar inputan tersebut teersusun tersusun dan dapat dihapus salah satunya jika dibutuhkan. contoh jika di laravel/js adalah select2doc