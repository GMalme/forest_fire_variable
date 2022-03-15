from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import RandomActivation
import datetime
from mesa.batchrunner import BatchRunner

from .agent import TreeCell


class ForestFire(Model):
    """
    Simple Forest Fire model.
    """

    def __init__(self, width=100, height=100, density=0.65, prob_fire=0.65, start_fire=0.45):
        """
        Create a new forest fire model.
        Args:
            width, height: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        """
        # Set up model objects
        self.schedule = RandomActivation(self)
        self.grid = Grid(width, height, torus=False)

        self.datacollector = DataCollector(
            {
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
                "Burned Out": lambda m: self.count_type(m, "Burned Out"),
            }
        )

        # Place a tree in each cell with Prob = density
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                # Create a tree
                new_tree = TreeCell((x, y),prob_fire, self)
                # Set all trees in the first column on fire.
                if x == 0 and y<=start_fire:
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

def fine(model):
    return lambda model: model.count_type(model, "Fine")

def fire(model):
    return lambda model: model.count_type(model, "On Fire")

def burned(model):
    return lambda model: model.count_type(model, "Burned Out")




def batch_run():
    fix_params = {
        "height": 100,
        "width": 100,
    }

    variable_params = {
        "density": [0.01, 1.0, 0.5], 
        "prob_fire": [0.01, 0.5, 1.0],
        "start_fire": [5, 50, 90]
    }
    experiments_per_parameter_configuration = 10
    max_steps_per_simulation = 10
    batch_run = BatchRunner(
        ForestFire,
        variable_params,
        fix_params,
        iterations = experiments_per_parameter_configuration,
        max_steps = max_steps_per_simulation,
        model_reporters = {
            "Fine": fine(ForestFire),
            "Fire": fire(ForestFire),
            "Burned Out": burned(ForestFire),
        },
        #agent_reporters= {
         #   "Humid" : humid
        #},

    )

    batch_run.run_all()

    run_model_data = batch_run.get_model_vars_dataframe()
    #run_agent_data = batch_run.get_agent_vars_dataframe() 

    now = datetime.datetime.now().strftime("%Y-%m-%d")
    file_name_suffix =  ("iter"+str(10)+
                        "steps"+str(100)+"lower_firemans"+now
                        )
    run_model_data.to_csv("model_data"+file_name_suffix+".csv")
    #run_agent_data.to_csv("agent_data"+file_name_suffix+".csv")
    