"""Class and functions for specifying movements and getting incidence counts."""

class Movement:
    """Specifies a path sub-sequence.

    A movement specifies a sub-path sequence on a network. Movements are
    specified using a list. Within the list an Ellipsis (``...``) will match
    zero or more nodes. Any other value must match a node in the path exactly.
    Each path on the network is incident on the movement zero or more times. For
    example if the movement is ``[..., 2, 3, ...]``, the paths ``[1, 2, 3]`` and
    ``[1, 2, 3, 4]`` are each incident once on the movement; the path ``[2, 3,
    2, 3]`` is incident twice; and the path ``[4, 5, 6]`` is incident zero
    times. These examples and others are listed in the table below.

    ===================== ================ ===============
    movement              path             incidence count
    ===================== ================ ===============
    ``[..., 2, 3, ...]``  ``[1, 2, 3]``     1
    ``[..., 2, 3, ...]``  ``[1, 2, 3, 4]``  1
    ``[..., 2, 3, ...]``  ``[2, 3, 2, 3]``  2
    ``[..., 2, 3, ...]``  ``[4, 5, 6]``     0
    ``[2, 3]``            ``[1, 2, 3]``     0
    ``[2, 3]``            ``[2, 3]``        1
    ``[2, 3]``            ``[2]``           0
    ``[..., 1]``          ``[1]``           1
    ``[..., 1]``          ``[2, 1]``        1
    ``[..., 1]``          ``[2, 1, 0]``     0
    ===================== ================ ===============


    Args:
        movement: the movement specification list. May include ellipsis.

    Examples:
        Initialize a Movement instance:

        >>> from felt import Movement
        >>> movement = Movement([..., 2, 3, ...])
    """
    def __init__(self, movement):
        self._movement = movement

    def incidence_count(self, path):
        """Get the incidence count for a path on the movement.
        
        Args:
            path: a list or Path instance

        Returns:
            int: the incidence count; always non-negative.

        Examples:
            Get an incidence count:

            >>> from felt import Movement
            >>> movement = Movement([..., 2, 3, ...])
            >>> movement.incidence_count([1, 2, 3])
            1

        """
        return _incidence_count(self._movement, list(path))

class NoMovement(Exception):
    """Used in incidence counts functions to signal that the path
    is not incident on the movement."""
    pass

def _incidence_count(movement, path):
    movement = movement[:]
    path = path[:]

    if not movement:
        raise ValueError('movement cannot be empty')
    if not path:
        raise ValueError('path cannot be empty')

    count = 0
    while path:
        try:
            path = _match_movement(movement, path)
        except NoMovement:
            break
        else:
            count += 1
    return count

def _match_movement(movement, path):
    while movement:
        movement, path = _match_movement_elem(movement, path)
    if movement:
        raise NoMovement()
    return path

def _match_movement_elem(movement, path):
    movement = movement[:]
    path = path[:]

    if movement[0] == Ellipsis:
        while movement and (movement[0] == Ellipsis):
            movement.pop(0)
        if not movement:
            return [], path
        x = movement.pop(0)
        try:
            i = path.index(x)
        except ValueError:
            raise NoMovement()
        else:
            return  movement, path[i+1:]
    else:
        if not path:
            raise NoMovement()
        x = movement.pop(0)
        if x == path[0]:
            return movement, path[1:]
        else:
            raise NoMovement()
