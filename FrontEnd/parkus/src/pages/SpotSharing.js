import MatchmakingTitle from "../components/SpotSharing/Matchmaking/MatchmakingTitle/MatchmakingTitle";
import {Stack, Typography} from "@mui/material";
import MatchmakingGroups from "../components/SpotSharing/Matchmaking/MatchmakingGroup/MatchmakingGroups";
import MatchmakingButton from "../components/SpotSharing/Matchmaking/MatchmakingButton/MatchmakingButton";
import {checkScheduleCompleted, getCurrUser, getGroupId, matchmake} from "../services/requests"
import React, {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";


function SpotSharing() {
    let content;
    const navigate = useNavigate();

    const [availableGroups, setAvailableGroups] = useState(false);
    const [completedSchedule, setCompletedSchedule] = useState(false);
    const [notMemberOfGroup, setNotMemberOfGroup] = useState(false);



    async function handleMatchmakeClick() {
        const currUser = await getCurrUser();
        setAvailableGroups( await matchmake(currUser).then(data => data.availableGroups))
        console.log(availableGroups)
    }

    function handleGroupClick(id){
        navigate(`/groups/${id}`);
    }

    useEffect(() => {
        async function init(){

            var userid = await getCurrUser();
            console.log(userid);

            var groupId = await getGroupId(userid);
            console.log("spotsharing useEffect",groupId);

            if(groupId === 'None'){
                setNotMemberOfGroup(true)
                console.log("member of group", notMemberOfGroup)
            }

        }
        init();
    }, []);
    // async function checkInGroup(){
    //     const userid = getCurrUser()
    //     const groupid = getGroupId(userid)
    //     if(groupid['groupid'] !== "None"){
    //         setMemberOfGroup(true)
    //     }
    // }

    useEffect(() => {
        try {
            const userid = getCurrUser()
            const scheduleMade = checkScheduleCompleted(userid)
            if(scheduleMade['scheduleMade'] !== "None"){
                setCompletedSchedule(true)
            }
        }catch (e) {
            console.error('Error fetching whether schedule complete:',e)
        }

    }, [completedSchedule]);


    return (
        <Stack>
            <MatchmakingTitle></MatchmakingTitle>
            {notMemberOfGroup ? (//check if they're a member of a group already
                <section>
                    {completedSchedule ? (//check if they have schedule blocks
                        <section>
                            {availableGroups ? (//matchmake completed
                                <section>
                                    <MatchmakingButton handleMatchmakeClick={handleMatchmakeClick}/>
                                    <MatchmakingGroups data={availableGroups} handleGroupClick={handleGroupClick}></MatchmakingGroups>
                                </section>
                            ):(//matchmake hasn't been completed
                                <section>
                                    <MatchmakingButton handleMatchmakeClick={handleMatchmakeClick}/>
                                </section>
                            )}
                        </section>
                    ):(
                        <section>
                            <h1>Uh Oh!</h1>
                            <h3> You haven't put in your schedule yet, to join a group head to the schedule tab</h3>
                        </section>
                    )}
                </section>
            ) : (
                <section>
                    <h1>Uh Oh!</h1>
                    <h3> You are already in a group!</h3>
                </section>
            )}
        </Stack>


    )

}

export default SpotSharing;