import dspy

from creator.schemas.simple import SlideTypeUnion


class SimpleUnitCreation(dspy.Signature):
    """Create a learning unit based on a given input."""
    input = dspy.InputField()
    title:str = dspy.OutputField()
    slides:list[SlideTypeUnion] = dspy.OutputField()
