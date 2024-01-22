import mediapipe as mp
import cv2
import pygame
import random
import time

countdown_time = 60 
Main_X_velocity=8
Main_Y_velocity=4
NoOfBalls=10

pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
Score=0
screen_width,screen_height=1280,720
screen = pygame.display.set_mode((screen_width, screen_height))
ColorOptions=[(255,0,0),(0,255,0),(0,0,255),(255,255,0),(128,0,128)]
BlueGreen=(147,225,216)
Melon=(255,166,158)
Marron=(170,68,101)
Purple2=(134,22,87)

HandColor=random.choice(ColorOptions)
balls_list=[]
clock.tick(60)

class  BallTracking:
    def __init__(self,x,y,r,velocity_x, velocity_y,ball_color):
        self.x = x
        self.y = y
        self.r = r
        self.ball_color = ball_color
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
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
    
    def check_new_ball(x,r):
        for i in balls_list:
            if i:
                return True
            if abs(i.x - x) <= i.r + r:
                return False
        return True
    
    def check_ball_boundary_interaction(self):
        if self.x-self.r<=0 or self.x+self.r>=screen_width:
            self.velocity_x=-self.velocity_x
        if self.y-2*self.r>=screen_height:
            balls_list.remove(self)
            balls_list.append(BallTracking.create_ball())

    def check_balls_interaction():
        for i in range(len(balls_list)):
            for j in range(len(balls_list)):
                if i != j:
                    dis = ((balls_list[i].x - balls_list[j].x) ** 2 + (balls_list[i].y - balls_list[j].y) ** 2) ** 0.5
                    if dis <= balls_list[i].r + balls_list[j].r:
                        
                        balls_list[i].velocity_x, balls_list[j].velocity_x = balls_list[j].velocity_x, balls_list[i].velocity_x
                        balls_list[i].velocity_y, balls_list[j].velocity_y = balls_list[j].velocity_y, balls_list[i].velocity_y

                        
                        

    def update_ball(self):
        self.y += self.velocity_y
        self.x += self.velocity_x
    
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
    
class HandRecognition:
    def __init__(self):
        self.mp_hands = mp.solutions.hands.Hands(
            max_num_hands=1,  # Enforce only one hand detection
            min_detection_confidence=0.1,
            min_tracking_confidence=0.1
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def get_index_fingertip_coordinates(self, hand_landmarks_list, frame):
        if hand_landmarks_list:
            hand_landmarks = hand_landmarks_list[0]  # Access the first (and only) hand
            index_fingertip = hand_landmarks.landmark[8]
            x = int(index_fingertip.x * frame.shape[1])
            y = int(index_fingertip.y * frame.shape[0])
            return x, y
        else:
            return None, None

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
    
class GameEnvironment:
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Color Harmony Challenge")

    def draw_balls(self,ball):
        if ball.x:
            pygame.draw.circle(self.screen, ball.ball_color, (ball.x, ball.y), ball.r)
            
     
    def draw_Index_finger(self,x,y):
        if x and y:
            pygame.draw.circle(self.screen, HandColor, (x,y), 10)
            
    def display_time(self, remaining_time):
        font = pygame.font.Font(None, 72)
        text = font.render(f"Time: {remaining_time // 60:02d}:{remaining_time % 60:02d}", True, (0, 0, 0))
        self.screen.blit(text, (10, 10))
    
    def display_score(self, Score):
        font = pygame.font.Font(None, 72)
        global screen_width
        score_text = font.render(f"Score: {Score}", True, (0, 0, 0))
        self.screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))

    def update_screen(self, frame):
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        self.screen.blit(frame_surface, (0, 0))
    
class Main_Menu:
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
    
    def Text_Display(text,height,width,size):
        font = pygame.font.Font(None, size)
        text = font.render(text, True, Marron)
        rect = text.get_rect(center=(width, height))
        screen.blit(text,rect)

class Main_Score:
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
    
    def retrieve_top_scores(scores_filename):
        with open(scores_filename, 'r') as file:
            scores_file = [int(line.strip()) for line in file]
        scores_file.sort(reverse=True)
        return scores_file

class Sound:
    def Sound_Play_Loss():
        sound = pygame.mixer.Sound('Loss.mp3')
        sound.play()
    def Sound_Play_Win():
        sound = pygame.mixer.Sound('Win.mp3')
        sound.play()


def main():
    global HandColor,balls_list,Score
    game=True
    cap = cv2.VideoCapture(0)
    Hand_Recognition=HandRecognition()
    Game_Environment=GameEnvironment()

    for i in range(NoOfBalls):
            balls_list.append(BallTracking.create_ball())
    start_time = time.time()
    while game:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (screen_width, screen_height))
        frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                Main_Score.store_scores("scores.txt",Score)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game = False
                    Main_Score.store_scores("scores.txt",Score)

        frame,hand_landmarks =Hand_Recognition.detect_and_highlight_hands(frame)
        finger_x, finger_y = Hand_Recognition.get_index_fingertip_coordinates(hand_landmarks, frame)
        Game_Environment.draw_Index_finger(finger_x,finger_y)
        elapsed_time = time.time() - start_time
        remaining_time = max(0, countdown_time - int(elapsed_time))
        Game_Environment.display_time(remaining_time)
        Game_Environment.display_score(Score)
        BallTracking.check_balls_interaction()
        pygame.display.update()
        Game_Environment.update_screen(frame)
        if remaining_time==5:
            alarm_sound = pygame.mixer.Sound('AlarmClock.mp3')
            alarm_sound.play()
        if remaining_time<=0:
            restart_rect=Main_Menu.button("RESTART",100)
            quit_rect=Main_Menu.button("QUIT",-100)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if restart_rect.collidepoint(mouse_pos):
                    cap.release()
                    cv2.destroyAllWindows()
                    Main_Score.store_scores("scores.txt",Score)
                    balls_list=[]
                    Score=0
                    game=False
                    main()
                if quit_rect.collidepoint(mouse_pos):
                    Main_Score.store_scores("scores.txt",Score)
                    game = False
            continue
        
        for ball in balls_list:
            Game_Environment.draw_balls(ball)
            BallTracking.check_ball_boundary_interaction(ball)
            BallTracking.update_ball(ball)
            k,HandColor=BallTracking.check_finger_ball_interaction(ball,finger_x,finger_y)
            
            if k==1:
                balls_list.remove(ball)
                balls_list.append(BallTracking.create_ball())     
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()



def draw_menu():
    screen.fill((221,255,247))
    pygame.display.set_caption("Color Harmony Challenge")
    start_rect=Main_Menu.button("START",100)
    quit_rect=Main_Menu.button("QUIT",-100)
    Main_Menu.Text_Display("Color Harmony",100,screen_width // 2,72)
    Main_Menu.Text_Display("Challenge",150,screen_width // 2,72)
    Main_Menu.Text_Display("Press ESC key any time to exit the game anytime",screen_height-100,screen_width // 2,18)
    
    Score_File=Main_Score.retrieve_top_scores("scores.txt")
    Main_Menu.Text_Display("HighScores",150,screen_width-100,36)
    for i in range(5):
        Main_Menu.Text_Display(f"{i + 1}. {Score_File[i]}",170+i*20,screen_width-100,25)
    run = True
    while run:
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
               mouse_pos = pygame.mouse.get_pos()

               if start_rect.collidepoint(mouse_pos):
                   main()
               if quit_rect.collidepoint(mouse_pos):
                   run = False
    
draw_menu()
