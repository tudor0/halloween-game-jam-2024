import pytmx
import pygame

class Map:
    def __init__(self, map_file):
        # Initialize the map by loading the .tmx file using pytmx.
        self.tmx_data = pytmx.util_pygame.load_pygame(map_file)
        self.width = self.tmx_data.width
        self.height = self.tmx_data.height
        self.tilewidth = self.tmx_data.tilewidth
        self.tileheight = self.tmx_data.tileheight

        self.collidables = self.load_collidables()

    def load_collidables(self):
        collidables = []
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x,y,gid in layer:
                    tile = self.tmx_data.get_tile_properties_by_gid(gid)
                    if tile and tile.get("collidables"):
                        rect = pygame.Rect(
                            x * self.tilewidth,
                            y * self.tileheight,
                            self.tilewidth,
                            self.tileheight
                        )
                        collidables.append(rect)
        return collidables

    def render(self, surface):
        screen_width, screen_height = surface.get_size()
        map_width, map_height = self.get_size()

        scale_x = screen_width / map_width
        scale_y = screen_height / map_height

        # Renders the map on the provided surface.
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)

                    # Only draw if tile exists (to avoid NoneType errors)
                    if tile:
                        # Scale the tile
                        scaled_tile = pygame.transform.scale(tile,
                                                             (int(self.tilewidth * scale_x),
                                                              int(self.tileheight * scale_y)))
                        surface.blit(scaled_tile, (x * self.tilewidth * scale_x, y * self.tileheight * scale_y))

    def get_size(self):
        # Returns the pixel size of the map.
        return self.width * self.tilewidth, self.height * self.tileheight

    def check_collision(self, rect):
        for collidable in self.collidables:
            if rect.colliderect(collidable):
                return True
        return False