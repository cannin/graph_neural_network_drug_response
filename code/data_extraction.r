library(rcellminer)
library(rcellminerData)

# Get PubChemID and Cell Line

drugAnnot <- getFeatureAnnot(rcellminerData::drugData)[["drug"]]['PUBCHEM_ID']
drugAnnot <- na.omit(drugAnnot)
write.csv(
    drugAnnot,
    file = '../data/nci60PubChemID.csv',
)

# Get the PubChemID

write.table(
    as.array(drugAnnot$PUBCHEM_ID),
    file = '../data/PubChemID.csv',
    col.names=FALSE,
    row.names=FALSE,
)

# Get Drug response between Cell Lines and PubChemID

nci60Act <- exprs(getAct(drugData))
write.csv(
    nci60Act,
    file = '../data/nci60Act.csv',
)
