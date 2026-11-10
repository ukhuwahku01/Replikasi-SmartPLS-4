# Paket draf paper JADS KidSense

Buka `paper_jads/output/KidSense_JADS_Draft_Paper.docx` untuk mengedit naskah dan PDF dengan nama yang sama untuk membaca hasil render. Draf memakai template JADS asli yang diunggah, memuat 13 halaman, 10 tabel, dua gambar, 17 referensi jurnal, dan identitas tiga penulis yang diberikan.

Baca `paper_jads/output/CATATAN_PENULIS.md` untuk informasi yang masih perlu dilengkapi sebelum pengajuan. Penanda kuning tidak boleh diganti dengan fakta yang belum dikonfirmasi. Referensi belum diperiksa ulang pada situs penerbit secara daring.

Paket ini menyertakan template asli, tabel, bukti numerik terpilih, gambar PNG/SVG, dan skrip pembentuk naskah. Repositori backup lengkap berisi data/ekspor asli dan seluruh riwayat analisis: https://github.com/ukhuwahku01/Replikasi-SmartPLS-4.

Untuk membentuk ulang paper dari bukti yang telah disimpan, pertahankan struktur direktori setelah ekstraksi, gunakan Python dengan python-docx, matplotlib, numpy, dan PyMuPDF, lalu jalankan `python paper_jads/build_paper.py`. Konversi Word ke PDF dengan Microsoft Word atau LibreOffice; `python paper_jads/validate_paper.py` memeriksa dokumen dan tabel PDF. Skrip pembentuk paper tidak menghitung ulang bootstrap dari data mentah; skrip analisis lengkap berada pada arsip GitHub.

Sumber asli tidak diubah. Perbedaan tanggal/metadata dokumen yang dibuat ulang dapat menghasilkan hash dokumen berbeda tanpa perubahan angka.
