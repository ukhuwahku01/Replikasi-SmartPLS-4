# Bukti replikasi KidSense SmartPLS4

Mulai dari hasil/KidSense_Replikasi_SmartPLS4_Final.xlsx dan hasil/KidSense_Laporan_Replikasi_Final.md.

Replikasi numerik selesai pada ekspor yang tersedia. Dua pasangan HTMT dan fit global tetap memerlukan catatan; CVPAT keseluruhan tidak signifikan terhadap LM.

Folder sumber berisi delapan unggahan asli (lima sumber awal dan tiga ekspor native), tanpa perubahan. Folder audit berisi skrip, JSON/CSV, galat prediksi, dan fold native yang direkonstruksi.

Runtime pembuktian: Python3.12.14, NumPy2.3.5, pandas2.2.3, SciPy1.17.0, openpyxl3.1.5, scikit-learn1.8.0. Skrip audit menyimpan path asli /workspace. Sesuaikan path jika dijalankan di mesin lain; paket ini bukan installer SmartPLS atau project native yang dapat dibuka langsung.

Kecocokan perhitungan tidak membuktikan consent, seleksi responden323→271, kausalitas, atau seluruh validitas model.
