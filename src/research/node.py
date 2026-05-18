class Node:
    def __init__(self, name, longitude, latitude, country):
        self.name = name
        self.longitude: float = longitude
        self.latitude: float = latitude
        self.country = country

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return (
            self.name == other.name
            and self.longitude == other.longitude
            and self.latitude == other.latitude
            and self.country == other.country
        )

    def __hash__(self):
        return hash((self.name, self.longitude, self.latitude, self.country))

    def __repr__(self):
        return (
            f"Node(name={self.name!r}, longitude={self.longitude!r}, "
            f"latitude={self.latitude!r}, country={self.country!r})"
        )
