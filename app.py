from flask import Flask, request, render_template, redirect, url_for

# Mengimpor kelas Flask dari modul flask.
# Flask: Kelas utama untuk membuat aplikasi web.
# request: Objek yang berisi semua data dari permintaan HTTP yang masuk (form, query params, headers, dll.).
# render_template: Fungsi untuk merender file template HTML (misalnya login.html, admin.html).
# redirect: Fungsi untuk mengarahkan pengguna ke URL lain.
# url_for: Fungsi untuk membangun URL untuk fungsi view tertentu, ini lebih baik daripada menulis URL secara manual karena otomatis menyesuaikan jika nama fungsi berubah.

app = Flask(__name__)

# Membuat instance aplikasi Flask.
# __name__ adalah variabel khusus Python yang akan berisi nama modul saat ini.
# Ini memberi tahu Flask di mana mencari template dan file statis.

# --- Simulasi Database Pengguna ---
# Ini adalah "database" sederhana kita berupa dictionary.
# Di dunia nyata, kamu akan menggunakan database seperti PostgreSQL atau MySQL.
USERS_DB = {
    "admin": "admin_pass",       # Username: admin, Password: admin_pass
    "user1": "user_pass",        # Username: user1, Password: user_pass
    "guest": "guest_pass"        # Username: guest, Password: guest_pass
}
# Ini adalah dictionary Python yang berfungsi sebagai simulasi database pengguna.
# Setiap kunci (key) adalah username, dan nilai (value) adalah password yang terkait.
# Konsep: Dalam aplikasi nyata, kamu akan berinteraksi dengan database sungguhan (misal SQL) untuk menyimpan dan mengambil data pengguna.

# ----------------------------------

# --- Route untuk Menampilkan Form Login (GET request) ---
# Saat seseorang mengakses URL utama ("/") dengan metode GET,
# kita akan menampilkan halaman login.html.
@app.route("/", methods=["GET"])
# Ini adalah "decorator" Flask. Ini mengikat fungsi `show_login_form` ke URL "/".
# `methods=["GET"]` berarti fungsi ini hanya akan merespons permintaan HTTP dengan metode GET.
# Contoh: Ketika kamu mengetik `http://127.0.0.1:5000/` di browser dan menekan Enter, itu adalah permintaan GET.
def show_login_form():
    # Mengambil pesan error dari URL query parameter jika ada (setelah redirect dari /proses_login)
    error_message = request.args.get("error")
    # `request.args` adalah dictionary berisi semua parameter query dari URL (setelah tanda '?').
    # `get("error")` mencoba mengambil nilai dari parameter bernama "error".
    # Jika URL-nya `/?error=Username%20atau%20Password%20salah.`, maka `error_message` akan berisi "Username atau Password salah.".
    # Konsep: Meneruskan data antar halaman melalui URL, sering digunakan untuk pesan status atau error.
    return render_template("login.html", error=error_message)
    # Merender file HTML bernama "login.html".
    # `error=error_message` meneruskan variabel `error_message` ke dalam template HTML,
    # sehingga kamu bisa menampilkannya di `login.html` menggunakan `{{ error }}`.
    # Konsep: Pemisahan logika (Python) dari presentasi (HTML) menggunakan template engine.

