# KidSense: konstruk terjelaskan dan sensitivitas M1

Buka output/KidSense_Draf_Terklarifikasi_dan_M1.docx atau PDF, dan output/KidSense_Tinjauan_Konstruk_dan_M1.xlsx.

Definisi dan12item berasal dari pesan peneliti dan tersimpan verbatim di definitions_and_items_user.json. M0 native tetap dipertahankan. M1 adalah analisis Python eksploratori posthoc dengan10000bootstrap; belum dijalankan native diSmartPLS dan tidak menyelesaikan HTMT. Menambah semua directpaths menyaturasi bagian kovarians struktural skor, bukan seluruh model indikator.

Python3.12,NumPy,pandas,scipy,openpyxl,python-docx,matplotlib dipakai untuk perhitungan dan artefak. Skrip menggunakan path mesin /workspace; sesuaikan bila dijalankan di mesin lain. Tidak ada data atau model asli yang ditimpa. Protokol nativeM1 disediakan agar pengguna dapat memverifikasi hasil secara terpisah.

Klarifikasi terbaru: responden hanya menilai deskripsi/gambar rancangan. Naskah diperbarui sebagai survei persepsi atas konsep dan niat hipotetis kondisional; bukan pengujian penggunaan prototipe. Semua angka tetap.

Pembaruan: bootstrap native M1 lengkap telah diterima dan diverifikasi pada KidSense_M1_DenganTR_Bootstrap_10000.xlsx. Tabel/gambar utama M1 kini memakai CI native percentile. Hasil dan batas model posthoc tetap dipertahankan.
