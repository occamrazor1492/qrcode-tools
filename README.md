# qrcode-tools

打包：
pyinstaller --onefile --add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk' --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl' -F -w getQrcode-modi.py

pyinstaller在这个目录里\AppData\Roaming\Python\Python39\Scripts>

不搞环境变量了
环境变量怎么搞https://kb.objectrocket.com/elasticsearch/build-a-stand-alone-executable-elasticsearch-application-using-python-646
