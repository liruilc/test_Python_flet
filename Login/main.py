
# Magno Efren 
# https://www.youtube.com/@MagnoEfren/videos

import flet as ft 
body =  ft.Container(
            ft.Row([
                ft.Container(
                    ft.Column(controls= [
                        ft.Container(
                            ft.Image(
                                src='logo.png',
                                width=70,
                                ),
                            padding= ft.padding.only(150,20)
                            ),
                        ft.Text(
                            'Iniciar Sesión',
                            width=360,
                            size=30,
                            weight ='w900',# type: ignore
                            text_align = 'center'# type: ignore
                            ),
                        ft.Container(
                            ft.TextField(
                                width=280,
                                height=40,
                                hint_text= 'Correo electronico',
                                border ='underline',# type: ignore
                                color ='black',
                                prefix_icon = ft.icons.EMAIL,
                                ),
                                padding = ft.padding.only(20,10)
                            ),
                        ft.Container(
                            ft.TextField(
                                width=280,
                                height=40,
                                hint_text= 'Contraseña',
                                border ='underline',# type: ignore
                                color ='black',
                                prefix_icon = ft.icons.LOCK,
                                password = True,
                                ),
                                padding = ft.padding.only(20,10)
                            ),
                        ft.Container(
                            ft.Checkbox(
                                label ='Recordar contraseña', 
                                check_color='black'
                                ),
                            padding = ft.padding.only(40),
                            ),
                        ft.Container(
                            ft.ElevatedButton(
                                content = ft.Text(
                                    'INICIAR',
                                    color = 'white',
                                    weight ='w500',# type: ignore
                                    ),
                                width =280,
                                bgcolor = 'black',
                                ),
                                padding = ft.padding.only(25,10)
                            ),
                        ft.Container(
                            ft.Row([
                                ft.Text(
                                    '¿No tiene una cuenta?'
                                    ),
                                ft.TextButton(
                                    'Crear una cuenta'
                                    ),
                                ], spacing=8),
                            padding = ft.padding.only(40)
                            ),                                                               
                        ], 
                        alignment = ft.MainAxisAlignment.SPACE_EVENLY,       
                        ),
                    gradient= ft.LinearGradient(['red', 'orange']),     
                    width=380,
                    height =460,
                    border_radius=20
                ),
                ],
                alignment = ft.MainAxisAlignment.SPACE_EVENLY,
                ),
        padding= 10,
        )

def main(page:ft.Page):
    page.window_width =800# type: ignore
    page.window_height = 520# type: ignore
    page.padding = 0
    page.vertical_alignment = "center"# type: ignore
    page.horizontal_alignment = "center"# type: ignore
    #page.window_bgcolor = ft.colors.TRANSPARENT
    #page.window_title_bar_buttons_hidden = True
    #page.window_frameless = True
    #page.window_title_bar_hidden = True
    #page.bgcolor = ft.colors.TRANSPARENT
    page.add(
            body
        )

ft.app(target=main)
