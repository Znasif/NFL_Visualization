import pandas as pd
# Import libraries
import pygame # A python library for creating graphical user interfaces
import math # A python library for mathematical functions

class NFL:
  def __init__(self):
    """
    https://www.kaggle.com/competitions/nfl-big-data-bowl-2022/data
    """
    parent_folder = "/mnt/d/Codes/NFL/"
    self.game_link = "games.csv"#"https://gist.githubusercontent.com/f-banda/0a7448ddba470ee6009e8bbaf4751a34/raw/56d07b202921b591e8c2390048758c4b3fd3df7b/games.csv"
    self.play_link = "plays.csv"#"https://gist.githubusercontent.com/f-banda/0a7448ddba470ee6009e8bbaf4751a34/raw/56d07b202921b591e8c2390048758c4b3fd3df7b/plays.csv"
    self.player_link = "players.csv"#"https://gist.githubusercontent.com/f-banda/0a7448ddba470ee6009e8bbaf4751a34/raw/56d07b202921b591e8c2390048758c4b3fd3df7b/players.csv"
    self.track_link = "track.csv"#"https://dl.dropboxusercontent.com/s/0jvkqf9wnfjdlrf/dataTracking2020.csv"
    self.download()

  def download(self):
    self.game = pd.read_csv(self.game_link)
    self.play = pd.read_csv(self.play_link)
    self.player = pd.read_csv(self.player_link)
    self.track = pd.read_csv(self.track_link)

  def import_pbp_data(self, ls):
    season = self.game[self.game["season"].isin(ls)]
    game = self.play[self.play["gameId"].isin(season["gameId"])]
    play = self.track
    return play


# Draw field
def draw_field():
    screen.fill(GREEN) # Fill the screen with green color
    pygame.draw.rect(screen, WHITE, (OFFSET, OFFSET, WIDTH - OFFSET * 2, HEIGHT - OFFSET * 2), 5) # Draw the field boundary with white color and 5 pixels width
    pygame.draw.line(screen, WHITE, (WIDTH / 2, OFFSET), (WIDTH / 2, HEIGHT - OFFSET), 5) # Draw the midfield line with white color and 5 pixels width
    pygame.draw.line(screen, WHITE, (OFFSET + SCALE * 10, OFFSET), (OFFSET + SCALE * 10, HEIGHT - OFFSET), 5) # Draw the left end zone line with white color and 5 pixels width
    pygame.draw.line(screen, WHITE, (WIDTH - OFFSET - SCALE * 10, OFFSET), (WIDTH - OFFSET - SCALE * 10, HEIGHT - OFFSET), 5) # Draw the right end zone line with white color and 5 pixels width

    for i in range(1, 10): # For each yard line from 10 to 90
        x = OFFSET + SCALE * (i * 10 + 10) # Calculate the x coordinate of the yard line
        pygame.draw.line(screen, WHITE, (x, OFFSET), (x, HEIGHT - OFFSET)) # Draw the yard line with white color

        if i % 5 == 0: # If the yard line is a multiple of five
            font = pygame.font.SysFont("Arial", 20) # Create a font object with Arial font and size 20
            text = font.render(str(i * 10), True, WHITE) # Create a text object with the yard number and white color
            screen.blit(text, (x - text.get_width() / 2, OFFSET / 2)) # Blit the text object on the top of the yard line

            text = font.render(str(100 - i * 10), True, WHITE) # Create a text object with the opposite yard number and white color
            screen.blit(text, (x - text.get_width() / 2, HEIGHT - OFFSET / 2 - text.get_height())) # Blit the text object on the bottom of the yard line

# Draw players and ball
def draw_players_and_ball(frame):
    frame_data = play_data[play_data["frame_id"] == frame] # Filter the data by frame id

    for index, row in frame_data.iterrows(): # For each row in the frame data

        x = row["x"] * SCALE + WIDTH / 2 # Convert the x coordinate from yards to pixels and center it on the screen
        y = row["y"] * SCALE + HEIGHT / 2 # Convert the y coordinate from yards to pixels and center it on the screen

        if math.isnan(row["nfl_id"]): # If the row is the ball
            pygame.draw.circle(screen, YELLOW, (x, y), 5) # Draw a yellow circle with radius 5 pixels
        else: # If the row is a player
            if row["team"] == "home": # If the player is on the home team
                color = RED # Use red color
            elif row["team"] == "away": # If the player is on the away team
                color = BLUE # Use blue color
            else: # If the player is on neither team (should not happen)
                color = WHITE # Use white color

            pygame.draw.circle(screen, color, (x, y), 10) # Draw a colored circle with radius 10 pixels
            font = pygame.font.SysFont("Arial", 15) # Create a font object with Arial font and size 15
            text = font.render(str(row["jersey_number"]), True, WHITE) # Create a text object with the jersey number and white color
            screen.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2)) # Blit the text object on the center of the circle

if __name__ == "__main__":
    nfl = NFL()

    # Define constants
    WIDTH = 800 # The width of the window
    HEIGHT = 600 # The height of the window
    FPS = 60 # The frames per second of the animation
    SCALE = 10 # The scale factor for converting yards to pixels
    OFFSET = 50 # The offset for the field boundaries
    WHITE = (255, 255, 255) # The color white
    BLACK = (0, 0, 0) # The color black
    GREEN = (0, 128, 0) # The color green
    YELLOW = (255, 255, 0) # The color yellow
    RED = (255, 0, 0) # The color red
    BLUE = (0, 0, 255) # The color blue

    # Initialize pygame and create window
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("NFL Data Visualization")
    clock = pygame.time.Clock()

    # Load data
    pbp_data = nfl.import_pbp_data([2020]) # Import play-by-play data for 2020 season
    game_id = 2020091000 # Select a game id to visualize
    game_data = pbp_data[pbp_data["gameId"] == game_id] # Filter the data by game id
    play_id = 612 # Select a play id to visualize
    play_data = game_data[game_data["playId"] == play_id] # Filter the data by play id

    # Main loop
    running = True # A flag to indicate whether the program is running or not
    frame = 1 # A variable to store the current frame id
    max_frame = play_data["frame_id"].max() # A variable to store the maximum frame id
    
    while running: # While the program is running
        clock.tick(FPS) # Limit the loop to run at FPS times per second
    
        for event in pygame.event.get(): # For each event in the event queue
            if event.type == pygame.QUIT: # If the event is quitting the program
                running = False # Set the running flag to False
    
        draw_field() # Draw the field
        draw_players_and_ball(frame) # Draw the players and ball for the current frame
    
        frame += 1 # Increment the frame by one
    
        if frame > max_frame: # If the frame exceeds the maximum frame
            frame = 1 # Reset the frame to one
    
        pygame.display.flip() # Update the display
    
    pygame.quit() # Quit pygame
