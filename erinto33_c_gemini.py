import copy
import math
import matplotlib.pyplot as plt

def print_admin(l, max):
    """Prints the current state of the diagonals array up to the given maximum index.

    Args:
        l: The array containing diagonal information in the format [start_vertex, end_vertex, index_of_intersecting_diagonal].
        max: The maximum index to print up to.
    """
    print(f"current max={max}")
    for i in range(max):
        print(f"{i},{l[i]}")  # Prints diagonal information for each index

def w2ws(w, a_array, a_max, o, n):
    """Converts a set of diagonals into a sorted, semicolon-separated string for dictionary keys.

    Args:
        w: The array to store the normalized diagonals.
        a_array: The input array of diagonals.
        a_max: The maximum index of valid diagonals in a_array.
        o: The offset to rotate the diagonals by.
        n: The number of vertices in the polygon.
    """
    # Normalize and sort diagonals after applying rotation offset
    for j_ in range(a_max):
        a = (a_array[j_][0] + o) % n
        b = (a_array[j_][1] + o) % n
        w[j_] = [min(a, b), max(a, b)]
    w.sort()
    # Create a string representation of sorted diagonals
    ws = ""
    for l in w:
        ws += f"{l[0]},{l[1]};"
    return ws

def build_dict(a_array, a_max, rot_dict, u_list, n):
    """Builds a dictionary of rotated diagonal sets and their occurrences,
        and collects unique non-intersecting diagonal sets.

    Args:
        a_array: The input array of diagonals.
        a_max: The maximum index of valid diagonals in a_array.
        rot_dict: The dictionary to store rotated diagonal sets and their counts.
        u_list: The list to store unique non-intersecting diagonal sets.
        n: The number of vertices in the polygon.
    """
    w = [[0, 0] for _ in range(a_max)]  # Initialize an array for normalized diagonals
    ws = w2ws(w, a_array, a_max, 0, n)  # Initial string representation of diagonals

    c = rot_dict.get(ws, 0)  # Get existing count or 0 for new sets
    rot_dict[ws] = c + 1  # Increment count for this diagonal set

    if c == 0:  # If this is a new unique set
        u_list.append(copy.deepcopy(a_array[0:a_max]))  # Add to unique list
        # Explore all rotations of this set
        for i_ in range(1, n):
            ws = w2ws(w, a_array, a_max, i_, n)  
            rot_dict[ws] = rot_dict.get(ws, 0) + 1 

def max_1_intersecting_diagonals(n):
    """Calculates the maximum number of diagonals in an n-sided convex polygon
        such that each diagonal intersects at most one other diagonal in the interior of the polygon.

    Args:
        n: The number of sides of the polygon.
    """
    if n < 4:  # Base case: No intersecting diagonals possible for triangles and below
        return 0

    max_diagonals = 0 
    admin_array = [[0, 1, -1] for _ in range(n * (n + 1) // 2)]  # Store [start, end, intersecting_diagonal_index]
    admin_x = 1  # Index of the current diagonal being considered

    rot_dict = dict()  # Dictionary for rotated diagonal sets and counts
    u_list = list()    # List for unique non-intersecting diagonal sets

    printIt = False  # Debugging flag

    while True:
        # Backtracking logic to systematically explore diagonals...

        admin_x -= 1  # Move to the previous diagonal
        if admin_x < 0:  # If all diagonals have been explored, exit
            break

        # Get information about the current diagonal
        i, last_j, idx = admin_array[admin_x]
        if printIt:
            print(f"back admin_x={admin_x} ({i},{last_j}) idx={idx}")
            printIt = False

        if (
            idx >= 0
        ):  # Restore the count of the affected element if it was changed earlier
            admin_array[idx][2] = -1
            idx = -1

        stop_j = (
            n if i != 0 else n - 1
        )  # Determine the ending vertex for the current diagonal
        for j in range(last_j + 1, stop_j):  # Iterate through possible ending vertices
            valid = True
            # Check if the current diagonal intersects with previous ones
            for x in range(admin_x):
                if diagonals_intersect(i, j, admin_array[x][0], admin_array[x][1]):
                    if idx >= 0 or admin_array[x][2] >= 0:
                        valid = False  # Diagonal intersects, mark it as invalid
                        if idx >= 0:  # Reverse the earlier change if necessary
                            admin_array[idx][2] = -1
                            idx = -1
                        break  # Exit the inner loop since the diagonal is invalid
                    admin_array[x][2] = admin_x  # Mark the element as changed
                    idx = x  # Save the index of the changed element

            if valid:  # If the diagonal is valid, add it to the admin_array
                admin_array[admin_x] = [i, j, idx]
                idx = -1
                if (
                    admin_x == max_diagonals
                ):  # If a new maximum is found, update and reset
                    max_diagonals += 1
                    rot_dict = dict()
                    u_list = list()
                admin_x += 1
                if admin_x == max_diagonals:
                    build_dict(admin_array, max_diagonals, rot_dict, u_list, n)
                    continue  # Continue to the next diagonal

        # If all ending vertices for the current starting vertex are exhausted
        if i < n - 2:
            # Add a fake element to move to the next starting vertex
            admin_array[admin_x] = [i + 1, i + 2, -1]
            admin_x += 1
        else:
            # printIt=True
            pass
    if False:
        for k in rot_dict.keys():
            print(f"{rot_dict[k]}*")
            print(k)
        print(f"Number of solutions {len(u_list)}")
        for l in u_list:
            print_admin(l, max_diagonals)
    plot_polygons_with_diagonals(u_list)

    return max_diagonals


def diagonals_intersect(i1, j1, i2, j2):
    """Checks if two diagonals intersect.

    Args:
        i1, j1: Starting and ending vertices of the first diagonal.
        i2, j2: Starting and ending vertices of the second diagonal.
    """
    return (i1 < i2 < j1 < j2) or (
        i2 < i1 < j2 < j1
    )  # Simplified check, works for all convex polygons


def plot_polygons_with_diagonals(u_list):
    scale = 4 # to have much larger plot
    plt.figure(figsize=(7.6 * scale, 13.3 * scale))
    plt.axis("off")  # Remove axes
    plt.title("")  # Remove title
    for i, l in enumerate(u_list):
        yo, xo = divmod(i, 4)
        plot_polygon_with_diagonals(n, l, scale, xo * 2.5 * scale, yo * 2.5 * scale)
    plt.savefig("erinto33.jpg")
    plt.close()


def plot_polygon_with_diagonals(n, diagonals, d, xo, yo):
    """Plots a polygon with the given diagonals.

    Args:
        n: The number of sides of the polygon.
        diagonals: A list of diagonals, each represented as a pair of vertex indices.
        xo: offset in x axis
        yo: offset in y exis
    """
    # Calculate coordinates of vertices
    angles = [
        (0.5 - 2 * k / n) * 3.14159265359 for k in range(n)
    ]  # like a clock, but 0 instead of 12
    x = [d * math.cos(a) + xo for a in angles]
    y = [d * math.sin(a) + yo for a in angles]

    # Plot the diagonals
    for d in diagonals:
        plt.plot([x[d[0]], x[d[1]]], [y[d[0]], y[d[1]]], "r-")

    if True:
        # Connect the last point to the first
        plt.plot(x + [x[0]], y + [y[0]], "b-")


# Test for a 12-sided convex polygon
n = 12
max_diagonals = max_1_intersecting_diagonals(n)
print(
    f"In a regular polygon with {n} sides, a maximum of {max_diagonals} diagonals can be drawn such that each diagonal intersects at most one other diagonal in the interior of the polygon."
)
