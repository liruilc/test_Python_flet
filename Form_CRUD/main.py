import flet as ft 
from contact_manager import ContactManager
from fpdf import FPDF
import pandas as pd
import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Tabla de Datos', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def create_form(page: ft.Page):
    # sourcery skip: assign-if-exp, boolean-if-exp-identity, remove-unnecessary-cast
    data_manager = ContactManager()
    selected_row = None

    name = ft.TextField(label="姓名", border_color="purple")
    age = ft.TextField(label="年龄", border_color="purple", 
                      input_filter=ft.NumbersOnlyInputFilter(),
                      max_length=2)
    email = ft.TextField(label="邮件", border_color="purple")
    phone = ft.TextField(label="电话", border_color="purple",
                        input_filter=ft.NumbersOnlyInputFilter(),
                        max_length=9)
    
    data_table = ft.DataTable(
        expand=True,
        border=ft.border.all(2, "purple"),
        border_radius=10,
        data_row_color={
            ft.ControlState.SELECTED: "purple400",  # 更柔和的紫色
            ft.ControlState.HOVERED: "purple100",   # 悬停效果
            ft.ControlState.PRESSED: "purple200"
        },
        show_checkbox_column=True,
        divider_thickness=0.5,        # 更细的分隔线
        heading_row_color="purple900", # 表头背景色
        heading_row_height=70,        # 更高的表头
        columns=[
            ft.DataColumn(
                ft.Text("姓名", 
                    color="white",
                    weight=ft.FontWeight.BOLD,
                    size=16
                ),
                tooltip="姓名 的联系方式"  # 添加工具提示
            ),
            ft.DataColumn(
                ft.Text("年龄",
                    color="white",
                    weight=ft.FontWeight.BOLD,
                    size=16
                ),
                tooltip="年龄 的联系方式"
            ),
            ft.DataColumn(
                ft.Text("邮件",
                    color="white", 
                    weight=ft.FontWeight.BOLD,
                    size=16
                ),
                tooltip="邮件 的联系方式",
                numeric=True
            ),
            ft.DataColumn(
                ft.Text("电话",
                    color="white",
                    weight=ft.FontWeight.BOLD,
                    size=16
                ),
                tooltip="电话号码",
                numeric=True
            ),
        ],
        column_spacing=50,  # 增加列间距
        horizontal_margin=10,  # 添加水平边距
    )

    def show_data():
        data_table.rows = []
        for x in data_manager.get_contacts():
            data_table.rows.append(
                ft.DataRow(
                    on_select_changed=lambda e, row=x: get_index(e, row),
                    cells=[
                        ft.DataCell(ft.Text(x[1])),
                        ft.DataCell(ft.Text(str(x[2]))),
                        ft.DataCell(ft.Text(x[3])),
                        ft.DataCell(ft.Text(str(x[4]))),
                    ]
                )
            )
        page.update()

    def add_data(e):
        if all([name.value, age.value, email.value, phone.value]):
            contact_exists = any(row[1] == name.value for row in data_manager.get_contacts())
            
            if not contact_exists:
                data_manager.add_contact(name.value, age.value, email.value, phone.value)
                clean_fields()
                show_data()
            else:
                print("该联系人已存在于数据库中.")
        else:
            print("输入您的详细信息")

    def get_index(e, row):
        nonlocal selected_row
        if e.control.selected:
            e.control.selected = False
        else:
            e.control.selected = True
        selected_row = row
        page.update()

    def edit_field_text(e):
        if selected_row:
            name.value = selected_row[1]
            age.value = selected_row[2]
            email.value = selected_row[3]
            phone.value = selected_row[4]
            page.update()
        else:
            print("先选择一行")

    def update_data(e):
        if selected_row and all([name.value, age.value, email.value, phone.value]):
            data_manager.update_contact(selected_row[0], name.value, age.value, 
                                     email.value, phone.value)
            clean_fields()
            show_data()

    def delete_data(e):
        if selected_row:
            data_manager.delete_contact(selected_row[1])
            show_data()
        else:
            print("先选择一行")

    def search_data(e):
        search = search_field.value.lower()# type: ignore
        filtered_data = [x for x in data_manager.get_contacts() 
                        if search in x[1].lower()]
        data_table.rows = []
        
        if search:
            for x in filtered_data:
                data_table.rows.append(
                    ft.DataRow(
                        on_select_changed=lambda e, row=x: get_index(e, row),
                        cells=[
                            ft.DataCell(ft.Text(x[1])),
                            ft.DataCell(ft.Text(str(x[2]))),
                            ft.DataCell(ft.Text(x[3])),
                            ft.DataCell(ft.Text(str(x[4]))),
                        ]
                    )
                )
        else:
            show_data()
        page.update()

    def clean_fields():
        name.value = ""
        age.value = ""
        email.value = ""
        phone.value = ""
        page.update()

    def save_pdf(e):
        pdf = PDF()
        pdf.add_page()
        column_widths = [10, 40, 20, 80, 40]
        data = data_manager.get_contacts()
        header = ("ID", "姓名", "年龄", "邮件", "电话")
        data.insert(0, header)
        for row in data:
            for item, width in zip(row, column_widths):
                pdf.cell(width, 10, str(item), border=1)
            pdf.ln()
        file_name = datetime.datetime.now().strftime("DATA %Y-%m-%d_%H-%M-%S") + ".pdf"
        pdf.output(file_name)

    def save_excel(e):
        file_name = datetime.datetime.now().strftime("DATA %Y-%m-%d_%H-%M-%S") + ".xlsx"
        contacts = data_manager.get_contacts()
        df = pd.DataFrame(contacts, columns=["ID", "姓名", "年龄", "邮件", "Teléfono"])
        df.to_excel(file_name, index=False)

    # Create form container
    form = ft.Container(
        bgcolor="#222222",
        border_radius=10,
        col=4,
        padding=20,  # 增加内边距
        expand=True,  # 让容器填充可用空间
        content=ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # 改为 SPACE_BETWEEN 以实现均匀分布
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,  # 让子元素水平拉伸
            expand=True,  # 让 Column 填充容器
            spacing=0,  # 移除默认间距，使用 SPACE_BETWEEN 来控制间距
            controls=[
                ft.Text(
                    "输入您的详细信息",
                    size=40,
                    text_align="center",# type: ignore
                    color="white",
                    font_family="Segoe Script",
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Container(
                    content=ft.Column(
                        spacing=60,  # 输入框之间的间距
                        controls=[
                            name,
                            age,
                            email,
                            phone,
                        ],
                    ),
                    expand=True,  # 让输入框区域可以伸缩
                ),
                ft.Container(
                    content=ft.Row(
                        spacing=25,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                content=ft.TextButton(
                                    text="保存",
                                    icon=ft.Icons.SAVE,
                                    icon_color="white",
                                    style=ft.ButtonStyle(
                                        color=ft.colors.WHITE,
                                        bgcolor=ft.colors.PURPLE,
                                        animation_duration=300,
                                        overlay_color={"hovered": ft.colors.PURPLE_200},# type: ignore
                                        side=ft.BorderSide(1, ft.colors.PURPLE_300),
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                    ),
                                    on_click=add_data,
                                    tooltip="保存新联系人",
                                ),
                                shadow=ft.BoxShadow(
                                    spread_radius=1,
                                    blur_radius=4,
                                    color="#6200EE4D",
                                    offset=ft.Offset(0, 2),
                                ),
                                padding=5,
                            ),
                            ft.Container(
                                content=ft.TextButton(
                                    text="更新",
                                    icon=ft.Icons.UPDATE,
                                    icon_color="white",
                                    style=ft.ButtonStyle(
                                        color=ft.colors.WHITE,
                                        bgcolor=ft.colors.PURPLE,
                                        animation_duration=300,
                                        overlay_color={"hovered": ft.colors.PURPLE_200},# type: ignore
                                        side=ft.BorderSide(1, ft.colors.PURPLE_300),
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                    ),
                                    on_click=update_data,
                                    tooltip="更新选定的联系人",
                                ),
                                shadow=ft.BoxShadow(
                                    spread_radius=1,
                                    blur_radius=4,
                                    color="#6200EE4D",
                                    offset=ft.Offset(0, 2),
                                ),
                                padding=5,
                            ),
                            ft.Container(
                                content=ft.TextButton(
                                    text="删除",
                                    icon=ft.Icons.DELETE,
                                    icon_color="white",
                                    style=ft.ButtonStyle(
                                        color=ft.colors.WHITE,
                                        bgcolor=ft.colors.PURPLE,
                                        animation_duration=300,
                                        overlay_color={"hovered": ft.colors.PURPLE_200},# type: ignore
                                        side=ft.BorderSide(1, ft.colors.PURPLE_300),
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                    ),
                                    on_click=delete_data,
                                    tooltip="删除选定的联系人",
                                ),
                                shadow=ft.BoxShadow(
                                    spread_radius=1,
                                    blur_radius=4,
                                    color="#6200EE4D",
                                    offset=ft.Offset(0, 2),
                                ),
                                padding=5,
                            ),
                        ]
                    )
                ),
            ]
        )
    )

    search_field = ft.TextField(
        suffix_icon=ft.Icons.SEARCH,
        label="搜索 姓名",
        border=ft.InputBorder.UNDERLINE,
        border_color="white",
        label_style=ft.TextStyle(color="white"),
        on_change=search_data,
    )

    # Create table container
    table = ft.Container(
        bgcolor="#222222",
        border_radius=10,
        padding=10,
        col=8,
        content=ft.Column(
            expand=True,
            controls=[
                ft.Container(
                    padding=10,
                    content=ft.Row(
                        controls=[
                            search_field,
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                on_click=edit_field_text,
                                icon_color="white",
                            ),
                            ft.IconButton(
                                tooltip="下载 PDF",
                                icon=ft.Icons.PICTURE_AS_PDF,
                                icon_color="white",
                                on_click=save_pdf,
                            ),
                            ft.IconButton(
                                tooltip="下载 EXCEL",
                                icon=ft.Icons.SAVE_ALT,
                                icon_color="white",
                                on_click=save_excel,
                            ),
                        ]
                    ),
                ),
                ft.Column(
                    expand=True,
                    scroll="auto",# type: ignore
                    controls=[
                        ft.ResponsiveRow([data_table])
                    ]
                )
            ]
        )
    )

    # Create main container
    main_container = ft.ResponsiveRow(
        controls=[form, table]
    )

    # Initial data load
    show_data()
    
    return main_container

def create_action_button(text, icon, on_click):
    return ft.TextButton(
        text=text,
        icon=icon,
        icon_color="white",
        style=ft.ButtonStyle(
            color="white",
            bgcolor="purple",
            animation_duration=300,  # 添加动画效果
            side={  # 添加边框效果
                ft.MaterialState.DEFAULT: ft.BorderSide(1, "purple300"),# type: ignore
                ft.MaterialState.HOVERED: ft.BorderSide(2, "purple100"),# type: ignore
            },
            shape={  # 圆角形状
                ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=8),# type: ignore
                ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=12),# type: ignore
            },
            shadow=ft.BoxShadow(  # 添加阴影# type: ignore
                spread_radius=1,
                blur_radius=4,
                color=ft.colors.with_opacity(0.3, "purple"),
            ),
        ),
        on_click=on_click,
    )
def main(page: ft.Page):
    page.bgcolor = "black"
    page.title = "CRUD SQLite"
    page.window.min_width = 1100
    page.window.min_height = 500
    
    form = create_form(page)
    page.add(form)
    page.update()

if __name__ == "__main__":
    ft.app(main)