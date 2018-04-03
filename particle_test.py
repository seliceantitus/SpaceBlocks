import random
import pygame
 
screen_size = (1200, 600)
 
class Color:
    BLACK = (0, 0, 0)
    DARK_GRAY = (200, 200, 200)
    BLUE = (0, 100, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
 
class Vector2:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
 
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
 
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
 
    def __mul__(self, val):
        return Vector2(self.x * val, self.y * val)
 
    def __truediv__(self, val):
        return Vector2(self.x / val, self.y / val)
 
    def coords(self):
        return (self.x, self.y)
     
    def __repr__(self):
        return str(self.coords())
 
surface_cache = {}
def get_surface(size, color):
    key = (size, color)
    if key not in surface_cache:
        surface = pygame.surface.Surface(size)
        surface.fill(color)
        surface_cache[key] = surface
    return surface_cache[key]
 
class Particle:
    def __init__(self, position=None, movement=None, color=Color.BLACK, age=10, width=1, height=1):
        # where it starts
        position.x -= width
        position.y -= height
        self.position = position
 
        # how far it should move, per second
        self.speed = movement
 
        self.age = 0
        self.max_age = age
        self.surface = get_surface((width, height), color)
        self.visible = True
 
    def update(self, delta=0):
        self.position += self.speed * delta / 1000
 
        self.age += delta / 1000
        alpha = 256 * (1 - (self.age / self.max_age))
        self.surface.set_alpha(alpha)
        return alpha > 0
 
    def draw(self, screen):
        screen.blit(self.surface, self.position.coords())
 
class ParticleEngine:
    def __init__(self, particle_count=0, color=Color.BLACK, width_range=(0, 1), height_range=(0, 1), x_start_range=(0, 1), y_start_range=(0, 1), x_direction_range=(1, 2), y_direction_range=(1, 2), age_range=(1, 2)):
        self.particle_count = particle_count
        self.color = color
        self.width_range = width_range
        self.height_range = height_range
        self.x_start_range = x_start_range
        self.x_direction_range = x_direction_range
        self.y_start_range = y_start_range
        self.y_direction_range = y_direction_range
        self.age_range = age_range
        self.particles = []
        self.spawn()
 
    def _generate_value(self, range):
        return min(range) + (random.random() * abs(range[0] - range[1]))
 
    def spawn(self):
        # don't spawn too many at once, so we don't slow down the update loop too much between draws
        per_tick = 100
        start_count = len(self.particles)
        while self.particle_count > len(self.particles) and len(self.particles) - start_count < per_tick:
            x_pos = self._generate_value(self.x_start_range)
            y_pos = self._generate_value(self.y_start_range)
            start_position = Vector2(x_pos, y_pos)
 
            x_move = self._generate_value(self.x_direction_range)
            y_move = self._generate_value(self.y_direction_range)
            movement = Vector2(x_move, y_move)
 
            max_age = self._generate_value(self.age_range)
            width = self._generate_value(self.width_range)
            height = self._generate_value(self.height_range)
             
            self.particles.append(Particle(position=start_position, movement=movement, color=self.color, age=max_age, width=width, height=height))
 
    def update(self, delta):
        self.spawn()
        # update all particles, removing those that have died
        self.particles = [particle for particle in self.particles if particle.update(delta)]
         
    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)
                 
def build_particle_engines():
    snow = ParticleEngine(
        particle_count=1000, color=Color.WHITE,
        width_range=(1, 3), height_range=(1, 5),
        x_start_range=(0, screen_size[0]), y_start_range=(0, 0),
        x_direction_range=(-5, 5), y_direction_range=(10, 50),
        age_range=(2, 15)
    )
 
    # less sleet than snow, but it falls faster
    # think of it as "heavier" than snow, so it also has less horizontal movement, and is smaller
    # this might look very similar to snow, but keep in mind that it's the minor changes that make things seem "real"
    sleet = ParticleEngine(
        particle_count=500, color=Color.DARK_GRAY,
        width_range=(1, 2), height_range=(2, 3),
        x_start_range=(0, screen_size[0]), y_start_range=(0, 0),
        x_direction_range=(-2, 2), y_direction_range=(40, 80),
        age_range=(1, 12)
    )
 
    center = screen_size[0] / 2
    fire = ParticleEngine(
        particle_count=10, color=Color.RED,
        width_range=(1, 2), height_range=(1, 5),
        x_start_range=(center, center), y_start_range=(screen_size[1], screen_size[1]),
        x_direction_range=(-5, 5), y_direction_range=(-50, -10),
        age_range=(1, 5)
    )
 
    warm_fire = ParticleEngine(
        particle_count=5, color=Color.YELLOW,
        width_range=(1, 2), height_range=(1, 2),
        x_start_range=(center, center), y_start_range=(screen_size[1], screen_size[1]),
        x_direction_range=(-5, 5), y_direction_range=(-10, -5),
        age_range=(1, 3)
    )
 
    return [snow, sleet, fire, warm_fire]
 
def game_loop():
    screen = pygame.display.set_mode(screen_size)
    engines = build_particle_engines()
    clock = pygame.time.Clock()
    delta = 0
 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == 27:
                return
 
        screen.fill(Color.BLACK)
 
        for engine in engines:
            engine.update(delta)
            engine.draw(screen)
 
        pygame.display.flip()
        # max fps=60
        delta = clock.tick(60)
 
pygame.init()
game_loop()
pygame.quit()