# --- Route untuk Memproses Login (POST request) ---
# Saat form login disubmit (metode POST) ke URL "/proses_login",
# logika ini akan dijalankan.
@app.route("/proses_login", methods=["POST"])
# Mengikat fungsi `process_login` ke URL "/proses_login".
# `methods=["POST"]` berarti fungsi ini hanya akan merespons permintaan HTTP dengan metode POST.
# Contoh: Saat kamu mengisi form login di `login.html` dan menekan tombol submit, browser akan mengirimkan permintaan POST ke URL ini.
def process_login():
    # Mengambil data username dan password dari form HTML
    username = request.form.get("username")
    # `request.form` adalah dictionary berisi semua data yang dikirimkan melalui form HTML (metode POST).
    # `get("username")` mengambil nilai dari input form dengan atribut `name="username"`.
    password = request.form.get("password")
    # Mengambil nilai dari input form dengan atribut `name="password"`.
    # Konsep: Mengakses data yang dikirimkan oleh pengguna melalui form.

    # Memeriksa kredensial pengguna di USERS_DB
    if username in USERS_DB and USERS_DB[username] == password:
    # Memeriksa apakah `username` ada sebagai kunci di `USERS_DB`.
    # Dan juga memeriksa apakah password yang dimasukkan cocok dengan password yang tersimpan di `USERS_DB` untuk username tersebut.
    # Konsep: Logika otentikasi sederhana.

        # Jika login berhasil:
        if username == "admin":
            # Jika user adalah 'admin', arahkan ke halaman admin
            return redirect(url_for("admin_dashboard"))
            # Mengarahkan browser pengguna ke URL yang dihasilkan oleh fungsi `admin_dashboard`.
            # `url_for("admin_dashboard")` akan menghasilkan string "/admin_dashboard".
            # Konsep: Pengalihan URL setelah tindakan berhasil (misalnya login).
        else:
            # Untuk user lain, arahkan ke dashboard pengguna
            # Kita mengirim username sebagai bagian dari URL
            return redirect(url_for("user_dashboard", username=username))
            # Mengarahkan ke URL yang dihasilkan oleh fungsi `user_dashboard`.
            # `username=username` akan menyertakan username sebagai bagian dari URL,
            # contoh: `/user_dashboard/user1`.
            # Konsep: Dynamic URL berdasarkan data yang relevan.
    else:
        # Jika login gagal, arahkan kembali ke halaman login
        # dan sertakan pesan error melalui query parameter di URL
        return redirect(url_for("show_login_form", error="Username atau Password salah."))
        # Mengarahkan kembali ke fungsi `show_login_form` (URL "/")
        # dan menyertakan parameter query `error` dengan pesan kesalahan.
        # Ini akan menghasilkan URL seperti `/?error=Username%20atau%20Password%20salah.`.
        # Konsep: Penanganan error dan umpan balik pengguna.

# --- Route untuk Halaman Admin ---
# Hanya bisa diakses setelah login sebagai 'admin'.
@app.route("/admin_dashboard")
# Mengikat fungsi `admin_dashboard` ke URL "/admin_dashboard".
def admin_dashboard():
    return render_template("admin.html")
    # Merender template HTML khusus untuk admin.
    # Konsep: Halaman yang dilindungi atau diakses berdasarkan peran pengguna.

# --- Route untuk Halaman Dashboard Pengguna ---
# Bisa diakses oleh semua pengguna non-admin yang berhasil login.
# URL-nya akan menyertakan username (misal: /user_dashboard/user1)
@app.route("/user_dashboard/<username>")
# Mengikat fungsi `user_dashboard` ke URL "/user_dashboard/<username>".
# `<username>` adalah bagian dinamis dari URL. Apapun yang ada di posisi itu
# akan ditangkap dan diteruskan sebagai argumen `username` ke fungsi.
# Contoh: Jika URL-nya `/user_dashboard/john_doe`, maka `username` dalam fungsi akan berisi "john_doe".
def user_dashboard(username):
    # Mengirim username ke template untuk ditampilkan
    return render_template("user_dashboard.html", username=username)
    # Merender template `user_dashboard.html` dan meneruskan variabel `username` ke dalamnya.
    # Konsep: URL dinamis dan personalisasi konten berdasarkan pengguna.

# --- Menjalankan Aplikasi Flask ---
# app.run(debug=True) digunakan saat pengembangan,
# ini akan otomatis me-reload server saat ada perubahan kode dan menampilkan debugger.
# app.run(debug=False) atau cukup app.run() digunakan saat produksi,
# lebih aman dan stabil.
if __name__ == "__main__":
    try:
        app.run(debug=True) # Kamu bisa ganti ke False untuk mencoba mode produksi
    except Exception as e:
        print(f"\n--- An error occurred during Flask app startup ---")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {e}")
        import traceback
        traceback.print_exc() # Ini akan mencetak full traceback untuk lebih detail
        print(f"---------------------------------------------------\n")
