from models import Employee, User
import config
if config.STATUS == "TEST":
    from models import db
else:
    from exts import db


def insert_new_employee(uid, rid):
    """
    Inserts employee into Employee table.

    Args:
        uid: A user ID that corresponds to a user in the User table. A integer.
        rid: A restaurant ID that corresponds to a restaurant in the Restaurant
          table. A integer.

    Returns:
        None.
    """
    employee = Employee(uid = uid, rid = rid)
    db.session.add(employee)
    db.session.commit()
    return None


def get_employees(rid):
    """
    Fetches rows from the Employee table.

    Retrieves a list of employees from the Employee table that work at a
    restaurant with the given restaurant ID.

    Args:
        rid: A restaurant ID that corresponds to a restaurant in the Restaurant
          table. A integer.

    Returns:
        A list of employees containing all employee have restaurant ID that
        match rid.
    """
    employee_list = []
    employees = Employee.query.filter(Employee.rid == rid).all()
    for e in employees:
        employee = User.query.filter(User.uid == e.uid).first()
        dict = {
            "uid": employee.uid,
            "name": employee.name,
            "email": employee.email
        }
        employee_list.append(dict)
    return employee_list


def delete_employee(uid):
    """
    Removes a row from the Employee table and User Table.

    Deletes a employee user from the database.

    Args:
        uid: A user ID that corresponds to a user in the User and Employee
          table. A integer.

    Returns:
        None.
    """
    # Deletes employee from employee table
    Employee.query.filter(Employee.uid == uid).delete()
    db.session.commit()
    # Deletes employee from user table
    User.query.filter(User.uid == uid).delete()
    db.session.commit()
    return None


def get_employee_rid(uid):
    employee = Employee.query.filter(Employee.uid == uid).first()
    if employee:
        return employee.rid
    else:
        return None
