local CustomBuildGui = sdk.get_managed_singleton("snow.gui.GuiManager"):get_field("<refGuiCustomBuildup>k__BackingField")

local tempData = CustomBuildGui:get_field("_TempEquipInventoryData"):get_field("_CustomBuildup")
local moneyObj = sdk.get_managed_singleton("snow.data.DataManager"):get_field("_HandMoney")
local oldValue = moneyObj:get_field("_Value")

function parseEntry(result) 
    local data = {}
    data.id = result:get_field("_id")
    data.lotId = result:get_field("_Id")
    data.val = result:get_field("_ValueIndex")
    data.skillId = result:get_field("_SkillId")
    return data
end

function parseList(result)
    local data = {}
    for i=0,6 do
        data[i+1] = parseEntry(tempData[i]) 
    end
    return data
end

function dumpCycle(n)
    local data = {}
    for i = 0,n do 
        CustomBuildGui:call("executeArmorCustomBuildup")
        data[i+1] = parseList(tempData)
        moneyObj:set_field("_Value",oldValue)
    end
    return data
end

out = dumpCycle(10000)
json.dump_file("dump.json",out)