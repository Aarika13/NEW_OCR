from ..app import process_directory
if (ent.label_ == "AMOUNT"):
    try:
        amt = float(ent.text)
        if amt > max_amt:
            data["AMOUNT"] = amt
    except Exception as e:
        pass