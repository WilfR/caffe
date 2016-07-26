import wlrutil

dbName = 'Selected2'
tsneDataName = 'Selected2Data.txt'
tsneLabelName = 'Selected2Label.txt'

dbName = 'HvsVLevelDB'
tsneDataName = 'HvsVLevelDBData.txt'
tsneLabelName = 'HvsVLevelDBLabel.txt'



wlrutil.LevelDBToTSNE( dbName, tsneDataName, tsneLabelName )
