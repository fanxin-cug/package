# package
地图投影（双标准正等角圆锥投影）
将经纬度坐标转换为大地坐标并绘制地图
#使用的第三方库：numpy和pyplotlib

#文件说明
1.txt是黑龙江省经纬度数据
2.txt是中国地图经纬度数据
map.py -1.txt -figure1.png
map1.py -2.txt -figure2.png
map2.py -2.txt -figure3.png
map1是在每个region求最低纬度
map2是指定一个最低纬度
