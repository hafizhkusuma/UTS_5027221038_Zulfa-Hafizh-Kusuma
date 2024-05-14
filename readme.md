Berikut adalah dokumentasi dalam bentuk markdown file untuk proyek yang telah Anda kerjakan:

# Dokumentasi Sistem Manajemen Poin Mahasiswa

Dokumentasi ini memberikan gambaran umum tentang Sistem Manajemen Poin Mahasiswa yang diimplementasikan menggunakan gRPC dan Python.

## Persyaratan

Untuk menjalankan Sistem Manajemen Poin Mahasiswa, Anda memerlukan persyaratan berikut:

- Python 3.x
- Tkinter (untuk GUI)
- gRPC
- MongoDB
- colorama

Anda dapat menginstal dependensi dengan menggunakan pip:

```bash
pip install grpcio grpcio-tools protobuf colorama
```

## Gambaran Implementasi

Sistem Manajemen Poin Mahasiswa terdiri dari dua komponen utama: server yang diimplementasikan dalam Python menggunakan gRPC, dan klien yang diimplementasikan baik lewat terminal maupun menggunakan Tkinter untuk antarmuka pengguna grafis. MongoDB digunakan sebagai database untuk menyimpan informasi mahasiswa.

### Implementasi gRPC

gRPC (Google Remote Procedure Call) adalah kerangka kerja RPC open-source yang memungkinkan komunikasi antara sistem yang terdistribusi. Dalam sistem ini, gRPC digunakan untuk mendefinisikan antarmuka layanan dan mengimplementasikan pemanggilan prosedur jarak jauh antara klien dan server.

Implementasi gRPC melibatkan langkah-langkah berikut:

1. **Mendefinisikan Layanan**: Antarmuka layanan didefinisikan menggunakan Protocol Buffers (protobuf). Antarmuka layanan mencakup metode RPC untuk menambahkan, memperbarui, mendapatkan, dan menghapus poin mahasiswa.

2. **Menghasilkan Kode**: Definisi layanan protobuf dikompilasi menggunakan kompilator `protoc` untuk menghasilkan kode klien dan server dalam Python.

3. **Mengimplementasikan Server**: Server mengimplementasikan antarmuka layanan yang didefinisikan dalam file protobuf. Ini mencakup metode untuk menangani operasi tambah, perbarui, dapatkan, dan hapus pada poin mahasiswa. MongoDB digunakan sebagai database backend untuk menyimpan informasi mahasiswa.

4. **Mengimplementasikan Klien**: Aplikasi klien berinteraksi dengan server menggunakan kode klien gRPC yang dihasilkan. Ini menyediakan antarmuka pengguna grafis (GUI) menggunakan Tkinter untuk memungkinkan pengguna melakukan operasi CRUD pada poin mahasiswa.

### Integrasi MongoDB

MongoDB adalah database NoSQL yang digunakan untuk menyimpan informasi mahasiswa dalam Sistem Manajemen Poin Mahasiswa. Integrasi MongoDB melibatkan langkah-langkah berikut:

1. **Persiapan Database**: MongoDB diinstal dan dikonfigurasi pada sistem lokal atau server jarak jauh.

2. **Koneksi Database**: Server membangun koneksi ke database MongoDB menggunakan pustaka PyMongo. Data mahasiswa disimpan dalam koleksi MongoDB.

3. **Operasi Data**: Server melakukan operasi CRUD pada data mahasiswa yang disimpan dalam koleksi MongoDB. Ini termasuk menambahkan, memperbarui, mendapatkan, dan menghapus poin mahasiswa.

## Struktur Berkas

Struktur berkas proyek adalah sebagai berikut:

```
student_management_system/
│
├── student.proto            # Berkas definisi Protocol Buffers gRPC
├── student_pb2.py           # Kode Python gRPC yang dihasilkan (protobuf)
├── student_pb2_grpc.py      # Kode Python gRPC yang dihasilkan (protobuf)
├── student_server.py        # Implementasi server gRPC
├── student_client.py        # Implementasi klien baris perintah
└── student_client_ui.py     # Implementasi klien GUI berbasis Tkinter
```

## Penggunaan

Untuk menjalankan Sistem Manajemen Poin Mahasiswa, ikuti langkah-langkah berikut:

1. **Memulai MongoDB**: Pastikan MongoDB berjalan pada sistem lokal Anda atau server jarak jauh.

2. **Menjalankan Server**: Mulai server gRPC dengan menjalankan skrip `student_server.py`:

   ```bash
   python student_server.py
   ```

3. **Menjalankan Klien**: Anda dapat memilih untuk menjalankan klien baris perintah (`student_client.py`) atau klien GUI (`student_client_ui.py`):

   Klien baris perintah:
   ```bash
   python student_client.py
   ```

   Klien GUI:
   ```bash
   python student_client_ui.py
   ```

4. **Melakukan Operasi**: Gunakan antarmuka klien untuk menambahkan, memperbarui, mendapatkan, dan menghapus poin mahasiswa sesuai kebutuhan.

## Kesimpulan

Sistem Manajemen Poin Mahasiswa menunjukkan penggunaan gRPC untuk membangun komunikasi yang efisien dan skalabel antara sistem yang terdistribusi. Dengan mengintegrasikan MongoDB sebagai database backend, sistem menyediakan solusi yang kokoh untuk mengelola informasi dan poin mahasiswa. Antarmuka pengguna grafis yang diimplementasikan menggunakan Tkinter meningkatkan pengalaman pengguna dan membuat sistem mudah digunakan.

Dengan peningkatan dan penambahan lebih lanjut, seperti otentikasi, logging, dan penanganan kesalahan, Sistem Manajemen Poin Mahasiswa dapat diperluas untuk memenuhi persyaratan berbagai lembaga pendidikan dan organisasi.