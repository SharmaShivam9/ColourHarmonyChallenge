# ColourHarmonyChallenge
This repository contains a simple game implemented in Python using the Mediapipe library for hand tracking and Pygame for the graphical user interface. The game involves tracking the movement of the user's index finger, represented by a colored circle, and matching it with falling balls of corresponding colors. It is surprisingly intersting and captivating Game. This game was made as an assignment in project Image Processing using Machine Learning under the GDSC  (Google Developer Student Club), IIT Kanpur.


### How to Play
1. Execute the program and enjoy the Color Harmony Challenge.
2. Balls of different colors will be falling from the top of the screen.
3. The color of your hand is randomly assigned at the beginning.
4. Use your hand (tracked by the camera) to catch balls of the same color as your hand.
5. Each correct catch earns you 5 points, but catching the wrong color deducts 5 points.
6. The game lasts for 60 seconds. Try to score as high as possible!

### Requirements
+ Python 3.7+
+ OpenCV
+ MediaPipe
+ Pygame
+ Webcam

### Setup
Use the following code in command line to install required modules
      
       pip install mediapipe opencv-python pygame

### Key Features
+ Real-time hand tracking using MediaPipe
+ Catching balls with fingertip collision detection
+ Scorekeeping and time countdown
+ Colorful and responsive user interface
+ High score list to track your progress

### Main Menu
The main menu allows you to:
+ **START**: Begin a new Color Harmony Challenge.
+ **QUIT**: Exit the game

### Game Over Screen
After the game ends, you will see a Game Over screen with options:
+ ** RESTART**: Start a new game.
+ **QUIT**: Exit the game.

### Additional Notes:

+ The game is optimized for playing with one hand.
+ The webcam should be able to clearly see your hand for accurate tracking.
+ Adjust the screen brightness and contrast if the hand detection is not working properly.
+ You can change few varibles like speed of ball and no of balls coming at one time.
+ Feel free to modify the game parameters and colors in the ColourHarmonyChallenge.py file.

### Customization
In start of code only, you find few variables whose value you can alter to change gaming experience:

```python
countdown_time = 60  
Main_X_velocity=8
Main_Y_velocity=4
NoOfBalls=10
```

### Code Blocks 
Multiple classes have been used to make this game. Their Explanation is as follows

#### *class  BallTracking*
As the name suggests this is mainly used to used to track all stats of ball moving on screen and to update the ball acoording to the possible interactions.

##### Initialization
```python
    def __init__(self,x,y,r,velocity_x, velocity_y,ball_color):
        self.x = x
        self.y = y
        self.r = r
        self.ball_color = ball_color
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
```

##### Creating New Ball

```python
    @classmethod
    def create_ball(cls):
        new_ball = cls(
            x=int(random.uniform(screen_width / 4, screen_width / 4 * 3)),
            y=0,
            r=random.uniform(10, 30),
            ball_color=random.choice(ColorOptions),
            velocity_x=random.uniform(-Main_X_velocity,Main_X_velocity),
            velocity_y=Main_Y_velocity
            )
        if BallTracking.check_new_ball(new_ball.x,new_ball.r):
            return new_ball
```

##### Checking New Ball

```python
    def check_new_ball(x,r):
        for i in balls_list:
            if i:
                return True
            if abs(i.x - x) <= i.r + r:
                return False
        return True
```

##### Ball and Boundary Interaction

```python
    def check_ball_boundary_interaction(self):
        if self.x-self.r<=0 or self.x+self.r>=screen_width:
            self.velocity_x=-self.velocity_x
        if self.y-2*self.r>=screen_height:
            balls_list.remove(self)
            balls_list.append(BallTracking.create_ball())
```

##### Ball to Ball Interaction

```python
    def check_balls_interaction():
        for i in range(len(balls_list)):
            for j in range(len(balls_list)):
                if i != j:
                    dis = ((balls_list[i].x - balls_list[j].x) ** 2 + (balls_list[i].y - balls_list[j].y) ** 2) ** 0.5
                    if dis <= balls_list[i].r + balls_list[j].r:
                        
                        balls_list[i].velocity_x, balls_list[j].velocity_x = balls_list[j].velocity_x, balls_list[i].velocity_x
                        balls_list[i].velocity_y, balls_list[j].velocity_y = balls_list[j].velocity_y, balls_list[i].velocity_y
```


##### Ball's Position Change
```python
    def update_ball(self):
        self.y += self.velocity_y
        self.x += self.velocity_x
```
    
##### Index Finger and Ball Interaction

