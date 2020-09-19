"""
Animation and stuff for the table

"""
import pygame
from . import definitions


def draw_table(
    screen: pygame.Surface, width: int, height: int, border_width: int
) -> None:
    """
    Draw a pool table on a pygame Surface

    This will be a block green pygame Surface with black circles in the corners + halfway up the right/left edges

    Also a 20 pixel brown border

    """
    # Green background
    screen.fill(definitions.POOL_TABLE_GREEN)

    # Black pockets in the corners and halfway down the vertical edges
    # Pocket size is defined by the shorter side
    shorter_side = width if width < height else height
    pocket_radius = shorter_side // 15

    # Probably store some of these as variables
    pocket_positions = (
        (border_width, border_width),
        (width - border_width, border_width),
        (border_width, height - border_width),
        (width - border_width, height - border_width),
        (border_width, height // 2),
        (width - border_width, height // 2),
    )

    for position in pocket_positions:
        pygame.draw.circle(screen, definitions.BLACK, position, pocket_radius)

    # Brown table lookin borders around the edges
    pygame.draw.rect(
        screen, definitions.POOL_TABLE_EDGE_BROWN, [0, 0, border_width, height]
    )
    pygame.draw.rect(
        screen, definitions.POOL_TABLE_EDGE_BROWN, [0, 0, width, border_width]
    )
    pygame.draw.rect(
        screen,
        definitions.POOL_TABLE_EDGE_BROWN,
        [width - border_width, 0, width, height],
    )
    pygame.draw.rect(
        screen,
        definitions.POOL_TABLE_EDGE_BROWN,
        [0, height - border_width, width, height],
    )
