#mengimport library yang diperlukan
import pygame, sys
import pygame.font

WIDTH, HEIGHT = 400, 400 #menyatakan lebar dan panjangnya yaitu 400px
TITLE = "Smooth Movement" #menyatakan judulnya

pygame.init() #menginisialisasi pygame
win = pygame.display.set_mode((WIDTH, HEIGHT)) #membuat display dengan mengeset lebar dan panjang
pygame.display.set_caption(TITLE) #mengeset judulnya
clock = pygame.time.Clock() #inisialisasi clock

pygame.font.init() #menginisialisasi font
font_color=(128,128,128) # mengeset warna yaitu merupakan warna gray
font_obj=pygame.font.Font("MADE.otf",35) #memanggil font yang ada dilokal dengan font size 35
text_obj=font_obj.render("Elya Kumala Fauziyah", True, font_color) #membuat text dengan mengeset text dan font color


class Player: #membuat class Player
    def __init__(self, x, y): 
        self.x=int(x) #inisialisasi self.x yaitu dinyatakan dalam integer x
        self.y=int(y) #inisialisasi self.x yaitu dinyatakan dalam integer y
        self.rect = pygame.Rect(int(self.x), int(self.y), 32, 32) # inisialisasi objek perseginya dengan memanggil self.x dan self.y dengan ukururan 32x32
        self.color = (250, 120, 60) #inisialisasi color pada objek persegiya
        self.velX = 10 
        self.velY = 10
        self.left_pressed = False #dinyatakan dalam bentuk false
        self.right_pressed = False #dinyatakan dalam bentuk false
        self.up_pressed = False #dinyatakan dalam bentuk false
        self.down_pressed = False #dinyatakan dalam bentuk false
        self.speed = 10 #kecepatan bergerak objeknya
    
    def draw(self, win): #untuk menggambar rect nya
        pygame.draw.rect(win, self.color, self.rect)
    
    
    def update(self): #untuk mengupdate
        self.velX=0
        self.velY=0
        if self.left_pressed and not self.right_pressed and self.x > 0: #pada sisi kiri diberi batasan 0
            self.velX = -self.speed
        if self.right_pressed and not self.left_pressed and self.x < 370: #pada sisi kanan diberi batasan 370
            self.velX = self.speed
        if self.up_pressed and not self.down_pressed and self.y >0: #pada sisi atas diberi batasan 0
            self.velY = -self.speed
        if self.down_pressed and not self.up_pressed and self.y <370: #pada sisi bawah diberi batasan 370
            self.velY = self.speed
        
        self.x += self.velX
        self.y += self.velY

        self.rect = pygame.Rect(int(self.x), int(self.y), 32, 32) #menyatakan rect nya/perseginya
       

player = Player(WIDTH/2, HEIGHT/2) #dinyatakan jika widht dibagi 2 dan heiht dibagi 2



while True: #jika True maka dijalankan
    
    for event in pygame.event.get(): #menggunakan perulangan for pada event
        if event.type == pygame.QUIT: # menggunakan pengkondisisan if pada event.type
             pygame.quit() #untuk keluar game
             sys.exit()  #untuk keluar game
        if event.type == pygame.KEYDOWN: #menggunakan pengkondisian if pada event.type di keyboard bawah
            if event.key == pygame.K_LEFT : #menggunakan pengkondisian if pada keyboard kiri
                player.left_pressed=True #menyatakan true berarti dapat di klik
            if event.key == pygame.K_RIGHT: #menggunakan pengkondisian if pada keyboard kiri
                player.right_pressed=True #menyatakan true berarti dapat di klik
            if event.key == pygame.K_UP: #menggunakan pengkondisian if pada keyboard kiri
                player.up_pressed=True #menyatakan true berarti dapat di klik
            if event.key == pygame.K_DOWN: #menggunakan pengkondisian if pada keyboard kiri
                player.down_pressed=True #menyatakan true berarti dapat di klik
        if event.type == pygame.KEYUP: #menggunakan pengkondisian if pada event.type di keyboard atas
            if event.key == pygame.K_LEFT: #menggunakan pengkondisian if pada keyboard kiri
                player.left_pressed=False #menyatakan true berarti tidak dapat di klik
            if event.key == pygame.K_RIGHT: #menggunakan pengkondisian if pada keyboard kanan
                player.right_pressed=False#menyatakan true berarti tidak dapat di klik
            if event.key == pygame.K_UP: #menggunakan pengkondisian if pada keyboard atas
                player.up_pressed=False #menyatakan true berarti tidak dapat di klik
            if event.key == pygame.K_DOWN: #menggunakan pengkondisian if pada keyboard bawah
                player.down_pressed=False
                
        

        win.fill((12,24,36)) #warna background nya
        player.draw(win) #fungsi untuk memanggil draw nya
        win.blit(text_obj,(22,0)) # fungsi untuk memanggil font nya

        player.update() #fungsi untuk mengupdate
        pygame.display.flip() #fungsi untuk mengupdate dispaly

        clock.tick(120) #menyatakan fps

