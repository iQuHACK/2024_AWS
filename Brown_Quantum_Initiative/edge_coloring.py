def color_edges_of_complete_graph(n):
    # Determine the number of colors needed (chromatic index)
    num_colors = n if n % 2 == 1 else n - 1

    # Initialize the colors for each edge
    # edge_colors = {}
    colors_to_edges = dict()
    for color in range(n):
        colors_to_edges[color] = []

    # Assign colors to edges
    for i in range(n):
        for j in range(i + 1, n):
            # For each edge (i, j), assign a color based on a greedy approach
            # We use the modulo operator to cycle through colors
            color = (i + j) % num_colors
            colors_to_edges[color].append((i, j))

    return colors_to_edges
