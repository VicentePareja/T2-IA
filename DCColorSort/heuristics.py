def no_heuristic(state):
    '''
        This function uses no computation at all and just returns 0 (Dijkstra's algorithm)

        Returns:
            (int) : a zero.
    '''
    return 0

def wagdy_heuristic(state):
    '''
        For each succesive pair of balls that are not the same color, add an estimated cost of 2

        Returns:
            f (int) : the heuristic's value.
    '''
    cost = 0
    for tube in state.tubes:
        for i in range(len(tube) - 1):
            if tube[i] != tube[i+1]:  # If consecutive balls are of different color
                cost += 2  # Add a cost of 2
    return cost

def repeated_color_heuristic(state):
    '''
        For each ball that is not the same color of the most repeated color in a tube, add
        an estimated cost of 1.

        Returns:
            f (int) : the heuristic's value.
    '''
    cost = 0
    for tube in state.to_list():
        if not tube:
            continue

        # Calculate the count of each color in the tube
        color_counts = {color: tube.count(color) for color in tube}
        
        # Find the most repeated color
        most_repeated_color = max(color_counts, key=color_counts.get)
        
        # Add the balls that are not of the same color as the most repeated color
        cost += sum(1 for color in tube if color != most_repeated_color)

    return cost
