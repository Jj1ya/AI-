import pymongo

def Connect_DB():
    connect_to =pymongo.MongoClient("localhost",27017)
    mdb = connect_to.vehicle
    collection = mdb.v_data
    return collection

def execl_to_DB(collection):
    wb = load_workbook("test.xlsx")
    ws = wb.active
    for x in range(1, ws.max_row+1):
        db_data = {
            "time": ws.cell(row=x, column=2).value,
            "vel": ws.cell(row=x, column=3).value,
            "acc": acc,
            "n_vel": ws.cell(row=x, column=3).value
        }
        collection.insert_one(db_data)

collection = Connect_DB
execl_to_DB(collection)