import time, json
from typing import List
from ctypes import *
# from pxr import Sdf, Usd


class Timer:
    Name: str
    def __init__(self, timerName: str):
        self.Name = timerName
    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, *args):
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time
        print(f"{self.Name}: took {self.elapsed_time:.6f} seconds")

class Configurator:
    def __init__(self, context):
        # self.Stage: Usd.Stage = stage
        # self.ProductPrim: Sdf.Prim = self.FindProductPrim(self.Stage)
        # if self.ProductPrim is None:
        #      raise ValueError("***  ERROR: No asset loaded in stage")
        # self.ProductPrimName: str = self.ProductPrim.GetName()
        # self.ProductPrimPath: str = str(self.ProductPrim.GetPath())
        self.CustomData: dict = self.GetCustomData(self) #Config json
        self.Selections: dict = self.GetCustomDataSelection(self)
        self.OutputCalculator = cdll.LoadLibrary('D:\BlenderAddons\Blender_addons\MultipleFileTest\M_DLL\OutputCalculator.dll')
        # self.OutputCalculator.CanUseDLL = False

    # Temporary hacky way to find Product Prim
    # @staticmethod
    # def FindProductPrim(stage: Usd.Stage):
    #     for prim in stage.Traverse():
    #         customData = prim.GetCustomData()
    #         if customData is None or customData == {}:
    #             continue
    #         if len(str(customData)) < 500:
    #             continue
    #         return prim

    @staticmethod
    def GetCustomData(self):
        with open('D:\BlenderAddons\Blender_addons\MultipleFileTest\M_DLL\ConfigJson.json', 'r') as d:
            customData = d.read()
            customDataa = json.loads(customData)
        # customData = productPrim.GetCustomData()
        # if "MaterialColors" in customData:
        #     del customData["MaterialColors"]
        return customDataa

    @staticmethod
    def GetCustomDataSelection(self):
        with open('D:\BlenderAddons\Blender_addons\MultipleFileTest\M_DLL\Selections.json', 'r') as d:
            customData = d.read()
            customDataa = json.loads(customData)
        # customData = productPrim.GetCustomData()
        # if "MaterialColors" in customData:
        #     del customData["MaterialColors"]
        return customDataa

    def GetConfigurationNames(self, showEmpty: bool = False):
        metaVariantSets = []
        for metaVariantSet in self.CustomData["metaVariantSets"]:
            if self.CustomData["metaVariantSets"][metaVariantSet]["variants"]:
                metaVariantSets.append(metaVariantSet)
            elif showEmpty:
                metaVariantSets.append(metaVariantSet)
        return metaVariantSets
    
    @staticmethod
    def CalculateOutputNissan(self, productPrimPath: str = 'AAAAAAAAA'):
        # if len(self.CustomData) == 0:
        #     self.CustomData= self.GetCustomData()
        # if len(self.Selections) == 0:
        #     self.Selections = self.GetCustomDataSelection()
        # if len(self.OutputCalculator) == None:
        #     self.OutputCalculator = cdll.LoadLibrary('D:\BlenderAddons\Blender_addons\MultipleFileTest\M_DLL\OutputCalculator.dll')
        actions = []
        for key in self.Selections:
            targetSelection = self.Selections[key]
            for variantPath in self.CustomData["metaVariantSets"][key]["variants"][targetSelection]["usdVariants"]:
                v = self.CustomData["metaVariantSets"][key]["variants"][targetSelection]["usdVariants"][variantPath]
                targetState = v["variant"]
                targetPath = productPrimPath + "/" + v["primPath"]
                targetVariantSetName = v["variantSet"]

                if targetPath not in [action["Path"] for action in actions]:
                    actions.append({
                        "Path": targetPath,
                        "Variant": targetVariantSetName,
                        "State": targetState
                    })
        return actions

    def CallForHelp(self):
        return self.CalculateOutputNissan(self)
    # def GetOptionsForConfiguration(self, configuration: str):
    #     return list(self.CustomData["metaVariantSets"][configuration]["variants"].keys())

    # @staticmethod
    # def GetAllAvailableActions(customData: dict, productPrimPath: str) -> List[str]:
    #     vsPaths: List[str] = []
    #     for configuration in customData["metaVariantSets"]:
    #         for option in customData["metaVariantSets"][configuration]["variants"]:
    #             if not isinstance(customData["metaVariantSets"][configuration], dict):
    #                 continue
    #             if not isinstance(customData["metaVariantSets"][configuration]["variants"][option], dict):
    #                 continue
    #             for vsOptionPath in customData["metaVariantSets"][configuration]["variants"][option]["usdVariants"]:
    #                 path = productPrimPath + "/" + vsOptionPath
    #                 if path not in vsPaths:
    #                     vsPaths.append(path)
    #     return vsPaths

    # @staticmethod
    # def GetVariantSetAtPrimPath(stage: Usd.Stage, primPath: str, variantSetName: str):
    #     prim = stage.GetPrimAtPath(primPath)
    #     if not prim.IsValid():
    #         return None
    #     variantSets = prim.GetVariantSets()
    #     if variantSets.HasVariantSet(variantSetName):
    #         return variantSets.GetVariantSet(variantSetName)
    #     return None

    # def ExecuteActions(self, actions):
    #     with Sdf.ChangeBlock():
    #         for actionDict in actions:
    #             path = actionDict["Path"]
    #             state = actionDict["State"]
    #             variant = actionDict["Variant"]

    #             vs = self.GetVariantSetAtPrimPath(self.Stage, path, variant)
    #             if vs is None:
    #                 try:
    #                     import carb
    #                     carb.log_error(f"Unable to find Variant Set {variant} at path {path}")
    #                 except:
    #                     print(f"Unable to find Variant Set {variant} at path {path}")
    #                 finally:
    #                     continue

    #             if vs.GetVariantSelection() == state:
    #                 continue
    #             vs.SetVariantSelection(state)

    # def ApplyConfiguration(self):
    #     with Timer("Applying Configuration"):
    #         if self.OutputCalculator.CanUseDLL:
    #             actions = self.OutputCalculator.Execute(self.CustomData, self.Selections)
    #         else:
    #             actions = self.CalculateOutputNissan(self.CustomData, self.Selections, self.ProductPrimPath)
    #         self.ExecuteActions(actions)

    # def ApplyConfigurationDodge(self):
    #     with Timer("Applying Configuration"):
    #         if self.OutputCalculator.CanUseDLL:
    #             actions = self.OutputCalculator.Execute(self.CustomData, self.Selections)
    #         else:
    #             actions = self.CalculateOutputDodge(self.CustomData, self.Selections, self.ProductPrimPath)
    #         self.ExecuteActions(actions)

    # def ApplyCombination(self, combination: dict, executeActions: bool = False):
    #     with Timer("Applying Combination"):
    #         if self.OutputCalculator.CanUseDLL:
    #             actions = self.OutputCalculator.Execute(self.CustomData, combination)
    #         else:
    #             actions = self.CalculateOutputNissan(self.CustomData, combination, self.ProductPrimPath)
    #         if executeActions:
    #             self.ExecuteActions(actions)
    #         return actions

    # def ApplyCombinationDodge(self, combination: dict):
    #     with Timer("Applying Combination"):
    #         if self.OutputCalculator.CanUseDLL:
    #             actions = self.OutputCalculator.Execute(self.CustomData, self.Selections)
    #         else:
    #             actions = self.CalculateOutputDodge(self.CustomData, combination, self.ProductPrimPath)
    #         self.ExecuteActions(actions)

    # def SetSelection(self, configuration: str, optionsIndex):
    #     options = self.GetOptionsForConfiguration(configuration)
    #     self.Selections[configuration] = options[optionsIndex]


    # @staticmethod
    # def CalculateOutputNissan(customDataDict: dict, selections: dict, productPrimPath: str = 'AAAAAAAAA'):
    #     actions = []
    #     for key in selections:
    #         targetSelection = selections[key]
    #         for variantPath in customDataDict["metaVariantSets"][key]["variants"][targetSelection]["usdVariants"]:
    #             v = customDataDict["metaVariantSets"][key]["variants"][targetSelection]["usdVariants"][variantPath]
    #             targetState = v["variant"]
    #             targetPath = productPrimPath + "/" + v["primPath"]
    #             targetVariantSetName = v["variantSet"]

    #             if targetPath not in [action["Path"] for action in actions]:
    #                 actions.append({
    #                     "Path": targetPath,
    #                     "Variant": targetVariantSetName,
    #                     "State": targetState
    #                 })
    #     return actions

    # @staticmethod
    # def CalculateOutputDodge(customDataDict: dict, selections: dict, productPrimPath: str):
    #     availableActions = Configurator.GetAllAvailableActions(customDataDict, productPrimPath)
    #     actions = {}
    #     selectedOptions = []
    #     turnOffActions = {}
    #     paintActions = customDataDict["Paints"][selections["Paints"]]
    #     for action in paintActions:
    #         actions[action] = customDataDict["Paints"][selections["Paints"]][action]
    #     if selections["Standard"] != "off":
    #         standardActions = customDataDict["Standard"][selections["Standard"]]
    #         for action in standardActions:
    #             actions[action] = customDataDict["Standard"][selections["Standard"]][action]
    #         return [(a, actions[a]) for a in actions]
    #     for key in customDataDict:
    #         if key == "Paints" or key == "Standard" or key == "TurnOffs" or selections[key] == "off":
    #             continue
    #         else:
    #             selectedOptions.append(key)

    #     for option in selectedOptions:
    #         optionActions = customDataDict[option][selections[option]]
    #         for action in optionActions:
    #             if action in actions:
    #                 newState = customDataDict[option][selections[option]][action]
    #                 oldState = actions[action]
    #                 if newState != oldState:
    #                     actions[action] = "on"
    #             else:
    #                 actions[action] = customDataDict[option][selections[option]][action]

    #         if option + "_off" in customDataDict["TurnOffs"]:
    #             acs = customDataDict["TurnOffs"][option + "_off"]
    #             for action in acs:
    #                 if action not in turnOffActions:
    #                     turnOffActions[action] = customDataDict["TurnOffs"][option + "_off"][action]

    #     for action in turnOffActions:
    #         if action in actions:
    #             actions[action] = turnOffActions[action]

    #     for action in availableActions:
    #         if action not in actions:
    #             actions[action] = "off"

    #     return [{
    #         "Path": action,
    #         "Variant": actions[action],
    #         "State": "materialVariant" if action.split("/")[-1].startswith("switch_") else action.split("/")[-1]
    #     } for action in actions]