import pygame

from playfield import Path, Parameter


class PuzzleGUI:
    def __init__(self, puzzle, finder=None, cell_size=56):
        self.puzzle = puzzle
        self.finder = finder
        self.show_graph = False
        self.cell_size = cell_size
        self.status_height = 144

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

        self.graph_unseen_color = (160, 160, 160)
        self.graph_reviewed_color = (230, 170, 60)
        self.graph_accepted_color = (50, 150, 90)
        self.graph_rejected_color = (200, 80, 80)
        self.graph_edge_color = (180, 180, 180)
        self.graph_accepted_edge_color = (50, 150, 90)
        self.graph_solution_path_color = (40, 110, 220)
        self.graph_dead_end_path_color = (220, 100, 50)

        self.animation_active = False
        self.animation_start = None
        self.animation_end = None
        self.animation_start_time = 0
        self.animation_duration = 120

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
                    self.try_move(0, -1)

                elif event.key == pygame.K_RIGHT:
                    self.try_move(1, 0)

                elif event.key == pygame.K_DOWN:
                    self.try_move(0, 1)

                elif event.key == pygame.K_LEFT:
                    self.try_move(-1, 0)

                elif event.key == pygame.K_r:
                    self.animation_active = False
                    self.puzzle.reset_filled_paths()

                elif event.key == pygame.K_g:
                    self.show_graph = not self.show_graph

                elif event.key == pygame.K_n and self.finder is not None:
                    self.finder.next_solution()

                elif event.key == pygame.K_p and self.finder is not None:
                    self.finder.previous_solution()

                elif event.key == pygame.K_d and self.finder is not None:
                    self.finder.next_dead_end()

                elif event.key == pygame.K_a and self.finder is not None:
                    self.finder.previous_dead_end()

                elif event.key == pygame.K_s and self.finder is not None:
                    self.finder.set_selected_solution(0)

                elif event.key == pygame.K_ESCAPE:
                    self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and hasattr(self, "graph_button_rect"):
                    if self.graph_button_rect.collidepoint(event.pos):
                        self.show_graph = not self.show_graph

    def path_center(self, path):
        return (
            path.x * self.cell_size + self.cell_size // 2,
            path.y * self.cell_size + self.cell_size // 2,
        )

    def try_move(self, dx, dy):
        if self.animation_active:
            return

        old_path = self.puzzle.current_path
        moved = self.puzzle.move_player(dx, dy)
        new_path = self.puzzle.current_path

        if moved and old_path is not None and new_path is not None and old_path is not new_path:
            self.animation_start = self.path_center(old_path)
            self.animation_end = self.path_center(new_path)
            self.animation_start_time = pygame.time.get_ticks()
            self.animation_active = True

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

        if self.show_graph:
            self.draw_graph_overlay()

        self.draw_movement_animation()
        self.draw_status()

    def draw_movement_animation(self):
        if not self.animation_active:
            return

        elapsed = pygame.time.get_ticks() - self.animation_start_time
        t = min(1.0, elapsed / self.animation_duration)

        start_x, start_y = self.animation_start
        end_x, end_y = self.animation_end
        cx = start_x + (end_x - start_x) * t
        cy = start_y + (end_y - start_y) * t

        pygame.draw.circle(self.screen, self.current_color, (int(cx), int(cy)), 8)

        if t >= 1.0:
            self.animation_active = False

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

        label = parameter.get_element()
        font_size = int(self.cell_size * 0.45) if len(label) > 2 else int(self.cell_size * 0.55)
        param_font = pygame.font.SysFont(None, font_size)

        text_surface = param_font.render(
            label,
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

        graph_hint = "Graph ON" if self.show_graph else "Graph OFF"
        lines = [
            status_text,
            "Arrows: move | R: reset | G: graph | N/P: solutions | D/A: dead ends | S: shortest",
            f"[G] Graph ({graph_hint}) | Esc: quit",
        ]

        if self.puzzle.parameters:
            parameter = self.puzzle.parameters[0]
            lines.append(
                f"Parameter: {parameter.parameter_type} {parameter.get_element()}",
            )

        if self.finder is not None:
            summary = self.finder.get_search_summary()
            lines.append(
                "Solver: "
                f"found={summary['found']} | "
                f"solutions={summary['solution_count']} | "
                f"dead_ends={summary['dead_end_count']} | "
                f"explored={summary['explored_states']}",
            )

            if summary["display_mode"] == "solution" and summary["solution_count"] > 0:
                label = (
                    "Shortest found solution"
                    if summary["selected_solution_index"] == 0
                    else "Selected solution"
                )
                lines.append(
                    f"{label} "
                    f"{summary['selected_solution_index'] + 1}/"
                    f"{summary['solution_count']} "
                    f"(len {summary['solution_length']})",
                )
            elif summary["display_mode"] == "dead_end" and summary["dead_end_count"] > 0:
                lines.append(
                    "Dead-end path "
                    f"{summary['selected_dead_end_index'] + 1}/"
                    f"{summary['dead_end_count']}",
                )

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

        graph_label = self.status_font.render(
            "[G]",
            True,
            self.graph_accepted_color if self.show_graph else self.status_text_color,
        )
        graph_x = self.width - graph_label.get_width() - 12
        graph_y = status_y
        self.graph_button_rect = pygame.Rect(
            graph_x - 4,
            graph_y - 2,
            graph_label.get_width() + 8,
            graph_label.get_height() + 4,
        )
        self.screen.blit(graph_label, (graph_x, graph_y))

    def draw_graph_overlay(self):
        for y in range(self.puzzle.rows):
            for x in range(self.puzzle.cols):
                path = self.puzzle.field[y][x]

                if not isinstance(path, Path):
                    continue

                cx, cy = self.path_center(path)

                for dx, dy in [(1, 0), (0, 1)]:
                    neighbour = self.puzzle.get_path_at(path.x + dx, path.y + dy)

                    if neighbour is not None:
                        nx, ny = self.path_center(neighbour)
                        pygame.draw.line(
                            self.screen,
                            self.graph_edge_color,
                            (cx, cy),
                            (nx, ny),
                            1,
                        )

        for y in range(self.puzzle.rows):
            for x in range(self.puzzle.cols):
                path = self.puzzle.field[y][x]

                if not isinstance(path, Path):
                    continue

                coord = (path.x, path.y)
                color = self._graph_node_color(coord)
                radius = self._graph_node_radius(coord)
                cx, cy = self.path_center(path)

                pygame.draw.circle(self.screen, color, (cx, cy), radius)
                pygame.draw.circle(self.screen, (40, 40, 40), (cx, cy), radius, 1)

        if self.finder is not None:
            if self.finder.display_mode == "dead_end" and self.finder.selected_dead_end_path:
                self.draw_path_sequence(
                    self.finder.selected_dead_end_path,
                    self.graph_dead_end_path_color,
                    max(4, self.cell_size // 10),
                    max(8, self.cell_size // 7),
                )
            elif self.finder.solution_path:
                self.draw_path_sequence(
                    self.finder.solution_path,
                    self.graph_solution_path_color,
                    max(6, self.cell_size // 7),
                    max(10, self.cell_size // 5),
                )

    def draw_path_sequence(self, path, color, line_width, node_radius):
        if not path:
            return

        for index in range(len(path) - 1):
            start = self.path_center(path[index])
            end = self.path_center(path[index + 1])
            pygame.draw.line(self.screen, color, start, end, line_width)

        for node in path:
            cx, cy = self.path_center(node)
            pygame.draw.circle(self.screen, color, (cx, cy), node_radius)
            pygame.draw.circle(self.screen, (20, 20, 20), (cx, cy), node_radius, 2)

    def _graph_node_color(self, coord):
        if self.finder is None:
            return self.graph_unseen_color

        if self.finder.display_mode == "dead_end":
            if coord in self.finder.get_selected_dead_end_coords():
                return self.graph_dead_end_path_color

        if coord in self.finder.get_selected_solution_coords():
            return self.graph_accepted_color

        if coord in self.finder.accepted:
            return self.graph_accepted_color
        if coord in self.finder.rejected:
            return self.graph_rejected_color
        if coord in self.finder.reviewed:
            return self.graph_reviewed_color

        return self.graph_unseen_color

    def _graph_node_radius(self, coord):
        if self.finder is None:
            return 6

        if self.finder.display_mode == "dead_end":
            if coord in self.finder.get_selected_dead_end_coords():
                return max(8, self.cell_size // 7)

        if coord in self.finder.get_selected_solution_coords():
            return max(10, self.cell_size // 5)

        return 6
