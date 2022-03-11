from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import RandomActivation
from mesa.batchrunner import BatchRunner
from datetime import datetime

from .agent import TreeCell

def num_state(model,state):
    #print(dir(model.grid))
    return sum(1 for a in model.schedule.agents if a.condition is state)

def num_fine(model):
    return num_state(model,"Fine")

def num_onFire(model):
    return num_state(model,"On Fire")

def num_burned(model):
    return num_state(model,"Burned Out")


class ForestFire(Model):
    """
    Simple Forest Fire model.
    """

    def __init__(self, height=100, width=100, density=0.65, chama_inicial=0.45):
        """
        Create a new forest fire model.

        Args:
            height, width: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        """
        # Initialize model parameters
        self.height = height
        self.width = width
        self.density = density

        # Set up model objects
        self.schedule = RandomActivation(self)
        self.grid = Grid(height, width, torus=False)

        self.datacollector = DataCollector(
            {
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
                "Burned Out": lambda m: self.count_type(m, "Burned Out"),
            }
        )

        # Place a tree in each cell with Prob = density
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < self.density:
                # Create a tree
                new_tree = TreeCell((x, y), self)
                # Set all trees in the first column on fire.
                
                if x == 0 and y>chama_inicial:
                    new_tree.condition = "On Fire"
                self.grid._place_agent((x, y), new_tree)
                self.schedule.add(new_tree)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        # Halt if no more fire
        if self.count_type(self, "On Fire") == 0:
            self.running = False

    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count




def batch_run():
        fix_params={
            "width":100,
            "height":100,
        }
        variable_params={
            "density": [0.25, 0.5, 0.75],
            "chama_inicial": [5, 50, 80]
        }
        experiments_per_parameter_configuration = 10
        max_steps_per_simulation = 10
        batch_run = BatchRunner(
            ForestFire,
            variable_parameters=variable_params,
            fixed_parameters=fix_params,
            iterations=10,
            max_steps=100,
            model_reporters={
                "Fine": num_fine,
                "On Fire": num_onFire,
                "Burned Out": num_burned
            }
        )
        batch_run.run_all()

        run_model_data = batch_run.get_model_vars_dataframe()
        #run_agent_data = batch_run.get_agent_vars_dataframe()

        now = str(datetime.now())
        file_name_suffix =  ('_iter_'+str(experiments_per_parameter_configuration)+
                        '_steps_'+str(max_steps_per_simulation)+'_'+
                        now)
        run_model_data.to_csv('model_data'+'.csv')
        #run_agent_data.to_csv('agent_data'+file_name_suffix+'.csv')