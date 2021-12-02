class OutputService:
    """
    Outputs the game state. The responsibility of the class of objects is to draw the game state on the terminal. 
    """
        
    def draw_actor(self, actor):
        """Renders the given actors on the screen.

        Args:
            actor (Actor): The actor to render.
        """
        actor.draw()

    def draw_actors(self, actors):
        """Renders the given list of actors on the screen.

        Args:
            actors (list): The actors to render.
        """ 
        for actor in actors:
            self.draw_actor(actor)