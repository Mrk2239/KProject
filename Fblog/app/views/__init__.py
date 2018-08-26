# 从自己的子模块中导入蓝图对象

# 将所有子view收归在一起，方便将来from app.views import XXX,YYY,AAA,...
from app.views.main import mainbp
from app.views.posts import postbp
from app.views.users import userbp

# 可以吗？？？——不可以，因为当前模块执行
# from manage import app