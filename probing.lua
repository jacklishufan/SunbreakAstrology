local AlchemyFacility = sdk.get_managed_singleton("snow.data.FacilityDataManager"):get_field("_AlchemyFacility")
local Patturns = AlchemyFacility:get_field("_Function"):get_field("<PatturnDataList>k__BackingField")
local urnParam = Patturns[9]:get_field("_Param")




local AlchemyFacilityFunction = AlchemyFacility:get_field("_Function")
local ReserveInfoList = AlchemyFacilityFunction:get_field("_ReserveInfoList")


-- patturn_id: 0-9, skill_id: 0 - 96
function setupSkills(patturn_id,skill_id) 
    AlchemyFacility:call("selectPatturn",Patturns[patturn_id])
    local skillList = AlchemyFacility:call("getSelectableSkillList")
    if skill_id >= 0 then 
        local selectedSkill = skillList[skill_id]
        AlchemyFacility:call("selectTargetSkillTable",selectedSkill)
    end
end

-- AlchemyFacility:call("reserveAlchemy")
-- AlchemyFacility:call("reserveAlchemy")
-- AlchemyFacility:call("reserveAlchemy")
-- AlchemyFacility:call("reserveAlchemy")


function dumpReserveInfo(reserveInfo) 
    data = {}
    local outputInfoList = reserveInfo:get_field("_OutputInfoList")
    log.info(
    string.format("DDDD Table Length %s \n",type(outputInfoList))
    )
    for i = 0,4 do 
        local outputInfo = outputInfoList[i]
        log.info(
            string.format("XXXX Table Length %s \n",type(outputInfo))
        )
        local skillIds = outputInfo:get_field("_SkillIdList")
        local skillLvs = outputInfo:get_field("_SkillLvList")
        local slots = outputInfo:get_field("_SlotLvList")
        entry = {}
        entry.skill1 = skillIds[0]:call("getValue"):get_field("mValue")
        entry.skill2 = skillIds[1]:call("getValue"):get_field("mValue")
        entry.skill1_level = skillLvs[0]:get_field("mValue")
        entry.skill2_level = skillLvs[1]:get_field("mValue")
        entry.slot1 = slots[0]:call("getValue"):get_field("mValue")
        entry.slot2 = slots[1]:call("getValue"):get_field("mValue")
        entry.slot3 = slots[2]:call("getValue"):get_field("mValue")
        data[i+1] = entry
    end
    return data
end


function dumpCycle(cycles) 
    outputs = {}
    local j = 0
    for j=0,cycles do
        for i = 0,9 do 
            -- setupSkills(patturn_id,skill_id)
            AlchemyFacilityFunction:call("reserveAlchemy")
            log.info("HERE")
            outputs[j*10+i+1] = dumpReserveInfo(ReserveInfoList[i])
            AlchemyFacilityFunction:call("finishedLastMakaPot")
        end
        AlchemyFacility:call("cleanupReserveInfo")
    end
    return outputs
end

-- main --

-- config
-- setup
-- setupSkills(patturn_id,skill_id)
-- set cost 0 to avoid bugs
local cache_cost = {}
for i=0,9 do
    local urnParam = Patturns[i]:get_field("_Param")
    cache_cost[i] = urnParam:get_field("_CostVillagePoint")
    urnParam:set_field("_CostVillagePoint",0)
end
-- cleanup
AlchemyFacility:call("cleanupReserveInfo")


-- run
outputs = dumpCycle(10000)
-- for i = 0,9 do 
--     setupSkills(patturn_id,skill_id)
--     AlchemyFacility:call("reserveAlchemy")
--     log.info("HERE")
--     outputs[j*10+i+1] = dumpReserveInfo(ReserveInfoList[i])
--     AlchemyFacilityFunction:call("finishedLastMakaPot")
-- end
-- for i = 0,9 do 
--     setupSkills(patturn_id,skill_id)
--     AlchemyFacility:call("reserveAlchemy")
--     -- outputs[j*10+i+1] = dumpReserveInfo(ReserveInfoList[i])
--     AlchemyFacilityFunction:call("finishedLastMakaPot")
-- end
-- reset cost
for i=0,9 do
    local urnParam = Patturns[i]:get_field("_Param")
    urnParam:set_field("_CostVillagePoint",cache_cost[i])
end
json.dump_file("output_bowgun.json", outputs)
