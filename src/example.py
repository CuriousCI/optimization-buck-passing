from openbox import space

SPACE: space.Space = space.Space()
SPACE.add_variables(
    [
        space.Real("x1", -2.5, 2.5, 0),
        space.Real("x2", -2.4, 2.7, 0),
    ],
)
