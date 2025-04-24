import flet as ft
import requests
from api import buscar_usuario, buscar_treino,registrar_treino, buscar_historico
from urllib.parse import  urlparse, parse_qs


def main(page: ft.Page):
    page.title = "Quattor Musculação"

    # Cupertino Navigation Bar (definida fora das funções de página)
    def on_nav_change(e):
        if e.control.selected_index == 0:
            page.go("/")
        elif e.control.selected_index == 1:
            page.go("/registrar")
        elif e.control.selected_index == 2:
            page.go("/historico")
        page.update()

    nav_bar = ft.CupertinoNavigationBar(
        bgcolor=ft.colors.ORANGE_500,
        inactive_color=ft.colors.WHITE70,
        active_color=ft.colors.BLACK,
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
        height=100,
        on_change=on_nav_change
    )

    def home_page():
        nav_bar.selected_index = 0
        nav_bar.active_color = ft.colors.BLACK
        nav_bar.inactive_color = ft.colors.WHITE70
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
            navigation_bar=nav_bar,
            bgcolor=ft.colors.GREY_100
        )
        page.views.append(view)

    def registrar_page():
        nav_bar.selected_index = 1
        nav_bar.active_color = ft.colors.BLACK
        nav_bar.inactive_color = ft.colors.WHITE70
        if not page.data:
            page.open(ft.SnackBar(ft.Text("Por favor, entre com uma matrícula ou CPF")))
            page.go("/")
            return
        resultado = page.data  # Recupera o resultado
        
        

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

    def registrar_exercicio(e, exercicio, grupo):
        resultado = page.data
        # Encontrar o campo de carga no container pai
        container = e.control.parent.parent.parent
        # O campo de carga está na terceira linha (índice 2) do Column
        campo_carga = container.content.controls[2].controls[0]
        carga = campo_carga.value if campo_carga.value else "0"
        
        treino = {
            "matricula": resultado["registration"],
            "grupo": grupo,
            "nome": exercicio["nome"],
            "carga": carga
        }
        try:
            registrado = registrar_treino(treino)
            if registrado and isinstance(registrado, dict):
                # Mudar a cor do botão e desabilitá-lo
                botao = e.control
                botao.bgcolor = ft.colors.GREEN
                botao.color = ft.colors.WHITE
                botao.disabled = True
                botao.text = "✓"
                page.open(ft.SnackBar(ft.Text(f"Exercício {exercicio['nome']} registrado com sucesso!")))
            else:
                page.open(ft.SnackBar(ft.Text(f"Erro ao registrar exercício {exercicio['nome']}")))
        except Exception as e:
            page.open(ft.SnackBar(ft.Text(f"Erro ao registrar exercício: {str(e)}")))
        page.update()

    def treino_page(grupo):
        nav_bar.selected_index = 1
        nav_bar.active_color = ft.colors.BLACK
        nav_bar.inactive_color = ft.colors.WHITE70
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
            container = ft.Container(
                content=ft.Column([
                    # Nome do exercício
                    ft.Row([
                        ft.Text(
                            exercicio['nome'],
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            selectable=True,
                            width=300,
                            
                            overflow=ft.TextOverflow.ELLIPSIS
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START
                    ),
                    # Repetições
                    ft.Row([
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.icons.REPEAT, color=ft.colors.GREY_400),
                                ft.Text(
                                    exercicio['Repeticoes'],
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.ORANGE_600
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                            )
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START
                    ),
                    # Carga
                    ft.Row([
                        ft.TextField(
                            label="Carga",
                            text_align=ft.TextAlign.CENTER,
                            width='full',
                            height=42,
                            border_width=1,
                            border_color=ft.colors.GREY_300,
                            border_radius=10,
                            bgcolor=ft.colors.GREY_50,

                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                    ),
                    # Botão Registrar
                    ft.Row([
                        ft.ElevatedButton('+',
                            # icon=ft.icons.DONE,
                            width=50,
                            height=20,
                            # color=ft.colors.WHITE,
                            bgcolor=ft.colors.ORANGE_100,
                            on_click=lambda e, ex=exercicio: registrar_exercicio(e, ex, grupo)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END
                    )
                ],
                spacing=10
                ),
                padding=ft.padding.all(10),
                expand=True,
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.GREY_300)
            )
            lista_exercicios.controls.append(container)
        def on_registrar_treino(e):
            resultado = page.data 
            exercicios_selecionados = []
            
            # Coletar exercícios selecionados e suas cargas
            for container in lista_exercicios.controls:
                # Acessar o conteúdo do Container que é um Column
                column = container.content
                # Acessar o primeiro Container dentro do Column que contém o Row
                row_container = column.controls[0]
                # Acessar o Row dentro do Container
                row = row_container.content
                checkbox = row.controls[0]
                nome_exercicio = row.controls[1].value
                # Acessar o campo de carga que está no terceiro Container do Column
                campo_carga = column.controls[2].content
                carga = campo_carga.value
                
                if checkbox.value:  # Se o exercício foi selecionado
                    exercicios_selecionados.append({
                        "nome": nome_exercicio,
                        "carga": carga if carga else "0"
                    })
            
            if not exercicios_selecionados:
                page.open(ft.SnackBar(ft.Text("Selecione pelo menos um exercício")))
                return
                
            for exercicio in exercicios_selecionados:
                treino = {
                    "matricula": resultado["registration"],
                    "grupo": grupo,
                    "nome": exercicio["nome"],
                    "carga": exercicio["carga"]
                }
                try:
                    registrado = registrar_treino(treino)
                    if registrado and isinstance(registrado, dict):
                        print(f"Exercício {exercicio['nome']} registrado com sucesso:", registrado)
                    else:
                        print(f"Resposta inesperada da API para {exercicio['nome']}:", registrado)
                except Exception as e:
                    print(f"Erro ao registrar exercício {exercicio['nome']}: {str(e)}")
            
            page.open(ft.SnackBar(ft.Text(f"Treino de {grupo} registrado com sucesso")))
            page.go("/registrar")
            page.update()

         # Botão
        # registar_button = ft.FilledButton(
        #     text="Registrar Treino", 
        #     width=300, 
        #     bgcolor=ft.colors.GREY_500,
        #     icon="add",
        #     on_click=on_registrar_treino
        # )
        content = ft.Column(
            controls=[nome_grupo,  lista_exercicios ],
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
        nav_bar.selected_index = 2
        nav_bar.active_color = ft.colors.BLACK
        nav_bar.inactive_color = ft.colors.WHITE70
        if not page.data:
            page.open(ft.SnackBar(ft.Text("Por favor, entre com uma matrícula ou CPF")))
            page.go("/")
            return
        resultado = page.data
        historico = buscar_historico(resultado["registration"])
        
        historico_exercicios = ft.ListView(
            expand=True,
            spacing=10,
            padding=20,
            auto_scroll=False,
            height=550,
        )

        for grupo, exercicios in historico.items():
            # Container para o grupo
            grupo_container = ft.Container(
                content=ft.Column([
                    ft.Text(
                        grupo,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.ORANGE_600
                    ),
                    # Lista de exercícios do grupo
                    ft.ListView(
                        controls=[
                            ft.Container(
                                content=ft.Column([
                                    ft.Row([
                                        ft.Text(
                                            exercicio['nome'],
                                            size=15,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.colors.GREY_600,
                                            width=250
                                        ),
                                        ft.Text(
                                            f"{exercicio['carga']}kg",
                                            size=16,
                                            color=ft.colors.ORANGE_500
                                        )
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                    ft.Text(
                                        f"Data: {exercicio['data']}",
                                        size=14,
                                        color=ft.colors.GREY_400
                                    )
                                ]),
                                bgcolor=ft.colors.WHITE,
                                border_radius=10,
                                padding=10,
                                shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.GREY_300),
                            ) for exercicio in exercicios
                        ],
                        spacing=5,
                        height=len(exercicios) * 80
                    )
                ]),
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                padding=10,
                shadow=ft.BoxShadow(blur_radius=6, color=ft.colors.GREY_300),
            )
            historico_exercicios.controls.append(grupo_container)

        logo = ft.Image(
            src="https://quattoracademia.com.br/logo_preto.svg",
            width=30,
            height=30,
            fit=ft.ImageFit.FIT_WIDTH,
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

