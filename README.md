# check_bareos
Icinga2 check plugin for the bareos backup solution using the bareos RestAPI

Currently only the status of the last jobs of each client can be monitored

## Usage
```shell
    './check_bareos.py' '-H' '<ipaddress>' '-P' '<password>' '-p' '8080' '-u' '<user>'
```

## Output
```shell
[OK] 8 of 8 Jobs ok:
[OK] JobID: 67, host1 (Incremental), ExecutionTime: 00:00:10, (Usage: 180.0MB, Files: 187)
[OK] JobID: 66, host2 (Incremental), ExecutionTime: 00:00:09, (Usage: 375.88MB, Files: 190)
[OK] JobID: 65, host3 (Incremental), ExecutionTime: 00:00:15, (Usage: 166.83MB, Files: 948)
[OK] JobID: 64, host4 (Incremental), ExecutionTime: 00:00:12, (Usage: 277.75MB, Files: 6017)
[OK] JobID: 63, host5 (Incremental), ExecutionTime: 00:03:08, (Usage: 4.18GB, Files: 9457)
[OK] JobID: 62, host6 (Incremental), ExecutionTime: 00:01:08, (Usage: 1.14GB, Files: 132)
[OK] JobID: 61, host7 (Incremental), ExecutionTime: 00:00:11, (Usage: 148.93MB, Files: 82)
[OK] JobID: 59, host8 (Incremental), ExecutionTime: 00:00:58, (Usage: 945.1MB, Files: 415)

```