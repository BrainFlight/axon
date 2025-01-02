import ray

from config import GlobalConfig


@ray.remote
class TrainingJobRunner:
    def __init__(self, config: GlobalConfig):
        self.config = config

    def run_training_job(
        self, model_name: str, model_args: dict, num_cpus: int = 1, num_gpus: int = 1
    ):
        """
        Run training job.

        Args:
            model_name (str): Model name.
            model_args (dict): Model arguments.
            num_cpus (int): Number of CPUs.
            num_gpus (int): Number of GPUs.

        Returns:
            str: Training job status.
        """
        pass
