# Sistem Fuzzy Penentuan Rating Performa Pemain CS2

Sistem Logika Fuzzy (Metode Mamdani) untuk menentukan rating performa pemain Counter-Strike 2 (CS2) berdasarkan statistik performa individu.

## Deskripsi Masalah
Penilaian performa pemain seringkali hanya didasarkan pada jumlah eliminasi (K/D). Sistem ini hadir untuk memberikan penilaian yang lebih adil dengan menggabungkan dua aspek krusial:
1. **ADR (Average Damage per Round)**: Mengukur kontribusi serangan/kerusakan yang diberikan kepada musuh.
2. **K/D Ratio**: Mengukur efisiensi eliminasi dan daya tahan hidup.

## Variabel Fuzzy

### 1. Input: ADR (Average Damage per Round)
- **Rendah**: < 65
- **Normal**: 55 - 95
- **Tinggi**: > 85

### 2. Input: K/D Ratio
- **Kecil**: < 1.0
- **Sedang**: 0.8 - 1.4
- **Besar**: > 1.2

### 3. Output: Match Rating
- **Bronze**: 0 - 50
- **Silver**: 40 - 70
- **Gold**: 65 - 90
- **MVP**: 85 - 100

## Aturan Fuzzy (9 Rules)
Sistem menggunakan 9 aturan inferensi untuk menentukan rating:
1. IF ADR Tinggi AND K/D Besar THEN MVP
2. IF ADR Tinggi AND K/D Sedang THEN Gold
3. IF ADR Tinggi AND K/D Kecil THEN Silver
4. IF ADR Normal AND K/D Besar THEN Gold
5. IF ADR Normal AND K/D Sedang THEN Silver
6. IF ADR Normal AND K/D Kecil THEN Bronze
7. IF ADR Rendah AND K/D Besar THEN Silver
8. IF ADR Rendah AND K/D Sedang THEN Bronze
9. IF ADR Rendah AND K/D Kecil THEN Bronze




