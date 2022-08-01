import sys

import pandas as pd


def get_ccle_dataframe(file_name):

    # Read in the file
    nci60Act = pd.read_csv(
        file_name,
        index_col=0,
    )

    # Rename the columns to match the CCLE Setup
    nci60Act = nci60Act.rename(
        columns={
            "BR:HS 578T": "BR:HS 578 T",
            "BR:T-47D": "BR:T47D",
            "CNS:SF-295": "CNS:SF295",
            "CNS:SF-268": "CNS:SF268",
            "CNS:SF-539": "CNS:SF539",
            "CNS:SNB-19": "CNS:SNB19",
            "CO:HT29": "CO:HT 29",
            "CO:SW-620": "SW620",
            "LE:HL-60(TB)": "LE:HL-60",
            "ME:LOX IMVI": "ME:LOXIMVI",
            "LC:A549/ATCC": "LC:A549",
            "OV:IGROV1": "OV:IGROV 1",
            "RE:RXF 393": "RE:RXF-393",
            "RE:TK-10": "RE:TK10",
        }
    )

    # These are not listed in the table and train data
    nci60Act = nci60Act.drop(["ME:MDA-N", "OV:NCI/ADR-RES", "RE:UO-31"], axis=1)

    # replace ' ' with '_' in the column names
    nci60Act.columns = nci60Act.columns.str.replace(" ", "-")

    # Rename the columns to match the CCLE Setup
    col = []
    for i in nci60Act.columns:
        tmp = i.split(":")
        if len(tmp) == 2:
            col.append(tmp[1])
        else:
            col.append(tmp[0])

    nci60Act.columns = col

    # Read table of cell line names
    sanger_cell_lines = pd.read_csv("../data/sanger_to_ccle.csv", index_col=0)

    # Create a dictionary of the cell line names
    ccle_dict = {
        i.upper(): j
        for i, j in zip(
            sanger_cell_lines["Sanger name"], sanger_cell_lines["CCLE Label"]
        )
    }

    # Create a new column for the cell line names
    nci60Act.columns = [ccle_dict[i] for i in nci60Act.columns]

    # Save the dataframe to a csv file
    nci60Act.to_csv(
        file_name.replace(".csv", "_ccle.csv"),
    )


if __name__ == "__main__":
    # require file PATH as an argument
    args = sys.argv

    if len(args) == 2:
        get_ccle_dataframe(str(args[1]))
    else:
        print("Argument Error, please provide a file path to a nci60 file")
