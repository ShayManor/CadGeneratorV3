from src.helpers.create_path import create_path


def create_model(prompt: str, path: str, feedback: str = None):
    """
    Creates cad model from updated feedback and prompt
    :param path: Path to model
    :param prompt: Original prompt to create model
    :param feedback: Feedback from previous model, can be None
    :return: Nothing
    """


def get_feedback(prompt: str, path: str) -> str:
    pass


def create_full_model(prompt: str, name: str, iterations: int = 1) -> str:
    """
    :param name: Name of cad model
    :param iterations: Number of iterations
    :param prompt: Prompt to create cad model
    :return: Path to created cad model
    """
    path = None
    feedback = None
    for iteration in range(iterations):
        print(f"Begin iteration {iteration + 1}")
        if iteration != 0:
            feedback = get_feedback(prompt, path)
        path = create_path(name)
        create_model(prompt, path, feedback)

        #  If there is a previous cad model, get feedback
        #  Call create_model to make the new cad model
    return path
