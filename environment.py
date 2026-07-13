from enum import Enum, auto
import copy


class CellType(Enum):
    WALL = auto()
    GRASS = auto()
    START = auto()
    END = auto()
    PIT = auto()
    DIAMOND = auto()


class Action(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


ACTION_DELTA = {
    Action.UP:    (-1, 0),
    Action.DOWN:  (1, 0),
    Action.LEFT:  (0, -1),
    Action.RIGHT: (0, 1),
}

REWARDS = {
    "step": -1,
    "diamond": 30,
    "goal": 100,
    "pit": -100,
}

# Исходная карта - НЕ меняется во время эпизодов, только читается
GRID = [
    [CellType.GRASS, CellType.GRASS, CellType.GRASS, CellType.END],
    [CellType.GRASS, CellType.WALL,  CellType.GRASS, CellType.DIAMOND],
    [CellType.START, CellType.GRASS, CellType.GRASS, CellType.PIT],
]


class GridWorldEnv:
    def __init__(self, grid=GRID):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])

        # находим стартовую позицию и позицию алмаза один раз при создании
        self.start_pos = self._find_cell(CellType.START)
        self.diamond_pos = self._find_cell(CellType.DIAMOND)

        # состояние текущего эпизода (задаётся в reset())
        self.robot_pos = None
        self.diamond_collected = None
        self.done = None
        self.steps = None
        self.score = None

        self.reset()

    def _find_cell(self, cell_type):
        """Найти координаты (row, col) первой клетки заданного типа на карте."""
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col] == cell_type:
                    return (row, col)
        return None

    def reset(self):
        """Сбросить среду в начальное состояние нового эпизода.
        Возвращает начальное состояние."""
        self.robot_pos = list(self.start_pos)
        self.diamond_collected = False
        self.done = False
        self.steps = 0
        self.score = 0
        return self.get_state()

    def get_state(self):
        """Текущее состояние агента: позиция + собран ли алмаз.
        Алмаз обязателен в состоянии - иначе агент не отличит
        "здесь алмаз ещё лежит" от "я его уже забрал"."""
        row, col = self.robot_pos
        return (row, col, self.diamond_collected)

    def step(self, action):
        """Выполнить действие. Возвращает (new_state, reward, done)."""
        if self.done:
            # эпизод уже закончен - ничего не меняем
            return self.get_state(), 0, True

        d_row, d_col = ACTION_DELTA[action]
        new_row = self.robot_pos[0] + d_row
        new_col = self.robot_pos[1] + d_col

        reward = REWARDS["step"]

        # проверка границ и стены - если нельзя пройти, позиция не меняется,
        # но штраф за шаг всё равно начисляется (агент "потратил ход" впустую)
        in_bounds = 0 <= new_row < self.height and 0 <= new_col < self.width
        if in_bounds and self.grid[new_row][new_col] != CellType.WALL:
            self.robot_pos[0] = new_row
            self.robot_pos[1] = new_col

        self.steps += 1
        cell = self.grid[self.robot_pos[0]][self.robot_pos[1]]

        # проверка событий на текущей клетке
        if cell == CellType.DIAMOND and not self.diamond_collected:
            self.diamond_collected = True
            reward += REWARDS["diamond"]

        elif cell == CellType.PIT:
            reward += REWARDS["pit"]
            self.done = True

        elif cell == CellType.END:
            reward += REWARDS["goal"]
            self.done = True

        self.score += reward
        return self.get_state(), reward, self.done