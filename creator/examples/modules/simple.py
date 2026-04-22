from creator.main import ContentCreator
import dspy
from ..signatures import SimpleUnitCreation
from creator.main import ContentCreator
from creator.unit.unit import Unit
from llm.provider.openrouter import OpenrouterLM


class Simple(ContentCreator):
    def __init__(self,llm=OpenrouterLM("google/gemma-4-26b-a4b-it"), callbacks=None):
        super().__init__(callbacks)
        self.agent = dspy.Predict(SimpleUnitCreation)
        self.agent.set_lm(llm)


    def forward(self,input, *args, **kwargs) -> Unit:
        result = self.agent(input=input,*args, **kwargs)
        return Unit(**result)
    


__all__ = ["Simple"]