```python
    def check_finger_ball_interaction(self, finger_x, finger_y):
        global HandColor,Score
        if finger_x==None or finger_y==None:
            return 0,HandColor
        dis = ((self.x - finger_x) ** 2 + (self.y - finger_y) ** 2) ** (1 / 2)
        if dis <= self.r and self.ball_color == HandColor:
            Score+=5
            Sound.Sound_Play_Win()
            return 1, HandColor
        if dis <= self.r and self.ball_color != HandColor:
            Score-=5
            Sound.Sound_Play_Loss()
            return 1, self.ball_color
        return 0, HandColor
```

#### *class HandRecognition*

It uses mediapipe module to track hands and index finger.

##### Initialization
```python
    def __init__(self):
        self.mp_hands = mp.solutions.hands.Hands(
            max_num_hands=1,  # Enforce only one hand detection
            min_detection_confidence=0.1,
            min_tracking_confidence=0.1
        )
        self.mp_drawing = mp.solutions.drawing_utils
```

##### Index Finger Coordinated

```python
    def get_index_fingertip_coordinates(self, hand_landmarks_list, frame):
        if hand_landmarks_list:
            hand_landmarks = hand_landmarks_list[0]  # Access the first (and only) hand
            index_fingertip = hand_landmarks.landmark[8]
            x = int(index_fingertip.x * frame.shape[1])
            y = int(index_fingertip.y * frame.shape[0])
            return x, y
        else:
            return None, None
```

##### Hand Detection

```python
    def detect_and_highlight_hands(self, frame):
        results = self.mp_hands.process(frame)
        hand_landmarks_list = results.multi_hand_landmarks

        if hand_landmarks_list:
            hand_landmarks = hand_landmarks_list[0] 
            landmark_drawing_spec = mp.solutions.drawing_utils.DrawingSpec(
                color=HandColor, 
                thickness=2,
                circle_radius=2,
            )
            self.mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS, landmark_drawing_spec
            )

        return frame, hand_landmarks_list
```

#### *class GameEnvironment:*

This used pygame module to create a gaming environment.

##### Initialization

```python
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Color Harmony Challenge")
```

##### Creation of Balls

```python
    def draw_balls(self,ball):
        if ball.x:
            pygame.draw.circle(self.screen, ball.ball_color, (ball.x, ball.y), ball.r)
```
            
##### Index Finger 

```python
    def draw_Index_finger(self,x,y):
        if x and y:
            pygame.draw.circle(self.screen, HandColor, (x,y), 10)
```
            
##### Time

```python
    def display_time(self, remaining_time):
        font = pygame.font.Font(None, 72)
        text = font.render(f"Time: {remaining_time // 60:02d}:{remaining_time % 60:02d}", True, (0, 0, 0))
        self.screen.blit(text, (10, 10))
```

##### Score

```python
    def display_score(self, Score):
        font = pygame.font.Font(None, 72)
        global screen_width
        score_text = font.render(f"Score: {Score}", True, (0, 0, 0))
        self.screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))
```

##### Initialization of Pygame Screen

```python
    def update_screen(self, frame):
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        self.screen.blit(frame_surface, (0, 0))
```

#### *class Main_Menu*
This class is used to customize main menu further.

##### Display Button
```python
    def button(Display_Text,offset):
        padding = 30 
        text = font.render(Display_Text, True, Melon)
        rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - offset))
        rect.inflate_ip(70,70)
        pygame.draw.rect(screen, Purple2, rect)
        rect.inflate_ip(-40,-40)
        pygame.draw.rect(screen, (255,255,255), rect,3)
        rect.inflate_ip(padding-5, padding-5)
        pygame.draw.rect(screen, (255,255,255), rect,4)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
        return rect
```
##### Display Text
```python
    def Text_Display(text,height,width,size):
        font = pygame.font.Font(None, size)
        text = font.render(text, True, Marron)
        rect = text.get_rect(center=(width, height))
        screen.blit(text,rect)
```
		
#### *class Main_Score*
This class is used for displaying highest scores and saving scores.

##### Saving Scores
```python
    def store_scores(scores_filename, new_score):
     try:
        with open(scores_filename, 'r') as file:
            scores_file = [int(line.strip()) for line in file]
        if new_score in scores_file:
            return
        scores_file.append(new_score)
        scores_file.sort()
        with open(scores_filename, 'w') as file:
            for score in scores_file:
                file.write(f"{score}\n")

     except FileNotFoundError:
        with open(scores_filename, 'w') as file:
            file.write(f"{new_score}\n")
```

#### Retrieveing Score

```python
    def retrieve_top_scores(scores_filename):
        with open(scores_filename, 'r') as file:
            scores_file = [int(line.strip()) for line in file]
        scores_file.sort(reverse=True)
        return scores_file
```
		
#### class Sound
This class is used to play sounds and make game more interactive.

```python
    def Sound_Play_Loss():
        sound = pygame.mixer.Sound('Loss.mp3')
        sound.play()
    def Sound_Play_Win():
        sound = pygame.mixer.Sound('Win.mp3')
        sound.play()
```
### End
