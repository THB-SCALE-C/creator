from pathlib import Path
from typing import Any
from dspy import Signature,Module,Prediction
from .unit_assembler.UnitAssembler import UnitAssembler
from .content_creator.ContentCreator import ContentCreator, CreatorOutput
from .lib.types import AssemblerConfig, SignatureSlide


class Creator:

    @classmethod
    def assemble_unit_with_content(cls, content:dict[str,Any]|None,output_dir=".out",out_name="unit.h5p"):
        if not content:
            raise ValueError("No learning unit created. Create first.")
        presentation = UnitAssembler.assemble_content(content)
        assembled_unit_path = UnitAssembler.assemble_h5p(presentation, output_dir=output_dir, out_name=out_name)
        return assembled_unit_path
        
    @classmethod
    def create_unit_from_prediction(cls,prediction:Prediction):
        return CreatorOutput(prediction)
    
    @classmethod
    def assemble_unit_from_prediction(cls,prediction:Prediction,output_dir=".out",out_name="unit.h5p"):
        unit = CreatorOutput(prediction)
        presentation = UnitAssembler.assemble_content(unit.to_dict())
        assembled_unit_path = UnitAssembler.assemble_h5p(presentation, output_dir=output_dir, out_name=out_name)
        return assembled_unit_path

    def __init__(self, 
                 unit_assembler_props: AssemblerConfig|dict[str,Any]={}, 
                 signature_class: type[Signature] | None = None, 
                 signature_json: None | list[SignatureSlide] = None, 
                 module_predictor:type[Module]|None=None, 
                 **model_props) -> None:
        
        self._content_creator = ContentCreator(model_props=model_props)
        self._unit_assembler = UnitAssembler(unit_assembler_props)
        if signature_class:
            self._content_creator.set_lu_signature(signature_class)
        elif signature_json:
            self._content_creator.set_lu_signature_with_json(signature_json)
        elif module_predictor:
            self._content_creator.set_dspy_module_predictor(module_predictor)    
        else:
            raise ValueError("Either signature_class, signature_json or module_predictor must be provided.")
        
        if not module_predictor:
            if instructions := model_props.get("instructions"):
                self._content_creator.add_instructions(instructions)

            if model_props.get("cot", False):
                self._content_creator.enable_cot()

    def create_unit(self, topic: str, **kwargs):
        self.unit = self._content_creator.invoke(topic, **kwargs)
        return self.unit
    


    def assemble_unit(self,output_dir=".out",out_name="unit.h5p"):
        if not self.unit:
            raise ValueError("No learning unit created. Create first.")
        content = self.unit.to_dict()
        assembled_unit_path = self.assemble_unit_with_content(content,output_dir,out_name)
        return assembled_unit_path
    
    @property
    def history(self):
        if not self._content_creator.predictor:
            return None
        return self._content_creator.predictor.history
    
    @property
    def system_prompt(self):
        if not self._content_creator.predictor:
            return None
        try:
            return self._content_creator.predictor.history[0]["messages"][0]["content"]
        except:
            return None
        
    @property
    def raw_response(self):
        if not self._content_creator.predictor:
            return None
        try:
            return self._content_creator.predictor.history[0]["response"].choices[0].message.content
        except:
            return None