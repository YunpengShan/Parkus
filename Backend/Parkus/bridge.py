##Bridge
# Communicating with the database
#import psycopg2
import time
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from supabase import create_client, Client

##Database connection & cursor
# connect to db
url = "https://rtneojaduhodjxqmymlq.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ0bmVvamFkdWhvZGp4cW15bWxxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU2NjUxMjQsImV4cCI6MjA0MTI0MTEyNH0.iq-IWDdhTBBcAQcBCC23Li9m2DVjOQDF_2uw8cpHYu0"
supabase: Client = create_client(url, key)


CONNECTION_STRING = "user=postgres.rtneojaduhodjxqmymlq password=NyidWTNcMUDH8Pn5 host=aws-0-ca-central-1.pooler.supabase.com port=6543 dbname=postgres"

##Database connection & cursor
# connect to db
#conn = psycopg2.connect("dbname=parkus user=postgres password=notasecret")


# def get_group_members(groupid):
#     """
#     returns a list of all the members of a group and their schedules
#     :param groupid: the selected group's id
#     :return: a list of tuples of a userid, groupid, scheduleid, day of week, start time, and end time
#     """
#     with conn.cursor() as cur:
#         cur.execute('''
#         SELECT u.userid,
#         g.groupid,s.scheduleid, s.dow, s.start_time, s.end_time
#         FROM schedule_blocks s
#         INNER JOIN users u ON s.userid = u.userid
#         INNER JOIN parking_groups g ON u.groupid = g.groupid
#         WHERE g.groupid = %s
#         ORDER BY g.groupid, u.userid, s.dow;
#         ''', groupid)
#     group_data = cur.fetchall()
#     return group_data

# def get_all_users()
def member_userid_for_group(groupid):
    """
    Returns the user id of each member of thr group with selected group id
    :param groupid: selected group's id
    :return: list of tuples of the user id
    """
    response = (
        supabase.table("users")
        .select("userid", "first_name", "last_name")
        .eq("groupid", groupid)
        .execute()
    )
    return response.data

    ##Old Code
    # with conn.cursor() as cur:
    #     cur.execute('''
    #     SELECT u.userid, u.first_name, u.last_name
    #     FROM users u
    #     WHERE u.groupid = %s
    #     ''', str(groupid))
    #     members = cur.fetchall()
    #     return members

def member_count_by_groupid(groupid):
    """
    returns the number of members in the group with the given ID
    :param groupid: the selected group's id
    :return: the number of members
    """
    response = (
        supabase.table("users")
        .select("userid", count="exact")
        .eq("groupid", groupid)
        .execute()
    )

    return len(response.data)

    # with conn.cursor() as cur:
    #     cur.execute('''SELECT COUNT(u.userid) as members, g.groupid
    #                     FROM parking_groups g
    #                     INNER JOIN users u ON u.groupid = g.groupid
    #                     WHERE g.groupid = %s
    #                     GROUP BY g.groupid
    #                     ORDER BY g.groupid''', str(groupid))
    #     member_count = cur.fetchone()[0]
    #     return member_count


def group_by_groupid(groupid):
    """
    Returns the group matching the given id
    :param groupid:the selected group's id
    :return: a dictionary represention of a group
    """

    response = (
        supabase.table("parking_groups")
        .select("*")
        .eq("groupid", groupid)
        .execute()
    )
    return response.data

    # with conn.cursor() as cur:
    #     cur.execute("SELECT * FROM parking_groups WHERE groupid = %s", groupid)
    #     group = cur.fetchall()
    #     group_dict = {
    #         "groupid":group[0],
    #         "permitid":group[1],
    #         "fullypaid":group[2]
    #     }
    #     return group_dict

###Vacancy Queries
def get_all_groupids():
    """
    Returns a dictionary(json) of all groupids
    :return:
    """
    response = (
        supabase.table("parking_groups")
        .select('groupid')
        .execute()
    )
    return response.data

def active_permit(permitid):
    """
    Returns a bool indicating whether the given group has an active permit
    :param groupid:
    :return:
    """
    response = (
        supabase.table("parking_permits")
        .select('permitid')
        .eq('permitid', permitid)
        .eq('active_status', True)
        .execute()
    )
    return len(response.data) > 0

