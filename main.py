# -- existing imports and initializations --
import pygame
import sys
import random
import time
from MazeGenerator import generateMaze  # Import the generateMaze function

pygame.init()

# Screen settings
WIDTH, HEIGHT = 832, 640
TILE_SIZE = 64
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EcoBlock Simulator")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ASSETS_PATH = "assets/"

MAXCAPACITY = 20
MAXSPEED = 8

# Load sounds
dropTrash_sound = pygame.mixer.Sound(ASSETS_PATH + "SFX/Drop Trash.mp3")
pickupTrash_sound = pygame.mixer.Sound(ASSETS_PATH + "SFX/Pickup Trash.mp3")
storeTrash_sound = pygame.mixer.Sound(ASSETS_PATH + "SFX/Store Trash.mp3")
bg_music = pygame.mixer.Sound(ASSETS_PATH + "SFX/Bg Music.mp3")
bg_music.set_volume(0.3)
bg_music.play(-1)

# Load images
grass_img = pygame.transform.scale(pygame.image.load(ASSETS_PATH + "grass.png"), (TILE_SIZE, TILE_SIZE))
sidewalk_img = pygame.transform.scale(pygame.image.load(ASSETS_PATH + "sidewalk.png"), (TILE_SIZE, TILE_SIZE))
house_img = pygame.transform.scale(pygame.image.load(ASSETS_PATH + "house.png"), (TILE_SIZE, TILE_SIZE))
bin_img = pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Trash Bin.png"), (TILE_SIZE, TILE_SIZE))
bot_img = {"walk": {
            "north": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Playable/North 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Playable/North 2.png"), (TILE_SIZE, TILE_SIZE)),
            ],
            "south": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Playable/South 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Playable/South 2.png"), (TILE_SIZE, TILE_SIZE)),
            ],
            "east": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Playable/East 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Playable/East 2.png"), (TILE_SIZE, TILE_SIZE)),
            ],
            "west": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Playable/West 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Playable/West 2.png"), (TILE_SIZE, TILE_SIZE)),
            ]
        }}

trash_images = [
    pygame.transform.scale(pygame.image.load(ASSETS_PATH + "plastic-bottle.png"), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load(ASSETS_PATH + "plastic.png"), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load(ASSETS_PATH + "eaten-apple.png"), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load(ASSETS_PATH + "fishbone.png"), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load(ASSETS_PATH + "battery.png"), (TILE_SIZE, TILE_SIZE))
]

# NPC types
npc_imgs = {
    "educated": {
        "walk": {
            "north": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Educated-NPC/North 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Educated-NPC/North 2.png"), (TILE_SIZE, TILE_SIZE)),
            ],
            "south": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Educated-NPC/South 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Educated-NPC/South 2.png"), (TILE_SIZE, TILE_SIZE)),
            ],
            "east": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Educated-NPC/East 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Educated-NPC/East 2.png"), (TILE_SIZE, TILE_SIZE)),
            ],
            "west": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Educated-NPC/West 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Educated-NPC/West 2.png"), (TILE_SIZE, TILE_SIZE)),
            ]
        }
    },
    "normal": {
        "walk": {
            "north": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Neutral-NPC/North 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Neutral-NPC/North 2.png"), (TILE_SIZE, TILE_SIZE)),
            ],
            "south": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Neutral-NPC/South 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Neutral-NPC/South 2.png"), (TILE_SIZE, TILE_SIZE)),
            ],
            "east": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Neutral-NPC/East 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Neutral-NPC/East 2.png"), (TILE_SIZE, TILE_SIZE)),
            ],
            "west": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Neutral-NPC/West 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Neutral-NPC/West 2.png"), (TILE_SIZE, TILE_SIZE)),
            ]
        }
    },
    "non-educated": {
        "walk": {
            "north": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Non-Educated-NPC/North 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Non-Educated-NPC/North 2.png"), (TILE_SIZE, TILE_SIZE)),
            ],
            "south": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Non-Educated-NPC/South 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Non-Educated-NPC/South 2.png"), (TILE_SIZE, TILE_SIZE)),
            ],
            "east": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Non-Educated-NPC/East 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Non-Educated-NPC/East 2.png"), (TILE_SIZE, TILE_SIZE)),
            ],
            "west": [
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Non-Educated-NPC/West 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Non-Educated-NPC/West 2.png"), (TILE_SIZE, TILE_SIZE)),
            ]
        }
    }
}

