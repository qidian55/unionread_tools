## 首订统计
1. 将书籍整理成类似`8_1.csv`的格式，命名为`月_日.csv`（待统计日期）。若存在作者信息缺失，整理成`8_1.txt`的格式，命名为`月_日.txt`（待统计日期）。
2. 将`subscribe_count.py`中`count_data=['8','1']`修改为待统计日期。
3. 运行`subscribe_count.py`，实时输出结果并保存至`月_日_result.csv`。
4. 运行`pretty.py 月_日_result.csv`，输出格式化表格。