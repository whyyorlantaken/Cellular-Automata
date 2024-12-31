# Libraries
import numpy as np
from multiprocessing import Pool
import matplotlib.pyplot as plt
from IPython.display import Image
import imageio
from pathlib import Path
from tqdm import tqdm


class LifeLikeCA:

    def __init__(self, rule: int = 5, matrix: np.ndarray = None):

        # Attributes
        self.rule = rule
        self.matrix = matrix
        self.n, self.m = matrix.shape

    def get_rules(self):

        # Convert the integer to binary
        binary = np.binary_repr(self.rule, width = 18)

        # Reverse the string
        binary = binary[::-1]

        # Extract the birth and survive rules
        birth = np.array([int(x) for x in binary[:9]])
        survive = np.array([int(x) for x in binary[9:]])

        # Get the indices of the 1s
        birth_rule = np.where(birth)[0]
        survive_rule = np.where(survive)[0]

        return birth_rule, survive_rule

    def moore_neighbors(self, row, col):
    
        # Get the indices (the order doesn't matter)
        indices = np.array([
            #[row, col],        

            [(row - 1) % self.n, col],            # up
            [(row + 1) % self.n, col],            # down
            [row, (col - 1) % self.m],            # left
            [row, (col + 1) % self.m],            # right
            
            [(row - 1) % self.n, (col - 1) % self.m],  # upper left
            [(row - 1) % self.n, (col + 1) % self.m],  # upper right
            [(row + 1) % self.n, (col - 1) % self.m],  # lower left
            [(row + 1) % self.n, (col + 1) % self.m]   # lower right
        ])
        
        return self.matrix[indices[:, 0], indices[:, 1]]
    
    def parallel_count(self, processors = 4):
        
        # Create all coordinates
        coords = np.array([(i, j) for i in range(self.n) for j in range(self.m)])
        
        # Split coordinates into chunks: one per processor
        coord_chunks = np.array_split(coords, processors)
        
        # Prepare arguments for each process
        args = [(self.matrix, chunk, self.n, self.m) for chunk in coord_chunks]
        
        # Pool of processors
        with Pool(processors) as pool:

            # Call the function for each set of coordinates
            # and run it in parallel
            results = pool.map(self.count, args)
        
        # Combine them
        return np.concatenate(results).reshape(self.n, self.m)

    def count(self, args):

        # Unpack the arguments
        matrix, coords, self.n, self.m = args

        # Initialize the counts
        counts = np.zeros(len(coords), dtype = int)
        
        # Loop over the coordinates: enumerate gives the index and the value
        for i, (row, col) in enumerate(coords):

            # Get the neighbors
            neighbors = self.moore_neighbors(row, col)

            # Count them
            counts[i] = np.sum(neighbors)
        
        return counts
    
    def movie(self, generations: int, processors: int, fps: int = 5,
              path: str = ".", shape = (6, 6), cmap: str = "Blues",
              gif_name: str = "movie", display: bool = False):
        
        # Get the rules
        birth, survive = self.get_rules()

        # Save the initial state
        self.image(state = self.matrix, path = path + "0000.png", shape = shape, cmap = cmap)

        # Loop
        for m in range(generations):

            # Create an empty matrix
            new_matrix = np.zeros((self.n, self.m), dtype = int)

            # Get the neighbors
            all_neighbours = self.parallel_count(processors)

            # Loop over each cell
            for i in range(self.n):
                for j in range(self.m):

                    # Cell neighbors
                    neighbours = all_neighbours[i, j]

                    # Apply the rules:
                    # 1. Birth
                    if self.matrix[i, j] == 0 and neighbours in birth:
                        new_matrix[i, j] = 1

                    # 2. Survival
                    elif self.matrix[i, j] == 1 and neighbours in survive:
                        new_matrix[i, j] = 1

                    # 3. Death
                    else:
                        new_matrix[i, j] = 0

            # Restart
            self.matrix = new_matrix.copy()

            # Save the image
            self.image(state = self.matrix, path = f"{path}{str(m+1).zfill(4)}.png", shape = shape,
                      cmap = cmap)
            
        # Print update
        print(f"All images have been generated.\n")

        # Get all files
        files = Path(path).glob('*.png')

        # Sort them numerically
        files = sorted(files, key=lambda x: int(x.stem))
        
        # Create a list to save the images
        images = []

        # Read images with progress bar
        for f in tqdm(files, desc="Reading images"):
            images.append(imageio.imread(f))
    
        # Save GIF
        imageio.mimsave(f'{path}/{gif_name}.gif', images, fps = fps, loop = 0)

        # Print the direction of the gif
        print(f"\nGif is in {path} as {gif_name}.gif.\n")

        # Display the GIF
        if display:
            
            print(f"Displaying the gif...\n")

            return Image(filename = f'{path}/{gif_name}.gif')

    def image(self, state, path: str = ".", shape = (5,5),
              cmap: str = "Blues", show: bool = False, save: bool = True):
        
        # Create the plot with tight layout and no padding
        fig = plt.figure(figsize = shape, frameon=False)
        plt.imshow(state, cmap = cmap, aspect='auto')
        plt.axis("off")
        
        plt.gca().set_position([0, 0, 1, 1])
        plt.margins(0,0)
        
        if show:
            plt.show()
        if save:
            plt.savefig(path, bbox_inches='tight', pad_inches=0)
        plt.close()
    
    def __str__(self):
        return f"Born with {self.get_rules()[0]} and survive with {self.get_rules()[1]} neighbors."