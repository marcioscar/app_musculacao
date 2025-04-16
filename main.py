import flet as ft
import requests
from api import buscar_usuario, buscar_treino,registrar_treino, buscar_historico
from urllib.parse import  urlparse, parse_qs


def main(page: ft.Page):
    page.title = "Musculação APP"
    def home_page():
        logo = ft.Image(
            src="https://quattoracademia.com.br/logo_preto.svg",  
            width=50,
            height=50,
            fit=ft.ImageFit.FIT_WIDTH,
        )
        matricula_input = ft.TextField(label="Matrícula OU CPF", text_align=ft.TextAlign.CENTER, keyboard_type=ft.KeyboardType.NUMBER)
        
        def on_buscar_usuario(e):
            matricula = matricula_input.value
            if matricula:
                resultado = buscar_usuario(matricula)
                if resultado and resultado.get('name'):  # Se tem o nome do usuário
                    page.data = resultado
                    page.go("/registrar")
                    page.update()
                else:
                    page.open(ft.SnackBar(ft.Text(f"Aluno não encontrado ou Inativo")))
            else:
                page.open(ft.SnackBar(ft.Text(f" Por favor, digite uma matrícula ou CPF")))

        # Botão
        entrar_button = ft.ElevatedButton(
            text="Entrar", 
            width=200, 
            height=50, 
            on_click=on_buscar_usuario
        )
        

        # Organizando os elementos
        content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=logo,
                        padding=ft.padding.only(bottom=90, top=20)
                    ),
                    ft.Container(
                        content=matricula_input,
                        padding=ft.padding.only(bottom=20)
                    ),
                    ft.Container(
                        content=entrar_button
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            
            expand=True
        )

        safe_area = ft.SafeArea(
            content=content,
            maintain_bottom_view_padding=True
        )

        # Criando a view com o conteúdo e a barra de navegação
        view = ft.View(
            route="/",
            controls=[safe_area],
            bgcolor=ft.colors.GREY_100
        )
        page.views.append(view)

    def registrar_page():
        resultado = page.data  # Recupera o resultado
        def on_nav_change(e):
            if e.control.selected_index == 0:
                page.go("/")
            elif e.control.selected_index == 1:
                page.go("/registrar")
            elif e.control.selected_index == 2:
                page.go("/historico")
            page.update()

        # Navigation Bar
        nav_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.icons.HOME,
                    label="Home",
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.PERSON_3,
                    label="Treinos",
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.HISTORY,
                    label="Histórico",
                ),
            ],
            selected_index=1,
            bgcolor=ft.colors.ORANGE_500,
            indicator_color=ft.colors.WHITE,
            label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
            height=100,
            on_change=on_nav_change
        )

        logo = ft.Image(
            src="https://quattoracademia.com.br/logo_preto.svg",
            width=30,
            height=30,
            fit=ft.ImageFit.FIT_WIDTH,
        )
        

        avatar = ft.CircleAvatar(
            content=ft.Text(""),
            width=60,
            height=60,
        )
        
        if resultado["photo"]:
            avatar.foreground_image_src = resultado["photo"]

        card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=avatar,
                            title=ft.Text(resultado["name"]),
                            subtitle=ft.Text(
                                resultado["plano"]
                            ),
                        ),
                        
                    ]
                ),
                width=400,
                padding=10,
                
            )
        )
        grupos = ['ABDOME', 'BICEPS',"COSTAS",'GLUTEOS',"MEMBROS SUPERIORES 1",'MEMBROS SUPERIORES 2','MEMBROS INFERIORES GERAL','MEMBROS SUPERIORES GERAL' ,"OMBROS",'PANTURRILHA','PEITORAL','POSTERIORES DE COXAS','QUADS', 'TRICEPS']
        
        lista_grupos = ft.ListView(
            expand=True,
            spacing=10,
            padding=20,
            auto_scroll=False,
            height=500,  # Altura fixa para o ListView
        )
        for grupo in grupos:
            lista_grupos.controls.append(ft.Container(
                content=ft.Text(grupo, size=18, font_family="Arial", color=ft.colors.GREY_600),
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                padding=10,
               
                shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.GREY_300),
                on_click=lambda e, g=grupo: page.go(f"/treino?grupo={g}")
            ))

        content = ft.Column(
            controls=[logo, card, lista_grupos],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20, 
            expand=True,  
        )

        safe_area = ft.SafeArea(
            content=content,
            maintain_bottom_view_padding=True
        )

        # Criando a view com o conteúdo e a barra de navegação
        view = ft.View(
            route="/registrar",
            controls=[safe_area],
            navigation_bar=nav_bar
        )
        page.views.append(view)
        page.update()

    def treino_page(grupo):
        def on_nav_change(e):
            if e.control.selected_index == 0:
                page.go("/")
            elif e.control.selected_index == 1:
                page.go("/registrar")
            elif e.control.selected_index == 2:
                page.go("/historico")

            page.update()
        # Navigation Bar
        nav_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.icons.HOME,
                    label="Home",
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.PERSON_3,
                    label="Treinos",
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.HISTORY,
                    label="Histórico",
                ),
            ],
            selected_index=1,
            bgcolor=ft.colors.ORANGE_500,
            indicator_color=ft.colors.WHITE,
            label_behavior=ft.NavigationBarLabelBehavior.ONLY_SHOW_SELECTED,
            height=100,
            on_change=on_nav_change
        )
        
        treinos = buscar_treino(grupo)
        logo = ft.Image(
            src="https://quattoracademia.com.br/logo_preto.svg",
            width=30,
            height=30,
            fit=ft.ImageFit.FIT_WIDTH,
        )
        lista_exercicios = ft.ListView(
            expand=True,
            spacing=10,
            padding=20,
            auto_scroll=False,
            height=500,  # Altura fixa para o ListView
        )
        nome_grupo = ft.Text(grupo, size=22, weight=ft.FontWeight.BOLD, font_family="Arial", color=ft.colors.GREY_600)

        for exercicio in treinos:
            lista_exercicios.controls.append(ft.Container(
                content=ft.Column([    
                    ft.Row([
                        ft.Checkbox(
                            active_color=ft.colors.ORANGE_500,
                            width=30
                        ),
                        ft.Container(
                            content=ft.Text(
                                exercicio['nome'],
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                selectable=True
                            ),
                            width=300,
                            expand=True
                        ),
                    ]),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.icons.REPEAT, color=ft.colors.GREY_400),
                            ft.Text(
                                exercicio['Repeticoes'],
                                size=22,
                                weight=ft.FontWeight.BOLD,
                                font_family="Arial",
                                color=ft.colors.ORANGE_600
                            ),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        alignment=ft.alignment.center
                    ),
                    ft.Text(exercicio['obs']),
                ]),
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                padding=10,
                shadow=ft.BoxShadow(blur_radius=6, color=ft.colors.GREY_300),
            ))
        def on_registrar_treino(e):
            resultado = page.data 
            treinos = {
                "matricula": resultado["registration"],
                "grupo": grupo,
            }
            try:
                registrado = registrar_treino(treinos)
                if registrado and isinstance(registrado, dict):
                    page.open(ft.SnackBar(ft.Text(f" {grupo} atualizado com sucesso")))
                    print("Treino registrado com sucesso:", registrado)
                    page.go("/registrar")
                else:
                    print("Resposta inesperada da API:", registrado)
            except Exception as e:
                print(f"Erro ao registrar treino: {str(e)}")
                # Mostrar mensagem de erro para o usuário
              
            page.update()

         # Botão
        registar_button = ft.FilledButton(
            text="Registrar Treino", 
            width=300, 
            bgcolor=ft.colors.GREY_500,
            icon="add",
            on_click=on_registrar_treino
        )
        content = ft.Column(
            controls=[logo,nome_grupo,  lista_exercicios, registar_button],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20, 
            expand=True,  
        )

        safe_area = ft.SafeArea(
            content=content,
            maintain_bottom_view_padding=True
        )    

        view = ft.View(
            route="/treino",
            controls=[safe_area],
            navigation_bar=nav_bar
        )
        page.views.append(view)
        page.update()
        
    def historico_page():
        resultado = page.data
        historico = buscar_historico(resultado["registration"])
        
        historico_exercicios = ft.ListView(
            expand=True,
            spacing=10,
            padding=20,
            auto_scroll=False,
            height=550,  # Altura fixa para o ListView
        )
        for exercicio in historico:
            historico_exercicios.controls.append(ft.Container(
                content=ft.Column([
                    ft.Text(
                        exercicio['grupo'],
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.ORANGE_600
                    ),
                    ft.Text(
                        f" {exercicio['data']}",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.GREY_600,
                        text_align=ft.TextAlign.CENTER,
                        
                    )
                    
                ]
                
                ),
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                padding=10,
                shadow=ft.BoxShadow(blur_radius=6, color=ft.colors.GREY_300),
                
                        
            ))
        

        logo = ft.Image(
            src="https://quattoracademia.com.br/logo_preto.svg",
            width=30,
            height=30,
            fit=ft.ImageFit.FIT_WIDTH,
        )
        
        def on_nav_change(e):
            if e.control.selected_index == 0:
                page.go("/")
            elif e.control.selected_index == 1:
                page.go("/registrar")
            elif e.control.selected_index == 2:
                page.go("/historico")

            page.update()
        # Navigation Bar
        nav_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.icons.HOME,
                    label="Home",
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.PERSON_3,
                    label="Treinos",
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.HISTORY,
                    label="Histórico",
                ),
            ],
            selected_index=2,
            bgcolor=ft.colors.ORANGE_500,
            indicator_color=ft.colors.WHITE,
            label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
            height=100,
            on_change=on_nav_change
        )
        content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=logo,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=historico_exercicios,
                        alignment=ft.alignment.center,
                        expand=True
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20, 
                expand=True,  
            ),
            alignment=ft.alignment.center,
            expand=True
        )

        safe_area = ft.SafeArea(
            content=content,
            maintain_bottom_view_padding=True
        )    

        view = ft.View(
            route="/historico",
            controls=[safe_area],
            navigation_bar=nav_bar
        )
        page.views.append(view)
        page.update()
      



    def route_change(e):
        page.views.clear()

        if page.route == "/":
            home_page()
        elif page.route == "/registrar":
            registrar_page()

        elif page.route.startswith( "/treino"):
            parsed_url = urlparse(page.route)
            grupo = parse_qs(parsed_url.query)['grupo'][0]
            treino_page(grupo)

        elif page.route == "/historico":
            historico_page()

        

        page.update()    
            
    page.on_route_change = route_change
    page.go("/")

ft.app(main)

