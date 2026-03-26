# -*- coding: utf-8 -*-
import sys
print(f"Python version: {sys.version}")

# 测试PyQt5导入
try:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
    print("PyQt5导入成功")
    
    # 测试基本功能
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("测试窗口")
    window.setGeometry(100, 100, 300, 200)
    
    label = QLabel("PyQt5工作正常！", window)
    label.setGeometry(50, 50, 200, 50)
    
    window.show()
    print("窗口显示成功")
    
    sys.exit(app.exec_())
except Exception as e:
    print(f"错误: {str(e)}")
    import traceback
    traceback.print_exc()