def get_group_size(groupid):
    """
    Returns the size of the group
    :param groupid:
    :return:
    """
    response = (
        supabase.table('users')
        .select('userid')
        .eq("groupid", groupid)
        .execute()
    )

    return len(response.data)

def get_permit_by_groupid(groupid):
    """
    Returns the permit of the given group
    :param groupid:
    :return:
    """
    response = (
        supabase.table('parking_groups')
        .select('permitid')
        .eq("groupid", groupid)
        .execute()
    )
    return response.data[0]

## User Schedule
def schedule_blocks_for_user(userid):
    """
    returns the schedule blocks for the given user in the form of a list of tuples
    :param userid: selected user's id
    :return: the list of schedule blocks
    """
    response = (
        supabase.table("schedule_blocks")
            .select("scheduleid", "dow", "start_time", "end_time")
            .eq("userid", userid)
            .order("dow")
            .execute()
    )
    return response.data
    # with conn.cursor() as cur:
    #     cur.execute("""
    #     SELECT s.scheduleid, s.dow, s.start_time, s.end_time
    #     FROM schedule_blocks s
    #     WHERE s.userid = %s
    #     ORDER BY dow;
    #     """, (userid,))
    #     schedule = cur.fetchall()
    #     return schedule

def validate_no_group(userid):
    """
    Checks that given user has no group
    :param userid: user's id
    :return: bool
    """
    response = (
        supabase.table("users")
        .select("*")
        .is_("groupid", "null")
        .eq("userid", userid)
        .execute()
    )

    return len(response.data) > 0
    # with conn.cursor() as cur:
    #     cur.execute("""
    #     SELECT *
    #     FROM users u
    #     WHERE u.userid = %s AND u.groupid is null""",
    #                 (userid,))
    #     return cur.fetchone()

def get_group_leader(groupid):
    """
    Returns the leader's userid for the given groupid
    :param groupid:
    :return: userid for group leader
    """
    permitid_response = (
        supabase.table("parking_groups")
        .select("permitid")
        .eq("groupid", groupid)
        .execute()
    )
    print(permitid_response.data[0])

    if len(permitid_response.data)==1:
        userid_response = (
            supabase.table("parking_permits")
            .select("userid")
            .eq("permitid", permitid_response.data[0]['permitid'])
            .execute()
        )
        return userid_response.data[0]

    return None

def get_group_id(userid):
    """
    Returns the group id for the given userid
    :param userid:
    :return:
    """
    response = (
        supabase.table("users")
        .select("groupid")
        .eq("userid", userid)
        .execute()
    )
    return response.data[0]

def get_group_members(groupid):
    """
    Returns the userid, first name, last name, license plate number,
     email, and image url for each member of the given group
    :param groupid:
    :return:
    """
    response = (
        supabase.table("users")
        .select("userid", "first_name", "last_name", "license_plate_number", "email", "image_proof_url")
        .eq("groupid", groupid)
        .execute()
    )
    return response.data

def get_car_info(platenum):
    """
    Returns the car info for the given platenum
    :param platenum:
    :return:
    """
    response = (
        supabase.table("cars")
        .select("*")
        .eq("license_plate_number", platenum)
        .execute()
    )
    return response.data[0]

def paid_member(userid):
    """
    Checks if the given user is paid
    :param userid: given user's id
    :return: True if the user is paid, False otherwise
    """
    response =(
        supabase.table("users")
        .select("*")
        .neq("image_proof_url", None)
        .execute()
    )
    return len(response.data) > 0


def get_group_member(userid):
    """
    Returns the userid, first name, last name, license_plate_number, email, image url,
    and car info for the given userid
    :param userid:
    :return:
    """
    response = (
        supabase.table("users")
        .select("userid", "first_name", "last_name", "license_plate_number", "email", "image_proof_url")
        .eq("userid", userid)
        .execute()
    )
    return response.data[0]


def get_group_permit(leaderid):
    """
    Returns the imageurl of the permit for the given leader
    :param leaderid:
    :return:
    """
    response = (
        supabase.table("users")
        .select("image_proof_url")
        .eq("userid", leaderid)
        .execute()
    )
    return response.data[0]



