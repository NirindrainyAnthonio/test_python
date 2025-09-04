import random
import sys

import pygame

# ============================
# Paramètres du jeu
# ============================
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
CELL_SIZE = 20

FPS = 10  # Vitesse du jeu (peut être modifiée)

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
YELLOW = (200, 200, 0)

# Directions
UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"


# ============================
# Classe Snake
# ============================
class Snake:
    def __init__(self):
        self.positions = [(100, 100), (80, 100), (60, 100)]
        self.direction = RIGHT
        self.grow = False

    def move(self):
        head_x, head_y = self.positions[0]

        if self.direction == RIGHT:
            new_head = (head_x + CELL_SIZE, head_y)
        elif self.direction == LEFT:
            new_head = (head_x - CELL_SIZE, head_y)
        elif self.direction == UP:
            new_head = (head_x, head_y - CELL_SIZE)
        elif self.direction == DOWN:
            new_head = (head_x, head_y + CELL_SIZE)

        # Ajouter une nouvelle tête
        self.positions = [new_head] + self.positions

        # Si on ne doit pas grandir, on supprime la dernière partie
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False

    def change_direction(self, new_direction):
        """Changer la direction sans autoriser les demi-tours directs"""
        opposite = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
        if opposite.get(new_direction) != self.direction:
            self.direction = new_direction

    def grow_snake(self):
        """Activer la croissance du serpent"""
        self.grow = True

    def check_collision(self):
        """Vérifier si le serpent se mord ou sort de l'écran"""
        head_x, head_y = self.positions[0]

        # Collision avec les murs
        if (
            head_x < 0
            or head_x >= WINDOW_WIDTH
            or head_y < 0
            or head_y >= WINDOW_HEIGHT
        ):
            return True

        # Collision avec lui-même
        if (head_x, head_y) in self.positions[1:]:
            return True

        return False

    def draw(self, surface):
        """Dessiner le serpent"""
        for i, pos in enumerate(self.positions):
            if i == 0:  # La tête
                pygame.draw.rect(
                    surface, YELLOW, (pos[0], pos[1], CELL_SIZE, CELL_SIZE)
                )
            else:
                pygame.draw.rect(surface, GREEN, (pos[0], pos[1], CELL_SIZE, CELL_SIZE))


# ============================
# Classe Food
# ============================
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        """Mettre la nourriture à une position aléatoire"""
        self.position = (
            random.randint(0, (WINDOW_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
            random.randint(0, (WINDOW_HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
        )

    def draw(self, surface):
        """Dessiner la nourriture"""
        pygame.draw.rect(
            surface, RED, (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE)
        )


# ============================
# Fonction principale
# ============================
def game_loop():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("🐍 Snake Game")

    snake = Snake()
    food = Food()
    score = 0

    font = pygame.font.SysFont("Arial", 24, bold=True)

    while True:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(RIGHT)

        # Déplacer le serpent
        snake.move()

        # Vérifier les collisions
        if snake.check_collision():
            game_over(screen, score)

        # Vérifier si le serpent mange la nourriture
        if snake.positions[0] == food.position:
            score += 10
            snake.grow_snake()
            food.randomize_position()

        # Dessiner
        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)

        # Afficher le score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)


# ============================
# Écran de Game Over
# ============================
def game_over(screen, score):
    font_big = pygame.font.SysFont("Arial", 50, bold=True)
    font_small = pygame.font.SysFont("Arial", 30)

    screen.fill(BLUE)
    text = font_big.render("GAME OVER", True, WHITE)
    score_text = font_small.render(f"Votre score: {score}", True, YELLOW)
    restart_text = font_small.render(
        "Appuyez sur ESPACE pour rejouer ou ESC pour quitter", True, WHITE
    )

    screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, 100))
    screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, 180))
    screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, 250))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()  # Rejouer
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


# ============================
# Lancement du jeu
# ============================
if __name__ == "__main__":
    game_loop()
