import shelve
from pythonFiles.add_user import Staff


def staff_account():
    staff_dict = {}
    staff = shelve.open('storage.db', 'c')
    try:
        staff_dict = staff['Staff']
    except:
        print("First time adding")
        # It's normal to receive this error message when its the first time creating.

    staff_detail = Staff('John', 'Sebastian', 'JohnSeb@gmail.com', 'Staffpassword')
    # Change staff values when adding

    staff_id = staff_detail.get_user_id()

    for i in staff_dict:
        if staff_detail.get_email() != staff_dict[i].get_email():
            while True:
                for j in staff_dict:
                    if staff_dict[j].get_user_id() == staff_id:
                        print("Existing staff ids", staff_id)
                        staff_id += 1
                    else:
                        break
    staff_dict[staff_id] = staff_detail
    staff['Staff'] = staff_dict

    # Clear staff details
    # staff.pop('Staff')

    staff.close()
