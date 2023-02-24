# server.py
from flask import Flask, render_template, jsonify
import psutil,os,datetime,platform,getpass,socket,subprocess

app = Flask(__name__)

global net_up,net_do
net_up = -1
net_do = -1


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_info', methods=["POST"])
def get_info():
    try:
        global net_up,net_do
        # cpu线程数
        thread_count = psutil.cpu_count()
        # 获取SWAP信息
        swap = psutil.swap_memory()

        # 获取磁盘吞吐量
        disk_io_counters = psutil.disk_io_counters()
        disk_read = round(disk_io_counters.read_bytes / (1024**2), 1)
        disk_write = round(disk_io_counters.write_bytes /(1024**2) ,1)
        disk_io = str(disk_read) + "MB|" +str(disk_write) + "MB"
        # 获取SWAP总量
        swap_total = round(swap.total / (1024.0 ** 2), 2)

        # 获取SWAP使用率
        swap_percent = swap.percent

        # 版本
        version = platform.version()

        # 获取cpu类型
        cpu_model = platform.processor()
        if cpu_model == "":
            output = subprocess.check_output(['cat', '/proc/cpuinfo']).decode('utf-8')
            for line in output.split('\n'):
                if 'model name' in line:
                    cpu_model = line.split(':')[1].strip()

        # 获取cpu名称
        cpu_name = platform.platform()

        # 获取CPU温度
        try:
            cpu_temp = psutil.sensors_temperatures().get('coretemp')[0].current
        except:
            cpu_temp = "0"

        # 获取cpu内核数
        num_cpus = psutil.cpu_count(logical=False)

        # 获取本机IP
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)

        # 获取用户名
        username = getpass.getuser()

        # 获取系统名称
        # system_name = os.uname().sysname
        system_name = platform.system()

        # 获取 CPU 架构
        # cpu_arch = os.uname().machine
        cpu_arch = platform.machine()

        # 获取总存储大小
        total_size = 0
        for part in psutil.disk_partitions():
            usage = psutil.disk_usage(part.mountpoint)
            total_size += usage.total
        total_storage = round(total_size / (1024 ** 3), 2)

        # 获取总存储已使用百分比
        used_size = 0
        for part in psutil.disk_partitions():
            usage = psutil.disk_usage(part.mountpoint)
            used_size += usage.used
        used_storage = round(used_size / total_size * (10 ** 2), 2)

        # 获取内存大小及内存使用量
        memory = psutil.virtual_memory()
        mem_sy = int(memory.available / (1024.0 ** 2))
        total_memory = round(memory.total / (1024.0 ** 3), 2)
        memory_usage = round(memory.used / (1024.0 ** 3) / total_memory * (10 ** 2), 2)

        # 获取流量总上传及下载
        net_io_counters = psutil.net_io_counters()
        total_upload = round(net_io_counters.bytes_sent / (1024.0 ** 3), 2)
        total_download = round(net_io_counters.bytes_recv / (1024.0 ** 3), 2)
        upload = round(net_io_counters.bytes_sent/(1024**2), 3)
        download = round(net_io_counters.bytes_recv / (1024.0 ** 2), 3)
        if net_do == -1 and net_up == -1:
            net_do = download
            net_up = upload
            net_do_rec = net_do
            net_up_rec = net_up
        else:
            net_do_rec = round(abs(net_do-download),2)
            net_up_rec = round(abs(net_up-upload),2)
            net_do = download
            net_up = upload
        # 获取负载
        # load = os.getloadavg()
        load = 0.0
        for load1 in psutil.getloadavg():
            load += load1
        load = round(load, 3)
        # cpu使用率
        cpu_percent = psutil.cpu_percent(interval=1)

        # cpu空闲
        cpu_kx = 100-cpu_percent

        # 获取进程数
        process_count = len(psutil.pids())

        # 获取连接数
        connection_count = len(psutil.net_connections())

        # 获取开机日期
        uptime_date = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d")
        
        # 开机时间
        uptime = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%H:%M:%S")

        # 获取当前日期
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        # 当前时间
        date_time = datetime.datetime.now().strftime("%H:%M:%S")
        
        # 获取CPU频率，单位为MHz
        freq = int(psutil.cpu_freq().current)

        data = {
            'code': 200,
            'text': 'ok',
            'system_name': system_name,
            'cpu_arch': cpu_arch,
            'total_memory': total_memory,
            'memory_usage': memory_usage,
            'total_upload': total_upload,
            'total_download': total_download,
            'load': load,
            'process_count': process_count,
            'connection_count': connection_count,
            'uptime': uptime,
            'date': date,
            'time': date_time,
            'uptime_date': uptime_date,
            'username': username,
            'ip': ip,
            'hostname': hostname,
            'cpu_freq': freq,
            'cpu_sums': num_cpus,
            'cpu_temp': cpu_temp,
            'cpu_model': cpu_model,
            'disk_free': total_storage,
            'disk_percent': used_storage,
            'cpu_kx': cpu_kx,
            'version': version,
            'cpu_used': cpu_percent,
            'swap_size': swap_total,
            'swap_used': swap_percent,
            'thread_count': thread_count,
            'mem_sy': mem_sy,
            'net_upload':net_up_rec,
            'net_download':net_do_rec,
            'cached': disk_io,
            'cpu_name': cpu_name
        }
    except Exception as err:
        data = {
            'code': 404,
            'text': str(err)
        }
    return data

if __name__ == '__main__':
    app.run(host='::', port=5219, debug=False)
