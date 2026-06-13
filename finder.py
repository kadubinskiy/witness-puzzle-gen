from collections import deque

from playfield import Path, Parameter


class PuzzleFinder:
    def __init__(self, puzzle, algorithm="dfs"):
        self.puzzle = puzzle
        self.algorithm = algorithm
        self.reviewed = set()
        self.accepted = set()
        self.rejected = set()
        self.solution_path = []
        self.explored_states = 0
        self.dead_ends = 0
        self.search_trace = []

        self.solutions = []
        self.dead_end_paths = []
        self.selected_solution_index = 0
        self.selected_dead_end_index = 0
        self.selected_dead_end_path = []
        self.display_mode = "solution"

    def coord(self, path):
        return (path.x, path.y)

    def path_to_coords(self, path):
        return {self.coord(node) for node in path}

    def get_path_at(self, x, y):
        if not self.puzzle.is_in_bounds(x, y):
            return None

        cell = self.puzzle.field[y][x]

        if isinstance(cell, Path):
            return cell

        return None

    def get_neighbours(self, path):
        neighbours = []
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        for dx, dy in directions:
            neighbour = self.get_path_at(path.x + dx, path.y + dy)

            if neighbour is not None:
                neighbours.append(neighbour)

        return neighbours

    def count_adjacent_candidate_paths(self, parameter, candidate_coords):
        count = 0
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        for dx, dy in directions:
            nx = parameter.x + dx
            ny = parameter.y + dy

            if (nx, ny) in candidate_coords:
                count += 1

        return count

    def validate_parameter_against_candidate(self, parameter, candidate_coords):
        count = self.count_adjacent_candidate_paths(parameter, candidate_coords)
        parameter_type = getattr(parameter, "parameter_type", "exact")
        required = getattr(parameter, "required", 1)

        if parameter_type == "exact":
            return count == required
        if parameter_type == "minimum":
            return count >= required
        if parameter_type == "maximum":
            return count <= required
        if parameter_type == "even":
            return count % 2 == 0
        if parameter_type == "odd":
            return count % 2 == 1

        raise ValueError(f"Unknown parameter type: {parameter_type}")

    def validate_all_parameters_against_candidate(self, candidate_path):
        candidate_coords = {self.coord(path) for path in candidate_path}
        return all(
            self.validate_parameter_against_candidate(parameter, candidate_coords)
            for parameter in self.puzzle.parameters
        )

    def reset_search_state(self):
        self.reviewed = set()
        self.accepted = set()
        self.rejected = set()
        self.solution_path = []
        self.solutions = []
        self.dead_end_paths = []
        self.selected_solution_index = 0
        self.selected_dead_end_index = 0
        self.selected_dead_end_path = []
        self.display_mode = "solution"
        self.search_trace = []
        self.explored_states = 0
        self.dead_ends = 0

    def solve(self, algorithm=None, **kwargs):
        algorithm = algorithm or self.algorithm
        self.algorithm = algorithm

        if algorithm == "dfs":
            return self.find_solutions(**kwargs)

        if algorithm == "bfs":
            max_dead_ends = kwargs.get("max_dead_ends", 100)
            max_states = kwargs.get("max_states", 10000)
            return self.find_shortest_bfs(
                max_dead_ends=max_dead_ends,
                max_states=max_states,
            )

        raise ValueError(f"Unknown search algorithm: {algorithm}")

    def find_solution(self):
        return self.solve()

    def find_solutions(self, max_solutions=50, max_dead_ends=100):
        self.reset_search_state()

        if self.puzzle.start is None or self.puzzle.end is None:
            raise ValueError("Puzzle must have start and end before solving")

        self._dfs(
            current=self.puzzle.start,
            target=self.puzzle.end,
            visited=set(),
            path=[],
            max_solutions=max_solutions,
            max_dead_ends=max_dead_ends,
        )

        return self._finalize_search_results()

    def find_shortest_bfs(self, max_dead_ends=100, max_states=10000):
        self.reset_search_state()

        if self.puzzle.start is None or self.puzzle.end is None:
            raise ValueError("Puzzle must have start and end before solving")

        start = self.puzzle.start
        end = self.puzzle.end
        start_coord = self.coord(start)

        queue = deque([(start, [start], {start_coord})])

        while queue:
            if self.explored_states >= max_states:
                return self._finalize_search_results()

            current, path, visited = queue.popleft()
            current_coord = self.coord(current)

            self.reviewed.add(current_coord)
            self.search_trace.append(("reviewed", current_coord))
            self.explored_states += 1

            if current is end:
                if self.validate_all_parameters_against_candidate(path):
                    self.solutions = [path.copy()]
                    self.solution_path = path.copy()
                    self.accepted = self.path_to_coords(self.solution_path)
                    self.display_mode = "solution"
                    for node in path:
                        self.search_trace.append(("accepted", self.coord(node)))
                    return True

                self.dead_ends += 1

                if len(self.dead_end_paths) < max_dead_ends:
                    self.dead_end_paths.append(path.copy())

                for node in path:
                    node_coord = self.coord(node)
                    self.rejected.add(node_coord)
                    self.search_trace.append(("rejected", node_coord))

                continue

            for neighbour in self.get_neighbours(current):
                neighbour_coord = self.coord(neighbour)

                if neighbour_coord not in visited:
                    next_visited = set(visited)
                    next_visited.add(neighbour_coord)
                    queue.append((
                        neighbour,
                        path + [neighbour],
                        next_visited,
                    ))

        return self._finalize_search_results()

    def _finalize_search_results(self):
        self.solutions.sort(key=len)

        if self.solutions:
            self.selected_solution_index = 0
            self.solution_path = self.solutions[0]
            self.accepted = self.path_to_coords(self.solution_path)
            self.display_mode = "solution"
            return True

        self.solution_path = []
        self.accepted = set()
        self.display_mode = "dead_end" if self.dead_end_paths else "solution"

        if self.dead_end_paths:
            self.selected_dead_end_index = 0
            self.selected_dead_end_path = self.dead_end_paths[0]

        return False

    def _dfs(self, current, target, visited, path, max_solutions, max_dead_ends):
        if len(self.solutions) >= max_solutions:
            return

        current_coord = self.coord(current)

        self.reviewed.add(current_coord)
        self.search_trace.append(("reviewed", current_coord))
        self.explored_states += 1

        visited.add(current_coord)
        path.append(current)

        if current is target:
            if self.validate_all_parameters_against_candidate(path):
                if len(self.solutions) < max_solutions:
                    self.solutions.append(path.copy())
                    for node in path:
                        self.search_trace.append(("accepted", self.coord(node)))
            else:
                self.dead_ends += 1

                if len(self.dead_end_paths) < max_dead_ends:
                    self.dead_end_paths.append(path.copy())

                for node in path:
                    node_coord = self.coord(node)
                    self.rejected.add(node_coord)
                    self.search_trace.append(("rejected", node_coord))

            path.pop()
            visited.remove(current_coord)
            return

        found_any_unvisited = False

        for neighbour in self.get_neighbours(current):
            if len(self.solutions) >= max_solutions:
                break

            neighbour_coord = self.coord(neighbour)

            if neighbour_coord not in visited:
                found_any_unvisited = True
                self._dfs(neighbour, target, visited, path, max_solutions, max_dead_ends)

        if not found_any_unvisited:
            self.dead_ends += 1

        self.rejected.add(current_coord)
        self.search_trace.append(("rejected", current_coord))

        path.pop()
        visited.remove(current_coord)

    def set_selected_solution(self, index):
        if not self.solutions:
            return False

        self.selected_solution_index = index % len(self.solutions)
        self.display_mode = "solution"
        self.solution_path = self.solutions[self.selected_solution_index]
        self.accepted = self.path_to_coords(self.solution_path)
        return True

    def next_solution(self):
        if not self.solutions:
            return False

        return self.set_selected_solution(self.selected_solution_index + 1)

    def previous_solution(self):
        if not self.solutions:
            return False

        return self.set_selected_solution(self.selected_solution_index - 1)

    def set_selected_dead_end(self, index):
        if not self.dead_end_paths:
            return False

        self.selected_dead_end_index = index % len(self.dead_end_paths)
        self.display_mode = "dead_end"
        self.selected_dead_end_path = self.dead_end_paths[self.selected_dead_end_index]
        return True

    def next_dead_end(self):
        if not self.dead_end_paths:
            return False

        return self.set_selected_dead_end(self.selected_dead_end_index + 1)

    def previous_dead_end(self):
        if not self.dead_end_paths:
            return False

        return self.set_selected_dead_end(self.selected_dead_end_index - 1)

    def get_selected_solution_coords(self):
        if self.solution_path:
            return self.path_to_coords(self.solution_path)

        return set()

    def get_selected_dead_end_coords(self):
        if self.selected_dead_end_path:
            return self.path_to_coords(self.selected_dead_end_path)

        return set()

    def get_search_summary(self):
        return {
            "algorithm": self.algorithm,
            "found": bool(self.solutions),
            "solution_count": len(self.solutions),
            "dead_end_count": len(self.dead_end_paths),
            "explored_states": self.explored_states,
            "dead_ends": self.dead_ends,
            "selected_solution_index": self.selected_solution_index,
            "selected_dead_end_index": self.selected_dead_end_index,
            "solution_length": len(self.solution_path),
            "reviewed_count": len(self.reviewed),
            "accepted_count": len(self.accepted),
            "rejected_count": len(self.rejected),
            "display_mode": self.display_mode,
        }
