## 简介
本项目是基于[Pi Dashboard](https://github.com/nxez/pi-dashboard)进行的修改

## 已发现问题
- windows cpu温度无法获取
- windows 内存的CACHED无法获取
- windows 获取cpu名称暂未实现，可以参考以下代码
```python
# pip install wmi
# pip install pypiwin32
import wmi
cpuinfo = wmi.WMI()
for cpu in cpuinfo.Win32_Processor():
    print("您的CPU名称为:" + cpu.Name) # 11th Gen Intel(R) Core(TM) i7-1165G7 @ 2.80GHz
```