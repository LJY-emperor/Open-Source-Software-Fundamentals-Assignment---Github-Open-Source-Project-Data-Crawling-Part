import libcst as cst
from libcst.metadata import PositionProvider, MetadataWrapper
from libcst.codemod import CodemodCommand, ContextAwareTransformer
from libcst.matchers import findall, Call, Name

class TogaWidgetFinder(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(self):
        self.widget_calls = []

    def visit_Call(self, node):
        # 查找所有调用名为toga.的小部件初始化方法
        if isinstance(node.func, cst.Attribute) and isinstance(node.func.value, cst.Name) and node.func.value.value == 'toga':
            self.widget_calls.append(node)
        return True

def analyze_toga_widgets(file_path):
    with open(file_path, "r", encoding='utf-8') as source:
        wrapper = MetadataWrapper(cst.parse_module(source.read()))
        finder = TogaWidgetFinder()
        wrapper.visit(finder)

    for call in finder.widget_calls:
        print(f"Found widget creation: {call}")

# 包含Toga代码的文件叫app.py
analyze_toga_widgets('app.py')