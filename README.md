# `check_bareos.py`

A monitoring check plugin for the **Bareos** backup solution using the **Bareos REST API**.

This script provides a concise status overview of all backup jobs executed within the **last 24 hours**. It is suitable for integration with monitoring systems such as Nagios, Icinga, or custom dashboards.

---

## 🛠️ Usage

```shell
'./check_bareos.py' '-H' '<ipaddress>' '-P' '<password>' '-p' '8080' '-u' '<user>'
```

### Arguments:

- `-H` — Hostname or IP address of the Bareos Director  
- `-P` — Password for authentication  
- `-p` — REST API port (default: `8080`)  
- `-u` — API username  

---

## 📊 Example Output

```shell
[OK] 8 of 8 Jobs ok:
[OK] JobID: 138 - host1 (Level: INC, RunTime: 00:00:17, Status: TERMINATING, Use: 296.78MB, Files: 67)
[OK] JobID: 137 - host2 (Level: INC, RunTime: 00:00:02, Status: TERMINATING, Use: 17.81MB, Files: 17)
[OK] JobID: 136 - host3 (Level: INC, RunTime: 00:00:02, Status: TERMINATING, Use: 51.18MB, Files: 332)
[OK] JobID: 135 - host4 (Level: INC, RunTime: 00:02:15, Status: TERMINATING, Use: 1.9GB, Files: 515)
[OK] JobID: 134 - host5 (Level: INC, RunTime: 00:00:39, Status: TERMINATING, Use: 603.24MB, Files: 63)
[OK] JobID: 133 - host6 (Level: INC, RunTime: 00:00:01, Status: TERMINATING, Use: 8.03MB, Files: 9)
[OK] JobID: 132 - host7 (Level: INC, RunTime: 00:00:02, Status: TERMINATING, Use: 8.21MB, Files: 22)
[OK] JobID: 131 - host8 (Level: INC, RunTime: 00:01:02, Status: TERMINATING, Use: 1.03GB, Files: 128)
```

Each line includes:
- ✅ **Job ID**
- 🖥️ **Host name**
- 🗂️ **Backup level** (e.g., `INC` for incremental)
- ⏱️ **Execution time**
- 📌 **Job status** (e.g., `TERMINATING`)
- 💾 **Data usage**
- 📄 **Number of files backed up**

---

## ✅ Return Codes

- `0` — All jobs OK  
- `1` — One or more jobs failed or in warning state  
- `2` — Critical: API unreachable or invalid credentials  

---

## 📦 Dependencies

- Python ≥ 3.6  
- Requests (`pip install requests`)

---

May your backups remain ever intact,  
**– check_bareos.py**
