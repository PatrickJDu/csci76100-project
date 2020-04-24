import pygame

dis_width = 600
dis_height = 400
black = (0, 0, 0)
dis = pygame.display.set_mode((dis_width, dis_height))

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])






