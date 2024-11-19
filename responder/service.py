import networkx as nx
import osmnx as ox

def get_shortest_path(customer_location, responder_location):
    """
    Calculate the shortest path between the customer and responder using Dijkstra's algorithm.
    
    Parameters:
    - customer_location: Tuple (latitude, longitude) of the customer's location.
    - responder_location: Tuple (latitude, longitude) of the responder's location.
    
    Returns:
    - List of coordinates [(lat, lon), ...] representing the shortest path.
    """
    try:
        # Create a bounding box with some buffer distance
        buffer_distance = 0.01  # ~1km buffer (in degrees)
        south = min(customer_location[0], responder_location[0]) - buffer_distance
        north = max(customer_location[0], responder_location[0]) + buffer_distance
        west = min(customer_location[1], responder_location[1]) - buffer_distance
        east = max(customer_location[1], responder_location[1]) + buffer_distance

        # Use the new bbox parameter (south, west, north, east)
        G = ox.graph_from_bbox(north, south, east, west, network_type='drive')

        if G is None or len(G.nodes) == 0:
            raise ValueError("No graph nodes found within the requested bounding box.")

        # Find the nearest nodes to the customer and responder locations
        start_node = ox.distance.nearest_nodes(G, customer_location[1], customer_location[0])
        end_node = ox.distance.nearest_nodes(G, responder_location[1], responder_location[0])

        # Find the shortest path using Dijkstra's algorithm
        shortest_path = nx.shortest_path(G, source=start_node, target=end_node, weight='length')

        # Convert the path to a list of coordinates
        path_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in shortest_path]

        return path_coords
    except Exception as e:
        print(f"Error in get_shortest_path: {e}")
        return []
