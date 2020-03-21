import sys    # para usar exit()
import pygame

ANCHO = 640 # Ancho de la pantalla.
ALTO = 480  # Alto de la pantalla.
color_azul = (0, 0, 64)  # Color azul para el fondo.

class Bolita(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen
        self.image = pygame.image.load('img/bolita.png')
        # Obtener rectÃ¡ngulo de la imagen
        self.rect = self.image.get_rect()
        # PosiciÃ³n inicial centrada en pantalla.
        self.rect.centerx = ANCHO / 2
        self.rect.centery = ALTO / 2
        # Establecer velocidad inicial.
        self.speed = [3, 3]

    def update(self):
        # Evitar que salga por debajo.
        if self.rect.bottom >= ALTO or self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
        # Evitar que salga por la derecha.
        elif self.rect.right >= ANCHO or self.rect.left <= 0:
            self.speed[0] = -self.speed[0]
        # Mover en base a posiciÃ³n actual y velocidad.
        self.rect.move_ip(self.speed)

class Paleta(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen
        self.image = pygame.image.load('img/paleta.png')
        # Obtener rectÃ¡ngulo de la imagen
        self.rect = self.image.get_rect()
        # PosiciÃ³n inicial centrada en pantalla en X.
        self.rect.midbottom = (ANCHO / 2, ALTO - 20)
        # Establecer velocidad inicial.
        self.speed = [0, 0]

    def update(self, evento):
        # Buscar si se presionÃ³ flecha izquierda.
        if evento.key == pygame.K_LEFT and self.rect.left > 0:
            self.speed = [-5, 0]
        # Si se presionÃ³ flecha derecha.
        elif evento.key == pygame.K_RIGHT and self.rect.right < ANCHO:
            self.speed = [5, 0]
        else:
            self.speed = [0, 0]
        # Mover en base a posiciÃ³n actual y velocidad.
        self.rect.move_ip(self.speed)

class Ladrillo(pygame.sprite.Sprite):
    def __init__(self, posicion):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen
        self.image = pygame.image.load('img/ladrillo.png')
        # Obtener rectÃ¡ngulo de la imagen
        self.rect = self.image.get_rect()
        # PosiciÃ³n inicial, provista externamente.
        self.rect.topleft = posicion

class Muro(pygame.sprite.Group):
    def __init__(self, cantidadLadrillos):
        pygame.sprite.Group.__init__(self)

        pos_x = 0
        pos_y = 20
        for i in range(cantidadLadrillos):
            ladrillo = Ladrillo((pos_x, pos_y))
            self.add(ladrillo)

            pos_x += ladrillo.rect.width
            if pos_x >= ANCHO:
                pos_x = 0
                pos_y += ladrillo.rect.height

# Inicializando pantalla.
pantalla = pygame.display.set_mode((ANCHO, ALTO))
# Configurar tÃ­tulo de pantalla.
pygame.display.set_caption('Juego de ladrillos')
# Crear el reloj.
reloj = pygame.time.Clock()
# Ajustar repeticiÃ³n de evento de tecla presionada.
pygame.key.set_repeat(30)

bolita = Bolita()
jugador = Paleta()
muro = Muro(50)

while True:
    # Establecer FPS.
    reloj.tick(60)

    # Revisar todos los eventos.
    for evento in pygame.event.get():
        # Si se presiona la tachita de la barra de tÃ­tulo,
        if evento.type == pygame.QUIT:
            # cerrar el videojuego.
            sys.exit()
        # Buscar eventos del teclado,
        elif evento.type == pygame.KEYDOWN:
            jugador.update(evento)

    # Actualizar posiciÃ³n de la bolita.
    bolita.update()

    # ColisiÃ³n entre bolita y jugador.
    if pygame.sprite.collide_rect(bolita, jugador):
        bolita.speed[1] = -bolita.speed[1]

    # ColisiÃ³n de la bolita con el muro.
    lista = pygame.sprite.spritecollide(bolita, muro, False)
    if lista:
        ladrillo = lista[0]
        cx = bolita.rect.centerx
        if cx < ladrillo.rect.left or cx > ladrillo.rect.right:
            bolita.speed[0] = -bolita.speed[0]
        else:
            bolita.speed[1] = -bolita.speed[1]
        muro.remove(ladrillo)

    # Rellenar la pantalla.
    pantalla.fill(color_azul)
    # Dibujar bolita en pantalla.
    pantalla.blit(bolita.image, bolita.rect)
    # Dibujar jugador en pantalla.
    pantalla.blit(jugador.image, jugador.rect)
    # Dibujar el muro (con los ladrillos que tiene)
    muro.draw(pantalla)
    # Actualizar los elementos en pantalla.
    pygame.display.flip()