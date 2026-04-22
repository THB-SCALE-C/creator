from abc import abstractmethod
from typing import Any
from dspy import Prediction
import dspy

from .unit_assembler.UnitAssembler import UnitAssembler
from .unit.unit import Unit


class ContentCreator(dspy.Module):
    """Base DSPy module for generating and packaging learning units.

    Subclasses define the concrete generation architecture in ``__call__`` and
    return a :class:`Unit` instance. Utility class methods support converting
    predictions, assembling content, and exporting assembled H5P units.
    """

    ### CLASS METHODS
    @classmethod
    def assemble_unit_from_dict(cls, content:dict[str,Any]|None,output_dir=".out",out_name="unit.h5p", buffer=False, template_path:str|None=None):
        """Assemble an H5P unit directly from a content dictionary."""
        if not content:
            raise ValueError("No learning unit created. Create first.")
        assembler = UnitAssembler(template_path=template_path)
        presentation = assembler.assemble_content(content)
        assembled_unit_path = assembler.assemble_h5p(presentation, output_dir=output_dir, out_name=out_name,return_buffer=buffer)
        return assembled_unit_path
        
    @classmethod
    def create_unit_from_prediction(cls,prediction:Prediction):
        """Build a :class:`Unit` from a DSPy ``Prediction`` payload."""
        return Unit(**prediction)
    
    @classmethod
    def assemble_unit_from_prediction(cls,prediction:Prediction,output_dir=".out",out_name="unit.h5p", buffer=False, template_path:str|None=None):
        """Create and assemble an H5P unit from a DSPy ``Prediction``."""
        unit = Unit(**prediction)
        assembler = UnitAssembler(template_path=template_path)
        presentation = assembler.assemble_content(unit.to_dict())
        assembled_unit_path = assembler.assemble_h5p(presentation, output_dir=output_dir, out_name=out_name,return_buffer=buffer)
        return assembled_unit_path
    
    @classmethod
    def delete_temp_unit_folder(cls) -> None:
        """Delete temporary assembler artifacts created during unit export."""
        UnitAssembler.delete_temp_folder()

    ### INSTANCE CONFIGURATION
    def __init__(self, callbacks=None):
        """
        Initialize the creator base module.

        Use this class by subclassing it and implementing a custom architecture
        in ``def forward``.

        Use dspy.Signature to build custom strategies.
        Make sure the final output signature has the attributes `title` and `slides`.

        Unit generation can be delegated to content
        creation strategy ( ``self.content_creator`` and related
        variants) and produce a ``Unit`` object as the final result.
        """
        super().__init__(callbacks)

    def __call__(self, *args, **kwargs) -> Unit:
        """Run the creator pipeline and return a fully populated ``Unit``."""
        return super().__call__(*args, **kwargs) #type:ignore

    @abstractmethod
    def forward(self, *args, **kwargs) -> Unit:
        pass
    
    # def create_unit(self, topic: str, **kwargs):
    #     self.unit = self._content_creator.invoke(topic, **kwargs)
    #     return self.unit
    
    # def rework_unit(self, feedback: str, **kwargs):
    #     self.unit = self._content_creator.invoke(feedback, **kwargs)
    #     return self.unit
    
    # @property
    # def history(self):
    #     if not (predictor:=self.predictor()):
    #         return None
    #     return predictor.history
    
    # @property
    # def system_prompt(self):
    #     if not self._content_creator.predictor:
    #         return None
    #     try:
    #         return self._content_creator.predictor.history[0]["messages"][0]["content"]
    #     except:
    #         return None
        
    # @property
    # def raw_response(self):
    #     if not self._content_creator.predictor:
    #         return None
    #     try:
    #         return self._content_creator.predictor.history[0]["response"].choices[0].message.content
    #     except:
    #         return None
