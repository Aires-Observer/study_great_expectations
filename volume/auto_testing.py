import os

current_dir = os.path.dirname(os.path.abspath(__file__))
failed_scripts = []

for file in os.listdir('.'):
    if file.startswith('test_') and os.path.isfile(file):
        file_path = os.path.join(current_dir, file)
        print(f"Running {file}...")
        ret = os.system(f"python {file_path}") # 退出码如果是0则表示成功，非0则表示失败
        if ret != 0:
            failed_scripts.append(file)

if not failed_scripts:
    print("所有测试脚本均执行成功！")
else:
    print("有测试脚本执行失败：")
    for file in failed_scripts:
        print(f"  - {file}")