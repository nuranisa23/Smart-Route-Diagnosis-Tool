import os
import re
import platform
import time
from colorama import Fore, Style, init

# Inisialisasi colorama agar warna terminal aktif
init(autoreset=True)

def run_traceroute(target):
    """Menjalankan traceroute dan mengembalikan hasilnya sebagai list per baris."""
    print(Fore.CYAN + f"\n🚀 Menjalankan traceroute ke {target}...\n")
    command = f"traceroute {target}" if platform.system().lower() != "windows" else f"tracert {target}"
    result = os.popen(command).read()
    return result.splitlines()

def analyze_hop(line, hop_num):
    """Menganalisis satu baris hasil traceroute dan memberikan diagnosis."""
    if "*" in line:
        return f"Hop ke-{hop_num}: ⚠️ Timeout — kemungkinan ada firewall atau node tidak merespons."

    # Ambil nilai delay (ms)
    delays = re.findall(r"(\d+\.\d+)\s*ms", line)
    if not delays:
        return f"Hop ke-{hop_num}: ❌ Tidak ada data delay."

    # Konversi delay ke float dan hitung rata-rata
    avg_delay = sum(map(float, delays)) / len(delays)
    
    # Diagnosis berdasarkan delay
    if avg_delay > 200:
        return f"Hop ke-{hop_num}: 🔴 Terlalu lambat ({avg_delay:.1f} ms). Kemungkinan jaringan padat atau jauh."
    elif avg_delay > 100:
        return f"Hop ke-{hop_num}: 🟠 Sedikit lambat ({avg_delay:.1f} ms)."
    else:
        return f"Hop ke-{hop_num}: 🟢 Normal ({avg_delay:.1f} ms)."

def diagnose_traceroute(output_lines):
    """Memberikan analisis otomatis dari hasil traceroute."""
    print(Fore.YELLOW + "\n📊 Hasil Diagnosa Jaringan:\n" + Style.RESET_ALL)
    hop_count = 0
    timeout_count = 0
    for line in output_lines:
        match = re.match(r"\s*(\d+)\s", line)
        if match:
            hop_count += 1
            diagnosis = analyze_hop(line, hop_count)
            print(diagnosis)
            if "Timeout" in diagnosis:
                timeout_count += 1

    # Ringkasan akhir
    print("\n" + "-" * 50)
    print(Fore.CYAN + f"📡 Total Hop: {hop_count}")
    print(Fore.RED + f"⏱️ Timeout Ditemukan: {timeout_count}")
    if timeout_count == 0:
        print(Fore.GREEN + "✅ Rute stabil tanpa hambatan besar.")
    elif timeout_count < 3:
        print(Fore.YELLOW + "⚠️ Rute relatif stabil, namun ada beberapa hop tidak merespons.")
    else:
        print(Fore.RED + "❌ Banyak hop tidak merespons — kemungkinan rute terblokir atau jaringan bermasalah.")
    print("-" * 50)

def main():
    print(Fore.CYAN + "===== 🧠 SMART ROUTE DIAGNOSIS TOOL =====" + Style.RESET_ALL)
    target = input("Masukkan domain atau IP tujuan: ")
    start_time = time.time()
    result_lines = run_traceroute(target)
    diagnose_traceroute(result_lines)
    duration = time.time() - start_time
    print(Fore.YELLOW + f"\n⏳ Analisis selesai dalam {duration:.1f} detik.\n")

if __name__ == "__main__":
    main()