def upload_etransfer_image(imageUrl, userid):
    """
    Updates the given user's eTransfer Proof image url
    :param imageUrl: Url of the eTransfer Proof image
    :param userid: user's id
    :return: True if the user is uploaded, False otherwise
    """
    response = (
        supabase.table("users")
        .update({"image_proof_url": imageUrl})
        .eq("userid", userid)
        .execute()
    )
    return len(response.data[0]) > 0


"""
Validation functions
"""
def validate_userid(userid):
    response = (
        supabase.table("users")
        .select("*")
        .eq("userid", userid)
        .execute()
    )
    return len(response.data) > 0

def validate_groupid(groupid):
    response = (
        supabase.table("parking_groups")
        .select("*")
        .eq("groupid", groupid)
        .execute()
    )
    return len(response.data) > 0

def validate_permitid(permitiid):
    response = (
        supabase.table("parking_permits")
        .select("*")
        .eq("permitid", permitiid)
        .execute()
    )
    return len(response.data) > 0

def validate_scheduleid(scheduleid):
    response = (
        supabase.table("schedule_blocks")
        .select("*")
        .eq("scheduleid", scheduleid)
        .execute()
    )
    return len(response.data) > 0

def validate_license_plate_number(license_plate_number):
    """
    Checks if the given license plate number is valid
    :param license_plate_number:
    :return:
    """
    response =(
        supabase.table("cars")
        .select("*")
        .eq("license_plate_number", license_plate_number)
        .execute()
    )
    return len(response.data) > 0




def fetch_user_by_userid(user_id):
    """Fetches user data by userid from the Supabase database."""
    response = (
        supabase.table("users")
        .select("*")
        .eq("userid", user_id)
        .execute()
    )
    if response.data:
        return response.data[0]
    else:
        print("User not found.")
        return None

def check_parking_permit(user_id):
    """Checks if the user has a parking permit."""
    response = (
        supabase.table("parking_permits")
        .select("*")
        .eq("userid", user_id)
        .execute()
    )
    return response.data is not None and len(response.data) > 0

def insert_parking_permit(user_id, permit_number, active_status, permit_type, activate_date, expiration_date, campus_location):
    """Inserts a new parking permit into the Supabase database."""
    response = supabase.table("parking_permits").insert({
        "userid": user_id,
        "permit_number": permit_number,
        "active_status": active_status,
        "permit_type": permit_type,
        "activate_date": activate_date,
        "expiration_date": expiration_date,
        "campus_location": campus_location,
    }).execute()
    return response.data is not None and len(response.data) > 0

def fetch_parking_permits_by_userid(user_id):
    """Fetches all parking permits for a given user ID from the Supabase database."""
    response = (
        supabase.table("parking_permits")
        .select("*")
        .eq("userid", user_id)
        .execute()
    )
    if response.data:
        return response.data
    else:
        print("No permits found.")
        return []


if __name__ == "__main__":
    ##Testing has member paid
    print(paid_member('33d6127f-3a9e-4681-83a2-92c98db0881c'))

    ##Testing Get Car info
    print(get_car_info('ABC123'))

    ##Testing for get group members, leader, id
    print(get_group_members('44966fd0-2c0f-416d-baf8-80bfeb4ba075')) ##John, Michael, Matthew
    print(get_group_id('33d6127f-3a9e-4681-83a2-92c98db0881c'))## given john -> '44966fd0-2c0f-416d-baf8-80bfeb4ba075'
    print(get_group_leader('44966fd0-2c0f-416d-baf8-80bfeb4ba075'))##John

    ##Testing for matchmaking
    blocks = schedule_blocks_for_user('7ce19f4c-9d60-4539-8217-cfb3967f99ca')  # 5th user emily
    print(blocks)
    for block in blocks:
        print(block)
    # group1 = member_userid_for_group(1)
    # group1num = member_count_by_groupid(1)
    # for member in group1:
    #     print(member['userid'])
    #
    # for member in group1:
    #     print(member)
    #
    # print(group1num)
    # print(group_by_groupid(1))
    # print(groups_with_vacancies())