tile_map = [["grass" for _ in range(COLS)] for _ in range(ROWS)]

class TrashBin:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        screen.blit(bin_img, (self.x * TILE_SIZE, self.y * TILE_SIZE))

def generate_maze():
    global tile_map
    try:
        with open("maze.txt", "r") as file:
            lines = file.readlines()
            # Dynamically resize tile_map based on the maze dimensions
            tile_map = [["grass" for _ in range(len(lines[0].strip().split()))] for _ in range(len(lines))]
            for i, line in enumerate(lines):
                for j, char in enumerate(line.strip().split()):
                    if char == 'c':  # 'c' represents a sidewalk
                        tile_map[i][j] = 'sidewalk'
                    elif char in ['w', 'u']:  # 'w' and 'u' represent grass
                        tile_map[i][j] = 'grass'
                    elif char == 't':  # 't' represents a trash bin
                        tile_map[i][j] = 'trash_bin'
    except FileNotFoundError:
        print("Error: maze.txt not found. Please ensure the file exists in the same directory.")
        sys.exit(1)
        
generate_maze()

def place_houses():
    for _ in range(10):
        while True:
            x, y = random.randint(0, COLS - 1), random.randint(0, ROWS - 1)
            if tile_map[y][x] == "sidewalk":
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    house_x, house_y = x + dx, y + dy
                    if 0 <= house_x < COLS and 0 <= house_y < ROWS and tile_map[house_y][house_x] == "grass":
                        tile_map[house_y][house_x] = "house"
                        break
                break

place_houses()

def place_trash_bins():
    bins = []
    for y in range(ROWS):
        for x in range(COLS):
            if tile_map[y][x] == "trash_bin":  # Check if the tile is marked as a trash bin
                bins.append(TrashBin(x, y))
    return bins

# Generate trash bins
bins = place_trash_bins()

def draw_tile(x, y):
    tile_type = tile_map[y][x]
    if tile_type == "grass":
        screen.blit(grass_img, (x * TILE_SIZE, y * TILE_SIZE))
    elif tile_type == "sidewalk":
        screen.blit(sidewalk_img, (x * TILE_SIZE, y * TILE_SIZE))
    elif tile_type == "house":
        screen.blit(grass_img, (x * TILE_SIZE, y * TILE_SIZE))
        screen.blit(house_img, (x * TILE_SIZE, y * TILE_SIZE))
    elif tile_type == "trash_bin":
        screen.blit(grass_img, (x * TILE_SIZE, y * TILE_SIZE))
        screen.blit(bin_img, (x * TILE_SIZE, y * TILE_SIZE))

class Trash:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = random.choice(trash_images)

    def draw(self):
        screen.blit(self.image, (self.x * TILE_SIZE, self.y * TILE_SIZE))

class Bot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pixel_x = x * TILE_SIZE
        self.pixel_y = y * TILE_SIZE
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        self.speed = 4
        self.moving = False
        self.capacity = 5  # Maximum trash capacity
        self.current_trash = 0  # Current trash count

        # Animation attributes
        self.direction = "south"  # Default direction
        self.anim_frame = 0
        self.anim_timer = 0
        self.frame_interval = 6  # Frames before switching animation

        # Initialize the image with the first frame of the default direction
        self.image = bot_img["walk"][self.direction][self.anim_frame]

    def get_image(self):
        """Get the current animation frame based on direction and frame index."""
        return bot_img["walk"][self.direction][self.anim_frame % 2]

    def move(self, direction, is_walkable):
        if self.moving:
            return

        # Determine the next position based on the input direction
        if direction == "up":
            next_x, next_y = self.x, self.y - 1
            self.direction = "north"
        elif direction == "down":
            next_x, next_y = self.x, self.y + 1
            self.direction = "south"
        elif direction == "left":
            next_x, next_y = self.x - 1, self.y
            self.direction = "west"
        elif direction == "right":
            next_x, next_y = self.x + 1, self.y
            self.direction = "east"

        # Check if the next position is walkable
        if is_walkable(next_x, next_y):
            self.x, self.y = next_x, next_y
            self.target_x = self.x * TILE_SIZE
            self.target_y = self.y * TILE_SIZE
            self.moving = True

    def update(self, trash_list, bins):
        global money
        if self.moving:
            dx = self.target_x - self.pixel_x
            dy = self.target_y - self.pixel_y

            if abs(dx) <= self.speed and abs(dy) <= self.speed:
                self.pixel_x = self.target_x
                self.pixel_y = self.target_y
                self.moving = False

                # Check for trash at the current position and pick it up
                for trash in trash_list[:]:  # Use a copy of the list to avoid modification issues
                    if self.x == trash.x and self.y == trash.y:
                        if self.current_trash < self.capacity:
                            self.current_trash += 1
                            trash_list.remove(trash)
                            pickupTrash_sound.play()

                # Check if standing on a trash bin
                for bin in bins:
                    if self.x == bin.x and self.y == bin.y and self.current_trash > 0:
                        money += self.current_trash  # Earn $1 per trash
                        self.current_trash = 0  # Empty the trash
                        storeTrash_sound.play()  # Play sound when storing trash
            else:
                self.pixel_x += self.speed if dx > 0 else -self.speed if dx < 0 else 0
                self.pixel_y += self.speed if dy > 0 else -self.speed if dy < 0 else 0

        # Update animation timer and frame
        self.anim_timer += 1
        if self.anim_timer >= self.frame_interval:
            self.anim_frame = (self.anim_frame + 1) % 2
            self.image = self.get_image()
            self.anim_timer = 0

    def draw(self):
        screen.blit(self.image, (self.pixel_x, self.pixel_y))

