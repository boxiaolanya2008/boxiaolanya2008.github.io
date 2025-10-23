# Lua源代码还原总结报告

## 总体统计
- 总文件数: 73
- 总函数数: 8
- 总导入数: 126

## 模块分布
- 用户界面模块: 38 个文件
- 能力系统模块: 3 个文件
- 其他模块: 32 个文件

## 主要功能模块

### 用户界面模块

主要函数:
- ADFMGameHud_UMapBaseHUDController_OnClientMarkDetectorLocation_BS
- HUCharacterHeroResourceDataSingleton_GetAvatarTracingLineResourceInfo_BS
- IUCharacterHeroResourceDataSingleton::GetAvatarTracingLineResourceInfo_BS
- ADFMGameHud_UMapBaseHUDController_OnClientMarkDetectorLocation_BS
- HUCharacterHeroResourceDataSingleton_GetAvatarTracingLineResourceInfo_BS
- IUCharacterHeroResourceDataSingleton:GetAvatarTracingLineResourceInfo_BS
- AGPPlayerController::EndPlay_BS
- AGPPlayerController:EndPlay_BS

主要导入:
- QDFM.Business.Module.CommonWidgetModule.UI.CommonVideoView.CommonVideoProgressBar
- 4DFM.Business.Module.InventoryModule.InventoryConfig
- NDFM.Business.Module.CommonWidgetModule.UI.CommonVideoView.CommonVideoViewBase
- .DFM.StandaloneLua.BusinessTool.HeroHelperTool
- .DFM.StandaloneLua.BusinessTool.ShopHelperTool
- 7DFM.Business.DataStruct.Common.Agent.InputBindingAgent
- 9DFM.StandaloneLua.BusinessTool.StructTool.ItemConfigTool
- 0DFM.StandaloneLua.BusinessTool.WeaponHelperTool
- 9DFM.Business.Module.HeroModule.UI.HeroMain.HeroSkillIcon
- GDFM.Business.DataStruct.LitePackageStruct.LitePackageDownloadTableItem

### 能力系统模块

主要导入:
- 6DFM.Business.Module.SettlementModule.SettlementConfig
- 6DFM.Business.Module.ItemDetailModule.ItemDetailConfig
- 1DFM.Business.DataStruct.InventoryStruct.ItemSlot
- 1DFM.StandaloneLua.BusinessTool.VehicleHelperTool
- 8DFM.StandaloneLua.BusinessTool.StructTool.ItemOperaTool
- .DFM.StandaloneLua.BusinessTool.ShopHelperTool
- 9DFM.StandaloneLua.BusinessTool.StructTool.ItemConfigTool
- .DFM.StandaloneLua.BusinessTool.ItemHelperTool
- 3DFM.Business.DataStruct.InventoryStruct.SlotConfig
- ADFM.YxFramework.Managers.GameFlow.InGameControl.InGameController

### 其他模块

主要导入:
- BDFM.Business.ServerCenter.ServerConfig.CollectionRoomServerConfig
- BDFM.Business.Module.BattlefieldEntryModule.BattlefieldEntryConfig
- DFM.YxFramework.Util.StringUtil
- 8DFM.StandaloneLua.BusinessTool.StructTool.ItemOperaTool
- .DFM.StandaloneLua.BusinessTool.HeroHelperTool
- 9DFM.StandaloneLua.BusinessTool.StructTool.ItemConfigTool
- DFM.Business.Misc.DFMAudioConst
- .DFM.StandaloneLua.BusinessTool.ItemHelperTool
- ADFM.YxFramework.Managers.GameFlow.InGameControl.InGameController
