# from dataclasses import dataclass
# import time

# @dataclass
# class A:
#     timestamp: float = time.time()
#     path: str = "folder/" + str(timestamp)

# a1 = A()
# time.sleep(5)
# a2 = A()

# print("a1:", a1.timestamp, a1.path)
# print("a2:", a2.timestamp, a2.path)
from src.pipeline.training_pipeline import TrainingPipeline

if __name__ == "__main__":
    pipeline = TrainingPipeline()
    pipeline.run_pipeline()