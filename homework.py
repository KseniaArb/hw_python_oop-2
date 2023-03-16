from dataclasses import dataclass, asdict
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    INFORMATION = ('Тип тренировки: {training_type}; '
                   'Длительность: {duration:.3f} ч.; '
                   'Дистанция: {distance:.3f} км; '
                   'Ср. скорость: {speed:.3f} км/ч; '
                   'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.INFORMATION.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка спортивная ходьба."""

    KMH_IN_MSEC = 0.278
    CM_IN_M = 100
    MIN_IN_H = 60
    COEFFICIENT_WEIGHT = 0.035
    COEFFICIENT_WEIGHT_1 = 0.029

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_mean_speed(self) -> float:
        """Calculates mean speed while walking."""
        mean_speed = self.get_distance() / self.duration
        return (mean_speed)

    def get_spent_calories(self) -> float:
        """Calculates the calories spent while walking."""
        calories = (((self.COEFFICIENT_WEIGHT
                     * self.weight
                     + (((self.get_mean_speed()
                      * self.KMH_IN_MSEC) ** 2)
                      / (self.height / self.CM_IN_M))
                     * self.COEFFICIENT_WEIGHT_1
                     * self.weight))
                    * self.duration * 60
                    )

        return (calories)


class Swimming(Training):
    """Тренировка плавание."""

    LEN_STEP = 1.38
    COEFFICIENT_MID_SPEED = 1.1
    COEFFICIENT_WEIGHT = 2
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                 + self.COEFFICIENT_MID_SPEED)
                * self.COEFFICIENT_WEIGHT
                * self.weight
                * self.duration)

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    TRAININGS: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in TRAININGS:
        raise KeyError(f'Тип тренировки не известен {workout_type}')
    return TRAININGS [workout_type](*data)


if __name__ == '__main__':
    for workout_type, data in packages:
        training = read_package(workout_type, data)

packages = [
    ('SWM', [720, 1, 80, 25, 40]),
    ('RUN', [15000, 1, 75]),
    ('WLK', [9000, 1, 75, 180]),
]
