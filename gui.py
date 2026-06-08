import pygame

from playfield import Path, Parameter


class PuzzleGUI:
    def __init__(self, puzzle, cell_size=56):
        self.puzzle = puzzle
        self.cell_size = cell_size
        self.status_height = 56

        self.width = puzzle.cols * cell_size
        self.height = puzzle.rows * cell_size + self.status_height

        self.screen = None
        self.clock = None
        self.running = True

        self.font = None
        self.status_font = None

        self.bg_color = (245, 245, 245)
        self.grid_color = (210, 210, 210)

        self.path_color = (140, 140, 140)
        self.filled_path_color = (30, 30, 30)

        self.start_color = (40, 170, 80)
        self.end_color = (200, 50, 50)
        self.current_color = (50, 110, 220)

        self.parameter_color = (230, 220, 160)
        self.parameter_satisfied_color = (170, 230, 170)
        self.parameter_text_color = (20, 20, 20)
        self.status_text_color = (30, 30, 30)

    def run(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Witness-style Puzzle Prototype")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, int(self.cell_size * 0.55))
        self.status_font = pygame.font.SysFont(None, 22)

        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.puzzle.move_player(0, -1)

                elif event.key == pygame.K_RIGHT:
                    self.puzzle.move_player(1, 0)

                elif event.key == pygame.K_DOWN:
                    self.puzzle.move_player(0, 1)

                elif event.key == pygame.K_LEFT:
                    self.puzzle.move_player(-1, 0)

                elif event.key == pygame.K_r:
                    self.puzzle.reset_filled_paths()

                elif event.key == pygame.K_ESCAPE:
                    self.running = False

    def draw(self):
        self.screen.fill(self.bg_color)

        self.draw_grid()

        for y in range(self.puzzle.rows):
            for x in range(self.puzzle.cols):
                cell = self.puzzle.field[y][x]

                if isinstance(cell, Path):
                    self.draw_path(cell)

                elif isinstance(cell, Parameter):
                    self.draw_parameter(cell)

        self.draw_status()

    def draw_grid(self):
        for y in range(self.puzzle.rows):
            for x in range(self.puzzle.cols):
                rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )

                pygame.draw.rect(self.screen, self.grid_color, rect, 1)

    def draw_path(self, path):
        path.update_pose(self.puzzle.field)

        x = path.x
        y = path.y

        cx = x * self.cell_size + self.cell_size // 2
        cy = y * self.cell_size + self.cell_size // 2

        half = self.cell_size // 2

        if path.filled:
            color = self.filled_path_color
            width = max(4, self.cell_size // 8)
            radius = max(5, self.cell_size // 8)
        else:
            color = self.path_color
            width = max(2, self.cell_size // 14)
            radius = max(4, self.cell_size // 10)

        top, right, bottom, left = path.pose

        if top:
            pygame.draw.line(
                self.screen,
                color,
                (cx, cy),
                (cx, cy - half),
                width,
            )

        if right:
            pygame.draw.line(
                self.screen,
                color,
                (cx, cy),
                (cx + half, cy),
                width,
            )

        if bottom:
            pygame.draw.line(
                self.screen,
                color,
                (cx, cy),
                (cx, cy + half),
                width,
            )

        if left:
            pygame.draw.line(
                self.screen,
                color,
                (cx, cy),
                (cx - half, cy),
                width,
            )

        pygame.draw.circle(self.screen, color, (cx, cy), radius)

        if path.is_start:
            pygame.draw.circle(
                self.screen,
                self.start_color,
                (cx, cy),
                max(8, self.cell_size // 5),
                3,
            )

        if path.is_end:
            pygame.draw.circle(
                self.screen,
                self.end_color,
                (cx, cy),
                max(8, self.cell_size // 5),
                3,
            )

        if path is self.puzzle.current_path:
            pygame.draw.circle(
                self.screen,
                self.current_color,
                (cx, cy),
                max(10, self.cell_size // 4),
                2,
            )

    def draw_parameter(self, parameter):
        x = parameter.x
        y = parameter.y

        rect = pygame.Rect(
            x * self.cell_size + self.cell_size * 0.18,
            y * self.cell_size + self.cell_size * 0.18,
            self.cell_size * 0.64,
            self.cell_size * 0.64,
        )

        color = (
            self.parameter_satisfied_color
            if parameter.satisfied
            else self.parameter_color
        )

        pygame.draw.ellipse(self.screen, color, rect)
        pygame.draw.ellipse(self.screen, self.parameter_text_color, rect, 2)

        text_surface = self.font.render(
            str(parameter.required),
            True,
            self.parameter_text_color,
        )

        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_status(self):
        status_y = self.puzzle.rows * self.cell_size + 8

        if self.puzzle.game_status == "win":
            status_text = "WIN"
        elif self.puzzle.game_status == "try_again":
            status_text = "TRY AGAIN - press R"
        else:
            status_text = "Playing"

        lines = [
            status_text,
            "Arrows: move | R: reset | Esc: quit",
        ]

        for i, line in enumerate(lines):
            text_surface = self.status_font.render(
                line,
                True,
                self.status_text_color,
            )
            self.screen.blit(
                text_surface,
                (12, status_y + i * 22),
            )
