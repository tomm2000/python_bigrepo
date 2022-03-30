import pygame
pygame.init()
cosa = True

# dichiarazaione variabili
if cosa:
    lung = 600
    alt = 600
    latox = round(lung / 3, 0)
    latoy = round(alt / 3, 0)
    larx = latox / 6
    lary = latoy / 6
    quadrati = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    pros = 1
    mosse = 0
    vinto = False
    punti = [0, 0]
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((lung, alt))
    pos = ()
    done = False

# MAIN GAME LOOP
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        screen.fill((0, 0, 0))

        pos = pygame.mouse.get_pos()

        color = (0, 128, 128)

        # evento click (mossa)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(3):
                for j in range(3):
                    if (pos[0] < latox * (i + 1) and pos[1] < latoy * (j + 1)) and \
                            (pos[0] > latox * i and pos[1] > latoy * j):
                        if pros == 1 and quadrati[i][j] == 0:
                            quadrati[i][j] = 1
                            pros = 2
                            mosse += 1
                        elif pros == 2 and quadrati[i][j] == 0:
                            quadrati[i][j] = 2
                            pros = 1
                            mosse += 1
            if (pos[0] < 20 and pos[1] < 20) and (pos[0] > 0 and pos[1] > 0):
                        vinto = True
                        print("RESET")

        # tabella di gioco
        if cosa:
            pygame.draw.line(screen, (255, 255, 255), (latox, 0), (latox, latoy * 3))
            pygame.draw.line(screen, (255, 255, 255), (latox * 2, 0), (latox * 2, latoy * 3))
            pygame.draw.line(screen, (255, 255, 255), (0, latoy), (latox * 3, latoy))
            pygame.draw.line(screen, (255, 255, 255), (0, latoy * 2), (latox * 3, latoy * 2))
            pygame.draw.rect(screen, (0, 128, 128), pygame.Rect(0, 0, 20, 20))

        # disegno mosse
        for i in range(3):
            for j in range(3):
                if quadrati[i][j] == 1:
                    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect((latox * i) + (latox / 2) - (larx / 2),
                                                                      (latoy * j) + (latoy / 2) - (lary / 2), larx,
                                                                      lary))
                elif quadrati[i][j] == 2:
                    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect((latox * i) + (latox / 2) - (larx / 2),
                                                                      (latoy * j) + (latoy / 2) - (lary / 2), larx,
                                                                      lary))

        # test verticali
        for p in (0, 1):
            for i in range(3):
                if quadrati[i][0] == quadrati[i][1] == quadrati[i][2] == (p + 1):
                    vinto = True
                    punti[p] += 1
                    print("Punteggio: " + str(punti[0]) + " P. rosso, " + str(punti[1]) + " P. verde")

        # test orizzontali
        for p in (0, 1):
            for i in range(3):
                if quadrati[0][i] == quadrati[1][i] == quadrati[2][i] == (p + 1):
                    vinto = True
                    punti[p] += 1
                    print("Punteggio: " + str(punti[0]) + " P. rosso, " + str(punti[1]) + " P. verde")

        # test oblique
        for p in (0, 1):
            if quadrati[0][0] == quadrati[1][1] == quadrati[2][2] == (p + 1) or quadrati[2][0] == quadrati[1][1] \
                    == quadrati[0][2] == (p + 1):
                vinto = True
                punti[p] += 1
                print("Punteggio: " + str(punti[0]) + " P. rosso, " + str(punti[1]) + " P. verde")

        # test 9 mosse (pareggio)
        if mosse == 9:
            vinto = True
            print("Pareggio; punteggio: " + str(punti[0]) + " P. rosso, " + str(punti[1]) + " P. verde")

        # test vittoria
        if vinto:
            for i in range(3):
                for j in range(3):
                    quadrati[i][j] = 0
                    vinto = False
                    mosse = 0

        pygame.display.flip()
        clock.tick(180)
