import pymunk
from collections import namedtuple
from enum import IntEnum, unique


__all__ = ['Vector', 'Ball', 'Platform', 'Field']


Vector = namedtuple('Vector', 'x y')


@unique
class CollisionType(IntEnum):
    BALL = 1
    PLAYER_LEFT = 2
    PLAYER_RIGHT = 3
    SENSOR_LEFT = 4
    SENSOR_RIGHT = 5


class Ball:
    RADIUS = 5

    def __init__(self, position: Vector, direction: Vector) -> None:
        self._position = position
        self._body = pymunk.Body(1, pymunk.inf)
        self._body.position = position

        self._shape = pymunk.Circle(self._body, self.RADIUS)
        self._shape.elasticity = 1.0
        self._shape.collision_type = CollisionType.BALL

        self._body.apply_impulse_at_local_point(pymunk.Vec2d(direction))

        def constant_velocity(body: pymunk.Body, gravity, damping, dt):
            body.velocity = body.velocity.normalized() * 400
        self._body.velocity_func = constant_velocity

    def add_to_space(self, space):
        space.add(self._body, self._shape)

    @property
    def position(self):
        return self._position


class Platform:
    def __init__(self, position: Vector):
        # super().__init__(position)
        pass


class Field:
    def __init__(self, width, height):
        self._space = pymunk.Space()
        borders = [
            pymunk.Segment(self._space.static_body, (0, 800), (0, 800), 2),
            pymunk.Segment(self._space.static_body, (0, 800), (800, 800), 2),
            pymunk.Segment(self._space.static_body, (800, 800), (800, 0), 2),
            pymunk.Segment(self._space.static_body, (800, 0), (0, 0), 2)

            # pymunk.Segment(self._space.static_body, (0, 0), (width, 0), 2),
            # pymunk.Segment(self._space.static_body, (0, height),
            #                (width, height), 2),
        ]
        for border in borders:
            border.elasticity = 1.0

        self._space.add(borders)

        # left_sensor = pymunk.Segment(self._space.static_body, (0, 0),
        #                              (0, height), 2)
        # left_sensor.sensor = True
        # left_sensor.collision_type = CollisionType.SENSOR_LEFT
        #
        # def _handler(arbiter, space, data):
        #     print('test')
        #     return True
        #
        # h = self._space.add_collision_handler(CollisionType.BALL,
        #                                       CollisionType.SENSOR_LEFT)
        # h.begin = _handler
        # self._space.add(left_sensor)

        self._ball = Ball(Vector(width // 2, height // 2), Vector(1, 10))
        self._ball.add_to_space(self._space)

    def update(self, delta):
        self._space.step(delta)
