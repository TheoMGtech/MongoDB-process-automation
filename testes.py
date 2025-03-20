execution_path = { "mongosh_path": r"C:\Users\theomartins-ieg\OneDrive - Instituto Germinare\MongoShell_Arquivos\bin\mongosh.exe" }
execution_path = str(execution_path["mongosh_path"])
execution_path = execution_path[0:execution_path.index("\mongosh.exe")]
print(execution_path)