class NPC:
    def __init__(self, x, y, npc_type):
        self.x, self.y = x, y
        self.npc_type = npc_type
        self.pixel_x = x * TILE_SIZE
        self.pixel_y = y * TILE_SIZE
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        self.speed = 3
        self.prev_pos = None
        self.moving = False
        self.direction = "south"  # Default direction
        self.anim_frame = 0
        self.anim_timer = 0
        self.frame_interval = 5
        self.capacity = 3 if npc_type == "educated" else 0  # Educated NPCs have a capacity
        self.current_trash = 0  # Current trash count
        self.returning_to_bin = False  # Whether the NPC is returning to a trash bin
        
        # Initialize the image with the first frame of the default direction
        self.image = npc_imgs[npc_type]["walk"][self.direction][self.anim_frame]

    def get_image(self):
        if self.npc_type == "normal":
            return npc_imgs["normal"]["walk"][self.direction][self.anim_frame % 2]
        elif self.npc_type == "educated":
            return npc_imgs["educated"]["walk"][self.direction][self.anim_frame % 2]
        else:
            return npc_imgs["non-educated"]["walk"][self.direction][self.anim_frame % 2]

    def bfs(self, start, target, is_walkable):
        """Perform BFS to find the shortest path to the target."""
        queue = [(start, [])]  # (current_position, path)
        visited = set()

        while queue:
            (current_x, current_y), path = queue.pop(0)
            if (current_x, current_y) in visited:
                continue
            visited.add((current_x, current_y))

            # If we reach the target, return the path
            if (current_x, current_y) == target:
                return path

            # Explore neighbors
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = current_x + dx, current_y + dy
                if is_walkable(nx, ny) and (nx, ny) not in visited:
                    queue.append(((nx, ny), path + [(nx, ny)]))

        return None  # No path found

    def move(self, trash_list, bins):
        if self.moving:
            return

        def is_walkable(x, y):
            return 0 <= x < COLS and 0 <= y < ROWS and tile_map[y][x] in ["sidewalk", "trash_bin"]

        # If returning to a trash bin
        if self.returning_to_bin:
            nearest_bin = None
            shortest_path = None
            for bin in bins:
                path = self.bfs((self.x, self.y), (bin.x, bin.y), is_walkable)
                if path and (shortest_path is None or len(path) < len(shortest_path)):
                    nearest_bin = bin
                    shortest_path = path

            if shortest_path:
                next_x, next_y = shortest_path[0]

                # Calculate direction before updating position
                dx = next_x - self.x
                dy = next_y - self.y
                if dx == 1:
                    self.direction = "east"
                elif dx == -1:
                    self.direction = "west"
                elif dy == 1:
                    self.direction = "south"
                elif dy == -1:
                    self.direction = "north"

                # Update position
                self.prev_pos = (self.x, self.y)
                self.x, self.y = next_x, next_y

                # Check if the NPC has reached the trash bin
                if self.x == nearest_bin.x and self.y == nearest_bin.y:
                    global money
                    money += self.current_trash  # Earn $1 per trash
                    self.current_trash = 0  # Empty the trash
                    self.returning_to_bin = False  # Resume collecting trash

                    # Reset animation to idle frame
                    self.anim_frame = 0
                    self.image = self.get_image()

                self.target_x = self.x * TILE_SIZE
                self.target_y = self.y * TILE_SIZE
                self.moving = True
                return
        
        # If the NPC is educated, use BFS to find the nearest trash
        if self.npc_type == "educated" and trash_list:
            nearest_trash = None
            shortest_path = None
            for trash in trash_list:
                path = self.bfs((self.x, self.y), (trash.x, trash.y), is_walkable)
                if path and (shortest_path is None or len(path) < len(shortest_path)):
                    nearest_trash = trash
                    shortest_path = path

            # If a path to trash is found, move toward it
            if shortest_path:
                next_x, next_y = shortest_path[0]  # Take the first step in the path

                dx = next_x - self.x
                dy = next_y - self.y
                if dx == 1:
                    self.direction = "east"
                elif dx == -1:
                    self.direction = "west"
                elif dy == 1:
                    self.direction = "south"
                elif dy == -1:
                    self.direction = "north"

                self.prev_pos = (self.x, self.y)
                self.x, self.y = next_x, next_y
                

                # Pick up the trash if at the same position
                for trash in trash_list[:]:
                    if self.x == trash.x and self.y == trash.y:
                        if self.current_trash < self.capacity:
                            self.current_trash += 1
                            trash_list.remove(trash)

                        # Check if capacity is full
                        if self.current_trash >= self.capacity:
                            self.returning_to_bin = True

                self.target_x = self.x * TILE_SIZE
                self.target_y = self.y * TILE_SIZE
                self.moving = True
                return

        # Random movement if no trash is found
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = self.x + dx, self.y + dy
            if is_walkable(nx, ny):
                neighbors.append((nx, ny))

        if neighbors:
            self.prev_pos = (self.x, self.y)
            next_x, next_y = random.choice(neighbors)

            dx = next_x - self.x
            dy = next_y - self.y
            if dx == 1:
                self.direction = "east"
            elif dx == -1:
                self.direction = "west"
            elif dy == 1:
                self.direction = "south"
            elif dy == -1:
                self.direction = "north"

            self.x, self.y = next_x, next_y
            self.target_x = self.x * TILE_SIZE
            self.target_y = self.y * TILE_SIZE
            self.moving = True

            # Educated NPC picks up trash at the new position
            if self.npc_type == "educated":
                for trash in trash_list[:]:  # Use a copy of the list to avoid modification issues
                    if self.x == trash.x and self.y == trash.y:
                        if self.current_trash < self.capacity:
                            self.current_trash += 1
                            trash_list.remove(trash)

                        # Check if capacity is full
                        if self.current_trash >= self.capacity:
                            self.returning_to_bin = True

    def update(self, trash_list):
        if self.moving:
            dx = self.target_x - self.pixel_x
            dy = self.target_y - self.pixel_y

            if abs(dx) <= self.speed and abs(dy) <= self.speed:
                self.pixel_x = self.target_x
                self.pixel_y = self.target_y
                self.moving = False
            else:
                self.pixel_x += self.speed if dx > 0 else -self.speed if dx < 0 else 0
                self.pixel_y += self.speed if dy > 0 else -self.speed if dy < 0 else 0

        # Update animation timer and frame
        self.anim_timer += 1
        if self.anim_timer >= self.frame_interval:
            self.anim_frame = (self.anim_frame + 1) % 2
            self.image = self.get_image()
            self.anim_timer = 0

         # Throw trash based on type
        if random.random() < 0.02:
            should_throw = False
            if self.npc_type == "non-educated":
                should_throw = True
            elif self.npc_type == "normal" and random.random() < 0.5:
                should_throw = True

            if should_throw:
                # Check if this tile is a trash bin
                is_bin_tile = any(bin.x == self.x and bin.y == self.y for bin in bins)

                # Only add trash if it's not thrown into a bin
                if not is_bin_tile:
                    trash_list.append(Trash(self.x, self.y))
                    dropTrash_sound.play()

        return True

    def draw(self):
        screen.blit(self.image, (self.pixel_x, self.pixel_y))
        # Draw the capacity above the NPC
        if self.npc_type == "educated":
            font = pygame.font.SysFont(None, 24)
            capacity_text = f"{self.current_trash}/{self.capacity}"
            text_surface = font.render(capacity_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.pixel_x + TILE_SIZE // 2, self.pixel_y - 10))

# Game state
money = 20 # Initialize money to 20
capacity_upgrade_cost = 10  # Cost to upgrade capacity
speed_upgrade_cost = 15    # Cost to upgrade speed
trashes = []
bots = [Bot(1, 1)]
npcs = []

def generate_npc(npc_type):
    while True:
        edge = random.choice([0, 1, 2, 3])
        if edge == 0:
            x, y = random.randint(0, COLS - 1), 0
        elif edge == 1:
            x, y = random.randint(0, COLS - 1), ROWS - 1
        elif edge == 2:
            x, y = 0, random.randint(0, ROWS - 1)
        else:
            x, y = COLS - 1, random.randint(0, ROWS - 1)

        if tile_map[y][x] == "sidewalk":
            npc = NPC(x, y, npc_type)
            npc.level = 0  # Set the level to 0 regardless of type
            return npc


for _ in range(1):
    npcs.append(generate_npc("non-educated"))

for _ in range(2):
    npcs.append(generate_npc("normal"))

# Game loop
clock = pygame.time.Clock()
FRAME_RATE = 30 # Set a consistent frame rate
running = True
player_bot = Bot(1, 1)  # Initialize the player-controlled bot
menu_button_rect = pygame.Rect(WIDTH - 150, 10, 140, 40)  # Button dimensions
menu_open = False  # Track whether the menu is open

def is_walkable(x, y):
    return 0 <= x < COLS and 0 <= y < ROWS and tile_map[y][x] in ["sidewalk", "trash_bin"]

def draw_menu():
    # Draw a semi-transparent gray overlay on the background
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # Allow transparency
    overlay.fill((50, 50, 50, 150))  # RGBA: Dark gray with 150 alpha (transparency)
    screen.blit(overlay, (0, 0))

    # Draw the menu background
    menu_width, menu_height = WIDTH - 200, HEIGHT - 200  # Slightly smaller menu size
    menu_bg_rect = pygame.Rect(100, 100, menu_width, menu_height)
    pygame.draw.rect(screen, (50, 50, 50), menu_bg_rect)  # Dark gray background
    pygame.draw.rect(screen, (255, 255, 255), menu_bg_rect, 2)  # White border

    font = pygame.font.SysFont(None, 24)

    # Draw the title
    title_text = font.render("NPC Menu", True, (255, 255, 255))  # White text
    screen.blit(title_text, (menu_bg_rect.x + menu_width // 2 - 50, menu_bg_rect.y + 20))  # Centered title

    # Draw NPC details and images
    y_offset = menu_bg_rect.y + 60
    for npc in npc_list:
        # Draw NPC image
        npc_image = npc_imgs[npc["type"]]["walk"]["south"][0]  # Use the south-facing image
        screen.blit(npc_image, (menu_bg_rect.x + 20, y_offset))  # Display image on the left

        # Draw NPC details
        npc_text = f"{npc['name']} (Lv. {npc['level']}) - {npc['location']}"
        npc_surface = font.render(npc_text, True, (255, 255, 255))  # White text
        screen.blit(npc_surface, (menu_bg_rect.x + 100, y_offset + 10))  # Display text next to the image

        # Draw upgrade button
        upgrade_button_rect = pygame.Rect(menu_bg_rect.x + menu_width - 170, y_offset, 150, 40)
        pygame.draw.rect(screen, (100, 200, 100), upgrade_button_rect)  # Green button

        upgrade_text = font.render("Educate $10", True, (0, 0, 0))  # Black text
        text_rect = upgrade_text.get_rect(center=upgrade_button_rect.center)

        screen.blit(upgrade_text, text_rect)


        # Update the button rect in the NPC dictionary
        npc["upgrade_button"] = upgrade_button_rect
        y_offset += 80  # Move to the next NPC

def display_stats(money, bot_capacity, bot_current_trash, start_time, trash_count):
    font = pygame.font.SysFont(None, 28)  # Reduced font size to 28

    # Helper function to draw text with an outline
    def draw_text_with_outline(text, font, color, outline_color, x, y):
        # Render the outline by drawing the text in 8 surrounding directions
        outline_surface = font.render(text, True, outline_color)
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]:
            screen.blit(outline_surface, (x + dx, y + dy))
        # Render the main text
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))

    # Calculate the right-side position
    right_x = WIDTH - 200  # Adjust the X position for the right side

    # Display money in yellow with black outline
    money_text = f"Money: ${money}"
    draw_text_with_outline(money_text, font, (255, 255, 0), (0, 0, 0), 10, 5)  # Adjusted position

    # Display bot capacity in white with black outline
    capacity_text = f"Trash Capacity: {bot_current_trash}/{bot_capacity}"
    draw_text_with_outline(capacity_text, font, (255, 255, 255), (0, 0, 0), 10, 40)  # Adjusted position for better alignment

    # Display timer in white with black outline
    elapsed_time = int(time.time() - start_time)
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    timer_text = f"Time: {minutes:02}:{seconds:02}"
    draw_text_with_outline(timer_text, font, (255, 255, 255), (0, 0, 0), right_x, 5)

    # Display available trash count in white with black outline
    trash_text = f"Trash Available: {trash_count}"
    draw_text_with_outline(trash_text, font, (255, 255, 255), (0, 0, 0), right_x, 40)

    # Display instruction for upgrading NPCs
    tab_text = "Press [Tab] to upgrade NPC Education"
    draw_text_with_outline(tab_text, font, (255, 255, 255), (0, 0, 0), 10, HEIGHT - 60)  # Adjusted position

    # Display upgrade instructions in white with black outline
    upgrade_text_1 = f"[1] (${capacity_upgrade_cost}) to upgrade capacity"
    draw_text_with_outline(upgrade_text_1, font, (255, 255, 255), (0, 0, 0), 10, HEIGHT - 40)

    upgrade_text_2 = f"[2] (${speed_upgrade_cost}) to upgrade speed"
    draw_text_with_outline(upgrade_text_2, font, (255, 255, 255), (0, 0, 0), 10, HEIGHT - 20)
    
# Load the star image
star_img = pygame.transform.scale(pygame.image.load(ASSETS_PATH + "star.png"), (50, 50))
empty_star = pygame.transform.scale(pygame.image.load(ASSETS_PATH + "Grayscale Star.png"), (50, 50))

# Start time of the game
start_time = time.time()

def check_game_completion():
    global running
    if not trashes and all(npc["type"] == "educated" for npc in npc_list):
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)

        # Determine star rating based on time
        if elapsed_time <= 7 * 60:  # Less than or equal to 7 minutes
            stars = 5
        elif elapsed_time <= 10 * 60:  # Less than or equal to 10 minutes
            stars = 4
        elif elapsed_time <= 15 * 60:  # Less than or equal to 15 minutes
            stars = 3
        elif elapsed_time <= 20 * 60:  # Less than or equal to 20 minutes
            stars = 2
        else:
            stars = 1

        # Create a semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # Allow transparency
        overlay.fill((0, 0, 0, 150))  # RGBA: Black with 150 alpha (transparency)
        screen.blit(overlay, (0, 0))

        # Display the completion screen
        font = pygame.font.SysFont(None, 48)
        win_text = font.render("Congratulations! All NPCs are educated!", True, (0, 255, 0))  # Green text
        time_text = font.render(f"Time: {minutes}m {seconds}s", True, (255, 255, 255))  # White text

        # Draw the texts on the screen
        screen.blit(win_text, (WIDTH // 2 - 300, HEIGHT // 2 - 100))
        screen.blit(time_text, (WIDTH // 2 - 100, HEIGHT // 2 - 40))

        # Draw stars based on the rating
        for i in range(5):
            if i < stars:
                screen.blit(star_img, (WIDTH // 2 - 125 + i * 60, HEIGHT // 2 + 20))  # Filled star
            else:
                screen.blit(empty_star, (WIDTH // 2 - 125 + i * 60, HEIGHT // 2 + 20))

        pygame.display.flip()
        pygame.time.wait(5000)  # Wait for 5 seconds
        running = False  # Stop the game loop

    elif len(trashes) >= 100:
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)

        # Create a semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # Allow transparency
        overlay.fill((0, 0, 0, 150))  # RGBA: Black with 150 alpha (transparency)
        screen.blit(overlay, (0, 0))

        # Display the completion screen
        font = pygame.font.SysFont(None, 48)
        win_text = font.render("Game Over, The Town is VERY POLUTED!", True, (0, 255, 0))  # Green text
        time_text = font.render(f"Time: {minutes}m {seconds}s", True, (255, 255, 255))  # White text

        screen.blit(win_text, (WIDTH // 2 - 300, HEIGHT // 2 - 100))
        screen.blit(time_text, (WIDTH // 2 - 100, HEIGHT // 2 - 40))

        for i in range(5):
            screen.blit(empty_star, (WIDTH // 2 - 125 + i * 60, HEIGHT // 2 + 20))

        pygame.display.flip()
        pygame.time.wait(5000)  # Wait for 5 seconds
        running = False  # Stop the game loop

def update_npc_list():
    global npc_list
    npc_list = []
    for npc in npcs:
        npc_list.append({
            "name": f"{npc.npc_type.capitalize()} NPC",
            "level": npc.level,
            "location": f"({npc.x}, {npc.y})",
            "type": npc.npc_type,
            "upgrade_button": None  # This will be updated in the menu
        })

while running:
    # Handle player input for the bot
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_bot.move("up", is_walkable)
    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_bot.move("down", is_walkable)
    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_bot.move("left", is_walkable)
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_bot.move("right", is_walkable)
    screen.fill(WHITE)

    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:  # Toggle the menu with the Tab key
                menu_open = not menu_open
            elif event.key == pygame.K_1:  # Upgrade capacity
                if money >= capacity_upgrade_cost and player_bot.capacity < MAXCAPACITY:
                    money -= capacity_upgrade_cost
                    player_bot.capacity += 1  # Increase bot capacity
            elif event.key == pygame.K_2:  # Upgrade speed
                if money >= speed_upgrade_cost and player_bot.speed < MAXSPEED:
                    money -= speed_upgrade_cost
                    player_bot.speed += 1  # Increase bot speed
        elif event.type == pygame.MOUSEBUTTONDOWN and menu_open:
            mouse_pos = pygame.mouse.get_pos()
            for npc in npc_list:
                if npc["upgrade_button"] and npc["upgrade_button"].collidepoint(mouse_pos):
                    # Check if the NPC is already "educated" and at max level
                    if npc["type"] == "educated" and npc["level"] >= 10:
                        continue  # Skip further processing for this NPC
                    if money >= 10:  # Check if the player has enough money
                        money -= 10  # Deduct the upgrade cost
                        npc["level"] += 1  # Increase the NPC's level

                        # Upgrade the NPC type if applicable
                        if npc["type"] == "non-educated" and npc["level"] >= 10:
                            npc["type"] = "normal"
                            npc["level"] = 0
                        elif npc["type"] == "normal" and npc["level"] >= 10:
                            npc["type"] = "educated"
                            npc["level"] = 10

                        # Synchronize the level and type with the corresponding NPC in the npcs list
                        for actual_npc in npcs:
                            if actual_npc.x == int(npc["location"].strip("()").split(", ")[0]) and \
                               actual_npc.y == int(npc["location"].strip("()").split(", ")[1]):
                                actual_npc.level = npc["level"]
                                actual_npc.npc_type = npc["type"]
                                if npc["type"] == "educated":
                                    actual_npc.capacity = 3  # Set capacity for educated NPCs
                                break

    # Draw the game world
    for y in range(ROWS):
        for x in range(COLS):
            draw_tile(x, y)

    for trash_bin in bins:
        trash_bin.draw()

    for trash in trashes:
        trash.draw()
    player_bot.draw()
    for npc in npcs:
        npc.draw()

    # Pause game logic if the menu is open
    if not menu_open:
        # Update NPCs and the bot
        for npc in npcs:
            npc.move(trashes, bins)
            npc.update(trashes)
        player_bot.update(trashes, bins)

        # Synchronize npc_list with the current state of npcs
        update_npc_list()

        # Display money and bot capacity
        display_stats(money, player_bot.capacity, player_bot.current_trash, start_time, len(trashes))

        # Check for game completion
        check_game_completion()
    else:
        # Draw the NPC menu
        draw_menu()

    # Maintain a consistent frame rate
    pygame.display.flip()
    clock.tick(FRAME_RATE)

pygame.quit()
sys.exit()